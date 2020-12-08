<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/PyIT2FLS_icon.png" width="200"/></p>

## Defining Type 1 Mamdani Fuzzy Logic Systems
The **_T1Mamdani_** class is provided in PyIT2FLS for creating Type 1 Mamdani Fuzzy Logic Systems. The constructor function of the **_T1Mamdani_** class has two inputs:

1. **_engine_**: A string, indicating the inference engine of the system. The default value of this input is **_Product_**, but it can be selected among the engines Product, Minimum, Lukasiewicz, Zadeh, and Dienes-Rescher.
2. **_defuzzification_**: A string, indicating the defuzzification method of the system. The default value is **_CoG_**, which indicates the center of gravity defuzzification method. If the engine of the system is **_Product_** or **_Minimum_**, the defuzzification can be selected among **_CoG_** and **_CoA_**.





