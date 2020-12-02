<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/PyIT2FLS_icon.png" width="200"/></p>

## Defining TSK Interval Type 2 Fuzzy Logic Systems

TSK Fuzzy systems are used in a wide range of the scientific and engineering applications. The difference between TSK model and Mamdani model is the outputs of the systems. In TSK model outputs are not fuzzy sets but some functions. The PyIT2FLS toolkit provides the **_IT2TSK_** class for creating IT2 TSK FLSs. The **_IT2TSK_** class is designed based on the reference:

	Mendel, Jerry, et al. Introduction to type-2 fuzzy logic control: theory and applications. John Wiley & Sons, 2014.

### **_IT2TSK_** class
The constructor function of the **_IT2TSK_** class has two inputs:

1. **_t_norm_**: Function
2. **_s_norm_**: Function

The **_t_norm_** and **_s_norm_** inputs can be selected from the t-norm and s-norm functions provided by the PyIT2FLS.

The **_IT2TSK_** class has four functions embedded:

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

**_add_rule_** function: This function has two inputs, **_antecedent_** and **_consequent_**, which are lists of tuples. Each tuple in the **_antecedent_** list, expresses the assignment of an input variable to a fuzzy set. So, the length of the **_antecedent_** list must be equal with **_inputs_** list. The constitutive tuples of the **_consequent_** express the assignment of output variables to output states. The second element of the tuples in **_consequent_** list, must be a dictionary. This dictionary shows the output polynomial in the case of the rule. For example let an output polynomial be as 2 x1 + 4 x2 + 5. Then the dictionary for this case would be {"const":5., "x1":2., "x2":4.}. Note that this is written for an IT2 TSK FLS with two inputs, named x1 and x2. Also, the length of the **_consequent_** list must be equal with **_outputs_** list. Let's see an example of using the **_add_rule_** function. Assume that our system has two input variables named x1 and x2, and two output variables named y1 and y2. Also, assume that we have two fuzzy sets Small and Big, and the rule base of our system is as below.

1. IF x1 is Small AND x2 is Small THEN y1 = x1 + x2 + 1 AND y2 = 2 x1 - x2 + 1
2. IF x1 is Small AND x2 is Big THEN y1 = 1.5 x1 + 0.5 x2 + 0.5 AND y2 = 1.5 x1 - 0.5 x2 + 0.5
3. IF x1 is Big AND x2 is Small THEN y1 = 2 x1 + 0.1 x2 - 0.2 AND y2 = 0.5 x1 + 0.1 x2
4. IF x1 is Big AND x2 is Big THEN y1 = 4 x1 - 0.5 x2 - 1 AND y2 = -0.5 x1 + x2 - 0.5

We can add these rule to the rule-base of the system using the code below:

```python
mySys.add_rule([("x1", Small), ("x2", Small)], 
               [("y1", {"const":1., "x1":1., "x2":1.}), 
                ("y2", {"const":1., "x1":2., "x2":-1.})])
mySys.add_rule([("x1", Small), ("x2", Big)], 
               [("y1", {"const":0.5, "x1":1.5, "x2":0.5}), 
                ("y2", {"const":0.5, "x1":1.5, "x2":-0.5})])
mySys.add_rule([("x1", Big), ("x2", Small)], 
               [("y1", {"const":-0.2, "x1":2., "x2":0.1}), 
                ("y2", {"const":0., "x1":0.5, "x2":0.1})])
mySys.add_rule([("x1", Big), ("x2", Big)], 
               [("y1", {"const":-1., "x1":4., "x2":-0.5}), 
                ("y2", {"const":-0.5, "x1":-0.5, "x2":1.})])
```

**_evaluate_** function: This function has a single input variable of type dictionary. The keys of this dictionary must be the input variable names previously added to the **_inputs_** list of the **_IT2TSK_** class. The values corresponded with the input variables in the dictionary must be their values to evaluate the system. Let's see an example of calling the **_evaluate_** function.

```python
y = mySys.evaluate({"x1":0.923, "x2":0.745})
print(y["y1"], y["y2"])
```




