<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/PyIT2FLS_icon.png" width="200"/></p>

## Defining Type 1 Mamdani Fuzzy Logic Systems
The **_T1Mamdani_** class is provided in PyIT2FLS for creating Type 1 Mamdani Fuzzy Logic Systems. The constructor function of the **_T1Mamdani_** class has two inputs:

1. **_engine_**: A string, indicating the inference engine of the system. The default value of this input is **_Product_**, but it can be selected among the engines Product, Minimum, Lukasiewicz, Zadeh, and Dienes-Rescher.
2. **_defuzzification_**: A string, indicating the defuzzification method of the system. The default value is **_CoG_**, which indicates the center of gravity defuzzification method. If the engine of the system is **_Product_** or **_Minimum_**, the defuzzification can be selected among **_CoG_** and **_CoA_**.

The **_T1Mamdani_** class has four functions embedded:

1. **_add_input_variable_**
2. **_add_output_variable_**
3. **_add_rule_**
4. **_evaluate_**

And, it has three parameters:

1. **_inputs_**: List of strings
2. **_outputs_**: List of strings
3. **_rules_**: List of tuples
4. **_engine_**: String
5. **_defuzzification_**: String

#### Functions:

**_add_input_variable_** function: This function has a single input of type string, which is the name of a input variable. All the input variables must be defined for the system using this function. The variable name given to this function will be stored in the **_inputs_** list.

**_add_output_variable_** function: As the previous function, the only input of the **_add_output_variable_** is a string. Similarly, all the input variables must be defined for the system using this function. The variable name given to this function will be stored in the **_outputs_** list.

**_add_rule_** function: This function has two inputs, **_antecedent_** and **_consequent_**, which are lists of tuples. Each tuple in the **_antecedent_** list, expresses the assignment of an input variable to a fuzzy set. So, the length of the **_antecedent_** list must be equal with **_inputs_** list. Similarly, the constitutive tuples of the **_consequent_** express the assignment of output variables to fuzzy sets. Also, the length of the **_consequent_** list must be equal with **_outputs_** list. Let's see an example of using the **_add_rule_** function. Assume that our system has two input variables named x1 and x2, and two output variables named y1 and y2. Also, assume that we have three fuzzy sets Small, Medium, and Large, and the rule base of our system is as below.

1. IF x1 is Small AND x2 is Small THEN y1 is Small AND y2 is Large
2. IF x1 is Medium AND x2 is Medium THEN y1 is Medium AND y2 is Small
3. IF x1 is Large AND x2 is Large THEN y1 is Large AND y2 is Small

We can add these rule to the rule-base of the system using the code below:

```python
mySys.add_rule([("x1", Small), ("x2", Small)], [("y1", Small), ("y2", Large)])
mySys.add_rule([("x1", Medium), ("x2", Medium)], [("y1", Medium), ("y2", Small)])
mySys.add_rule([("x1", Large), ("x2", Large)], [("y1", Large), ("y2", Small)])
```

**_evaluate_** function: This function has a single input variable of type dictionary. The keys of this dictionary must be the input variable names added to the **_inputs_** list of the Mamdani class, and the values corresponded with the input variables must be their value to evaluate the system. Let's see an example of calling the **_evaluate_** function.

```python
s, c = mySys.evaluate({"x1":0.923, "x2":0.745})
```

The output of the evaluate function depends on the defuzzification method selected. For **_CoG_** defuzzification method, the output is a tuple, which the first item is a dictionary of the output fuzzy sets and the second is a dictionary of the crisp outputs of the system. For other defuzzification methods, the output will only be a dictionary of crisp numbers. It must be noticed that the keys of the output dictionaries are the output names defined previousley.



