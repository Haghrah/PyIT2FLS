<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/PyIT2FLS_icon.png" width="200"/></p>

## The PyIT2FLS Designer GUI
The **_PyIT2FLS Designer_** is a PyQt5 application, provided in the **_pyit2fls.designerui_** module, for interactively building, simulating, and saving/loading Type 1 Mamdani fuzzy logic systems, as [FML](https://github.com/Haghrah/PyIT2FLS/blob/master/markdown%20docs/FML.md) or [FCL](https://github.com/Haghrah/PyIT2FLS/blob/master/markdown%20docs/FCL.md) files.

The GUI depends on PyQt5, an optional extra of PyIT2FLS, so it is not installed (or imported) by default. Install it with:

```
pip3 install --upgrade "pyit2fls[gui]"
```

Then launch the designer with the console script:

```
pyit2fls-designer
```

or as a module:

```
python3 -m pyit2fls.designerui
```

The main window is organized into three tabs, walked through below by building the classic restaurant-tipping example (two inputs, `service` and `food`, one output, `tip`).

#### 1. Variables & Sets

This tab has an *Input Variables* panel and an *Output Variables* panel, each with:

- A list of the variables of that kind, with **Add**/**Remove** buttons. *Add* prompts for a name and a domain (left/right bound); the variable's terms start empty.
- A membership functions table for the variable currently selected in the list, with **Add MF**/**Remove MF** buttons. *Add MF* prompts for a term name, a shape (*Triangular*, *Trapezoidal*, *Gaussian*, or *Singleton*), and a comma-separated parameter list (the height is optional and defaults to 1, matching **_pyit2fls.FML_**'s **_generate_system_**).
- A plot of every term currently defined for the selected variable, redrawn automatically after every change.

Add `service` (domain 0 to 10) with terms `poor` (Gaussian, `0, 2`), `good` (Triangular, `3, 5, 7`), and `excellent` (Trapezoidal, `6, 8, 9, 10`); add `food` (domain 0 to 10) with terms `bad` and `great`; then add the output `tip` (domain 0 to 30) with terms `low`, `average`, and `high`.

#### 2. Fuzzy Rules

The rule builder lets you compose a rule as *IF \<variable\> is [NOT] \<term\> [AND/OR \<variable\> is [NOT] \<term\>] THEN \<variable\> is \<term\>*, with the variable/term combo boxes always reflecting whatever was defined in the Variables & Sets tab. Click **Add Rule to List** to append it to the rule base, shown below as a plain-text list; select a rule and click **Remove Selected Rule** to delete it.

```
R1: IF service IS poor AND food IS bad THEN tip IS low
R2: IF service IS good THEN tip IS average
R3: IF service IS excellent AND food IS great THEN tip IS high
```

As with **_pyit2fls.FML_**/**_pyit2fls.FCL_**, a rule's two antecedent clauses can only be AND-combined for evaluation to work — choosing *OR* is accepted by the builder (and saved faithfully to FML/FCL files) but will raise an error when the system is generated or evaluated. Model an OR relationship as two separate rules that share the same consequent instead.

#### 3. Simulation & Visualization

Every input variable gets a slider, ranged over its domain, with a live readout of its current crisp value. Click **Evaluate System** to build the system (via **_pyit2fls.FML_**'s **_generate_system_**) and evaluate it at the current slider values; the crisp output(s) are shown next to the sliders. For systems with exactly two inputs, the same click also plots the system's control surface — the output over the full 2D input space — on the right.

#### File menu

- **New System** clears the current variables, terms, and rules.
- **Open System...** loads a `.fml`, `.xml`, or `.fcl` file (dispatched by extension to **_pyit2fls.FML_**'s **_parse_fml_** or **_pyit2fls.FCL_**'s **_parse_fcl_**), replacing the current system.
- **Save System...** writes the current system out as FCL (`.fcl`) or FML (`.fml`) text, via **_pyit2fls.FCL_**'s **_export_fcl_** or **_pyit2fls.FML_**'s **_export_fml_**.

Since Open/Save round-trip through the same **_variables_**/**_rules_** representation used by **_pyit2fls.FML_** and **_pyit2fls.FCL_**, a system built in the designer can also be loaded and evaluated directly in a script, without the GUI:

```python
from pyit2fls.FCL import FCL

myFCL = FCL()
name, variables, rules = myFCL.parse_fcl(open("tipper.fcl").read())
mySys = myFCL.generate(variables, rules)
print(mySys.evaluate({"service": 8, "food": 9}))
```

#### Notes

The designer targets Type 1 Mamdani systems only, matching the scope of **_pyit2fls.FCL_** — IEC 61131-7 does not define Takagi-Sugeno rule blocks, and Interval Type 2 sets are not yet supported by either the FML or FCL modules.
