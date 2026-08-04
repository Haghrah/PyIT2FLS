"""
Support for the IEC 61131-7 Fuzzy Control Language (FCL) standard.

This module implements the core Mamdani-style subset of FCL: a single
``FUNCTION_BLOCK`` with ``VAR_INPUT``/``VAR_OUTPUT`` declarations,
``FUZZIFY``/``DEFUZZIFY`` blocks whose terms are piecewise-linear point
lists, and a single ``RULEBLOCK``. Structured Text method bodies and
multiple chained rule blocks (both part of the full IEC 61131-7 standard)
are not supported.

Like :mod:`pyit2fls.FML`, this module parses FCL text into the shared
``(name, variables, rules)`` intermediate representation described in
:func:`pyit2fls.FML.generate_system`, and reuses that function to build a
runnable :class:`pyit2fls.T1Mamdani` system. It also implements the
opposite direction, :func:`FCL.export_fcl`, so the PyIT2FLS designer GUI
(:mod:`pyit2fls.designerui`) can save a system as an FCL file.

See ``IEC61131-7.md`` in the repository root for a description of the
standard, and ``markdown docs/FCL.md`` for a tutorial.
"""
import re
try:
    from pyit2fls.FML import generate_system, negated_term_name, ensure_negated_term
except ImportError:
    # Allows `python3 pyit2fls/FCL.py` to be run directly: in that mode
    # Python's sys.path[0] is the pyit2fls/ directory itself, which shadows
    # the installed "pyit2fls" package with the sibling pyit2fls.py module.
    from FML import generate_system, negated_term_name, ensure_negated_term

#: Matches a floating point number, with optional sign and exponent.
_NUMBER = r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?"
#: Matches a single (x, y) point, as used in FUZZIFY/DEFUZZIFY TERM lists.
_POINT = re.compile(r"\(\s*(" + _NUMBER + r")\s*,\s*(" + _NUMBER + r")\s*\)")


def _strip_comments(text):
    """Removes ``(* ... *)`` FCL comments from the source text."""
    return re.sub(r"\(\*.*?\*\)", " ", text, flags=re.DOTALL)


def _parse_var_block(text, keyword):
    """Extracts declared variable names from a VAR_INPUT/VAR_OUTPUT block."""
    m = re.search(keyword + r"(.*?)END_VAR", text, re.DOTALL | re.IGNORECASE)
    if m is None:
        return []
    return re.findall(r"(\w+)\s*:\s*\w+\s*;", m.group(1))


def _parse_terms(body):
    """
    Parses every ``TERM <name> := (x,y) (x,y) ... ;`` entry in a
    FUZZIFY/DEFUZZIFY block body into the shared ``terms`` dict shape.
    """
    terms = {}
    for term_match in re.finditer(r"TERM\s+(\w+)\s*:=\s*(.*?);", body, re.DOTALL | re.IGNORECASE):
        term_name = term_match.group(1)
        points = _POINT.findall(term_match.group(2))
        if not points:
            raise ValueError(f"TERM {term_name} has no valid (x, y) points.")
        params = [float(v) for pair in points for v in pair]
        terms[term_name] = {"set": "pointsShape", "params": params, "complement": "false"}
    return terms


def _domain_from_terms(terms):
    xs = [x for term in terms.values() for x in term["params"][0::2]]
    return min(xs), max(xs)


def _parse_fuzzify_blocks(text, keyword, end_keyword, declared_vars):
    """Parses every FUZZIFY or DEFUZZIFY block, keyed by variable name."""
    variables = {}
    for block in re.finditer(keyword + r"\s+(\w+)(.*?)" + end_keyword, text, re.DOTALL | re.IGNORECASE):
        var_name, body = block.group(1), block.group(2)
        terms = _parse_terms(body)

        range_match = re.search(r"RANGE\s*:=\s*\(\s*(" + _NUMBER + r")\s*\.\.\s*(" + _NUMBER + r")\s*\)",
                                 body, re.IGNORECASE)
        if range_match:
            domainleft, domainright = float(range_match.group(1)), float(range_match.group(2))
        else:
            domainleft, domainright = _domain_from_terms(terms)

        method_match = re.search(r"METHOD\s*:\s*(\w+)\s*;", body, re.IGNORECASE)
        defuzzifier = method_match.group(1).upper() if method_match else None
        if defuzzifier is not None and defuzzifier not in ("COG", "COA"):
            raise NotImplementedError(
                f"The {defuzzifier} defuzzification method is not supported; "
                "only COG and COA are implemented.")

        variables[var_name] = {
            "domainleft": domainleft, "domainright": domainright,
            "defuzzifier": defuzzifier, "terms": terms,
        }

    missing = set(declared_vars) - set(variables)
    if missing:
        raise ValueError(f"No {keyword} block found for variable(s): {', '.join(sorted(missing))}")
    return variables


