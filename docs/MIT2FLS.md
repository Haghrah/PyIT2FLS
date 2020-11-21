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

1. KM_algorithm
2. EKM_algorithm
3. WEKM_algorithm
4. TWEKM_algorithm
5. EIASC_algorithm
6. WM_algorithm
7. BMM_algorithm
8. LBMM_algorithm
9. NT_algorithm







