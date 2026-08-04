<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/PyIT2FLS_icon.png" width="200"/></p>

## Reading and writing IEEE 1855 (FML) files
The **_FML_** class, provided in the **_pyit2fls.FML_** module, parses [IEEE 1855 Fuzzy Markup Language](https://github.com/Haghrah/PyIT2FLS/blob/master/IEEE1855.md) XML documents into a runnable **_T1Mamdani_** or **_T1TSK_** system, and can serialize a system back out as FML XML. See [IEEE1855.md](https://github.com/Haghrah/PyIT2FLS/blob/master/IEEE1855.md) for a full description of the standard and a worked example.

The **_FML_** class has three functions:

1. **_parse_fml_**
2. **_generate_**
3. **_export_fml_**

#### Functions:

**_parse_fml_** function: Takes a single input, the FML document as a string, and returns a tuple `(name, variables, rules)`. **_name_** is the system's name. **_variables_** and **_rules_** are plain dictionaries describing every input/output variable, term, and rule found in the document — this is the same intermediate representation produced by **_pyit2fls.FCL_**'s `parse_fcl` function, so a system parsed from either format can be built the same way.

```python
from pyit2fls.FML import FML

with open("SmartTipper.fml") as f:
    fml_text = f.read()

myFML = FML()
name, variables, rules = myFML.parse_fml(fml_text)
```

**_generate_** function: Takes the **_variables_** and **_rules_** dictionaries returned by **_parse_fml_**, and builds a **_T1Mamdani_** system (for a `mamdani` rule base) or a **_T1TSK_** system (for a `takagi-sugeno` rule base), with every input/output variable, term, and rule already added. It is a thin wrapper of the module-level **_generate_system_** function, also used by **_pyit2fls.FCL_**.

```python
mySys = myFML.generate(variables, rules)
S, C = mySys.evaluate({"service": 8, "food": 9})
```

**_export_fml_** function: Takes a name, and the same **_variables_**/**_rules_** dictionaries, and returns a pretty-printed FML XML string — the inverse of **_parse_fml_**. Useful for saving a system built programmatically, or one built with the [PyIT2FLS Designer](https://github.com/Haghrah/PyIT2FLS/blob/master/markdown%20docs/DesignerGUI.md) GUI.

```python
xml_text = myFML.export_fml(name, variables, rules)
with open("SmartTipper_copy.fml", "w") as f:
    f.write(xml_text)
```

#### Notes and known limitations:

- The `andMethod`/`activationMethod` attributes of a `RuleBase` select the underlying **_T1Mamdani_** inference engine (*Product*, *Minimum*, *Lukasiewicz*, *Zadeh*, or *Dienes-Rescher*); only the first `RuleBase` in a document is parsed.
- A `Clause`'s `NOT="true"` attribute is supported, and is implemented by lazily creating a complemented counterpart of the referenced term (named `NOT_<term>`).
- A rule whose antecedent clauses are connected with `connector="or"` across more than one `Clause` raises a `ValueError`: the underlying **_T1Mamdani_**/**_T1TSK_** engines only combine antecedent clauses with AND. Model an OR relationship as two separate rules that share the same consequent instead.
- A rule's `weight` attribute is parsed and kept in the **_rules_** dictionary, but is **not** applied while evaluating the generated system — doing so would require changes to the firing-strength arithmetic of every **_T1Mamdani_**/**_T1TSK_** evaluate method.
