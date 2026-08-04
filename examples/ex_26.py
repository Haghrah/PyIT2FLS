#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 04 2026

@author: arslan
"""


from pyit2fls.FCL import FCL

# Parsing an IEC 61131-7 (FCL) document describing the same fan-speed
# controller as ex_25.py, this time with piecewise-linear TERM points,
# building a runnable pyit2fls.T1Mamdani out of it, then evaluating and
# exporting it.
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
    RULE 1 : IF temp IS cold THEN fan IS low;
    RULE 2 : IF temp IS hot AND temp IS NOT cold THEN fan IS high;
END_RULEBLOCK

END_FUNCTION_BLOCK
"""

myFCL = FCL()
name, variables, rules = myFCL.parse_fcl(FCL_TEXT)
print(f"Parsed FCL system: {name}")

mySys = myFCL.generate(variables, rules)
fired_sets, crisp = mySys.evaluate({"temp": 25})
print(f"Crisp fan speed for temp=25: {crisp['fan']}")

# Round-trip: export the same system back out as FCL text, re-parse it, and
# confirm it evaluates to the same crisp output. Since every term here was
# already a "pointsShape" term, this round-trip is exact.
fcl_text = myFCL.export_fcl(name, variables, rules)
name2, variables2, rules2 = myFCL.parse_fcl(fcl_text)
mySys2 = myFCL.generate(variables2, rules2)
_, crisp2 = mySys2.evaluate({"temp": 25})
print(f"Crisp fan speed after FCL round-trip: {crisp2['fan']}")
