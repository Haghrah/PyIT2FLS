import xml.etree.ElementTree as ET
from numpy import (linspace, )
from pyit2fls import (T1Mamdani, T1TSK, T1FS, tri_mf, ltri_mf, rtri_mf, trapezoid_mf, gaussian_mf, singleton_mf, )

class FML:

    def __init__(self, ):
        pass

    def generate(self, variables, rules):
        """
        Generates a Type-1 Fuzzy Logic System (Mamdani or TSK) based on 
        parsed variables and rules.
        """
        # Mapping FML membership function shapes to pyit2fls functions
        MF_MAP = {
            "triangularShape": tri_mf,
            "trapezoidalShape": trapezoid_mf,
            "gaussianShape": gaussian_mf,
            "singletonShape": singleton_mf,
        }

        # Initialize the system based on the rule base type
        if rules["type"] == "mamdani":
            sys = T1Mamdani()
        elif rules["type"] == "takagi-sugeno":
            sys = T1TSK()
        else:
            raise ValueError(f"Unknown system type: {rules['type']}")
        
        # Cache to store created T1FS objects or TSK coefficients
        # Structure: {variable_name: {term_name: T1FS_or_coeff_dict}}
        sets_cache = {}

        # 1. Process Input and Output Variables
        for var_type in ["input", "output"]:
            for var_name, var_info in variables[var_type].items():
                if var_type == "input":
                    sys.add_input_variable(var_name)
                else:
                    sys.add_output_variable(var_name)
                
                sets_cache[var_name] = {}
                
                # Define the universe of discourse (domain) for T1FS
                domain = linspace(var_info["domainleft"], var_info["domainright"], 100)
                
                for term_name, term_info in var_info["terms"].items():
                    mf_type = term_info["set"]
                    params = [float(p) for p in term_info["params"]]
                    
                    # For all inputs and Mamdani outputs, we create T1FS objects
                    if rules["type"] == "mamdani" or var_type == "input":
                        # pyit2fls membership functions require a height parameter (params[-1])
                        # FML defaults to 1.0 if not specified
                        if mf_type == "triangularShape" and len(params) == 3:
                            params.append(1.0)
                        elif mf_type == "trapezoidalShape" and len(params) == 4:
                            params.append(1.0)
                        elif mf_type == "gaussianShape" and len(params) == 2:
                            params.append(1.0)
                        elif mf_type == "singletonShape" and len(params) == 1:
                            params.append(1.0)
                            
                        sets_cache[var_name][term_name] = T1FS(domain, MF_MAP[mf_type], params)

                        if term_info["complement"] == "true":
                            sets_cache[var_name][term_name] = - sets_cache[var_name][term_name]
                    
                    # For TSK outputs, we store coefficient dictionaries
                    else:
                        if mf_type == "singletonShape":
                            sets_cache[var_name][term_name] = {"const": float(params[0])}
                            # Initialize other input coefficients to 0 for linear TSK
                            for inp in variables["input"]:
                                sets_cache[var_name][term_name][inp] = 0.0
                        else:
                            # Default to 0 constant if shape is not a singleton
                            sets_cache[var_name][term_name] = {"const": 0.0}

        # 2. Add Rules to the System
        # Iterate through the rules dictionary populated by parse_fml
        rule_data = rules["rules"]
        if isinstance(rule_data, dict):
            rule_data = rule_data.values()

        for rule in rule_data:
            # Construct antecedent: list of (var_name, T1FS)
            antecedent = []
            for var_name, term_name in rule["antecedent"]:
                antecedent.append((var_name, sets_cache[var_name][term_name]))
            
            # Construct consequent: list of (var_name, T1FS) or (var_name, coeff_dict)
            consequent = []
            for var_name, term_name in rule["consequent"]:
                consequent.append((var_name, sets_cache[var_name][term_name]))
            
            sys.add_rule(antecedent, consequent)

        return sys


    def parse_fml(self, fml_xml_string):
        """
        Parses FML XML and populates FuzzyVariable and FuzzySet objects.
        A separate function would handle Rule parsing.
        """
        Variables = {"input":{}, 
                     "output":{}}
        
        # Parse the XML
        root = ET.fromstring(fml_xml_string)
        if root.tag != "FuzzySystem":
            raise ValueError("FML root should be a <FuzzySystem> tag.")
        
        system_name  = root.get("name")
        print(f"--- Parsing Fuzzy System: {system_name} ---")

        # Find the Knowledge Base
        kb = root.find("KnowledgeBase")
        if kb is None:
            raise ValueError("FML is missing a <KnowledgeBase> tag.")

        # Iterate through all <FuzzyVariable> elements
        for var_elem in kb.findall("FuzzyVariable"):
            var_name  = var_elem.get("name")
            var_type  = var_elem.get("type")

            Variables[var_type][var_name] = {}

            var_left  = float(var_elem.get("domainleft"))
            var_right = float(var_elem.get("domainright"))

            Variables[var_type][var_name]["domainleft"] = var_left
            Variables[var_type][var_name]["domainright"] = var_right
            Variables[var_type][var_name]["terms"] = {}
            
            # Iterate through all <FuzzyTerm> elements for this variable
            for ft_elem in var_elem.findall("FuzzyTerm"):
                ft_name = ft_elem.get("name")

                Variables[var_type][var_name]["terms"][ft_name] = {}

                ft_comp = ft_elem.get("complement")
                Variables[var_type][var_name]["terms"][ft_name]["complement"] = ft_comp
                
                # Get the fuzzy set from <FuzzyTerm>
                fs_elem = ft_elem[0]
                fs_type = fs_elem.tag
                Variables[var_type][var_name]["terms"][ft_name]["set"] = fs_type
                # Parse parameters string into a list of floats
                params = [float(fs_elem.attrib[f"param{i + 1}"].strip()) for i in range(len(fs_elem.attrib.keys()))]
                Variables[var_type][var_name]["terms"][ft_name]["params"] = params
                
                # Instantiate the library"s FuzzySet object and add it to the variable
                print(f"Variable {var_name}:\t{ft_name},\t{fs_type},\t{params}")

        # Rule Parsing
        Rules = {}

        rulebase_elem = root.find("RuleBase")
        if rulebase_elem is not None:
            print("\n--- Rule Base Found ---")
            rb_name = rulebase_elem.get("name")
            Rules["name"] = rb_name

            rb_type = rulebase_elem.get("type")
            Rules["type"] = rb_type

            rb_andMethod = rulebase_elem.get("andMethod")
            Rules["andMethod"] = rb_andMethod

            rb_orMethod = rulebase_elem.get("orMethod")
            Rules["orMethod"] = rb_orMethod

            rb_activationMethod = rulebase_elem.get("activationMethod")
            Rules["activationMethod"] = rb_activationMethod

            Rules["rules"] = {}
            for rule_elem in rulebase_elem.findall("Rule"):
                rule_name = rule_elem.get("name")
                Rules["rules"][rule_name] = {}
                Rules["rules"][rule_name]["connector"] = rule_elem.get("connector")
                Rules["rules"][rule_name]["weight"] = float(rule_elem.get("weight"))
                Rules["rules"][rule_name]["antecedent"] = []
                Rules["rules"][rule_name]["consequent"] = []

                # In a real parser, you"d recursively process antecedent/consequent
                antecedent = rule_elem.findall("Antecedent/Clause")
                consequent = rule_elem.findall("Consequent/Clause")

                # Look up the actual objects from the "variables" dictionary
                # For brevity, we just print the extracted rule logic
                antecedent_parts = []
                consequent_parts = []
                for clause in antecedent:
                    clause_var = clause.get("var")
                    clause_term = clause.get("term")
                    Rules["rules"][rule_name]["antecedent"].append((clause_var, clause_term))
                    antecedent_parts.append(f"{clause_var}\tIS\t{clause_term}")
                for clause in consequent:
                    clause_var = clause.get("var")
                    clause_term = clause.get("term")
                    Rules["rules"][rule_name]["consequent"].append((clause_var, clause_term))
                    consequent_parts.append(f"{clause_var}\tIS\t{clause_term}")

                rule_text = f"IF\t{rb_andMethod.join(antecedent_parts)}\tTHEN\t{rb_andMethod.join(consequent_parts)}"
                print(rule_text)
        
        return system_name, Variables, Rules





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

            <FuzzyVariable name="fan" type="output" domainleft="0" domainright="100">
                <FuzzyTerm name="low" complement="false"> 
                    <trapezoidalShape param1="0" param2="0" param3="20" param4="40"/>
                type="trapezoid" params="0, 0, 20, 40"/>
                </FuzzyTerm>
                <FuzzyTerm name="high" complement="false"> 
                    <trapezoidalShape param1="60" param2="80" param3="100" param4="100"/>
                </FuzzyTerm>
            </FuzzyVariable>
        </KnowledgeBase>

        <RuleBase name="MamdaniRules" type="mamdani" andMethod="prod" orMethod="max" activationMethod="min">
            <Rule name="1" connector="or" weight="1.0">
                <Antecedent>
                    <Clause var="temp" term="cold"/>
                </Antecedent>
                <Consequent>
                    <Clause var="fan" term="low"/>
                </Consequent>
            </Rule>
            <Rule name="2" connector="or" weight="1.0">
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
    result = myFML.parse_fml(FML_STRING)
    print(result)
    FS = myFML.generate(result[1], result[2])













