# PyIT2FLS
PyIT2FLS is providing a set of tools for fast and easy modeling of Interval Type 2 Fuzzy Sets (IT2FS) and Systems (IT2FLS). There are two main classes in this toolkit, named **_IT2FS_** and **_IT2FLS_**. The first one for defining IT2FSs and the latter for defining IT2FLSs. There are many functions defined in PyIT2FLS for utilizing these two classes, which would be introduced in the following.

## IT2FS
In this section we are going to see how IT2FSs can be defined using the **_IT2FS_** class. An IT2FS is defined by its Lower Membership Function (LMF) and Upper Membership Function (UMF). So first we need to know functions which can be used as LMFs and UMFs.

### List of membership function that can be used as LMF and UMF functions

|  Membership function  | Description | Parameters |
|:---------------------:|:-----------:|:----------:|
| zero_mf               |             |            |
| singleton_mf          |             |            |
| const_mf              |             |            |
| tri_mf                |             |            |
| ltri_mf               |             |            |
| rtri_mf               |             |            |
| trapezoid_mf          |             |            |
| gaussian_mf           |             |            |
| gauss_uncert_mean_umf |             |            |
| gauss_uncert_mean_lmf |             |            |
| gauss_uncert_std_umf  |             |            |
| gauss_uncert_std_lmf  |             |            |

## IT2FLS
