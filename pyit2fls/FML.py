import xml.etree.ElementTree as ET

class FML:

    def __init__(self, ):
        pass

    def parse_fml(self, fml_xml_string):
        """
        Parses FML XML and populates FuzzyVariable and FuzzySet objects.
        A separate function would handle Rule parsing.
        """
        
        # 3.1. Parse the XML
        root = ET.fromstring(fml_xml_string)
        system_name = root.get('name')
        print(f"--- Parsing Fuzzy System: {system_name} ---")

        # 3.2. Find the Knowledge Base
        kb = root.find('knowledgebase')
        if kb is None:
            raise ValueError("FML is missing a <knowledgebase> tag.")

        # 3.3. Iterate through all <variable> elements
        for var_elem in kb.findall('variable'):
            var_name = var_elem.get('name')
            var_type = var_elem.get('type')
            
            # 3.4. Iterate through all <fuzzyset> elements for this variable
            for fs_elem in var_elem.findall('fuzzyset'):
                # Parse parameters string into a list of floats
                params_str = fs_elem.get('params').split(',')
                params = [float(p.strip()) for p in params_str]
                
                # Instantiate the library's FuzzySet object and add it to the variable
                print(f"Set {var_name}: {fs_elem.get('name')}, {fs_elem.get('type')}, {params}")

        # 3.5. Rule Parsing (Simplified)
        rulebase_elem = root.find('rulebase')
        if rulebase_elem is not None:
            print("\n--- Rule Base Found ---")
            for rule_elem in rulebase_elem.findall('rule'):
                # In a real parser, you'd recursively process antecedent/consequent
                antecedent = rule_elem.find('antecedent/clause')
                consequent = rule_elem.find('consequent/clause')

                # Look up the actual objects from the 'variables' dictionary
                # For brevity, we just print the extracted rule logic
                print(f"Rule {rule_elem.get('id')}: IF {antecedent.get('variable')} IS {antecedent.get('fuzzyset')} THEN {consequent.get('variable')} IS {consequent.get('fuzzyset')}")




if __name__ == "__main__":
    FML_STRING = """
    <fuzzylogicsystem name="HVAC_Controller">
        <knowledgebase>
            <variable name="temp" type="input" min="0" max="100">
                <fuzzyset name="cold" type="triangular" params="0, 0, 40"/>
                <fuzzyset name="warm" type="triangular" params="30, 50, 70"/>
                <fuzzyset name="hot" type="triangular" params="60, 100, 100"/>
            </variable>

            <variable name="fan" type="output" min="0" max="100">
                <fuzzyset name="low" type="trapezoid" params="0, 0, 20, 40"/>
                <fuzzyset name="high" type="trapezoid" params="60, 80, 100, 100"/>
            </variable>
        </knowledgebase>

        <rulebase>
            <rule id="1">
                <antecedent><clause variable="temp" fuzzyset="cold"/></antecedent>
                <consequent><clause variable="fan" fuzzyset="low"/></consequent>
            </rule>
            <rule id="2">
                <antecedent><clause variable="temp" fuzzyset="hot"/></antecedent>
                <consequent><clause variable="fan" fuzzyset="high"/></consequent>
            </rule>
        </rulebase>
    </fuzzylogicsystem>
    """

    myFML = FML()
    myFML.parse_fml(FML_STRING)













