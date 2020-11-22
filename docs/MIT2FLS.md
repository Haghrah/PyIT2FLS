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
3. **_method_**: String
4. **_method_params_**: List
5. **_algorithm_**: Function
6. **_algorithm_params_**: List

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
1. **_add_input_variable_**

This function has a single input of type string, which is the name of a input variable. All the input variables must be defined for the system using this function. The variable name given to this function will be stored in the **_inputs_** list.

2. **_add_output_variable_**

As the previous function, the only input of the **_add_output_variable_** is a string. Similarly, all the input variables must be defined for the system using this function. The variable name given to this function will be stored in the **_outputs_** list.








