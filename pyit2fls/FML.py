"""
Support for the IEEE 1855 Fuzzy Markup Language (FML) standard.

This module parses FML XML documents into a lightweight intermediate
representation (a pair of ``variables``/``rules`` dictionaries), and builds
a runnable :class:`pyit2fls.T1Mamdani` or :class:`pyit2fls.T1TSK` system out
of that representation through :func:`generate_system`. The same
intermediate representation is also produced by :mod:`pyit2fls.FCL` (the
IEC 61131-7 Fuzzy Control Language parser) and consumed by the PyIT2FLS
designer GUI (:mod:`pyit2fls.designerui`), so all three share a single
system-building routine.

See ``IEEE1855.md`` in the repository root for a description of the FML
standard, and ``markdown docs/FML.md`` for a tutorial.
"""
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from numpy import linspace
from pyit2fls import (T1Mamdani, T1TSK, T1FS, tri_mf, ltri_mf, rtri_mf,
                       trapezoid_mf, gaussian_mf, singleton_mf, points_mf, )


#: Maps FML membership function shape tags to pyit2fls membership functions.
MF_MAP = {
    "triangularShape": tri_mf,
    "trapezoidalShape": trapezoid_mf,
    "gaussianShape": gaussian_mf,
    "singletonShape": singleton_mf,
    "pointsShape": points_mf,
}

#: Default number of samples used to discretize a variable's domain.
DOMAIN_RESOLUTION = 100


def _default_height(mf_type, params):
    """
    Appends the default height (1.0) to a parameter list if the caller
    omitted it, matching the shapes understood by ``MF_MAP``.
    """
    expected = {"triangularShape": 3, "trapezoidalShape": 4,
                "gaussianShape": 2, "singletonShape": 1}
    n = expected.get(mf_type)
    if n is not None and len(params) == n:
        params = params + [1.0]
    return params


def _engine_from_methods(and_method, activation_method):
    """
    Maps FML/FCL ``andMethod``/``activationMethod`` strings to one of the
    inference engines understood by :class:`pyit2fls.T1Mamdani`.
    """
    activation = (activation_method or "").strip().lower()
    if "lukasiewicz" in activation:
        return "Lukasiewicz"
    if "zadeh" in activation:
        return "Zadeh"
    if "dienes" in activation:
        return "Dienes-Rescher"

    and_ = (and_method or "").strip().lower()
    if and_ in ("min", "minimum"):
        return "Minimum"
    return "Product"


def _defuzzification_from_attr(defuzzifier):
    """
    Maps an FML/FCL defuzzifier attribute to a :class:`pyit2fls.T1Mamdani`
    defuzzification method.
    """
    value = (defuzzifier or "").strip().upper()
    if value in ("COA", "COGS"):
        return "CoA"
    return "CoG"


