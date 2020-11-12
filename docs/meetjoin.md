<p align="center"><img src="https://raw.githubusercontent.com/Haghrah/PyIT2FLS/master/PyIT2FLS_icon.png" width="200"/></p>

## Interval Type II Fuzzy Logic Operators
Two essential operators in Interval Type 2 Fuzzy Logic, are the meet and join operators. These operators are defined in PyIY2FLS as two functions **_meet_** and **_join_**. Both functions have four inputs. For these functions, the first three inputs are common, the universe of discourse, the first **_IT2FS_**, and the second **_IT2FS_**. The 4th input of the **_meet_** function is the desired t-norm, and for the **_join_** function, it is the desired s-norm.

There are two t-norms defined in PyIT2FLS by default, minimum t-norm and product t-norm. These two t-norms are accessible using two function named **_min_t_norm_** and **_product_t_norm_**, respectively. Each t-norm function has two inputs, that can be floating point numbers or numpy arrays.

The only s-norm defined in PyIT2FLS by default is maximum s-norm, that is accessible using the function **_max_s_norm_**.The s-norm function, similarly to t-norms, has two inputs, that can be floating point numbers or numpy arrays.

It must be noted that the users can define new t-norms and s-norms. The user defined t-norm or s-norm functions must follow the structure below:

```python
def userdefine_norm(a, b)
	return some_calculations(a, b)
```

### Examples