def _split_clauses(text, variables):
    """
    Splits the text of a rule's IF or THEN part into a connector
    (``"and"``/``"or"``) and a list of ``(variable, term)`` clauses,
    resolving ``IS NOT`` negation via :func:`ensure_negated_term`.
    """
    text = text.replace("(", " ").replace(")", " ")
    has_and = re.search(r"\bAND\b", text, re.IGNORECASE) is not None
    has_or = re.search(r"\bOR\b", text, re.IGNORECASE) is not None
    if has_and and has_or:
        raise NotImplementedError(
            "Mixing AND and OR within a single rule is not supported by the FCL parser.")
    connector = "or" if has_or else "and"

    clauses = []
    for part in re.split(r"\bAND\b|\bOR\b", text, flags=re.IGNORECASE):
        part = part.strip()
        if not part:
            continue
        m = re.match(r"(\w+)\s+IS\s+(NOT\s+)?(\w+)", part, re.IGNORECASE)
        if not m:
            raise ValueError(f"Could not parse rule clause: {part!r}")
        var_name, negated, term_name = m.group(1), m.group(2) is not None, m.group(3)
        if negated:
            term_name = ensure_negated_term(variables, var_name, term_name)
        clauses.append((var_name, term_name))
    return connector, clauses


def _parse_ruleblock(text, variables):
    blocks = list(re.finditer(r"RULEBLOCK\s+(\w+)(.*?)END_RULEBLOCK", text, re.DOTALL | re.IGNORECASE))
    if not blocks:
        raise ValueError("FCL is missing a RULEBLOCK.")
    if len(blocks) > 1:
        raise NotImplementedError(
            "Multiple chained RULEBLOCKs are not supported; only a single RULEBLOCK is.")
    block = blocks[0]
    body = block.group(2)

    def _method(name, default):
        m = re.search(name + r"\s*:\s*(\w+)\s*;", body, re.IGNORECASE)
        return m.group(1).lower() if m else default

    rules = {
        "name": block.group(1), "type": "mamdani",
        "andMethod": _method("AND", "min"),
        "orMethod": _method("OR", "max"),
        "activationMethod": _method("ACT", "min"),
        "accumulationMethod": _method("ACCU", "max"),
        "rules": {},
    }

    rule_pattern = (r"RULE\s+(\w+)\s*:\s*IF\s+(.*?)\s+THEN\s+(.*?)"
                     r"(?:\s+WITH\s+(" + _NUMBER + r")\s*)?;")
    for rule_match in re.finditer(rule_pattern, body, re.DOTALL | re.IGNORECASE):
        rule_name, if_text, then_text, weight = rule_match.groups()
        antecedent_connector, antecedent = _split_clauses(if_text, variables)
        consequent_connector, consequent = _split_clauses(then_text, variables)
        if consequent_connector == "or":
            raise ValueError(f"Rule {rule_name}: OR is not supported in the THEN part.")

        rules["rules"][rule_name] = {
            "connector": antecedent_connector,
            "weight": float(weight) if weight is not None else 1.0,
            "antecedent": antecedent,
            "consequent": consequent,
        }

    return rules