def generate_system(variables, rules):
    """
    Builds a Type 1 Fuzzy Logic System (Mamdani or TSK) out of the shared
    intermediate representation produced by :func:`FML.parse_fml` and
    :func:`pyit2fls.FCL.parse_fcl`.

    .. rubric:: Parameters

    variables : dict

        A dictionary with keys ``"input"`` and ``"output"``, each mapping
        variable names to a dict with keys ``"domainleft"``,
        ``"domainright"``, and ``"terms"``. ``"terms"`` maps term names to a
        dict with keys ``"set"`` (a key of :data:`MF_MAP`), ``"params"``
        (a list of floats), and ``"complement"`` (the string ``"true"`` or
        ``"false"``).

    rules : dict

        A dictionary with keys ``"type"`` (``"mamdani"`` or
        ``"takagi-sugeno"``), ``"andMethod"``, ``"orMethod"``,
        ``"activationMethod"``, and ``"rules"``. ``"rules"`` maps rule names
        to a dict with keys ``"antecedent"`` and ``"consequent"`` (each a
        list of ``(variable name, term name)`` tuples), ``"connector"``
        (``"and"`` or ``"or"``), and ``"weight"``.

    .. rubric:: Returns

    output : T1Mamdani or T1TSK

        The fuzzy logic system built from the given variables and rules.

    .. rubric:: Notes

    The underlying :class:`pyit2fls.T1Mamdani` and :class:`pyit2fls.T1TSK`
    engines only support antecedents whose clauses are implicitly AND-ed
    together (there is no seam for OR-combined clauses within a single
    rule), so a :class:`ValueError` is raised for any rule whose
    ``"connector"`` is ``"or"`` and which has more than one antecedent
    clause.

    Rule ``"weight"`` values are carried through by :func:`parse_fml` and
    :func:`pyit2fls.FCL.parse_fcl` but are **not** applied while
    evaluating the generated system: doing so would require changes to the
    firing-strength arithmetic in every ``T1Mamdani``/``T1TSK`` evaluate
    method, which is out of the scope of this module.
    """
    if rules["type"] == "mamdani":
        engine = _engine_from_methods(rules.get("andMethod"), rules.get("activationMethod"))
        defuzzifier = None
        for var_info in variables["output"].values():
            defuzzifier = var_info.get("defuzzifier", defuzzifier)
        if engine in ("Lukasiewicz", "Zadeh", "Dienes-Rescher"):
            sys = T1Mamdani(engine=engine)
        else:
            sys = T1Mamdani(engine=engine, defuzzification=_defuzzification_from_attr(defuzzifier))
    elif rules["type"] == "takagi-sugeno":
        sys = T1TSK()
    else:
        raise ValueError(f"Unknown system type: {rules['type']}")

    # Cache of T1FS objects (Mamdani) or TSK coefficient dicts (TSK),
    # keyed as sets_cache[variable_name][term_name].
    sets_cache = {}

    for var_type in ["input", "output"]:
        for var_name, var_info in variables[var_type].items():
            if var_type == "input":
                sys.add_input_variable(var_name)
            else:
                sys.add_output_variable(var_name)

            sets_cache[var_name] = {}
            domain = linspace(var_info["domainleft"], var_info["domainright"], DOMAIN_RESOLUTION)

            for term_name, term_info in var_info["terms"].items():
                mf_type = term_info["set"]
                params = _default_height(mf_type, [float(p) for p in term_info["params"]])

                if rules["type"] == "mamdani" or var_type == "input":
                    t1fs = T1FS(domain, MF_MAP[mf_type], params)
                    if str(term_info.get("complement")).lower() == "true":
                        t1fs = -t1fs
                    sets_cache[var_name][term_name] = t1fs
                else:
                    # Linear TSK output: a singleton term is treated as the
                    # constant coefficient of a (so far purely constant)
                    # linear consequent.
                    coeffs = {"const": float(params[0]) if mf_type == "singletonShape" else 0.0}
                    for inp in variables["input"]:
                        coeffs[inp] = 0.0
                    sets_cache[var_name][term_name] = coeffs

    rule_data = rules["rules"]
    if isinstance(rule_data, dict):
        rule_data = rule_data.values()

    for rule in rule_data:
        if rule.get("connector") == "or" and len(rule["antecedent"]) > 1:
            raise ValueError(
                "Rule antecedents with an 'or' connector across multiple clauses "
                "are not supported: the underlying T1Mamdani/T1TSK evaluation "
                "engines only combine antecedent clauses with AND.")

        antecedent = [(var_name, sets_cache[var_name][term_name])
                      for var_name, term_name in rule["antecedent"]]
        consequent = [(var_name, sets_cache[var_name][term_name])
                      for var_name, term_name in rule["consequent"]]
        sys.add_rule(antecedent, consequent)

    return sys


def negated_term_name(term_name):
    """Returns the name used for the complemented counterpart of a term."""
    return f"NOT_{term_name}"


def ensure_negated_term(variables, var_name, term_name):
    """
    Lazily creates the complemented (negated) counterpart of a term, and
    returns its name, so that clause-level negation -- FML's ``NOT="true"``
    clause attribute, or FCL's ``IS NOT`` -- can be expressed through the
    same per-term ``complement`` mechanism used by :func:`generate_system`,
    without any extra seam in the fuzzy logic system classes themselves.

    .. rubric:: Parameters

    variables : dict

        See :func:`generate_system`. Mutated in place: the negated term is
        added to ``variables[var_type][var_name]["terms"]`` the first time
        it is requested.

    var_name : str

    term_name : str

        The variable and term to negate.

    .. rubric:: Returns

    output : str

        The name of the (possibly newly created) complemented term.
    """
    var_type = "input" if var_name in variables["input"] else "output"
    terms = variables[var_type][var_name]["terms"]
    negated_name = negated_term_name(term_name)
    if negated_name not in terms:
        base = terms[term_name]
        was_negated = str(base.get("complement")).lower() == "true"
        terms[negated_name] = {
            "set": base["set"], "params": base["params"],
            "complement": "false" if was_negated else "true",
        }
    return negated_name


