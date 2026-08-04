#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 04 2026

@author: arslan
"""


from pyit2fls.FML import FML

# Parsing an IEEE 1855 (FML) document describing a Type 1 Mamdani fuzzy
# system that decides a fan speed from a room temperature, building a
# runnable pyit2fls.T1Mamdani out of it, then evaluating and exporting it.
FML_TEXT = """
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
name, variables, rules = myFML.parse_fml(FML_TEXT)
print(f"Parsed FML system: {name}")

mySys = myFML.generate(variables, rules)
fired_sets, crisp = mySys.evaluate({"temp": 25})
print(f"Crisp fan speed for temp=25: {crisp['fan']}")

# Round-trip: export the same system back out as FML XML, re-parse it, and
# confirm it evaluates to the same crisp output.
xml_text = myFML.export_fml(name, variables, rules)
name2, variables2, rules2 = myFML.parse_fml(xml_text)
mySys2 = myFML.generate(variables2, rules2)
_, crisp2 = mySys2.evaluate({"temp": 25})
print(f"Crisp fan speed after FML round-trip: {crisp2['fan']}")
