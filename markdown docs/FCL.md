<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/PyIT2FLS_icon.png" width="200"/></p>

## Reading and writing IEC 61131-7 (FCL) files
The **_FCL_** class, provided in the **_pyit2fls.FCL_** module, parses the core Mamdani subset of the [IEC 61131-7 Fuzzy Control Language](https://github.com/Haghrah/PyIT2FLS/blob/master/IEC61131-7.md) standard into a runnable **_T1Mamdani_** system, and can serialize a system back out as FCL text. See [IEC61131-7.md](https://github.com/Haghrah/PyIT2FLS/blob/master/IEC61131-7.md) for a full description of the standard, the scope implemented here, and a worked example.

The **_FCL_** class has three functions:

1. **_parse_fcl_**
2. **_generate_**
3. **_export_fcl_**

#### Functions:

**_parse_fcl_** function: Takes a single input, the FCL document as a string (starting with a `FUNCTION_BLOCK` declaration), and returns a tuple `(name, variables, rules)` — the same intermediate representation produced by **_pyit2fls.FML_**'s `parse_fml` function. FUZZIFY/DEFUZZIFY `TERM` point lists are stored as `"pointsShape"` terms, understood by the new **_points_mf_** membership function.

```python
from pyit2fls.FCL import FCL

with open("SmartTipper.fcl") as f:
    fcl_text = f.read()

myFCL = FCL()
name, variables, rules = myFCL.parse_fcl(fcl_text)
```

**_generate_** function: Takes the **_variables_** and **_rules_** dictionaries returned by **_parse_fcl_**, and builds a **_T1Mamdani_** system with every input/output variable, term, and rule already added. It is a thin wrapper of the module-level **_generate_system_** function defined in **_pyit2fls.FML_**.

```python
mySys = myFCL.generate(variables, rules)
S, C = mySys.evaluate({"service": 8, "food": 9})
```

**_export_fcl_** function: Takes a name, and the same **_variables_**/**_rules_** dictionaries, and returns FCL source text — the inverse of **_parse_fcl_**. Terms already stored as `"pointsShape"` (as produced by **_parse_fcl_**) round-trip exactly; other shapes (e.g. those authored through **_pyit2fls.FML_** or the [PyIT2FLS Designer](https://github.com/Haghrah/PyIT2FLS/blob/master/markdown%20docs/DesignerGUI.md)) are sampled at 21 evenly spaced points across the variable's domain, which is an approximation for non-piecewise-linear shapes such as `gaussianShape`.

```python
fcl_text = myFCL.export_fcl(name, variables, rules)
with open("SmartTipper_copy.fcl", "w") as f:
    f.write(fcl_text)
```

#### Scope and known limitations:

- Only the core Mamdani subset of IEC 61131-7 is supported: a single `FUNCTION_BLOCK` with `VAR_INPUT`/`VAR_OUTPUT`, `FUZZIFY`/`DEFUZZIFY` blocks, and a single `RULEBLOCK`. Structured Text method bodies and multiple chained `RULEBLOCK`s are not supported.
- `DEFUZZIFY`'s `METHOD` must be `COG` or `COA`; other methods (e.g. `LM`, `RM`, `COGS`) raise a `NotImplementedError` naming the unsupported method.
- A rule clause can be negated with `IS NOT` — implemented the same way as FML's `NOT="true"`, by lazily creating a complemented counterpart of the referenced term (named `NOT_<term>`).
- Mixing `AND` and `OR` within a single rule (without parentheses-based precedence) is not supported. A rule whose antecedent uses `OR` across more than one clause raises a `ValueError` when generating the system, since the underlying **_T1Mamdani_** engine only combines antecedent clauses with AND — model an OR relationship as two separate rules that share the same consequent instead.
- A rule's `WITH <weight>` and the `RULEBLOCK`'s `ACCU` (accumulation) setting are parsed and kept in the returned **_rules_** dictionary, but are **not** applied while evaluating the generated system.
