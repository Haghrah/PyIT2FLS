<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/PyIT2FLS_icon.png" width="200"/></p>

## Defining Mamdani Interval Type 2 Fuzzy Logic Systems
One of the most common models of the fuzzy systems is Mamdani model. In constrast with TSK model, the inputs and outputs of the system in Mamdani model are fuzzy sets. There are two ways to create interval type 2 mamdani fuzzy systems using PyIT2FLS:

1. Using **_IT2FLS_** class
2. Using **_Mamdani_** class

In the following, it will be introduced how to use these two classes.

### **_IT2FLS_** class
The constructor function of the **_IT2FLS_** class has no input parameters. The **_IT2FLS_** class has five functions embedded:

1. add_input_variable
2. add_output_variable
3. add_rule
4. evaluate
5. evaluate_list

Furthermore, it has three parameters:

1. inputs: List of string
2. outputs: List of string
3. rules: List of tuples

### **_Mamdani_** class




