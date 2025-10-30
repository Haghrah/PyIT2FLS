import xml.etree.ElementTree as ET

class FML:

    def __init__(self, ):
        pass

    def parse_fml(self, fml_xml_string):
        """
        Parses FML XML and populates FuzzyVariable and FuzzySet objects.
        A separate function would handle Rule parsing.
        """
        
        # Parse the XML
        root = ET.fromstring(fml_xml_string)
        system_name  = root.get('name')
        print(f"--- Parsing Fuzzy System: {system_name} ---")

        # Find the Knowledge Base
        kb = root.find('KnowledgeBase')
        if kb is None:
            raise ValueError("FML is missing a <KnowledgeBase> tag.")

        # Iterate through all <FuzzyVariable> elements
        for var_elem in kb.findall('FuzzyVariable'):
            var_name  = var_elem.get('name')
            var_type  = var_elem.get('type')
            var_left  = var_elem.get('domainleft')
            var_right = var_elem.get('domainright')
            
            # Iterate through all <FuzzyTerm> elements for this variable
            for ft_elem in var_elem.findall('FuzzyTerm'):
                ft_name = ft_elem.get('name')
                ft_comp = ft_elem.get('complement')
                # Get the fuzzy set from <FuzzyTerm>
                fs_elem = ft_elem[0]
                fs_type = fs_elem.tag
                # Parse parameters string into a list of floats
                params = [float(fs_elem.attrib[f"param{i + 1}"].strip()) for i in range(len(fs_elem.attrib.keys()))]
                
                # Instantiate the library's FuzzySet object and add it to the variable
                print(f"Variable {var_name}:\t{ft_name},\t{fs_type},\t{params}")

        # Rule Parsing (Simplified)
        rulebase_elem = root.find('RuleBase')
        if rulebase_elem is not None:
            print("\n--- Rule Base Found ---")
            rb_name = rulebase_elem.get('name')
            rb_type = rulebase_elem.get('type')
            rb_andMethod = rulebase_elem.get('andMethod')
            rb_orMethod = rulebase_elem.get('orMethod')
            rb_activationMethod = rulebase_elem.get('activationMethod')
            for rule_elem in rulebase_elem.findall('Rule'):
                # In a real parser, you'd recursively process antecedent/consequent
                antecedent = rule_elem.findall('Antecedent/Clause')
                consequent = rule_elem.findall('Consequent/Clause')

                # Look up the actual objects from the 'variables' dictionary
                # For brevity, we just print the extracted rule logic
                antecedent_parts = []
                consequent_parts = []
                for clause in antecedent:
                    clause_var = clause.get("var")
                    clause_term = clause.get("term")
                    antecedent_parts.append(f"{clause_var}\tIS\t{clause_term}")
                for clause in consequent:
                    clause_var = clause.get("var")
                    clause_term = clause.get("term")
                    consequent_parts.append(f"{clause_var}\tIS\t{clause_term}")

                rule_text = f"IF\t{rb_andMethod.join(antecedent_parts)}\tTHEN\t{rb_andMethod.join(consequent_parts)}"
                print(rule_text)





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
    myFML.parse_fml(FML_STRING)













