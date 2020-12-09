<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/PyIT2FLS_icon.png" width="200"/></p>

## Defining TSK Type 1 Fuzzy Logic Systems
In the TSK model, outputs are not fuzzy sets but some functions. The PyIT2FLS toolkit provides the **_T1TSK_** class for creating T1 TSK FLSs. The **_T1TSK_** class is designed based on the reference:

	Wang, Li-Xin. A course in fuzzy systems and control. Prentice-Hall, Inc., 1996.

### **_T1TSK_** class
The constructor function of the **_T1TSK_** class has no inputs.

The **_T1TSK_** class has four functions embedded:

1. **_add_input_variable_**
2. **_add_output_variable_**
3. **_add_rule_**
4. **_evaluate_**

And, it has three parameters:

1. **_inputs_**: List of strings
2. **_outputs_**: List of strings
3. **_rules_**: List of tuples

#### Functions:
**_add_input_variable_** function: This function has a single input of type string, which is the name of a input variable. All the input variables must be defined for the system using this function. The variable name given to this function will be stored in the **_inputs_** list.

**_add_output_variable_** function: As the previous function, the only input of the **_add_output_variable_** is a string. Similarly, all the input variables must be defined for the system using this function. The variable name given to this function will be stored in the **_outputs_** list.

**_add_rule_** function: This function has two inputs, **_antecedent_** and **_consequent_**, which are lists of tuples. Each tuple in the **_antecedent_** list, expresses the assignment of an input variable to a fuzzy set. So, the length of the **_antecedent_** list must be equal with **_inputs_** list. The constitutive tuples of the **_consequent_** express the assignment of output variables to output functions. So the second element of the tuples in **_consequent_** list, must be a function (or more generally a callable object). These functions can have input variables, too, and they are passed when the evaluate function of the **_T1TSK_** class is called. The length of the **_consequent_** list must be equal with **_outputs_** list. Let's see an example of using the **_add_rule_** function. Assume that our system has two input variables named x1 and x2, and eight output functions named yij, i=1, ..., 4, j = 1, 2. Also, assume that we have two fuzzy sets Small and Big, and the rule base of our system is as below.

1. IF x1 is Small AND x2 is Small THEN y1 = y11(x1, x2) AND y2 = y12(x1, x2)
2. IF x1 is Small AND x2 is Big THEN y1 = y21(x1, x2) AND y2 = y22(x1, x2)
3. IF x1 is Big AND x2 is Small THEN y1 = y31(x1, x2) AND y2 = y32(x1, x2)
4. IF x1 is Big AND x2 is Big THEN y1 = y41(x1, x2) AND y2 = y42(x1, x2)

```python
SYS.add_rule([("x1", Small), ("x2", Small)], 
             [("y1", y11), 
              ("y2", y12)])
SYS.add_rule([("x1", Small), ("x2", Big)], 
             [("y1", y21), 
              ("y2", y22)])
SYS.add_rule([("x1", Big), ("x2", Small)], 
             [("y1", y31), 
              ("y2", y32)])
SYS.add_rule([("x1", Big), ("x2", Big)], 
             [("y1", y41), 
              ("y2", y42)])
```

**_evaluate_** function: This function has two inputs. The first one is of type dictionary. The keys of this dictionary must be the input variable names previously added to the **_inputs_** list of the **_T1TSK_** class. The values corresponded with the input variables in the dictionary must be their values to evaluate the system. The second input of the function is a tuple, which indicates the parameters of the functions given as the consequent of the fuzzy rules. Let's see an example of calling the **_evaluate_** function.

```python
y = mySys.evaluate({"x1":0.923, "x2":0.745}, params=(2, 4))
print(y["y1"], y["y2"])
```

The only output of the **_evaluate_** function is a dictionary, which keys are output variable names and the values are the outputs.