class FML:
    """
    Parser and generator for the IEEE 1855 Fuzzy Markup Language (FML).

    .. rubric:: Functions

    parse_fml:

        Parses an FML XML string into the shared ``(name, variables, rules)``
        intermediate representation.

    generate:

        Builds a runnable :class:`pyit2fls.T1Mamdani`/:class:`pyit2fls.T1TSK`
        system out of that representation (a thin wrapper of
        :func:`generate_system`).

    .. rubric:: Examples

    >>> myFML = FML()
    >>> name, variables, rules = myFML.parse_fml(fml_xml_string)
    >>> system = myFML.generate(variables, rules)
    >>> system.evaluate({"temp": 25})
    """

    def generate(self, variables, rules):
        """
        Builds a Type 1 Fuzzy Logic System (Mamdani or TSK) based on parsed
        variables and rules. See :func:`generate_system`.
        """
        return generate_system(variables, rules)

    def parse_fml(self, fml_xml_string):
        """
        Parses an FML XML document.

        .. rubric:: Parameters

        fml_xml_string : str

            The FML document, as a string, with a root ``<FuzzySystem>`` tag.

        .. rubric:: Returns

        output : tuple

            A tuple ``(system_name, variables, rules)``. See
            :func:`generate_system` for the shape of ``variables`` and
            ``rules``.
        """
        Variables = {"input": {}, "output": {}}

        root = ET.fromstring(fml_xml_string)
        if root.tag != "FuzzySystem":
            raise ValueError("FML root should be a <FuzzySystem> tag.")

        system_name = root.get("name")

        kb = root.find("KnowledgeBase")
        if kb is None:
            raise ValueError("FML is missing a <KnowledgeBase> tag.")

        for var_elem in kb.findall("FuzzyVariable"):
            var_name = var_elem.get("name")
            var_type = var_elem.get("type")

            Variables[var_type][var_name] = {
                "domainleft": float(var_elem.get("domainleft")),
                "domainright": float(var_elem.get("domainright")),
                "defuzzifier": var_elem.get("defuzzifier"),
                "terms": {},
            }

            for ft_elem in var_elem.findall("FuzzyTerm"):
                ft_name = ft_elem.get("name")
                fs_elem = ft_elem[0]
                fs_type = fs_elem.tag
                params = [float(fs_elem.attrib[f"param{i + 1}"].strip())
                          for i in range(len(fs_elem.attrib.keys()))]

                Variables[var_type][var_name]["terms"][ft_name] = {
                    "complement": ft_elem.get("complement"),
                    "set": fs_type,
                    "params": params,
                }

        Rules = {"rules": {}}

        rulebase_elem = root.find("RuleBase")
        if rulebase_elem is not None:
            Rules["name"] = rulebase_elem.get("name")
            Rules["type"] = rulebase_elem.get("type")
            Rules["andMethod"] = rulebase_elem.get("andMethod")
            Rules["orMethod"] = rulebase_elem.get("orMethod")
            Rules["activationMethod"] = rulebase_elem.get("activationMethod")

            def _clause_term(clause):
                var_name, term_name = clause.get("var"), clause.get("term")
                if str(clause.get("NOT")).lower() == "true":
                    term_name = ensure_negated_term(Variables, var_name, term_name)
                return var_name, term_name

            for rule_elem in rulebase_elem.findall("Rule"):
                rule_name = rule_elem.get("name")
                weight = rule_elem.get("weight")
                Rules["rules"][rule_name] = {
                    "connector": rule_elem.get("connector"),
                    "weight": float(weight) if weight is not None else 1.0,
                    "antecedent": [_clause_term(clause)
                                   for clause in rule_elem.findall("Antecedent/Clause")],
                    "consequent": [_clause_term(clause)
                                   for clause in rule_elem.findall("Consequent/Clause")],
                }

        return system_name, Variables, Rules

    def export_fml(self, name, variables, rules):
        """
        Serializes a ``(name, variables, rules)`` triple, in the shared
        intermediate representation, back into FML XML text.

        .. rubric:: Parameters

        name : str

            Name of the fuzzy system (the ``<FuzzySystem name=...>``
            attribute).

        variables : dict

        rules : dict

            See :func:`generate_system` for the shape of ``variables`` and
            ``rules``.

        .. rubric:: Returns

        output : str

            The FML XML source text, pretty-printed.

        .. rubric:: Notes

        Every term, including the synthetic ``NOT_<term>`` complements
        created by :func:`pyit2fls.FCL.FCL.parse_fcl` for ``IS NOT``
        clauses, is written out as an ordinary ``<FuzzyTerm>`` with its
        ``complement`` attribute — that mechanism is native to FML, so no
        special-casing is needed for a correct round trip through
        :func:`parse_fml`.
        """
        def fmt(v):
            return f"{float(v):g}"

        root = ET.Element("FuzzySystem", {"name": name or "System"})
        kb = ET.SubElement(root, "KnowledgeBase")

        for var_type in ("input", "output"):
            for var_name, var_info in variables[var_type].items():
                attrs = {
                    "name": var_name, "type": var_type,
                    "domainleft": fmt(var_info["domainleft"]),
                    "domainright": fmt(var_info["domainright"]),
                }
                if var_type == "output" and var_info.get("defuzzifier"):
                    attrs["defuzzifier"] = var_info["defuzzifier"]
                var_elem = ET.SubElement(kb, "FuzzyVariable", attrs)

                for term_name, term_info in var_info["terms"].items():
                    term_elem = ET.SubElement(var_elem, "FuzzyTerm", {
                        "name": term_name,
                        "complement": str(term_info.get("complement", "false")),
                    })
                    shape_attrs = {f"param{i + 1}": fmt(p) for i, p in enumerate(term_info["params"])}
                    ET.SubElement(term_elem, term_info["set"], shape_attrs)

        rulebase = ET.SubElement(root, "RuleBase", {
            "name": rules.get("name") or "rules",
            "type": rules.get("type", "mamdani"),
            "andMethod": rules.get("andMethod", "prod"),
            "orMethod": rules.get("orMethod", "max"),
            "activationMethod": rules.get("activationMethod", "min"),
        })

        rule_data = rules["rules"]
        rule_items = rule_data.items() if isinstance(rule_data, dict) else enumerate(rule_data, start=1)
        for rule_name, rule in rule_items:
            rule_elem = ET.SubElement(rulebase, "Rule", {
                "name": str(rule_name),
                "connector": rule.get("connector", "and"),
                "weight": fmt(rule.get("weight", 1.0)),
            })
            antecedent_elem = ET.SubElement(rule_elem, "Antecedent")
            for var_name, term_name in rule["antecedent"]:
                ET.SubElement(antecedent_elem, "Clause", {"var": var_name, "term": term_name})
            consequent_elem = ET.SubElement(rule_elem, "Consequent")
            for var_name, term_name in rule["consequent"]:
                ET.SubElement(consequent_elem, "Clause", {"var": var_name, "term": term_name})

        raw = ET.tostring(root, encoding="unicode")
        return minidom.parseString(raw).toprettyxml(indent="    ")