class FCL:
    """
    Parser and generator for the core Mamdani subset of the IEC 61131-7
    Fuzzy Control Language (FCL).

    .. rubric:: Functions

    parse_fcl:

        Parses an FCL text document into the shared ``(name, variables,
        rules)`` intermediate representation (the same one produced by
        :func:`pyit2fls.FML.FML.parse_fml`).

    generate:

        Builds a runnable :class:`pyit2fls.T1Mamdani` system out of that
        representation (a thin wrapper of
        :func:`pyit2fls.FML.generate_system`).

    export_fcl:

        Serializes a ``(name, variables, rules)`` triple back into FCL text.

    .. rubric:: Examples

    >>> myFCL = FCL()
    >>> name, variables, rules = myFCL.parse_fcl(fcl_text)
    >>> system = myFCL.generate(variables, rules)
    >>> system.evaluate({"temp": 25})
    """

    def generate(self, variables, rules):
        """
        Builds a Type 1 Mamdani Fuzzy Logic System based on parsed
        variables and rules. See :func:`pyit2fls.FML.generate_system`.
        """
        return generate_system(variables, rules)

    def parse_fcl(self, fcl_text):
        """
        Parses an IEC 61131-7 FCL document (core Mamdani subset).

        .. rubric:: Parameters

        fcl_text : str

            The FCL document, as a string, starting with a
            ``FUNCTION_BLOCK`` declaration.

        .. rubric:: Returns

        output : tuple

            A tuple ``(system_name, variables, rules)``, with the same
            shape produced by :func:`pyit2fls.FML.FML.parse_fml`. FUZZIFY/
            DEFUZZIFY TERM points are stored with ``"set": "pointsShape"``,
            understood by :func:`pyit2fls.points_mf`.

        .. rubric:: Notes

        Only a single ``RULEBLOCK`` is supported. Rule ``WITH`` weights and
        the RULEBLOCK's ``ACCU`` (accumulation) setting are parsed and kept
        in the returned ``rules`` dict for reference, but are not applied
        while evaluating the generated system — see the notes in
        :func:`pyit2fls.FML.generate_system`.
        """
        text = _strip_comments(fcl_text)

        name_match = re.search(r"FUNCTION_BLOCK\s+(\w+)", text, re.IGNORECASE)
        if name_match is None:
            raise ValueError("FCL text must start with a FUNCTION_BLOCK declaration.")
        system_name = name_match.group(1)

        input_names = _parse_var_block(text, "VAR_INPUT")
        output_names = _parse_var_block(text, "VAR_OUTPUT")

        variables = {
            "input": _parse_fuzzify_blocks(text, "FUZZIFY", "END_FUZZIFY", input_names),
            "output": _parse_fuzzify_blocks(text, "DEFUZZIFY", "END_DEFUZZIFY", output_names),
        }
        rules = _parse_ruleblock(text, variables)

        return system_name, variables, rules

    def export_fcl(self, name, variables, rules):
        """
        Serializes a ``(name, variables, rules)`` triple, in the shared
        intermediate representation, back into FCL text.

        .. rubric:: Parameters

        name : str

            Name of the function block.

        variables : dict

            See :func:`pyit2fls.FML.generate_system`.

        rules : dict

            See :func:`pyit2fls.FML.generate_system`.

        .. rubric:: Returns

        output : str

            The FCL source text.

        .. rubric:: Notes

        Terms are always written out as explicit ``(x, y)`` point lists.
        Terms already stored with ``"set": "pointsShape"`` (as produced by
        :func:`parse_fcl`) round-trip exactly; other membership function
        shapes (e.g. those authored through :mod:`pyit2fls.FML` or the
        designer GUI) are sampled at 21 evenly spaced points across the
        variable's domain, which is an approximation for non-piecewise-
        linear shapes such as ``gaussianShape``.
        """
        try:
            from pyit2fls.FML import MF_MAP, _default_height
        except ImportError:
            from FML import MF_MAP, _default_height
        from numpy import linspace

        def _points_of(var_type, var_name, term_name, term_info):
            if term_info["set"] == "pointsShape":
                pts = term_info["params"]
                return list(zip(pts[0::2], pts[1::2]))
            var_info = variables[var_type][var_name]
            xs = linspace(var_info["domainleft"], var_info["domainright"], 21)
            mf = MF_MAP[term_info["set"]]
            # A term's height is optional wherever terms are authored (e.g.
            # the designer GUI); apply the same default-height normalization
            # generate_system uses before evaluating the raw mf function,
            # otherwise shapes saved without an explicit height (a valid,
            # common case) raise an IndexError here.
            params = _default_height(term_info["set"], list(term_info["params"]))
            ys = mf(xs, params)
            return list(zip(xs.tolist(), [float(y) for y in ys]))

        lines = [f"FUNCTION_BLOCK {name}", ""]

        for keyword, var_type in (("VAR_INPUT", "input"), ("VAR_OUTPUT", "output")):
            lines.append(keyword)
            for var_name in variables[var_type]:
                lines.append(f"    {var_name} : REAL;")
            lines.append("END_VAR")
            lines.append("")

        for fuzzify_kw, end_kw, var_type in (("FUZZIFY", "END_FUZZIFY", "input"),
                                              ("DEFUZZIFY", "END_DEFUZZIFY", "output")):
            for var_name, var_info in variables[var_type].items():
                lines.append(f"{fuzzify_kw} {var_name}")
                for term_name, term_info in var_info["terms"].items():
                    if term_name.startswith("NOT_"):
                        continue
                    points = _points_of(var_type, var_name, term_name, term_info)
                    points_text = " ".join(f"({x:g},{y:g})" for x, y in points)
                    lines.append(f"    TERM {term_name} := {points_text};")
                if var_type == "output":
                    lines.append(f"    METHOD : {var_info.get('defuzzifier') or 'COG'};")
                    lines.append("    DEFAULT := 0;")
                lines.append(f"    RANGE := ({var_info['domainleft']:g} .. {var_info['domainright']:g});")
                lines.append(end_kw)
                lines.append("")

        lines.append(f"RULEBLOCK {rules.get('name') or 'rules'}")
        lines.append(f"    AND : {rules.get('andMethod', 'min').upper()};")
        lines.append(f"    OR : {rules.get('orMethod', 'max').upper()};")
        lines.append(f"    ACT : {rules.get('activationMethod', 'min').upper()};")
        lines.append(f"    ACCU : {rules.get('accumulationMethod', 'max').upper()};")

        rule_data = rules["rules"]
        if isinstance(rule_data, dict):
            rule_data = rule_data.items()
        else:
            rule_data = enumerate(rule_data, start=1)

        for rule_name, rule in rule_data:
            def _clause_text(var, term):
                if term.startswith("NOT_"):
                    return f"{var} IS NOT {term[len('NOT_'):]}"
                return f"{var} IS {term}"

            connector = " AND " if rule.get("connector", "and") == "and" else " OR "
            antecedent = connector.join(_clause_text(var, term) for var, term in rule["antecedent"])
            consequent = " AND ".join(_clause_text(var, term) for var, term in rule["consequent"])
            lines.append(f"    RULE {rule_name} : IF {antecedent} THEN {consequent};")
        lines.append("END_RULEBLOCK")
        lines.append("")
        lines.append("END_FUNCTION_BLOCK")

        return "\n".join(lines)


