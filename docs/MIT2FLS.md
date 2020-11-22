<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/PyIT2FLS_icon.png" width="200"/></p>

## Defining Mamdani Interval Type 2 Fuzzy Logic Systems
One of the most common models of the fuzzy systems is Mamdani model. In constrast with TSK model, both of the inputs and outputs of the system in Mamdani model are fuzzy sets. There are two ways to create interval type 2 Mamdani fuzzy systems using PyIT2FLS:

1. Using **_IT2FLS_** class
2. Using **_Mamdani_** class

In the following, it will be introduced how to use these two classes.

### **_IT2FLS_** class
The constructor function of the **_IT2FLS_** class has no input parameters. The **_IT2FLS_** class has five functions embedded:

1. **_add_input_variable_**
2. **_add_output_variable_**
3. **_add_rule_**
4. **_evaluate_**
5. **_evaluate_list_**

And, it has three parameters:

1. **_inputs_**: List of strings
2. **_outputs_**: List of strings
3. **_rules_**: List of tuples

### **_Mamdani_** class
The constructor function of the **_Mamdani_** class has six inputs:

1. **_t_norm_**: Function
2. **_s_norm_**: Function
3. **_method_**: String with Centroid default value
4. **_method_params_**: List with None default value
5. **_algorithm_**: Function with EIASC_algorithm default value
6. **_algorithm_params_**: List with None default value

The **_t_norm_** and **_s_norm_** inputs can be selected from the t-norm and s-norm functions provided by the PyIT2FLS. The **_method_** can be one the methods listed below:

1. **_Centroid_**: Centroid method
2. **_CoSet_**: Center of sets method
3. **_CoSum_**: Center of sum method
4. **_Height_**: Height method
5. **_ModiHe_**: Modified height method

The only method that needs a parameter is the **_ModiHe_** method. The **_method_params_** of the **_ModiHe_** method is a list of spread values corresponding with the IT2FSs. (For more details about this method, please refer to the type two fuzzy logic reference books.)

The **_algorithm_** defines the type reduction algorithm, and can be selected from the algorithms listed below:

1. **_KM_algorithm_**
2. **_EKM_algorithm_**
3. **_WEKM_algorithm_**
4. **_TWEKM_algorithm_**
5. **_EIASC_algorithm_**
6. **_WM_algorithm_**
7. **_BMM_algorithm_**
8. **_LBMM_algorithm_**
9. **_NT_algorithm_**

It must be noticed that the items of the above list are function names and must be imported from PyIT2FLS before using. Of these nine algorithms, only **_WEKM_algorithm_**, **_BMM_algorithm_**, and **_LBMM_algorithm_** algorithms need **_algorithm_params_**. **_algorithm_params_** should be defined as a list of floating point numbers. (For more details about these algorithms, please refer to the type two fuzzy logic reference books.)

The **_Mamdani_** class has four functions embedded:

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

**_add_rule_** function: This function has two inputs, **_antecedent_** and **_consequent_**, which are lists of tuples. Each tuple in the **_antecedent_** list, expresses the assignment of an input variable to a fuzzy set. So, the length of the **_antecedent_** list must be equal with **_inputs_** list. Similarly, the constitutive tuples of the **_consequent_** express the assignment of output variables to fuzzy sets. Also, the length of the **_consequent_** list must be equal with **_outputs_** list. Let's see an example of using the **_add_rule_** function. Assume that our system has two input variables named x1 and x2, and two output variables named y1 and y2. Also, assume that we have three fuzzy sets Small, Medium, and Large, and the rule base of our system is as below.

1. IF x1 is Small  AND x2 is Small  THEN y1 is Small  AND y2 is Large
2. IF x1 is Medium AND x2 is Medium THEN y1 is Medium AND y2 is Small
3. IF x1 is Large  AND x2 is Large  THEN y1 is Large  AND y2 is Small

We can add these rule to the rule-base of the system using the code below:

```python
mySys.add_rule([("x1", Small), ("x2", Small)], [("y1", Small), ("y2", Large)])
mySys.add_rule([("x1", Medium), ("x2", Medium)], [("y1", Medium), ("y2", Small)])
mySys.add_rule([("x1", Large), ("x2", Large)], [("y1", Large), ("y2", Small)])
```

**_evaluate_** function: This function has a single input variable of type dictionary. The keys of this dictionary must be the input variable names added to the **_inputs_** list of the Mamdani class, and the values corresponded with the input variables must be their value to evaluate the system. Let's see an example of calling the **_evaluate_** function.

```python
mySys.evaluate({"x1":0.923, "x2":0.745})
```