if __name__ == "__main__":
    FML_STRING = """
    <FuzzySystem name="HVAC_Controller">
        <KnowledgeBase>
            <FuzzyVariable name="temp" type="input" domainleft="0" domainright="100">
                <FuzzyTerm name="cold" complement="false">
                    <triangularShape param1="0" param2="0" param3="40"/>
                </FuzzyTerm>
                <FuzzyTerm name="warm" complement="false">
                    <triangularShape param1="30" param2="50" param3="70"/>
                </FuzzyTerm>
                <FuzzyTerm name="hot" complement="false">
                    <triangularShape param1="60" param2="100" param3="100"/>
                </FuzzyTerm>
            </FuzzyVariable>

            <FuzzyVariable name="fan" type="output" domainleft="0" domainright="100" defuzzifier="COG">
                <FuzzyTerm name="low" complement="false">
                    <trapezoidalShape param1="-20" param2="0" param3="20" param4="40"/>
                </FuzzyTerm>
                <FuzzyTerm name="high" complement="false">
                    <trapezoidalShape param1="60" param2="80" param3="100" param4="120"/>
                </FuzzyTerm>
            </FuzzyVariable>
        </KnowledgeBase>

        <RuleBase name="MamdaniRules" type="mamdani" andMethod="prod" orMethod="max" activationMethod="min">
            <Rule name="1" connector="and" weight="1.0">
                <Antecedent>
                    <Clause var="temp" term="cold"/>
                </Antecedent>
                <Consequent>
                    <Clause var="fan" term="low"/>
                </Consequent>
            </Rule>
            <Rule name="2" connector="and" weight="1.0">
                <Antecedent>
                    <Clause var="temp" term="hot"/>
                </Antecedent>
                <Consequent>
                    <Clause var="fan" term="high"/>
                </Consequent>
            </Rule>
        </RuleBase>
    </FuzzySystem>
    """

    myFML = FML()
    name, variables, rules = myFML.parse_fml(FML_STRING)
    print(f"Parsed FML system: {name}")
    FS = myFML.generate(variables, rules)
    print(FS.evaluate({"temp": 25}))