if __name__ == "__main__":
    FCL_TEXT = """
    FUNCTION_BLOCK HVAC_Controller

    VAR_INPUT
        temp : REAL;
    END_VAR

    VAR_OUTPUT
        fan : REAL;
    END_VAR

    FUZZIFY temp
        TERM cold := (0,1) (40,0);
        TERM warm := (30,0) (50,1) (70,0);
        TERM hot := (60,0) (100,1);
    END_FUZZIFY

    DEFUZZIFY fan
        TERM low := (-20,0) (0,1) (20,1) (40,0);
        TERM high := (60,0) (80,1) (100,1) (120,0);
        METHOD : COG;
        DEFAULT := 0;
    END_DEFUZZIFY

    RULEBLOCK rules
        AND : MIN;
        ACT : MIN;
        ACCU : MAX;
        RULE 1 : IF temp IS cold THEN fan IS low;
        RULE 2 : IF temp IS hot THEN fan IS high;
    END_RULEBLOCK

    END_FUNCTION_BLOCK
    """

    myFCL = FCL()
    name, variables, rules = myFCL.parse_fcl(FCL_TEXT)
    print(f"Parsed FCL system: {name}")
    FS = myFCL.generate(variables, rules)
    print(FS.evaluate({"temp": 25}))
    print(myFCL.export_fcl(name, variables, rules))
