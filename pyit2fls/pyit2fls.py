from numpy import exp, ones_like, zeros_like, arange, multiply, \
     subtract, add, minimum, maximum, sign, c_, argmax, \
     array, where, hstack, logical_not, sqrt
from numpy import sum as npsum
from numpy import abs as npabs
from numpy import round as npround
from scipy.integrate import trapz
import matplotlib.pyplot as plt
from math import isclose

try:
    import typereduction
    isThereTypereduction = True
except:
    isThereTypereduction = False


def zero_mf(x, params=[]):
    """
    All zero membership function.
    
    Parameters
    ----------
    x : 
        numpy (n,) shaped array
        
        The array like input x indicates the points from the universe of 
        discourse, in which the membership function would be evaluated.
    params : 
        List 
        
        Additional parameters for the membership function, which is not 
        needed for zero memebership function.
    
    Returns
    -------
    ndarray
        Returns an array of membership values corresponding with the input.
    
    Examples
    --------
    
    >>> x = linspace(0, 1, 201)
    >>> membership_value = zero_mf(x)
    """
    return zeros_like(x)


def singleton_mf(x, params):
    """
    Singleton membership function.
    
    Parameters
    ----------
    x : 
        numpy (n,) shaped array
        
        The array like input x indicates the points from universe of 
        discourse in which the membership function would be evaluated.
    params : 
        List 
        
        Additional parameters for the membership function. params[0] indicates
        singleton center and params[1] indicates singleton height.
    
    Returns
    -------
    ndarray
        Returns membership values corresponding with the input.
        
    Notes
    -----
    The singleton center, params[0], must be in the discretized universe 
    of discourse.
    
    Examples
    --------
    
    >>> x = linspace(0, 1, 201)
    >>> membership_value = singleton_mf(x, [0.5, 1])
    """
    return multiply(params[1], x == params[0])


def const_mf(x, params):
    """
    Constant membership function.
    
    Parameters
    ----------
    x : 
        numpy (n,) shaped array
        
        The array like input x indicates the points from universe of 
        discourse in which the membership function would be evaluated.
    params : 
        List 
        
        Additional parameters for the membership function. params[0] indicates
        constant membership function's height.
    
    Returns
    -------
    ndarray
        Returns membership values corresponding with the input.
    
    Examples
    --------
    
    >>> x = linspace(0, 1, 201)
    >>> membership_value = const_mf(x, [0.5])
    """
    return multiply(params[0], ones_like(x))


def tri_mf(x, params):
    """
    Triangular membership function.

    Parameters
    ----------
    x : 
        numpy (n,) shaped array
        
        The array like input x indicates the points from universe of 
        discourse in which the membership function would be evaluated.
    params : 
        List 
        
        Additional parameters for the membership function. The left end, 
        center, right end, and height of the triangular 
        membership function are indicated by params[0], params[1], params[2], 
        and params[3], respectively.
    
    Returns
    -------
    ndarray
        Returns membership values corresponding with the input.
    
    Examples
    --------
    
    >>> x = linspace(0, 1, 201)
    >>> membership_value = tri_mf(x, [0.1, 0.3, 0.5, 1])
    """
    return minimum(1, maximum(0, ((params[3] * (x - params[0]) / (params[1] - params[0])) * (x <= params[1]) + \
               ((params[3] * ((params[2] - x) / (params[2] - params[1]))) * (x > params[1]))) ))


def rtri_mf(x, params):
    """
    Right triangular membership function.

    Parameters
    ----------
    x : 
        numpy (n,) shaped array
        
        The array like input x indicates the points from universe of 
        discourse in which the membership function would be evaluated.
    params : 
        List 
        
        Additional parameters for the membership function.  
        The right end, center, and height of the triangular 
        membership function are indicated by params[0], params[1], and params[2], 
        respectively.
    
    Returns
    -------
    ndarray
        Returns membership values corresponding with the input.
    
    Examples
    --------
    
    >>> x = linspace(0, 1, 201)
    >>> membership_value = ltri_mf(x, [0.5, 0.2, 1])
    """
    return minimum(1, maximum(0, (params[2] * (x <= params[1]) + \
               ((params[2] * ((params[0] - x) / (params[0] - params[1]))) * (x > params[1]))) ))

def ltri_mf(x, params):
    """
    Left triangular membership function.

    Parameters
    ----------
    x : 
        numpy (n,) shaped array
        
        The array like input x indicates the points from universe of 
        discourse in which the membership function would be evaluated.
    params : 
        List 
        
        Additional parameters for the membership function. The left end, 
        center, and height of the triangular 
        membership function are indicated by params[0], params[1] and params[2], 
        respectively.
    
    Returns
    -------
    ndarray
        Returns membership values corresponding with the input.
    
    Examples
    --------
    
    >>> x = linspace(0, 1, 201)
    >>> membership_value = rtri_mf(x, [0.3, 0.5, 1])
    """
    return minimum(1, maximum(0, ((params[2] * (x - params[0]) / (params[1] - params[0])) * (x <= params[1]) + \
               (params[2] * (x > params[1])) )))
    

def trapezoid_mf(x, params):
    """
    Trapezoidal membership function

    Parameters
    ----------
    x : 
        numpy (n,) shaped array
        
        The array like input x indicates the points from universe of 
        discourse in which the membership function would be evaluated.
    params : 
        List 
        
        Additional parameters for the membership function. The left end, 
        left center, right center, right end, and height 
        of the trapezoidal membership function are indicated by params[0], 
        params[1], params[2], params[3], and params[4], respectively.
    
    Returns
    -------
    ndarray
        Returns membership values corresponding with the input.
    
    Examples
    --------
    
    >>> x = linspace(0, 1, 201)
    >>> membership_value = trapezoid_mf(x, [0.1, 0.3, 0.5, 0.7, 1])
    """
    return minimum(1, maximum(0, ((((params[4] * ((x - params[0]) / (params[1] - params[0]))) * (x <= params[1])) +
                   ((params[4] * ((params[3] - x) / (params[3] - params[2]))) * (x >= params[2]))) +
               (params[4] * ((x > params[1]) * (x < params[2])))) ))


def gaussian_mf(x, params):
    """
    Gaussian membership function
    
    Parameters
    ----------
    x : 
        numpy (n,) shaped array
        
        The array like input x indicates the points from universe of 
        discourse in which the membership function would be evaluated.
    params : 
        List 
        
        Additional parameters for the membership function. The center, 
        standard deviation, and height 
        of the gaussian membership function are indicated by params[0], 
        params[1], and params[2], respectively.
    
    Returns
    -------
    ndarray
        Returns membership values corresponding with the input.
    
    Examples
    --------
    
    >>> x = linspace(0, 1, 201)
    >>> membership_value = gaussian_mf(x, [0.5, 0.05, 1])
    """
    return params[2] * exp(-(((params[0] - x) ** 2) / (2 * params[1] ** 2)))


def gauss_uncert_mean_umf(x, params):
    """
    Gaussian with uncertain mean UMF
    
    Parameters
    ----------
    x : 
        numpy (n,) shaped array
        
        The array like input x indicates the points from universe of 
        discourse in which the membership function would be evaluated.
    params : 
        List 
        
        Additional parameters for the membership function. The lower limit 
        of mean, upper limit of mean, standard deviation, and 
        height of the gaussian membership function are indicated by params[0], 
        params[1], params[2], and params[3], respectively.
    
    Returns
    -------
    ndarray
        Returns membership values corresponding with the input.
    
    Examples
    --------
    
    >>> x = linspace(0, 1, 201)
    >>> membership_value = gauss_uncert_mean_umf(x, [0.3, 0.7, 0.05, 1])
    """
    return (((gaussian_mf(x, [params[0], params[2], params[3]]) * (x <= params[0])) +
             (gaussian_mf(x, [params[1], params[2], params[3]]) * (x >= params[1]))) +
               (params[3] * ((x > params[0]) * (x < params[1]))))


def gauss_uncert_mean_lmf(x, params):
    """
    Gaussian with uncertain mean LMF
    
    Parameters
    ----------
    x : 
        numpy (n,) shaped array
        
        The array like input x indicates the points from universe of 
        discourse in which the membership function would be evaluated.
    params : 
        List 
        
        Additional parameters for the membership function. The lower limit 
        of mean, upper limit of mean, standard deviation, and 
        height of the gaussian membership function are indicated by params[0], 
        params[1], params[2], and params[3], respectively.
    
    Returns
    -------
    ndarray
        Returns membership values corresponding with the input.
    
    Examples
    --------
    
    >>> x = linspace(0, 1, 201)
    >>> membership_value = gauss_uncert_mean_lmf(x, [0.3, 0.7, 0.2, 1])
    """
    return ((gaussian_mf(x, [params[0], params[2], params[3]]) * (x >= (params[0] + params[1]) / 2)) +
            (gaussian_mf(x, [params[1], params[2], params[3]]) * (x < (params[0] + params[1]) / 2)))


def gauss_uncert_std_umf(x, params):
    """
    Gaussian with uncertain standard deviation UMF
    
    Parameters
    ----------
    x : 
        numpy (n,) shaped array
        
        The array like input x indicates the points from universe of 
        discourse in which the membership function would be evaluated.
    params : 
        List 
        
        Additional parameters for the membership function. The center, 
        lower limit of std., upper limit of std., and 
        height of the gaussian membership function are indicated by params[0], 
        params[1], params[2], and params[3], respectively.
    
    Returns
    -------
    ndarray
        Returns membership values corresponding with the input.
    
    Examples
    --------
    
    >>> x = linspace(0, 1, 201)
    >>> membership_value = gauss_uncert_std_umf(x, [0.5, 0.2, 0.5, 1])
    """
    return gaussian_mf(x, [params[0], params[2], params[3]])


def gauss_uncert_std_lmf(x, params):
    """
    Gaussian with uncertain standard deviation LMF
    
    Parameters
    ----------
    x : 
        numpy (n,) shaped array
        
        The array like input x indicates the points from universe of 
        discourse in which the membership function would be evaluated.
    params : 
        List 
        
        Additional parameters for the membership function. The center, 
        lower limit of std., upper limit of std., and 
        height of the gaussian membership function are indicated by params[0], 
        params[1], params[2], and params[3], respectively.
    
    Returns
    -------
    ndarray
        Returns membership values corresponding with the input.
    
    Examples
    --------
    
    >>> x = linspace(0, 1, 201)
    >>> membership_value = gauss_uncert_std_lmf(x, [0.5, 0.2, 0.5, 1])
    """
    return gaussian_mf(x, [params[0], params[1], params[3]])


def rgauss_uncert_std_umf(x, params):
    """
    Right Gaussian with uncertain standard deviation UMF
    
    Parameters
    ----------
    x : 
        numpy (n,) shaped array
        
        The array like input x indicates the points from universe of 
        discourse in which the membership function would be evaluated.
    params : 
        List 
        
        Additional parameters for the membership function. The center, 
        lower limit of std., upper limit of std., and 
        height of the gaussian membership function are indicated by params[0], 
        params[1], params[2], and params[3], respectively.
    
    Returns
    -------
    ndarray
        Returns membership values corresponding with the input.
    
    Examples
    --------
    
    >>> x = linspace(0, 1, 201)
    >>> membership_value = rgauss_uncert_std_umf(x, [0.5, 0.2, 0.5, 1])
    """
    return (x < params[0]) * params[3] + gauss_uncert_std_umf(x, params) * (x >= params[0])

def rgauss_uncert_std_lmf(x, params):
    """
    Right Gaussian with uncertain standard deviation LMF
    
    Parameters
    ----------
    x : 
        numpy (n,) shaped array
        
        The array like input x indicates the points from universe of 
        discourse in which the membership function would be evaluated.
    params : 
        List 
        
        Additional parameters for the membership function. The center, 
        lower limit of std., upper limit of std., and 
        height of the gaussian membership function are indicated by params[0], 
        params[1], params[2], and params[3], respectively.
    
    Returns
    -------
    ndarray
        Returns membership values corresponding with the input.
    
    Examples
    --------
    
    >>> x = linspace(0, 1, 201)
    >>> membership_value = rgauss_uncert_std_lmf(x, [0.5, 0.2, 0.5, 1])
    """
    return (x < params[0]) * params[3] + gauss_uncert_std_lmf(x, params) * (x >= params[0])

def lgauss_uncert_std_umf(x, params):
    """
    Left Gaussian with uncertain standard deviation UMF
    
    Parameters
    ----------
    x : 
        numpy (n,) shaped array
        
        The array like input x indicates the points from universe of 
        discourse in which the membership function would be evaluated.
    params : 
        List 
        
        Additional parameters for the membership function. The center, 
        lower limit of std., upper limit of std., and 
        height of the gaussian membership function are indicated by params[0], 
        params[1], params[2], and params[3], respectively.
    
    Returns
    -------
    ndarray
        Returns membership values corresponding with the input.
    
    Examples
    --------
    
    >>> x = linspace(0, 1, 201)
    >>> membership_value = lgauss_uncert_std_umf(x, [0.5, 0.2, 0.5, 1])
    """
    return (x > params[0]) * params[3] + gauss_uncert_std_umf(x, params) * (x <= params[0])

def lgauss_uncert_std_lmf(x, params):
    """
    Left Gaussian with uncertain standard deviation LMF
    
    Parameters
    ----------
    x : 
        numpy (n,) shaped array
        
        The array like input x indicates the points from universe of 
        discourse in which the membership function would be evaluated.
    params : 
        List 
        
        Additional parameters for the membership function. The center, 
        lower limit of std., upper limit of std., and 
        height of the gaussian membership function are indicated by params[0], 
        params[1], params[2], and params[3], respectively.
    
    Returns
    -------
    ndarray
        Returns membership values corresponding with the input.
    
    Examples
    --------
    
    >>> x = linspace(0, 1, 201)
    >>> membership_value = lgauss_uncert_std_lmf(x, [0.5, 0.2, 0.5, 1])
    """
    return (x > params[0]) * params[3] + gauss_uncert_std_lmf(x, params) * (x <= params[0])


def elliptic_mf(x, params):
    """
    Elliptic membership function.

    Parameters
    ----------
    x : 
        numpy (n,) shaped array
        
        The array like input x indicates the points from universe of 
        discourse in which the membership function would be evaluated.
        
    params : 
        list
        
        Parameters of the elliptic membership function. The center, width,
        exponent, and height of the elliptic membership function are 
        indicated by params[0], params[1], params[2], and params[3].

    Returns
    -------
    ndarray
        Returns membership values corresponding with the input.
    
    Examples
    --------
    
    >>> x = linspace(0, 1, 201)
    >>> membership_value = eliptic_mf(x, [0.5, 0.25, 1.3, 1.])
    
    """
    to_evaluate = ((x <= params[0] + params[1]) * (params[0] - params[1] <= x))
    x = x * to_evaluate + (params[0] + params[1]) * logical_not(to_evaluate)
    return params[3] * (1 - abs((x - params[0]) / params[1]) ** params[2]) ** (1. / params[2])

def semi_elliptic_mf(x, params):
    """
    Semi-elliptic membership function.

    Parameters
    ----------
    x : 
        numpy (n,) shaped array
        
        The array like input x indicates the points from universe of 
        discourse in which the membership function would be evaluated.
        
    params : 
        list
        
        Parameters of the semi-elliptic membership function. The center, width, and
        height of the semi-elliptic membership function are 
        indicated by params[0], params[1], and params[2].

    Returns
    -------
    ndarray
        Returns membership values corresponding with the input.
    
    Examples
    --------
    
    >>> x = linspace(0, 1, 201)
    >>> membership_value = eliptic_mf(x, [0.5, 0.25, 1.3, 1.])
    
    """
    to_evaluate = ((x <= params[0] + params[1]) * (params[0] - params[1] <= x))
    x = x * to_evaluate + (params[0] + params[1]) * logical_not(to_evaluate)
    return params[2] * npround(sqrt(abs(1 - ((params[0] - x) ** 2) / (params[1] ** 2))), decimals=6)

def gbell_mf(x, params):
    """
    Generalized bell shaped membership function.

    Parameters
    ----------
    x : 
        numpy (n,) shaped array
        
        The array like input x indicates the points from universe of 
        discourse in which the membership function would be evaluated.
        
    params : 
        list
        
        Parameters of the generalized bell shaped membership function. 
        The a, b, and c values and height of the generalized bell shaped membership 
        function formula are indicated by params[0], params[1], params[2], and params[3].

    Returns
    -------
    ndarray
        Returns membership values corresponding with the input.

    Examples
    --------

    >>> x = linspace(0., 1., 201)
    >>> membership_value = gbell_mf(x, [0.1, 1., 0.5, 1.])

    """
    return params[3] / (1 + npabs((x - params[2]) / params[0]) ** (2 * params[1]))


class T1FS:
    """ Type 1 Fuzzy Set (T1FS).
       
        Parameters
        ----------
        Parameters of the constructor function:
        
        domain:
            numpy (n,) shaped array
            
            Indicates the universe of discourse dedicated to the T1FS.
        
        mf:
            Membership function
        
        params:
            List of parameters of the membership function
            
        Functions
        ----------
        Functions defined in T1FS class:
        
            copy:
                Returns a copy of the T1FS.

            plot:
                Plots the T1FS.

            negation operator -:
                Returns the negated T1FS.
        
        Examples
        --------
        
        >>> mySet = T1FS(linspace(0., 1., 100), 
                         trapezoid_mf, [0, 0.4, 0.6, 1., 1.])
        >>> mySet.plot()
        
        """
    def __init__(self, domain, mf=zero_mf, params=[]):
        self.domain = domain
        self.mf = mf
        self.params = params
    
    def repr(self):
        return "Type 1 fuzzy set with " + self.mf.__name__ + " as membership function " + \
            "and " + str(self.params) + " as its parameters!"

    def copy(self):
        """
        Copies the T1FS.
        
        Returns
        -------
        T1FS
        
        Returns a copy of the T1FS.
        """
        return T1FS(self.domain, self.mf, self.params)

    def __call__(self, x):
        return self.mf(x, self.params)

    def __neg__(self):
        mf = lambda x, params: subtract(1, self.mf(x, params))
        return T1FS(self.domain, mf, params=self.params)

    def _CoG(self):
        int1 = trapz(self.domain * self(self.domain), self.domain)
        int2 = trapz(self(self.domain), self.domain)
        return int1 / int2

    def defuzzify(self, method="CoG"):
        """
        Defuzzifies the type 1 fuzzy set.

        Parameters
        ----------
        method:
            str

            Must be one of the methods listed below:
            1. CoG: Center of gravity
        
        Returns
        -------
        float
        
        Defuzzified crisp output.
        """
        if method == "CoG":
            return self._CoG()
        else:
            raise ValueError("The method" + method + " is not implemented yet!")

    def plot(self, title=None, legend_text=None, filename=None, 
             ext="pdf", grid=True, xlabel="Domain", ylabel="Membership degree"):
        """
        Plots the T1FS.
        
        Parameters
        ----------
        title:
            str
            
            If it is set, it indicates the title which would be 
            represented in the plot. If it is not set, the plot would not 
            have a title.
        
        legend_text:
            str
            
            If it is set, it indicates the legend text which would 
            be represented in the plot. If it is not set, the plot would 
            not contain a legend.
        
        filename:
            str
            
            If it is set, the plot would be saved as a filename.ext file.
        
        ext:
            str

            Extension of the output file with pdf default value.
        
        grid:
            bool

            Grid on/off.
        
        xlabel:
            str

            Label of the x axis.
        
        ylabel:
            str

            Label of the y axis.
        
        Examples
        --------
        
        >>> mySet = T1FS(linspace(0., 1., 100), 
                         trapezoid_mf, [0, 0.4, 0.6, 1., 1.])
        >>> mySet.plot(filename="mySet")
        """
        plt.figure()
        plt.plot(self.domain, self.mf(self.domain, self.params))
        if legend_text is not None:
            plt.legend([legend_text])
        if title is not None:
            plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(grid)
        if filename is not None:
            plt.savefig(filename + "." + ext, format=ext, dpi=300, bbox_inches="tight")
        plt.show()


def T1_Emphasize(t1fs, m=2.):
    """
    Function for creating emphasized T1FSs.
    
    Parameters
    ----------
    t1fs : 
        T1FS
        
        Type 1 fuzzy set to be emphasized.
        
    m : 
        float, optional
        
        Emphasis degree. The default value is 2.

    Returns
    -------
    emphasized : 
        T1FS
        
        Emphasized type 1 fuzzy set.

    """
    mf = lambda x, params : t1fs.mf(x, params) ** m
    emphasized = T1FS(t1fs.domain, mf, t1fs.params)
    return emphasized


def T1FS_plot(*sets, title=None, legends=None, filename=None, 
              ext="pdf", grid=True, xlabel="Domain", ylabel="Membership degree"):
    """
    Plots multiple T1FSs together in the same figure.
    
    Parameters
    ----------
    *sets:
        Multiple number of T1FSs which would be plotted.
    
    title:
        str
        
        If it is set, it indicates the title which would be 
        represented in the plot. If it is not set, the plot would not 
        have a title.
        
    legends:
        List of strs
        
        List of legend texts to be presented in plot. If it is not 
        set, no legend would be in plot.
        
    filename:
        str
        
        If it is set, the plot would be saved as a filename.ext file.
        
    ext:
        str

        Extension of the output file with pdf default value.
    
    grid:
        bool

        Grid on/off.
    
    xlabel:
        str

        Label of the x axis.
    
    ylabel:
        str

        Label of the y axis.

    Examples
    --------
    
    >>> domain = linspace(0., 1., 100)
    >>> t1fs1 = T1FS(domain, gaussian_mf, [0.33, 0.2, 1.])
    >>> t1fs2 = T1FS(domain, gaussian_mf, [0.66, 0.2, 1.])
    >>> T1FS_plot(t1fs1, t1fs2, title="Plotting T1FSs", 
                  legends=["First set", "Second set"])
    """
    plt.figure()
    for t1fs in sets:
        plt.plot(t1fs.domain, t1fs.mf(t1fs.domain, t1fs.params))
    if legends is not None:
        plt.legend(legends)
    if title is not None:
        plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(grid)
    if filename is not None:
        plt.savefig(filename + "." + ext, format=ext, dpi=300, bbox_inches="tight")
    plt.show()

def T1FS_AND(domain, t1fs1, t1fs2, t_norm):
    """
    And operator for T1FSs.
    
    Parameters
    ----------
    
    domain:
        numpy (n,) shaped array
        
        Indicates the universe of discourse dedicated to the output T1FS.
    
    t1fs1:
        T1FS
        
        First input of the and operator.
        
    t1fs2:
        T1FS
        
        Second input of the and operator.
    
    t_norm:
        function
        
        The t-norm function to be used.
    
    Returns
    -------
    T1FS
    
    Returns the AND of the two input T1FSs.
    
    Examples
    --------
    
    >>> domain = linspace(0., 1., 100)
    >>> t1fs1 = T1FS(domain, gaussian_mf, [0.33, 0.2, 1.])
    >>> t1fs2 = T1FS(domain, gaussian_mf, [0.66, 0.2, 1.])
    >>> t1fs3 = T1FS_AND(domain, t1fs1, t1fs2, min_t_norm)
    >>> t1fs3.plot()
    """
    mf = lambda x, params: t_norm(t1fs1.mf(x, t1fs1.params), t1fs2.mf(x, t1fs2.params))
    return T1FS(domain, mf)

def T1FS_OR(domain, t1fs1, t1fs2, s_norm):
    """
    Or operator for T1FSs.
    
    Parameters
    ----------
    
    domain:
        numpy (n,) shaped array
        
        Indicates the universe of discourse dedicated to the output T1FS.
    
    t1fs1:
        T1FS
        
        First input of the or operator.
        
    t1fs2:
        T1FS
        
        Second input of the or operator.
    
    s_norm:
        function
        
        The s-norm function to be used.
    
    Returns
    -------
    T1FS
    
    Returns the OR of the two input T1FSs.
    
    Examples
    --------
    
    >>> domain = linspace(0., 1., 100)
    >>> t1fs1 = T1FS(domain, gaussian_mf, [0.33, 0.2, 1.])
    >>> t1fs2 = T1FS(domain, gaussian_mf, [0.66, 0.2, 1.])
    >>> t1fs3 = T1FS_OR(domain, t1fs1, t1fs2, max_s_norm)
    >>> t1fs3.plot()
    """
    mf = lambda x, params: s_norm(t1fs1.mf(x, t1fs1.params), t1fs2.mf(x, t1fs2.params))
    return T1FS(domain, mf)


class T1Mamdani:
    """
    Type 1 Mamdani Fuzzy Logic System.

    Parameters
    ----------
    Parameters of the constructor function:

    engine="Product":
        str

        Inference engine of the type 1 Mamdani fuzzy logic system. 
        This parameters is a string an can be one of the following items: 
        Product, Minimum, Lukasiewicz, Zadeh, and Dienes-Rescher.
    
    defuzzification="CoG":
        str

        Defuzzification method of the system. When Lukasiewicz, Zadeh, and Dienes-Rescher 
        inference engines are selected, the defuzzification method is center of the 
        gravity by default. But for Product and Minimum inference engines, defuzzification 
        can be selected among the methods CoG and CoA.

    Members
    -------

    inputs:
        List of str

        List of the inputs names as str.
    
    outputs:
        List of str

        List of the outputs names as str.

    rules:
        List of tuples (antacedent, consequent)

        List of rules, which each rule is defined as a 
        tuple (antecedent, consequent)
        
        Both antacedent and consequent are lists of tuples. Each tuple 
        of this list shows assignement of a variable to a T1FS. 
        First element of the tuple must be the variable name (input or output) 
        as a str and the second element must be a T1FS.

    engine:
        str

        Indicates the engine selected by the user.
    
    defuzzification:
        str

        Indicates the defuzzification method selected by the user.

    Functions
    ---------

    add_input_variable:
        
        Adds an input variable to the inputs list of the T1FLS.
    
    add_output_variable:
        
        Adds an output variable to the outputs list of the T1FLS.
    
    add_rule:
        
        Adds a rule to the rules list of the T1FLS.
    
    copy:
        
        Returns a copy of the type 1 Mamdani fuzzy logic system.
    
    evaluate:
        
        Evaluates the T1 Mamdani FLS's output for the specified crisp input.
        The only input of the evaluate function is a dictionary in which the 
        keys are input variable names as str and the values are the crisp 
        value of inputs to be evaluated.
        The output of the evaluate function is depended on the method selected 
        while constructing the class. For more information, please refer to 
        the examples.
    """
    def __init__(self, engine="Product", defuzzification="CoG"):
        self.inputs = []
        self.outputs = []
        self.rules = []
        self.engine = engine
        if engine == "Product":
            self.evaluate = self._product_evaluate
            self.defuzzification = defuzzification
        elif engine == "Minimum":
            self.evaluate = self._minimum_evaluate
            self.defuzzification = defuzzification
        elif engine == "Lukasiewicz":
            self.evaluate = self._lukasiewicz_evaluate
        elif engine == "Zadeh":
            self.evaluate = self._zadeh_evaluate
        elif engine == "Dienes-Rescher":
            self.evaluate = self._dienes_rescher_evaluate
        else:
            raise ValueError("The " + engine + " fuzzy inference engine is not implemented yet!")
    
    def __repr__(self):
        return "Type 1 Mamadani fuzzy logic system with " + self.engine + " inference engine" + \
            "and " + self.defuzzification + " defuzzification error!"

    def copy(self):
        o = T1Mamdani(self.engine, self.defuzzification)
        o.inputs = self.inputs.copy()
        o.outputs = self.outputs.copy()
        o.rules = self.rules.copy()
        return o
    
    def add_input_variable(self, name):
        """
        Adds new input variable name.
        
        Parameters
        ----------
        
        name:
            str
            
            Name of the new input variable as a str.
        """
        self.inputs.append(name)
    
    def add_output_variable(self, name):
        """
        Adds new output variable name.
        
        Parameters
        ----------
        
        name:
            str
            
            Name of the new output variable as a str.
        """
        self.outputs.append(name)

    def add_rule(self, antecedent, consequent):
        """
        Adds a new rule to the rule base of the T1 Mamdani FLS.
        
        Parameters
        ----------
        
        antecedent:
            List of tuples
            
            Antecedent is a list of tuples in which each tuple indicates 
            assignement of a variable to a T1FS. First element of the 
            tuple must be input variable name as str, and the second 
            element of the tuple must be a T1FS.
            
        consequent:
            List of tuples
            
            Consequent is a list of tuples in which each tuple indicates 
            assignement of a variable to a T1FS. First element of the 
            tuple must be output variable name as str, and the second 
            element of the tuple must be a T1FS.
        """
        self.rules.append((antecedent, consequent))

    def _CoG(self, B):
        C = {}
        D = {}
        for out in self.outputs:
            C[out] = T1FS(B[out][0].domain)
            for B_l in B[out]:
                C[out] = T1FS_OR(B_l.domain, C[out], B_l, max_s_norm)
            D[out] = C[out].defuzzify()
        return C, D

    def _CoA(self, B):
        D = {}
        for out in self.outputs:
            a = 0.
            b = 0.
            for B_l in B[out]:
                tmp = B_l.defuzzify()
                a += tmp * B_l(tmp)
                b += B_l(tmp)
            D[out] = a / b
        return D

    def _product_evaluate(self, inputs):
        B = {out: [] for out in self.outputs}
        for rule in self.rules:
            f = 1.
            for input_statement in rule[0]:
                f = f * input_statement[1].mf(inputs[input_statement[0]], input_statement[1].params)
            for consequent in rule[1]:
                B_l = T1FS_AND(consequent[1].domain, 
                               T1FS(consequent[1].domain, const_mf, [f]), 
                               consequent[1], product_t_norm)
                B[consequent[0]].append(B_l)
        if self.defuzzification == "CoG":
            return self._CoG(B)
        elif self.defuzzification == "CoA":
            return self._CoA(B)
        else:
            raise ValueError("The " + self.defuzzification + \
                " defuzzification method is not implemented yet!")

    def _minimum_evaluate(self, inputs):
        B = {out: [] for out in self.outputs}
        for rule in self.rules:
            f = 1.
            for input_statement in rule[0]:
                f = min_t_norm(f, input_statement[1].mf(inputs[input_statement[0]], input_statement[1].params))
            for consequent in rule[1]:
                B_l = T1FS_AND(consequent[1].domain, 
                               T1FS(consequent[1].domain, const_mf, [f]), 
                               consequent[1], min_t_norm)
                B[consequent[0]].append(B_l)
        if self.defuzzification == "CoG":
            return self._CoG(B)
        elif self.defuzzification == "CoA":
            return self._CoA(B)
        else:
            raise ValueError("The " + self.defuzzification + \
                " defuzzification method is not implemented yet!")

    def _lukasiewicz_evaluate(self, inputs):
        B = {out: [] for out in self.outputs}
        for rule in self.rules:
            f = 1.
            for input_statement in rule[0]:
                f = min_t_norm(f, input_statement[1].mf(inputs[input_statement[0]], input_statement[1].params))
            for consequent in rule[1]:
                mf = lambda x, params: 1. - f + consequent[1].mf(x, consequent[1].params)
                B_l = T1FS(consequent[1].domain, mf)
                B[consequent[0]].append(B_l)
        C = {}
        D = {}
        for out in self.outputs:
            C[out] = T1FS(B[out][0].domain, const_mf, [1])
            for B_l in B[out]:
                C[out] = T1FS_AND(B_l.domain, C[out], B_l, min_t_norm)
            D[out] = C[out].defuzzify()
        return C, D

    def _zadeh_evaluate(self, inputs):
        B = {out: [] for out in self.outputs}
        for rule in self.rules:
            f = 1.
            for input_statement in rule[0]:
                f = min_t_norm(f, input_statement[1].mf(inputs[input_statement[0]], input_statement[1].params))
            for consequent in rule[1]:
                mf = lambda x, params: min_t_norm(f, consequent[1].mf(x, consequent[1].params))
                B_l = T1FS_OR(consequent[1].domain, 
                              T1FS(consequent[1].domain, const_mf, [1 - f]), 
                              T1FS(consequent[1].domain, mf), 
                              max_s_norm)
                B[consequent[0]].append(B_l)
        C = {}
        D = {}
        for out in self.outputs:
            C[out] = T1FS(B[out][0].domain, const_mf, [1])
            for B_l in B[out]:
                C[out] = T1FS_AND(B_l.domain, C[out], B_l, min_t_norm)
            D[out] = C[out].defuzzify()
        return C, D

    def _dienes_rescher_evaluate(self, inputs):
        B = {out: [] for out in self.outputs}
        for rule in self.rules:
            f = 1.
            for input_statement in rule[0]:
                f = min_t_norm(f, input_statement[1].mf(inputs[input_statement[0]], input_statement[1].params))
            for consequent in rule[1]:
                B_l = T1FS_OR(consequent[1].domain, 
                              T1FS(consequent[1].domain, const_mf, [1 - f]), 
                              consequent[1], max_s_norm)
                B[consequent[0]].append(B_l)
        C = {}
        D = {}
        for out in self.outputs:
            C[out] = T1FS(B[out][0].domain, const_mf, [1])
            for B_l in B[out]:
                C[out] = T1FS_AND(B_l.domain, C[out], B_l, min_t_norm)
            D[out] = C[out].defuzzify()
        return C, D


class T1TSK:
    """
    Type 1 TSK Fuzzy Logic System.

    Parameters
    ----------
    Parameters of the constructor function:

    The constructor function of the T1TSK class has no parameters.

    Members
    -------

    inputs:
        List of str

        List of the inputs names as str.
    
    outputs:
        List of str

        List of the outputs names as str.

    rules:
        List of tuples (antacedent, consequent)

        List of rules, which each rule is defined as a 
        tuple (antecedent, consequent)
        

    Functions
    ---------

    add_input_variable:
        
        Adds an input variable to the inputs list of the T1 TSK FLS.
    
    add_output_variable:
        
        Adds an output variable to the outputs list of the T1 TSK FLS.
    
    add_rule:
        
        Adds a rule to the rules list of the T1 TSK FLS.
    
    copy:
        
        Returns a copy of the T1 TSK FLS.
    
    evaluate:

        Evaluates the T1 TSK FLS based on the crisp inputs given by the user.

    """
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.rules = []
    
    def __repr__(self):
        return "Type 1 TSK fuzzy logic system!"

    def copy(self):
        """
        Returns a copy of the IT2FLS.
        """
        o = T1TSK()
        o.inputs = self.inputs.copy()
        o.outputs = self.outputs.copy()
        o.rules = self.rules.copy()
        return o

    def add_input_variable(self, name):
        """
        Adds new input variable name.
        
        Parameters
        ----------
        
        name:
            str
            
            Name of the new input variable as a str.
        """
        self.inputs.append(name)
    
    def add_output_variable(self, name):
        """
        Adds new output variable name.
        
        Parameters
        ----------
        
        name:
            str
            
            Name of the new output variable as a str.
        """
        self.outputs.append(name)
    
    def add_rule(self, antecedent, consequent):
        """
        Adds new rule to the rule base of the T1 TSK FLS.

        Parameters
        ----------

        antecedent:
            List of tuples
            
            Antecedent is a list of tuples in which each tuple indicates 
            assignement of a variable to a T1FS. First element of the 
            tuple must be input variable name as str, and the second 
            element of the tuple must be a T1FS.
        
        consequent:
            List of tuples

            Consequent is a list of tuples in which each tuple indicates 
            assignement of a variable to an output state. First element of the 
            tuple must be output vriable name as str, and the second element 
            of the tuple must be a callable object.
        """
        self.rules.append((antecedent, consequent))

    def evaluate(self, inputs, params):
        """
        Evaluates the T1 TSK FLS based on the crisp inputs given by the user.

        Parameters
        ----------
        inputs:
            dictionary

            Inputs is a dictionary, which the keys are input variable 
            names as str and the values are the crisp value of the inputs to 
            be evaluated.

        params:
            tuple

            This tuple is the parameters of the functions assigned to the 
            consequents of the system rules.

        Returns
        -------
        O:
            dictionary

            The output is a dictionary, which the keys are output variable 
            names as str and the values are the crisp output of the system.
        """
        F = []
        B = {out: 0. for out in self.outputs}
        for rule in self.rules:
            f = 1.
            for input_statement in rule[0]:
                f *= input_statement[1].mf(inputs[input_statement[0]], input_statement[1].params)
            F.append(f)
            for consequent in rule[1]:
                B[consequent[0]] += f * consequent[1](*params)
        f = npsum(F)
        for out in self.outputs:
            B[out] /= f
        return B


class IT2FS:
    """Interval Type 2 Fuzzy Set (IT2FS).
       
        Parameters
        ----------
        Parameters of the constructor function:
        
        domain:
            numpy (n,) shaped array
            
            Indicates the universe of discourse dedicated to the IT2FS.
        
        umf:
            Upper membership function
        
        umf_params:
            List of parameters of upper membership function
        
        lmf:
            Lower membership function
        
        lmf_params:
            List of parameters of lower membership function
        
        check_set:
            If it is True, then a function named check_set in IT2FS will 
            verify the LMF(x) < UMF(x) condition for any x in the domain. If the 
            user is sure that has selected the parameters of the membership 
            functions correct, then calling this time-consuming function 
            is not needed. By default the parameter check_set is False.
            
        Functions
        ----------
        Functions defined in IT2FS class:
        
            copy:
                Returns a copy of the IT2FS.
            plot:
                Plots the IT2FS.
            negation operator -:
                Returns the negated IT2FS.
        
        Examples
        --------
        
        >>> mySet = IT2FS(linspace(0., 1., 100), 
                          trapezoid_mf, [0, 0.4, 0.6, 1., 1.], 
                          tri_mf, [0.25, 0.5, 0.75, 0.6])
        >>> mySet.plot(filename="mySet")
        
        """

    def __init__(self, domain, umf=zero_mf, umf_params=[], lmf=zero_mf, lmf_params=[], check_set=False):
        self.umf = umf
        self.lmf = lmf
        self.umf_params = umf_params
        self.lmf_params = lmf_params

        self.domain = domain
        # self.upper = maximum(minimum(umf(domain, umf_params), 1), 0)
        # self.lower = maximum(minimum(lmf(domain, lmf_params), 1), 0)
        if check_set:
            self.check_set()

    def __repr__(self):
        return "Interval type 2 fuzzy set with " + self.umf.__name__ + " UMF function with " + \
             str(self.umf_params) + " parameters, and " + self.lmf.__name__ + \
             " LMF function with " + str(self.lmf_params) + " parameters."

    @property
    def upper(self):
        return maximum(minimum(self.umf(self.domain, self.umf_params), 1), 0)
    
    @property
    def lower(self):
        return maximum(minimum(self.lmf(self.domain, self.lmf_params), 1), 0)

    def check_set(self):
        """
        Verifies the LMF(x) < UMF(x) for any x in the domain.
        """
        for l, u in zip(self.lower, self.upper):
            if l > u:
                raise ValueError("LMF in some points in domain is larger than UMF.")

    def copy(self):
        """
        Copies the IT2FS.
        
        Returns
        -------
        IT2FS
        
        Returns a copy of the IT2FS.
        """
        return IT2FS(self.domain, umf=self.umf, umf_params=self.umf_params, lmf=self.lmf, lmf_params=self.lmf_params)

    def plot(self, title=None, legend_text=None, filename=None, 
             ext="pdf", grid=True, xlabel="Domain", ylabel="Membership degree"):
        """
        Plots the IT2FS.
        
        Parameters
        ----------
        title:
            str
            
            If it is set, it indicates the title which would be 
            represented in the plot. If it is not set, the plot would not 
            have a title.
        
        legend_text:
            str
            
            If it is set, it indicates the legend text which would 
            be represented in the plot. If it is not set, the plot would 
            not contain a legend.
        
        filename:
            str
        
            If it is set, the plot would be saved as a filename.ext file.
            
        ext:
            str

            Extension of the output file with pdf default value.
        
        grid:
            bool

            Grid on/off.
        
        xlabel:
            str

            Label of the x axis.
        
        ylabel:
            str

            Label of the y axis.
        
        Examples
        --------
        
        >>> mySet = IT2FS(linspace(0., 1., 100), 
                          trapezoid_mf, [0, 0.4, 0.6, 1., 1.], 
                          tri_mf, [0.25, 0.5, 0.75, 0.6])
        >>> mySet.plot(filename="mySet")
        """
        plt.figure()
        plt.fill_between(self.domain, self.upper, self.lower)
        if legend_text is not None:
            plt.legend([legend_text])
        if title is not None:
            plt.title(title)
        plt.plot(self.domain, self.upper, color="black")
        plt.plot(self.domain, self.lower, color="black")
        plt.grid(grid)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if filename is not None:
            plt.savefig(filename + "." + ext, format=ext, dpi=300, bbox_inches="tight")
        plt.show()

    def __neg__(self):
        """
        Negates the IT2FS.
        
        Returns
        -------
        IT2FS
        
        Returns a negated copy of the IT2FS.
        """
        umf = lambda x, params: subtract(1, self.umf(x, params))
        lmf = lambda x, params: subtract(1, self.lmf(x, params))
        neg_it2fs = IT2FS(self.domain, lmf, self.lmf_params, umf, self.umf_params)
        return neg_it2fs


def IT2_Emphasize(it2fs, m=2.):
    """
    Function for creating emphasized IT2FSs.
    
    Parameters
    ----------
    it2fs : 
        IT2FS
        
        Interval type 2 fuzzy set to be emphasized.
        
    m : 
        float, optional
        
        Emphasis degree. The default is 2.

    Returns
    -------
    emphasized : 
        IT2FS
        
        Emphasized interval type 2 fuzzy set.

    """
    lmf = lambda x, params : it2fs.lmf(x, it2fs.lmf_params) ** m
    umf = lambda x, params : it2fs.umf(x, it2fs.umf_params) ** m
    emphasized = IT2FS(it2fs.domain, 
                       umf, it2fs.umf_params, 
                       lmf, it2fs.lmf_params)
    return emphasized


def IT2FS_Elliptic(domain, params, check_set=False):
    """
    Creates an elliptic IT2FS.
    
    Parameters
    ----------
    
    domain:
        numpy (n,) shaped array
        
        Indicates the universe of discourse dedicated to the IT2FS.
    
    params:
        List
        
        The parameters of the elliptic IT2FS, 
        the center, width, UMF's exponent, LMF's exponent, and height are 
        indicated by params[0], params[1], params[2], params[3], and params[4], respectively.
    
    Returns
    -------
    IT2FS
        Returns an elliptic IT2FS with specified parameters.
    
    Examples
    --------
    
    >>> domain = linspace(0., 1., 100)
    >>> mySet = IT2FS_Elliptic(domain, [0.5, 0.25, 1.3, 0.7, 0.8])
    >>> mySet.plot()
    
    """
    return IT2FS(domain, 
                 elliptic_mf, [params[0], params[1], params[2], params[4]], 
                 elliptic_mf, [params[0], params[1], params[3], params[4]], check_set=check_set)

def IT2FS_Semi_Elliptic(domain, params, check_set=False):
    """
    Creates a semi-elliptic IT2FS.
    
    Parameters
    ----------
    
    domain:
        numpy (n,) shaped array
        
        Indicates the universe of discourse dedicated to the IT2FS.
    
    params:
        List
        
        The parameters of the semi-elliptic IT2FS, 
        the center, UMF's width, LMF's width, and height are 
        indicated by params[0], params[1], params[2], and params[3], respectively.
    
    Returns
    -------
    IT2FS
        Returns a semi-elliptic IT2FS with specified parameters.
    
    Examples
    --------
    
    >>> domain = linspace(0., 1., 100)
    >>> mySet = IT2FS_Semi_Elliptic(domain, [0.5, 0.15, 0.05, 0.6])
    >>> mySet.plot()
    
    """
    return IT2FS(domain, 
                 semi_elliptic_mf, [params[0], params[1], params[3]], 
                 semi_elliptic_mf, [params[0], params[2], params[3]], check_set=check_set)


def IT2FS_Gaussian_UncertMean(domain, params, check_set=False):
    """
    Creates an Gaussian IT2FS with uncertain mean value.
    
    Parameters
    ----------
    
    domain:
        numpy (n,) shaped array
        
        Indicates the universe of discourse dedicated to the IT2FS.
    
    params:
        List
        
        The parameters of the Gaussian IT2FS with uncertain mean value, 
        the mean center, mean spread, standard deviation, and height are 
        indicated by params[0], params[1], params[2], and params[3], respectively.
    
    Returns
    -------
    IT2FS
        Returns a Gaussian IT2FS with uncertain mean value with specified 
        parameters.
    
    Examples
    --------
    
    >>> domain = linspace(0., 1., 100)
    >>> mySet = IT2FS_Gaussian_UncertMean(domain, [0., 0.25, 0.2])
    >>> mySet.plot()
    
    """
    ml = params[0] - params[1] / 2.
    mr = params[0] + params[1] / 2.
    return IT2FS(domain, 
                 gauss_uncert_mean_umf, [ml, mr, params[2], params[3]], 
                 gauss_uncert_mean_lmf, [ml, mr, params[2], params[3]], check_set=check_set)


def IT2FS_Gaussian_UncertStd(domain, params, check_set=False):
    """
    Creates a Gaussian IT2FS with uncertain standard deviation value.
    
    Parameters
    ----------
    
    domain:
        numpy (n,) shaped array
        
        Indicates the universe of discourse dedicated to the IT2FS.
    
    params:
        List
        
        The parameters of the Gaussian IT2FS with uncertain standard 
        deviation value, the mean, standard deviation center, 
        standard deviation spread, and height are indicated by params[0], 
        params[1], params[2], and params[3], respectively.
    
    Returns
    -------
    IT2FS
        Returns a Gaussian IT2FS with uncertain standard deviation value 
        with specified parameters.
    
    Examples
    --------
    
    >>> domain = linspace(0., 1., 100)
    >>> mySet = IT2FS_Gaussian_UncertStd(domain, [0.5, 0.2, 0.05, 1.])
    >>> mySet.plot()
    
    """
    stdl = params[1] - params[2] / 2
    stdr = params[1] + params[2] / 2
    return IT2FS(domain, 
                 gauss_uncert_std_umf, [params[0], stdl, stdr, params[3]], 
                 gauss_uncert_std_lmf, [params[0], stdl, stdr, params[3]], check_set=check_set)


def IT2FS_RGaussian_UncertStd(domain, params, check_set=False):
    """
    Creates a Right Gaussian IT2FS with uncertain standard deviation value.
    
    Parameters
    ----------
    
    domain:
        numpy (n,) shaped array
        
        Indicates the universe of discourse dedicated to the IT2FS.
    
    params:
        List
        
        The parameters of the Gaussian IT2FS with uncertain standard 
        deviation value, the mean, standard deviation center, 
        standard deviation spread, and height are indicated by params[0], 
        params[1], params[2], and params[3], respectively.
    
    Returns
    -------
    IT2FS
        Returns a Gaussian IT2FS with uncertain standard deviation value 
        with specified parameters.
    
    Examples
    --------
    
    >>> domain = linspace(0., 1., 100)
    >>> mySet = R_IT2FS_Gaussian_UncertStd(domain, [0.5, 0.2, 0.05, 1.])
    >>> mySet.plot()
    
    """
    stdl = params[1] - params[2] / 2
    stdr = params[1] + params[2] / 2
    return IT2FS(domain, 
                  rgauss_uncert_std_umf, 
                  [params[0], stdl, stdr, params[3]],
                  rgauss_uncert_std_lmf, 
                  [params[0], stdl, stdr, params[3]], check_set=check_set)

R_IT2FS_Gaussian_UncertStd = IT2FS_RGaussian_UncertStd

def IT2FS_LGaussian_UncertStd(domain, params, check_set=False):
    """
    Creates a Left Gaussian IT2FS with uncertain standard deviation value.
    
    Parameters
    ----------
    
    domain:
        numpy (n,) shaped array
        
        Indicates the universe of discourse dedicated to the IT2FS.
    
    params:
        List
        
        The parameters of the Gaussian IT2FS with uncertain standard 
        deviation value, the mean, standard deviation center, 
        standard deviation spread, and height are indicated by params[0], 
        params[1], params[2], and params[3], respectively.
    
    Returns
    -------
    IT2FS
        Returns a Gaussian IT2FS with uncertain standard deviation value 
        with specified parameters.
    
    Examples
    --------
    
    >>> domain = linspace(0., 1., 100)
    >>> mySet = L_IT2FS_Gaussian_UncertStd(domain, [0.5, 0.2, 0.05, 1.])
    >>> mySet.plot()
    
    """
    stdl = params[1] - params[2] / 2
    stdr = params[1] + params[2] / 2
    return IT2FS(domain, 
                  lgauss_uncert_std_umf, 
                  [params[0], stdl, stdr, params[3]],
                  lgauss_uncert_std_lmf, 
                  [params[0], stdl, stdr, params[3]], check_set=check_set)


L_IT2FS_Gaussian_UncertStd = IT2FS_LGaussian_UncertStd

def IT2FS_plot(*sets, title=None, legends=None, filename=None, 
               ext="pdf", grid=True, xlabel="Domain", ylabel="Membership degree"):
    """
    Plots multiple IT2FSs together in the same figure.
    
    Parameters
    ----------
    *sets:
        Multiple number of IT2FSs which would be plotted.
    
    title:
        str
        
        If it is set, it indicates the title which would be 
        represented in the plot. If it is not set, the plot would not 
        have a title.
        
    legends:
        List of strs
        
        List of legend texts to be presented in plot. If it is not 
        set, no legend would be in plot.
        
    filename:
        str
        
        If it is set, the plot would be saved as a filename.ext file.
        
    ext:
        str

        Extension of the output file with pdf default value.
    
    grid:
        bool

        Grid on/off.
    
    xlabel:
        str

        Label of the x axis.
    
    ylabel:
        str

        Label of the y axis.
        
    Examples
    --------
    
    >>> domain = linspace(0., 1., 100)
    >>> it2fs1 = IT2FS_Gaussian_UncertStd(domain, [0.33, 0.2, 0.05])
    >>> it2fs2 = IT2FS_Gaussian_UncertStd(domain, [0.66, 0.2, 0.05])
    >>> IT2FS_plot(it2fs1, it2fs2, title="Plotting IT2FSs", 
                   legends=["First set", "Second set"])
    """
    plt.figure()
    for it2fs in sets:
        plt.fill_between(it2fs.domain, it2fs.upper, it2fs.lower, alpha=0.5)
    if legends is not None:
        plt.legend(legends)
    for it2fs in sets:
        plt.plot(it2fs.domain, it2fs.lower, color="black")
        plt.plot(it2fs.domain, it2fs.upper, color="black")
    if title is not None:
        plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(grid)
    if filename is not None:
        plt.savefig(filename + "." + ext, format=ext, dpi=300, bbox_inches="tight")
    plt.show()

def TR_plot(domain, tr, title=None, legend=None, filename=None, 
            ext="pdf", grid=True, xlabel="Domain", ylabel="Membership degree"):
    """
    Plots a type reduced IT2FS.
    
    Parameters
    ----------
    domain:
        numpy (n,) shaped array
        
        Indicates the universe of discourse dedicated to the IT2FS.
    
    tr:
        Tuple (l, r)
        
        Indicates the type reduced set to be plotted.
    
    title:
        str
        
        If it is set, it indicates the title which would be 
        represented in the plot. If it is not set, the plot would not 
        have a title.
        
    legend:
        str
        
        If it is set, it indicates the legend text which would 
        be represented in the plot. If it is not set, the plot would 
        not contain a legend.
        
    filename:
        str
        
        If it is set, the plot would be saved as a filename.ext file.
        
    ext:
        str

        Extension of the output file with pdf default value.
    
    grid:
        bool

        Grid on/off.
    
    xlabel:
        str

        Label of the x axis.
    
    ylabel:
        str

        Label of the y axis.
        
    Examples
    --------
    
    >>> tr1 = (0.2, 0.3)
    >>> TR_plot(linspace(0., 1., 100), tr1)
    """
    plt.figure()
    plt.plot([min(domain), tr[0], tr[0], tr[1], tr[1], max(domain)], 
              [0, 0, 1, 1, 0, 0], linewidth=2)
    plt.xlim((min(domain), max(domain)))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if title is not None:
        plt.title(title)
    if legend is not None:
        plt.legend([legend])
    plt.grid(grid)
    if filename is not None:
        plt.savefig(filename + "." + ext, format=ext, dpi=300, bbox_inches="tight")
    plt.show()

def crisp(tr):
    """
    Calculates the crisp number achieved from type reduced IT2FS.
    
    Parameters
    ----------
    
    tr:
        Tuple (l, r)
        
        Type reduced IT2FS
    
    Returns
    -------
    float
    
    Returns the crisp number achieved from type reduced IT2FS.
    
    Examples
    --------
    
    >>> tr1 = (0.1, 0.3)
    >>> print(crisp(tr1))
    """
    return (tr[0] + tr[1]) / 2

def crisp_list(trs, o=None):
    """
    Calculates the crisp outputs achieved by calling the evaluate_list 
    function from IT2FLS class.
    
    Parameters
    ----------
    
    trs:
        List of Tuple (l, r)
        
        Type reduced IT2FSs
    
    o:
        str
        
        The name of the output variable to be processed. If it is not given, 
        then the crisp outputs are calculated for all output variables.
    
    Returns
    -------
    List of float (or Dictionary of Lists of float)
    """
    if o is None:
        output = {}
        for key in trs[0].keys():
            output[key] = []
        for tr in trs:
            for key in trs[0].keys():
                output[key].append(crisp(tr[key]))
        return output
            
    else:
        output = []
        for tr in trs:
            output.append(crisp(tr[o]))
        return output

def min_t_norm(a, b):
    """
    Minimum t-norm function.
    
    Parameters
    ----------
    
    a:
        numpy (n,) shaped array
    
    b:
        numpy (n,) shaped array
    
    Returns
    -------
    Returns minimum t-norm of a and b
    
    Examples
    --------
    
    >>> a = random.random(10,)
    >>> b = random.random(10,)
    >>> c = min_t_norm(a, b)
    """
    return minimum(a, b)


def product_t_norm(a, b):
    """
    Product t-norm function.
    
    Parameters
    ----------
    
    a:
        numpy (n,) shaped array
    
    b:
        numpy (n,) shaped array
    
    Returns
    -------
    Returns product t-norm of a and b
    
    Examples
    --------
    
    >>> a = random.random(10,)
    >>> b = random.random(10,)
    >>> c = product_t_norm(a, b)
    """
    return multiply(a, b)

def lukasiewicz_t_norm(a, b):
    """
    Lukasiewicz t-norm function.
    
    Parameters
    ----------
    
    a:
        numpy (n,) shaped array
    
    b:
        numpy (n,) shaped array
    
    Returns
    -------
    Returns Lukasiewicz t-norm of a and b
    
    Examples
    --------
    
    >>> a = random.random(10,)
    >>> b = random.random(10,)
    >>> c = lukasiewicz_t_norm(a, b)
    """
    return maximum(0, a + b - 1)

def drastic_t_norm(a, b):
    """
    Drastic t-norm function.
    
    Parameters
    ----------
    
    a:
        numpy (n,) shaped array
    
    b:
        numpy (n,) shaped array
    
    Returns
    -------
    Returns drastic t-norm of a and b
    
    Examples
    --------
    
    >>> a = random.random(10,)
    >>> b = random.random(10,)
    >>> c = drastic_t_norm(a, b)
    """
    return b * (a == 1) + a * (b == 1)

def nilpotent_minimum_t_norm(a, b):
    """
    Nilpotent minimum t-norm function.
    
    Parameters
    ----------
    
    a:
        numpy (n,) shaped array
    
    b:
        numpy (n,) shaped array
    
    Returns
    -------
    Returns nilpotent minimum t-norm of a and b
    
    Examples
    --------
    
    >>> a = random.random(10,)
    >>> b = random.random(10,)
    >>> c = nilpotent_minimum_t_norm(a, b)
    """
    return minimum(a, b) * (a + b > 1)

def hamacher_product_t_norm(a, b):
    """
    Hamacher product t-norm function.
    
    Parameters
    ----------
    
    a:
        numpy (n,) shaped array
    
    b:
        numpy (n,) shaped array
    
    Returns
    -------
    Returns hamacher product t-norm of a and b
    
    Examples
    --------
    
    >>> a = random.random(10,)
    >>> b = random.random(10,)
    >>> c = hamacher_product_t_norm(a, b)
    """
    return ((a * b) / (a + b - a * b)) * logical_not((a == 0) * (b == 0))

def max_s_norm(a, b):
    """
    Maximum s-norm function.
    
    Parameters
    ----------
    
    a:
        numpy (n,) shaped array
    
    b:
        numpy (n,) shaped array
    
    Returns
    -------
    Returns maximum s-norm of a and b
    
    Examples
    --------
    
    >>> a = random.random(10,)
    >>> b = random.random(10,)
    >>> c = max_s_norm(a, b)
    """
    return maximum(a, b)

def probabilistic_sum_s_norm(a, b):
    """
    Probabilistic sum s-norm function.

    Parameters
    ----------

    a:
        numpy (n,) shaped array

    b:
        numpy (n,) shaped array

    Returns
    -------
    Returns probabilistic sum s-norm of a and b

    Examples
    --------

    >>> a = random.random(10,)
    >>> b = random.random(10,)
    >>> c = probabilistic_sum_s_norm(a, b)
    """
    return a + b - a * b

def bounded_sum_s_norm(a, b):
    """
    Bounded sum s-norm function.

    Parameters
    ----------

    a:
        numpy (n,) shaped array

    b:
        numpy (n,) shaped array

    Returns
    -------
    Returns bounded sum s-norm of a and b

    Examples
    --------

    >>> a = random.random(10,)
    >>> b = random.random(10,)
    >>> c = bounded_sum_s_norm(a, b)
    """
    return minimum(a + b, 1)

def drastic_s_norm(a, b):
    """
    Drastic s-norm function.

    Parameters
    ----------

    a:
        numpy (n,) shaped array

    b:
        numpy (n,) shaped array

    Returns
    -------
    Returns drastic s-norm of a and b

    Examples
    --------

    >>> a = random.random(10,)
    >>> b = random.random(10,)
    >>> c = drastic_s_norm(a, b)
    """
    return b * (a == 0) + a * (b == 0) + 1. * (a != 0.) * (b != 0.)

def nilpotent_maximum_s_norm(a, b):
    """
    Nilpotent maximum s-norm function.

    Parameters
    ----------

    a:
        numpy (n,) shaped array

    b:
        numpy (n,) shaped array

    Returns
    -------
    Returns nilpotent maximum s-norm of a and b

    Examples
    --------

    >>> a = random.random(10,)
    >>> b = random.random(10,)
    >>> c = nilpotent_maximum_s_norm(a, b)
    """
    return maximum(a, b) * (a + b < 1) + 1. * (a + b >= 1)

def einstein_sum_s_norm(a, b):
    """
    Einstein sum s-norm function.

    Parameters
    ----------

    a:
        numpy (n,) shaped array

    b:
        numpy (n,) shaped array

    Returns
    -------
    Returns einstein sum s-norm of a and b

    Examples
    --------

    >>> a = random.random(10,)
    >>> b = random.random(10,)
    >>> c = einstein_sum_s_norm(a, b)
    """
    return (a + b) / (1 + a * b)

def meet(domain, it2fs1, it2fs2, t_norm):
    """
    Meet operator for IT2FSs.
    
    Parameters
    ----------
    
    domain:
        numpy (n,) shaped array
        
        Indicates the universe of discourse dedicated to the IT2FS.
    
    it2fs1:
        IT2FS
        
        First input of the meet operator.
        
    it2fs2:
        IT2FS
        
        Second input of the meet operator.
    
    t_norm:
        function
        
        The t-norm function to be used.
    
    Returns
    -------
    IT2FS
    
    Returns the meet of the two input IT2FSs.
    
    Examples
    --------
    
    >>> domain = linspace(0., 1., 100)
    >>> it2fs1 = IT2FS_Gaussian_UncertStd(domain, [0.33, 0.2, 0.05, 1.])
    >>> it2fs2 = IT2FS_Gaussian_UncertStd(domain, [0.66, 0.2, 0.05, 1.])
    >>> it2fs3 = meet(domain, it2fs1, it2fs2, min_t_norm)
    >>> it2fs3.plot()
    """
    umf = lambda x, params: t_norm(it2fs1.umf(x, it2fs1.umf_params), 
                                   it2fs2.umf(x, it2fs2.umf_params))
    lmf = lambda x, params: t_norm(it2fs1.lmf(x, it2fs1.lmf_params), 
                                   it2fs2.lmf(x, it2fs2.lmf_params))
    it2fs = IT2FS(domain, umf, [], lmf, [])
    return it2fs


def join(domain, it2fs1, it2fs2, s_norm):
    """
    Join operator for IT2FSs.
    
    Parameters
    ----------
    
    domain:
        numpy (n,) shaped array
        
        Indicates the universe of discourse dedicated to the IT2FS.
    
    it2fs1:
        IT2FS
        
        First input of the join operator.
        
    it2fs2:
        IT2FS
        
        Second input of the join operator.
    
    s_norm:
        function
        
        The s-norm function to be used.
    
    Returns
    -------
    IT2FS
    
    Returns the join of the two input IT2FSs.
    
    Examples
    --------
    
    >>> domain = linspace(0., 1., 100)
    >>> it2fs1 = IT2FS_Gaussian_UncertStd(domain, [0.33, 0.2, 0.05, 1.])
    >>> it2fs2 = IT2FS_Gaussian_UncertStd(domain, [0.66, 0.2, 0.05, 1.])
    >>> it2fs3 = join(domain, it2fs1, it2fs2, max_s_norm)
    >>> it2fs3.plot()
    """
    umf = lambda x, params: s_norm(it2fs1.umf(x, it2fs1.umf_params), 
                                   it2fs2.umf(x, it2fs2.umf_params))
    lmf = lambda x, params: s_norm(it2fs1.lmf(x, it2fs1.lmf_params), 
                                   it2fs2.lmf(x, it2fs2.lmf_params))
    it2fs = IT2FS(domain, umf, [], lmf, [])
    return it2fs

def trim(intervals):
    v = intervals[:, 3]
    i, = where(v > 0)
    if i.size == 0:
        return False
    else:
        min1 = i[0]
        max1 = i[-1] + 1
    
        v = intervals[:, 2]
        i, = where(v > 0)
        if i.size == 0:
            min2 = min1
            max2 = max1
        else:
            min2 = i[0]
            max2 = i[-1] + 1
        return intervals[min(min1, min2):max(max1, max2), :]

def KM_algorithm(intervals, params=[]):  # intervals = [[a1, b1, c1, d1], [a2, b2, c2, d2], ...]
    """
    KM algorithm
    
    Parameters
    ----------
    
    intervals:
        numpy (n, 4) array
        
        Y = intervals[:, 0:2]
        
        F = intervals[:, 2:4]
    
    params:
        List
        
        List of parameters of algorithm, if it is needed.
    
    Returns
    -------
    Tuple (l, r)
    """
    # left calculations
    intervals = trim(intervals)
    
    if intervals is False:
        return 0., 0.
    
    w = (intervals[:, 2] + intervals[:, 3]) / 2.
    w_l = w[:]

    N = len(intervals)
    intervals = intervals[intervals[:,0].argsort()]
    y_l_prime_num = npsum(intervals[:, 0] * w_l)
    y_prime_den = npsum(w_l)
    y_l_prime = y_l_prime_num / y_prime_den
    
    while True:
        k_l = 0
        for i in range(0, N-1):
            if (intervals[i, 0] <= y_l_prime <= intervals[i+1, 0]) or \
                isclose(intervals[i, 0], y_l_prime) or \
                isclose(y_l_prime, intervals[i+1, 0]):
                k_l = i
                break
        
        ii = arange(N)
        w_l = (ii <= k_l) * intervals[:, 3] + (ii > k_l) * intervals[:, 2]
        y_l_num = npsum(intervals[:, 0] * w_l)
        y_l_den = npsum(w_l)
        y_l = y_l_num / y_l_den
        if isclose(y_l, y_l_prime, abs_tol=1.0e-6):
            break
        else:
            y_l_prime = y_l
    # right calculations
    w_r = w[:]
    
    intervals = intervals[intervals[:, 1].argsort()]
    y_r_prime_num = npsum(intervals[:, 1] * w_r)
    y_r_prime = y_r_prime_num / y_prime_den
    while True:
        k_r = 0
        for i in range(0, N-1):
            if (intervals[i, 1] <= y_r_prime <= intervals[i+1, 1]) or \
                isclose(intervals[i, 1], y_r_prime) or \
                isclose(y_r_prime, intervals[i+1, 1]):
                k_r = i
                break
        
        ii = arange(N)
        w_r = (ii <= k_r) * intervals[:, 2] + (ii > k_r) * intervals[:, 3]
        y_r_num = npsum(intervals[:, 1] * w_r)
        y_r_den = npsum(w_r)
        y_r = y_r_num / y_r_den
        if isclose(y_r, y_r_prime, abs_tol=1.0e-6):
            break
        else:
            y_r_prime = y_r
    return y_l, y_r


def EKM_algorithm(intervals, params=[]):
    """
    EKM algorithm
    
    Parameters
    ----------
    
    intervals:
        numpy (n, 4) array
        
        Y = intervals[:, 0:2]
        
        F = intervals[:, 2:4]
    
    params:
        List
        
        List of parameters of algorithm, if it is needed.
    
    Returns
    -------
    Tuple (l, r)
    """
    
    # Left calculations
    
    intervals = trim(intervals)
    
    if intervals is False:
        return 0, 0
    
    N = len(intervals)
    
    k_l = round(N / 2.4)

    intervals = intervals[intervals[:, 0].argsort()]
    a_l = npsum(intervals[:k_l, 0] * intervals[:k_l, 3]) + \
          npsum(intervals[k_l:, 0] * intervals[k_l:, 2])
    b_l = npsum(intervals[:k_l, 3]) + npsum(intervals[k_l:, 2])
    y_l_prime = a_l / b_l
    while True:
        k_l_prime = 0
        for i in range(0, N-1):
            if (intervals[i, 0] <= y_l_prime <= intervals[i+1, 0]) or \
                isclose(intervals[i, 0], y_l_prime, abs_tol=1.0e-6) or \
                isclose(y_l_prime, intervals[i+1, 0], abs_tol=1.0e-6):
                k_l_prime = i
                break
        if k_l_prime == k_l:
            y_l = y_l_prime
            break
        s_l = sign(k_l_prime - k_l)
        imin = min(k_l, k_l_prime) + 1
        imax = max(k_l, k_l_prime)
        
        a_l_prime = a_l + s_l * npsum(intervals[imin:imax, 0] * \
                    (intervals[imin:imax, 3] - intervals[imin:imax, 2]))
        b_l_prime = b_l + s_l * \
                    npsum(intervals[imin:imax, 3] - intervals[imin:imax, 2])
        y_l_second = a_l_prime / b_l_prime
        
        k_l = k_l_prime
        y_l_prime = y_l_second
        a_l = a_l_prime
        b_l = b_l_prime
    # Right calculations
    intervals = intervals[intervals[:, 1].argsort()]
    k_r = round(N / 1.7)
    a_r = npsum(intervals[:k_r, 1] * intervals[:k_r, 2]) + \
          npsum(intervals[k_r:, 1] * intervals[k_r:, 3])
    b_r = npsum(intervals[:k_r, 2]) + npsum(intervals[k_r:, 3])

    y_r_prime = a_r / b_r

    while True:
        k_r_prime = 0
        for i in range(0, N-1):
            if (intervals[i, 1] <= y_r_prime <= intervals[i+1, 1]) or \
                isclose(intervals[i, 1], y_r_prime, abs_tol=1.0e-6) or \
                isclose(y_r_prime, intervals[i+1, 1], abs_tol=1.0e-6):
                k_r_prime = i
                break
        if k_r_prime == k_r:
            y_r = y_r_prime
            break
        
        s_r = sign(k_r_prime - k_r)
        
        imin = min(k_r, k_r_prime) + 1
        imax = max(k_r, k_r_prime)
        a_r_prime = npsum(intervals[imin:imax, 1] * (intervals[imin:imax, 3] - 
                          intervals[imin:imax, 2]))
        b_r_prime = npsum(intervals[imin:imax, 3] - intervals[imin:imax, 2])
        
        a_r_prime = a_r - s_r * a_r_prime
        b_r_prime = b_r - s_r * b_r_prime
        y_r_second = a_r_prime / b_r_prime
        k_r = k_r_prime
        y_r_prime = y_r_second
        a_r = a_r_prime
        b_r = b_r_prime
    return y_l, y_r


def WEKM_algorithm(intervals, params=[]):
    """
    WEKM algorithm
    
    Parameters
    ----------
    
    intervals:
        numpy (n, 4) array
        
        Y = intervals[:, 0:2]
        
        F = intervals[:, 2:4]
    
    params:
        List
        
        List of parameters of algorithm, if it is needed.
    
    Returns
    -------
    Tuple (l, r)
    """
    
    # Left calculations
    intervals = intervals[intervals[:,0].argsort()]
    intervals = trim(intervals)
    
    if intervals is False:
        return 0, 0
    
    N = len(intervals)
    
    k_l = round(N / 2.4)
    a_l = 0
    b_l = 0
    for i in range(k_l):
        a_l += params[i] * intervals[i, 0] * intervals[i, 3]
        b_l += params[i] * intervals[i, 3]
    for i in range(k_l, N):
        a_l += params[i] * intervals[i, 0] * intervals[i, 2]
        b_l += params[i] * intervals[i, 2]
    y_l_prime = a_l / b_l
    while True:
        k_l_prime = 0
        for i in range(1, N):
            if (intervals[i - 1, 0] <= y_l_prime <= intervals[i, 0]) or \
                isclose(intervals[i - 1, 0], y_l_prime) or \
                isclose(y_l_prime, intervals[i, 0]):
                k_l_prime = i - 1
                break
        if k_l_prime == k_l:
            y_l = y_l_prime
            break
        s_l = sign(k_l_prime - k_l)
        a_l_prime = 0
        b_l_prime = 0
        for i in range(min(k_l, k_l_prime) + 1, max(k_l, k_l_prime)):
            a_l_prime += params[i] * intervals[i, 0] * (intervals[i, 3] - intervals[i, 2])
            b_l_prime += params[i] * (intervals[i, 3] - intervals[i, 2])
        a_l_prime = a_l + s_l * a_l_prime
        b_l_prime = b_l + s_l * b_l_prime
        y_l_second = a_l_prime / b_l_prime
        k_l = k_l_prime
        y_l_prime = y_l_second
        a_l = a_l_prime
        b_l = b_l_prime
    # Right calculations
    intervals = intervals[intervals[:,1].argsort()]
    k_r = round(N / 1.7)
    a_r = 0
    b_r = 0
    for i in range(k_r):
        a_r += params[i] * intervals[i, 1] * intervals[i, 2]
        b_r += params[i] * intervals[i, 2]
    for i in range(k_r, N):
        a_r += params[i] * intervals[i, 1] * intervals[i, 3]
        b_r += params[i] * intervals[i, 3]
    y_r_prime = a_r / b_r
    while True:
        k_r_prime = 0
        for i in range(1, N):
            if (intervals[i - 1, 1] <= y_r_prime <= intervals[i, 1]) or \
                isclose(intervals[i - 1, 1], y_r_prime) or \
                isclose(y_r_prime, intervals[i, 1]):
                k_r_prime = i - 1
                break
        if k_r_prime == k_r:
            y_r = y_r_prime
            break
        s_r = sign(k_r_prime - k_r)
        a_r_prime = 0
        b_r_prime = 0
        for i in range(min(k_r, k_r_prime) + 1, max(k_r, k_r_prime)):
            a_r_prime += params[i] * intervals[i, 1] * (intervals[i, 3] - intervals[i, 2])
            b_r_prime += params[i] * (intervals[i, 3] - intervals[i, 2])
        a_r_prime = a_r - s_r * a_r_prime
        b_r_prime = b_r - s_r * b_r_prime
        y_r_second = a_r_prime / b_r_prime
        k_r = k_r_prime
        y_r_prime = y_r_second
        a_r = a_r_prime
        b_r = b_r_prime
    return y_l, y_r


def TWEKM_algorithm(intervals, params):
    """
    TWEKM algorithm
    
    Parameters
    ----------
    
    intervals:
        numpy (n, 4) array
        
        Y = intervals[:, 0:2]
        
        F = intervals[:, 2:4]
    
    params:
        List
        
        List of parameters of algorithm, if it is needed.
    
    Returns
    -------
    Tuple (l, r)
    """
    params = []
    N = len(intervals)
    for i in range(N):
        if i == 0 or i == N-1:
            params.append(0.5)
        else:
            params.append(1)
    return WEKM_algorithm(intervals, params)


def EIASC_algorithm(intervals, params=[]):
    """
    EIASC algorithm
    
    Parameters
    ----------
    
    intervals:
        numpy (n, 4) array
        
        Y = intervals[:, 0:2]
        
        F = intervals[:, 2:4]
    
    params:
        List
        
        List of parameters of algorithm, if it is needed.
    
    Returns
    -------
    Tuple (l, r)
    """
    
    # Left calculations
    
    intervals = trim(intervals)
    
    if intervals is False:
        return 0, 0
    
    N = len(intervals)
    
    intervals = intervals[intervals[:, 0].argsort()]
    a_l = npsum(intervals[:, 0] * intervals[:, 2])
    b_l = npsum(intervals[:, 2])
    L = 0
    while True:
        d = intervals[L, 3] - intervals[L, 2]
        a_l += intervals[L, 0] * d
        b_l += d
        y_l = a_l / b_l
        L += 1
        if (y_l <= intervals[L, 0]) or isclose(y_l, intervals[L, 0]):
            break 
    # Right calculations
    intervals = intervals[intervals[:, 1].argsort()]
    a_r = npsum(intervals[:, 1] * intervals[:, 2])
    b_r = npsum(intervals[:, 2])
    R = N - 1
    while True:
        d = intervals[R, 3] - intervals[R, 2]
        a_r += intervals[R, 1] * d
        b_r += d
        y_r = a_r / b_r
        R -= 1
        if (y_r >= intervals[R, 1]) or isclose(y_r, intervals[R, 1]):
            break  
    return y_l, y_r


def WM_algorithm(intervals, params=[]):
    """
    WM algorithm
    
    Parameters
    ----------
    
    intervals:
        numpy (n, 4) array
        
        Y = intervals[:, 0:2]
        
        F = intervals[:, 2:4]
    
    params:
        List
        
        List of parameters of algorithm, if it is needed.
    
    Returns
    -------
    Tuple (l, r)
    """
    intervals = intervals[intervals[:,0].argsort()]
    intervals = trim(intervals)
    
    if intervals is False:
        return 0, 0
    
    F = intervals[:, 2:4]
    Y = intervals[:, 0:2]
    y_l_sup = min(npsum(F[:, 0] * Y[:, 0]) / npsum(F[:, 0]), 
                  npsum(F[:, 1] * Y[:, 0]) / npsum(F[:, 1]))
    y_r_inf = min(npsum(F[:, 1] * Y[:, 1]) / npsum(F[:, 1]), 
                  npsum(F[:, 0] * Y[:, 1]) / npsum(F[:, 0]))
    c = npsum(F[:, 1] - F[:, 0]) / (npsum(F[:, 0]) * npsum(F[:, 1]))
    y_l_inf = y_l_sup - c * (npsum(F[:, 0] * (Y[:, 0] - Y[0, 0])) * 
                             npsum(F[:, 1] * (Y[-1, 0] - Y[:, 0]))) / (npsum(F[:, 0] * (Y[:, 0] - Y[0, 0])) + npsum(F[:, 1] * (Y[-1, 0] - Y[:, 0])))
    y_r_sup = y_r_inf + c * (npsum(F[:, 1] * (Y[:, 1] - Y[0, 1])) * 
                             npsum(F[:, 0] * (Y[-1, 1] - Y[:, 1]))) / (npsum(F[:, 1] * (Y[:, 1] - Y[0, 1])) + npsum(F[:, 0] * (Y[-1, 1] - Y[:, 1])))
    y_l = (y_l_sup + y_l_inf) / 2
    y_r = (y_r_sup + y_r_inf) / 2
    return y_l, y_r


def BMM_algorithm(intervals, params):
    """
    BMM algorithm
    
    Parameters
    ----------
    
    intervals:
        numpy (n, 4) array
        
        Y = intervals[:, 0:2]
        
        F = intervals[:, 2:4]
    
    params:
        List
        
        List of parameters of algorithm, if it is needed.
    
    Returns
    -------
    float
    
    Crisp output
    """
    intervals = intervals[intervals[:,0].argsort()]
    intervals = trim(intervals)
    
    if intervals is False:
        return 0
    
    F = intervals[:, 2:4]
    Y = (intervals[:, 0] + intervals[:, 1]) / 2.
    m = params[0]
    n = params[1]
    #Y = Y.reshape((Y.size,))
    return m * npsum(F[:, 0] * Y) / npsum(F[:, 0]) + n * npsum(F[:, 1] * Y) / npsum(F[:, 1])


def LBMM_algorithm(intervals, params):
    """
    LBMM algorithm (BMM extended by Li et al.)
    
    Ref. An Overview of Alternative Type-ReductionApproaches for 
    Reducing the Computational Costof Interval Type-2 Fuzzy Logic 
    Controllers
    
    Parameters
    ----------
    
    intervals:
        numpy (n, 4) array
        
        Y = intervals[:, 0:2]
        
        F = intervals[:, 2:4]
    
    params:
        List
        
        List of parameters of algorithm, if it is needed.
    
    Returns
    -------
    float
    
    Crisp output
    """
    intervals = intervals[intervals[:,0].argsort()]
    intervals = trim(intervals)
    
    if intervals is False:
        return 0
    
    F = intervals[:, 2:4]
    Y = intervals[:, 0:2]
    m = params[0]
    n = params[1]
    return m * npsum(F[:, 0] * Y[:, 0]) / npsum(F[:, 0]) + n * npsum(F[:, 1] * Y[:, 1]) / npsum(F[:, 1])


def NT_algorithm(intervals, params=[]):
    """
    NT algorithm
    
    Parameters
    ----------
    
    intervals:
        numpy (n, 4) array
        
        Y = intervals[:, 0:2]
        
        F = intervals[:, 2:4]
    
    params:
        List
        
        List of parameters of algorithm, if it is needed.
    
    Returns
    -------
    float
    
    Crisp output
    """
    intervals = intervals[intervals[:,0].argsort()]
    intervals = trim(intervals)
    
    if intervals is False:
        return 0
    
    F = intervals[:, 2:4]
    Y = (intervals[:, 0] + intervals[:, 1]) / 2.
    return (npsum(Y * F[:, 1]) + npsum(Y * F[:, 0])) / (npsum(F[:, 0]) + npsum(F[:, 1]))


def Centroid(it2fs, alg_func, domain, alg_params=[]):
    """
    Centroid type reduction for an interval type 2 fuzzy set.
    
    Parameters
    ----------
    
    it2fs:
        IT2FS
        
        IT2FS which would be type reduced.
    
    alg_func:
        Function
        
        Type reduction algorithm to be used, which is one of these:
            
            KM_algorithm, EKM_algorithm, WEKM_algorithm, TWEKM_algorithm, 
            EIASC_algorithm, WM_algorithm, BMM_algorithm, LBMM_algorithm, and 
            NT_algorithm
    
    domain:
        numpy (n,) shaped array
        
        Indicates the universe of discourse dedicated to the IT2FS.
    
    alg_params:
        List
        
        List of parameters of type reduction algorithm if it is needed.
    
    Returns
    -------
    Based on selected type reduction algorithm tuple (l, r) or float
    
    Returns Centroid type reduction of the input IT2FS.
    """
    intervals = c_[domain, domain, it2fs.lower, it2fs.upper]
    return alg_func(intervals, alg_params)


def CoSet(firing_array, consequent_array, alg_func, domain, alg_params=[]):
    """
    Center of sets type reduction.
    
    Parameters
    ----------
    
    firing_array:
        numpy (m, 2) shaped array
        
        Firing strength of consequents.
    
    consequent_array:
        List of IT2FS
        
        List of consequents corresponding with the rules of IT2FLS
    
    alg_func:
        Function
        
        Type reduction algorithm to be used, which is one of these:
            
            KM_algorithm, EKM_algorithm, WEKM_algorithm, TWEKM_algorithm, 
            EIASC_algorithm, WM_algorithm, BMM_algorithm, LBMM_algorithm, and 
            NT_algorithm
    
    domain:
        numpy (n,) shaped array
        
        Indicates the universe of discourse dedicated to the IT2FS.
    
    alg_params:
        List
        
        List of parameters of type reduction algorithm if it is needed.
    
    Returns
    -------
    Based on selected type reduction algorithm tuple (l, r) or float
    
    Returns Center of sets type reduction of the input IT2FS.
    """
    intervals = []
    for l in range(len(consequent_array)):
        tmp = Centroid(consequent_array[l], alg_func, domain)
        intervals.append([tmp[0], tmp[1], firing_array[l, 0], firing_array[l, 1]])
    return alg_func(array(intervals), alg_params)


def CoSum(it2fs_array, alg_func, domain, alg_params=[]):
    """
    Center of sum type reduction for an interval type 2 fuzzy set.
    
    Parameters
    ----------
    
    it2fs_array:
        List of IT2FSs
        
        List of final IT2FSs achieved by evaluating rule base.
    
    alg_func:
        Function
        
        Type reduction algorithm to be used, which is one of these:
            
            KM_algorithm, EKM_algorithm, WEKM_algorithm, TWEKM_algorithm, 
            EIASC_algorithm, WM_algorithm, BMM_algorithm, LBMM_algorithm, and 
            NT_algorithm
    
    domain:
        numpy (n,) shaped array
        
        Indicates the universe of discourse dedicated to the IT2FS.
    
    alg_params:
        List
        
        List of parameters of type reduction algorithm if it is needed.
    
    Returns
    -------
    Based on selected type reduction algorithm tuple (l, r) or float
    
    Returns Center of sum type reduction of the input IT2FS.
    """
    lower_sum = zeros_like(domain)
    upper_sum = zeros_like(domain)
    for it2fs in it2fs_array:
        add(lower_sum, it2fs.lower, out=lower_sum)
        add(upper_sum, it2fs.lower, out=upper_sum)
    intervals = c_[domain, domain, lower_sum, upper_sum]
    return alg_func(intervals, alg_params)


def Height(it2fs_array, alg_func, domain, alg_params=[]):
    """
    Height type reduction for an interval type 2 fuzzy set.
    
    Parameters
    ----------
    
    it2fs_array:
        List of IT2FSs
        
        List of final IT2FSs achieved by evaluating rule base.
    
    alg_func:
        Function
        
        Type reduction algorithm to be used, which is one of these:
            
            KM_algorithm, EKM_algorithm, WEKM_algorithm, TWEKM_algorithm, 
            EIASC_algorithm, WM_algorithm, BMM_algorithm, LBMM_algorithm, and 
            NT_algorithm
    
    domain:
        numpy (n,) shaped array
        
        Indicates the universe of discourse dedicated to the IT2FS.
    
    alg_params:
        List
        
        List of parameters of type reduction algorithm if it is needed.
    
    Returns
    -------
    Based on selected type reduction algorithm tuple (l, r) or float
    
    Returns Height type reduction of the input IT2FS.
    """
    intervals = []
    for it2fs in it2fs_array:
        index = argmax(it2fs.upper)
        intervals.append([domain[index], domain[index], it2fs.lower[index], it2fs.upper[index]])
    return alg_func(array(intervals), alg_params)


def ModiHe(it2fs_array, spread_array, alg_func, domain, alg_params=[]):
    """
    Modified height type reduction for an interval type 2 fuzzy set.
    
    Parameters
    ----------
    
    it2fs_array:
        List of IT2FSs
        
        List of final IT2FSs achieved by evaluating rule base.
    
    spread_array:
        List of spread values corresponding with IT2FSs in it2fs_array. 
    
    alg_func:
        Function
        
        Type reduction algorithm to be used, which is one of these:
            
            KM_algorithm, EKM_algorithm, WEKM_algorithm, TWEKM_algorithm, 
            EIASC_algorithm, WM_algorithm, BMM_algorithm, LBMM_algorithm, and 
            NT_algorithm
    
    domain:
        numpy (n,) shaped array
        
        Indicates the universe of discourse dedicated to the IT2FS.
    
    alg_params:
        List
        
        List of parameters of type reduction algorithm if it is needed.
    
    Returns
    -------
    Based on selected type reduction algorithm tuple (l, r) or float
    
    Returns Modified height type reduction of the input IT2FS.
    """
    intervals = []
    j = 0
    for it2fs in it2fs_array:
        index = argmax(it2fs.upper)
        intervals.append([domain[index], domain[index],
                          it2fs.lower[index]/(spread_array[j] ** 2),
                          it2fs.upper[index]/(spread_array[j] ** 2)])
        j += 1
    return alg_func(array(intervals), alg_params)


class IT2FLS:
    """Interval type 2 fuzzy logic system.
    
    No construction parameter is needed.
    
    Members
    -------
    inputs:
        List of str
        
        List of names of inputs as str
    
    output:
        List of str
        
        List of names ot outputs as str
        
    rules:
        List of tuples (antecedent, consequent)
        
        List of rules which each rule is defined as a 
        tuple (antecedent, consequent)
        
        Both antacedent and consequent are lists of tuples. Each tuple 
        of this list shows assignement of a variable to an IT2FS. First 
        element of the tuple must be variable name (input or output) as 
        a str and the second element must be an IT2FS. 
    
    Functions
    ---------
    
    add_input_variable:
        
        Adds an input variable to the inputs list of the IT2FLS.
    
    add_output_variable:
        
        Adds an output variable to the outputs list of the IT2FLS.
    
    add_rule:
        
        Adds a rule to the rules list of the IT2FLS.
    
    copy:
        
        Returns a copy of the IT2FLS.
    
    evaluate:
        
        Evaluates the IT2FLS's output for a specified crisp input.
    
    Examples
    --------
    
    Assume that we are going to simulate an IT2FLS with two inputs and 
    two outputs. Each input is defined by three IT2FSs, Small, Medium, 
    and Large. These IT2FSs are from Gaussian type with uncertain 
    standard deviation value. The universe of discourse of the fuzzy 
    system is defined as the interval [0, 1]. Also, the rule base of 
    the system is defined as below:
        
        * IF x1 is Small and x2 is Small THEN y1 is Small and y2 is Large
        * IF x1 is Medium and x2 is Medium THEN y1 is Medium and y2 is Small
        * IF x1 is Large and x2 is Large THEN y1 is Large and y2 is Small
    
    The codes to simulate the aforementioned system using the PyIT2FLS 
    would be as below:
    
    >>> domain = linspace(0., 1., 100)
    >>> 
    >>> Small = IT2FS_Gaussian_UncertStd(domain, [0, 0.15, 0.1, 1.])
    >>> Medium = IT2FS_Gaussian_UncertStd(domain, [0.5, 0.15, 0.1, 1.])
    >>> Large = IT2FS_Gaussian_UncertStd(domain, [1., 0.15, 0.1, 1.])
    >>> IT2FS_plot(Small, Medium, Large, legends=["Small", "Medium", "large"])
    >>> 
    >>> myIT2FLS = IT2FLS()
    >>> myIT2FLS.add_input_variable("x1")
    >>> myIT2FLS.add_input_variable("x2")
    >>> myIT2FLS.add_output_variable("y1")
    >>> myIT2FLS.add_output_variable("y2")
    >>> 
    >>> myIT2FLS.add_rule([("x1", Small), ("x2", Small)], [("y1", Small), ("y2", Large)])
    >>> myIT2FLS.add_rule([("x1", Medium), ("x2", Medium)], [("y1", Medium), ("y2", Small)])
    >>> myIT2FLS.add_rule([("x1", Large), ("x2", Large)], [("y1", Large), ("y2", Small)])
    >>> 
    >>> it2out, tr = myIT2FLS.evaluate({"x1":0.9, "x2":0.9}, min_t_norm, max_s_norm, domain)
    >>> it2out["y1"].plot()
    >>> TR_plot(domain, tr["y1"])
    >>> print(crisp(tr["y1"]))
    >>> 
    >>> it2out["y2"].plot()
    >>> TR_plot(domain, tr["y2"])
    >>> print(crisp(tr["y2"]))
    >>> 
    
    Notes
    -----
    
    While using the PyIT2FLS the user must take care of the items listed below:
        
        * The UMF defined for an IT2FS must be greater than or equal with the LMF at all points of the discrete universe of discourse. 
        * The inputs and outputs defined must be compatible while adding the rules and evluating the IT2FLS.
    """
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.rules = []

    def __repr__(self):
        return "Interval type 2 Mamdani fuzzy logic system!"

    def add_input_variable(self, name):
        """
        Adds new input variable name.
        
        Parameters
        ----------
        
        name:
            str
            
            Name of the new input variable as a str.
        """
        self.inputs.append(name)

    def add_output_variable(self, name):
        """
        Adds new output variable name.
        
        Parameters
        ----------
        
        name:
            str
            
            Name of the new output variable as a str.
        """
        self.outputs.append(name)

    def add_rule(self, antecedent, consequent):
        """
        Adds new rule to the rule base of the IT2FLS.
        
        Parameters
        ----------
        
        antecedent:
            List of tuples
            
            Antecedent is a list of tuples in which each tuple indicates 
            assignement of a variable to an IT2FS. First element of the 
            tuple must be input variable name as str, and the second 
            element of the tuple must be an IT2FS.
            
        consequent:
            List of tuples
            
            Consequent is a list of tuples in which each tuple indicates 
            assignement of a variable to an IT2FS. First element of the 
            tuple must be output variable name as str, and the second 
            element of the tuple must be an IT2FS.
            
        """
        self.rules.append((antecedent, consequent))

    def copy(self):
        """
        Returns a copy of the IT2FLS.
        """
        o = IT2FLS()
        o.inputs = self.inputs.copy()
        o.outputs = self.outputs.copy()
        o.rules = self.rules.copy()
        return o
    
    def evaluate_list(self, inputs, t_norm, s_norm, domain, 
                      method="Centroid", method_params=[], 
                      algorithm="EIASC", algorithm_params=[]):
        """
        Evaluates the IT2FLS based on list of crisp inputs given by user.
        
        Parameters
        ----------
        
        inputs:
            dictionary
            
            Inputs is a dictionary in which the keys are input variable 
            names as str and the values are the list of crisp values 
            corresponded with the inputs to be evaluated.
            
        t_norm:
            function
            
            Indicates the t-norm operator to be used, and should be chosen 
            between min_t_norm, product_t_norm, or other user defined 
            t-norms.
        
        s_norm:
            function
            
            Indicates the s-norm operator to be used, and should be chosen 
            between max_s_norm or other user defined s-norms.
        
        domain:
            numpy (n,) shaped array
            
            Indicates the universe of discourse dedicated to the IT2FS.
        
        method="Centroid":
            str
            
            Indicates the type reduction method name and should be one 
            of the methods listed below:
                Centroid, CoSet, CoSum, Height, and ModiHe.
        
        method_params=[]:
            List
            
            Parameters of the type reduction method, if needed.
        
        algorithm="EIASC":
            Indicates the type reduction algorithm name and should be 
            one of the algorithms listed below:
                KM, EKM, WEKM, TWEKM, EIASC, WM, BMM, LBMM, and NT.
        
        algorithm_params=[]:
            List
            
            Parameters of the type reduction algorithm, if needed.
        
        Returns
        -------
        It depends on which method and algorithm for type reduction is 
        chosen. If Centroid type reduction method is chosen the output 
        is a tuple with two elements. First element is the overall IT2FS 
        outputs of the system as a list of dictionaries with output names as keys 
        and sets as values. The second output is outputs of the 
        selected type reduction algorithm as a list of dictionaries with 
        output names as keys and type reduction algorithm function output 
        as value. For other type reduction methods the only output is a list of  
        dictionaries of the type reduction algorithm function outputs for 
        each output variable name as a key.
        
        Notes
        -----
        
        While using the evaluate function some cares must be taken by the user 
        himself which are listed as below:
            * The inputs must be lay in the defined universe of discourse.
            * The type reduction method and the type reduction algorithm must be selected from the lists provided in docstrings.
        """
        inputs_list = []
        
        l = len(inputs[self.inputs[0]])
        for i in inputs.values():
            if len(i) != l:
                raise ValueError("All input lists must contain same number of values.")
        
        for i in range(l):
            inputs_list.append({})
            for j in self.inputs:
                inputs_list[-1][j] = inputs[j][i]
        
        if algorithm == "KM":
            alg_func = KM_algorithm
        elif algorithm == "EKM":
            alg_func = EKM_algorithm
        elif algorithm == "WEKM":
            alg_func = WEKM_algorithm
        elif algorithm == "TWEKM":
            alg_func = TWEKM_algorithm
        elif algorithm == "WM":
            alg_func = WM_algorithm
        elif algorithm == "LBMM":
            alg_func = LBMM_algorithm
        elif algorithm == "BMM":
            alg_func = BMM_algorithm        
        elif algorithm == "NT":
            alg_func = NT_algorithm       
        elif algorithm == "EIASC":
            alg_func = EIASC_algorithm
        else:
            raise ValueError("The " + algorithm + " algorithm is not implemented, yet!")
        
        outputs = []
        
        if method == "Centroid":
            Cs = []
            TRs = []
            for inputs in inputs_list:
                B = {out: [] for out in self.outputs}
                for rule in self.rules:
                    u = 1
                    l = 1
                    for input_statement in rule[0]:
                        u = t_norm(u, input_statement[1].umf(inputs[input_statement[0]], input_statement[1].umf_params))
                        l = t_norm(l, input_statement[1].lmf(inputs[input_statement[0]], input_statement[1].lmf_params))
                    for consequent in rule[1]:
                        B_l = meet(consequent[1].domain, 
                                   IT2FS(consequent[1].domain, const_mf, [u], const_mf, [l]), 
                                   consequent[1], t_norm)
                        B[consequent[0]].append(B_l)
                C = {out: IT2FS(B[out][0].domain) for out in self.outputs}
                TR = {}
                for out in self.outputs:
                    for B_l in B[out]:
                        C[out] = join(B_l.domain, C[out], B_l, s_norm)
                    TR[out] = Centroid(C[out], alg_func, B_l.domain, alg_params=algorithm_params)
                Cs.append(C)
                TRs.append(TR)
            return Cs, TRs
        elif method == "CoSet":
            for inputs in inputs_list:
                F = []
                G = {out: [] for out in self.outputs}
                for rule in self.rules:
                    u = 1
                    l = 1
                    for input_statement in rule[0]:
                        u = t_norm(u, input_statement[1].umf(inputs[input_statement[0]], input_statement[1].umf_params))
                        l = t_norm(l, input_statement[1].lmf(inputs[input_statement[0]], input_statement[1].lmf_params))
                    F.append([l, u])
                    for consequent in rule[1]:
                        G[consequent[0]].append(consequent[1])
                TR = {}
                for out in self.outputs:
                    TR[out] = CoSet(array(F), G[out], alg_func, 
                                    G[out][0].domain, alg_params=algorithm_params)
                outputs.append(TR)
            return outputs
        elif method == "CoSum":
            for inputs in inputs_list:
                B = {out: [] for out in self.outputs}
                for rule in self.rules:
                    u = 1
                    l = 1
                    for input_statement in rule[0]:
                        u = t_norm(u, input_statement[1].umf(inputs[input_statement[0]], input_statement[1].umf_params))
                        l = t_norm(l, input_statement[1].lmf(inputs[input_statement[0]], input_statement[1].lmf_params))
                    for consequent in rule[1]:
                        B_l = meet(consequent[1].domain, 
                                   IT2FS(consequent[1].domain, const_mf, [u], const_mf, [l]), 
                                   consequent[1], t_norm)
                        B[consequent[0]].append(B_l)
                TR = {}
                for out in self.outputs:
                    TR[out] = CoSum(B[out], alg_func, B[out][0].domain, alg_params=algorithm_params)
                outputs.append(TR)
            return outputs
        elif method == "Height":
            for inputs in inputs_list:
                B = {out: [] for out in self.outputs}
                for rule in self.rules:
                    u = 1
                    l = 1
                    for input_statement in rule[0]:
                        u = t_norm(u, input_statement[1].umf(inputs[input_statement[0]], input_statement[1].umf_params))
                        l = t_norm(l, input_statement[1].lmf(inputs[input_statement[0]], input_statement[1].lmf_params))
                    for consequent in rule[1]:
                        B_l = meet(consequent[1].domain, 
                                   IT2FS(consequent[1].domain, const_mf, [u], const_mf, [l]), 
                                   consequent[1], t_norm)
                        B[consequent[0]].append(B_l)
                TR = {}
                for out in self.outputs:
                    TR[out] = Height(B[out], alg_func, 
                                     B[out][0].domain, alg_params=algorithm_params)
                outputs.append(TR)
            return outputs
        elif method == "ModiHe":
            for inputs in inputs_list:
                B = {out: [] for out in self.outputs}
                for rule in self.rules:
                    u = 1
                    l = 1
                    for input_statement in rule[0]:
                        u = t_norm(u, input_statement[1].umf(inputs[input_statement[0]], input_statement[1].umf_params))
                        l = t_norm(l, input_statement[1].lmf(inputs[input_statement[0]], input_statement[1].lmf_params))
                    for consequent in rule[1]:
                        B_l = meet(consequent[1].domain, 
                                   IT2FS(consequent[1].domain, const_mf, [u], const_mf, [l]), 
                                   consequent[1], t_norm)
                        B[consequent[0]].append(B_l)
                TR = {}
                for out in self.outputs:
                    TR[out] = ModiHe(B[out], method_params, alg_func, 
                                     B[out][0].domain, alg_params=algorithm_params)
                outputs.append(TR)
            return outputs
        else:
            raise ValueError("The method " + method + " is not implemented yet!")
    
    
    def evaluate(self, inputs, t_norm, s_norm, domain, method="Centroid", 
                 method_params=[], algorithm="EIASC", algorithm_params=[]):
        """
        Evaluates the IT2FLS based on crisp inputs given by user.
        
        Parameters
        ----------
        
        inputs:
            dictionary
            
            Inputs is a dictionary in which the keys are input variable 
            names as str and the values are the crisp value of inputs to 
            be evaluated.
            
        t_norm:
            function
            
            Indicates the t-norm operator to be used, and should be chosen 
            between min_t_norm, product_t_norm, or other user defined 
            t-norms.
        
        s_norm:
            function
            
            Indicates the s-norm operator to be used, and should be chosen 
            between max_s_norm or other user defined s-norms.
        
        domain:
            numpy (n,) shaped array
            
            Indicates the universe of discourse dedicated to the IT2FS.
        
        method="Centroid":
            str
            
            Indicates the type reduction method name and should be one 
            of the methods listed below:
                Centroid, CoSet, CoSum, Height, and ModiHe.
        
        method_params=[]:
            List
            
            Parameters of the type reduction method, if needed.
        
        algorithm="EIASC":
            Indicates the type reduction algorithm name and should be 
            one of the algorithms listed below:
                KM, EKM, WEKM, TWEKM, EIASC, WM, BMM, LBMM, and NT.
        
        algorithm_params=[]:
            List
            
            Parameters of the type reduction algorithm, if needed.
        
        Returns
        -------
        It depends on which method and algorithm for type reduction is 
        chosen. If Centroid type reduction method is chosen the output 
        is a tuple with two elements. First element is the overall IT2FS 
        outputs of the system as a dictionary with output names as keys 
        and sets as values. The second output is outputs of the 
        selected type reduction algorithm as a dictionary with 
        output names as keys and type reduction algorithm function output 
        as value. For other type reduction methods the only output is the 
        dictionary of the type reduction algorithm function outputs for 
        each output variable name as a key.
        
        Notes
        -----
        
        While using the evaluate function some cares must be taken by the user 
        himself which are listed as below:
            * The inputs must be lay in the defined universe of discourse.
            * The type reduction method and the type reduction algorithm must be selected from the lists provided in docstrings.
        """
        if algorithm == "KM":
            alg_func = KM_algorithm
        elif algorithm == "EKM":
            alg_func = EKM_algorithm
        elif algorithm == "WEKM":
            alg_func = WEKM_algorithm
        elif algorithm == "TWEKM":
            alg_func = TWEKM_algorithm
        elif algorithm == "WM":
            alg_func = WM_algorithm
        elif algorithm == "LBMM":
            alg_func = LBMM_algorithm
        elif algorithm == "BMM":
            alg_func = BMM_algorithm        
        elif algorithm == "NT":
            alg_func = NT_algorithm       
        elif algorithm == "EIASC":
            alg_func = EIASC_algorithm
        else:
            raise ValueError("The " + algorithm + " algorithm is not implemented, yet!")

        if method == "Centroid":
            B = {out: [] for out in self.outputs}
            for rule in self.rules:
                u = 1
                l = 1
                for input_statement in rule[0]:
                    u = t_norm(u, input_statement[1].umf(inputs[input_statement[0]], input_statement[1].umf_params))
                    l = t_norm(l, input_statement[1].lmf(inputs[input_statement[0]], input_statement[1].lmf_params))
                for consequent in rule[1]:
                    B_l = meet(consequent[1].domain, 
                               IT2FS(consequent[1].domain, const_mf, [u], const_mf, [l]), 
                               consequent[1], t_norm)
                    B[consequent[0]].append(B_l)
            C = {out: IT2FS(B[out][0].domain) for out in self.outputs}
            TR = {}
            for out in self.outputs:
                for B_l in B[out]:
                    C[out] = join(B_l.domain, C[out], B_l, s_norm)
                TR[out] = Centroid(C[out], alg_func, B_l.domain, alg_params=algorithm_params)
            return C, TR
        elif method == "CoSet":
            F = []
            G = {out: [] for out in self.outputs}
            for rule in self.rules:
                u = 1
                l = 1
                for input_statement in rule[0]:
                    u = t_norm(u, input_statement[1].umf(inputs[input_statement[0]], input_statement[1].umf_params))
                    l = t_norm(l, input_statement[1].lmf(inputs[input_statement[0]], input_statement[1].lmf_params))
                F.append([l, u])
                for consequent in rule[1]:
                    G[consequent[0]].append(consequent[1])
            TR = {}
            for out in self.outputs:
                TR[out] = CoSet(array(F), G[out], alg_func, 
                                G[out][0].domain, alg_params=algorithm_params)
            return TR
        elif method == "CoSum":
            B = {out: [] for out in self.outputs}
            for rule in self.rules:
                u = 1
                l = 1
                for input_statement in rule[0]:
                    u = t_norm(u, input_statement[1].umf(inputs[input_statement[0]], input_statement[1].umf_params))
                    l = t_norm(l, input_statement[1].lmf(inputs[input_statement[0]], input_statement[1].lmf_params))
                for consequent in rule[1]:
                    B_l = meet(consequent[1].domain, 
                               IT2FS(consequent[1].domain, const_mf, [u], const_mf, [l]), 
                               consequent[1], t_norm)
                    B[consequent[0]].append(B_l)
            TR = {}
            for out in self.outputs:
                TR[out] = CoSum(B[out], alg_func, 
                                B[out][0].domain, alg_params=algorithm_params)
            return TR
        elif method == "Height":
            B = {out: [] for out in self.outputs}
            for rule in self.rules:
                u = 1
                l = 1
                for input_statement in rule[0]:
                    u = t_norm(u, input_statement[1].umf(inputs[input_statement[0]], input_statement[1].umf_params))
                    l = t_norm(l, input_statement[1].lmf(inputs[input_statement[0]], input_statement[1].lmf_params))
                for consequent in rule[1]:
                    B_l = meet(consequent[1].domain, 
                               IT2FS(consequent[1].domain, const_mf, [u], const_mf, [l]), 
                               consequent[1], t_norm)
                    B[consequent[0]].append(B_l)
            TR = {}
            for out in self.outputs:
                TR[out] = Height(B[out], alg_func, 
                                 B[out][0].domain, alg_params=algorithm_params)
            return TR
        elif method == "ModiHe":
            B = {out: [] for out in self.outputs}
            for rule in self.rules:
                u = 1
                l = 1
                for input_statement in rule[0]:
                    u = t_norm(u, input_statement[1].umf(inputs[input_statement[0]], input_statement[1].umf_params))
                    l = t_norm(l, input_statement[1].lmf(inputs[input_statement[0]], input_statement[1].lmf_params))
                for consequent in rule[1]:
                    B_l = meet(consequent[1].domain, 
                               IT2FS(consequent[1].domain, const_mf, [u], const_mf, [l]), 
                               consequent[1], t_norm)
                    B[consequent[0]].append(B_l)
            TR = {}
            for out in self.outputs:
                TR[out] = ModiHe(B[out], method_params, alg_func, 
                                 B[out][0].domain, alg_params=algorithm_params)
            return TR
        else:
            raise ValueError("The method " + method + " is not implemented yet!")


class IT2TSK:
    """
    Interval type 2 TSK fuzzy logic system.

    Parameters
    ----------
    Parameters of the constructor function:

    t_norm:
        function

        T-norm operator which would be used by FLS.
    
    s_norm:
        function

        S-norm operator which would be used bu FLS.
    
    Members
    -------

    inputs:
        List of str

        List of the inputs name as str.
    
    output:
        List of str
        
        List of the outputs name as str.

    rules:
        List of tuples (antecedent, consequent)
        
        List of rules which each rule is defined as a 
        tuple (antecedent, consequent)
        
        Both antacedent and consequent are lists of tuples. Each tuple 
        of the antacedent list shows assignement of a variable to an IT2FS. 
        First element of the tuple must be the input variable name  
        as a str, and the second element must be an IT2FS. 

        Each tuple of the consequent indicates assignement of a variable to 
        an output state. First element of the tuple must be output vriable 
        name as str, and the second element of the tuple must be a 
        dictionary. This dictionary shows the output polynomial in the case 
        of the rule. For example let an output polynomial be as 
        2 x1 + 4 x2 + 5. Then the dictionary for this case would be 
        {"const":5., "x1":2., "x2":4.}. Note that this is written for an 
        IT2 TSK FLS with two inputs, named x1 and x2.
    

    Functions
    ---------
    
    add_input_variable:
        
        Adds an input variable to the inputs list of the IT2 TSK FLS.
    
    add_output_variable:
        
        Adds an output variable to the outputs list of the IT2 TSK FLS.
    
    add_rule:
        
        Adds a rule to the rules list of the IT2 TSK FLS.
    
    copy:
        
        Returns a copy of the interval type 2 tsk fuzzy logic system.
    
    evaluate:

        Evaluates the IT2 TSK FLS based on the crisp inputs given by the user.

    Notes
    -----
    
    While using the IT2TSK class the user must take care of the items listed below:
        
        * The UMF defined for an IT2FS must be greater than or equal with the LMF at all points of the discrete universe of discourse. 
        * The inputs and outputs defined must be compatible while adding the rules and evluating the IT2FLS.

    """
    def __init__(self, t_norm, s_norm):
        self.inputs = []
        self.outputs = []
        self.rules = []
        self.__t_norm = t_norm
        self.__s_norm = s_norm
        if isThereTypereduction:
            self.algorithm = typereduction.EIASC_algorithm
        else:
            self.algorithm = EIASC_algorithm
    
    def __repr__(self):
        return "Interval type 2 TSK fuzzy logic system!"

    def add_input_variable(self, name):
        """
        Adds new input variable name.
        
        Parameters
        ----------
        
        name:
            str
            
            Name of the new input variable as a str.
        """
        self.inputs.append(name)

    def add_output_variable(self, name):
        """
        Adds new output variable name.
        
        Parameters
        ----------
        
        name:
            str
            
            Name of the new output variable as a str.
        """
        self.outputs.append(name)

    def add_rule(self, antecedent, consequent):
        """
        Adds new rule to the rule base of the IT2FLS.
        
        Parameters
        ----------
        
        antecedent:
            List of tuples
            
            Antecedent is a list of tuples in which each tuple indicates 
            assignement of a variable to an IT2FS. First element of the 
            tuple must be the input variable name as str, and the second 
            element of the tuple must be an IT2FS.
            
        consequent:
            List of tuples
            
            Consequent is a list of tuples in which each tuple indicates 
            assignement of a variable to an output state. First element of the 
            tuple must be output vriable name as str, and the second element 
            of the tuple must be a dictionary. This dictionary shows the 
            output polynomial in the case of the rule. For example let an 
            output polynomial be as 2 x1 + 4 x2 + 5. Then the dictionary for 
            this case would be {"const":5., "x1":2., "x2":4.}. Note that this 
            is written for an IT2 TSK FLS with two inputs, named x1 and x2.
        
        Example
        -------
        
        Assume that we are going to simulate an IT2 TSK FLS with two inputs 
        named x1 and x2. Our rule base is defined as below:
            
            * IF x1 is Small and x2 is Small THEN y1 = x1 + x2 + 1 and y2 = 2 x1 - x2 + 1
            * IF x1 is Small and x2 is Big THEN y1 = 1.5 x1 + 0.5 x2 + 0.5 and y2 = 1.5 x1 - 0.5 x2 + 0.5
            * IF x1 is Big and x2 is Small THEN y1 = 2. x1 + 0.1 x2 - 0.2 and y2 = 0.5 x1 + 0.1 x2
            * IF x1 is Big and x2 is Big THEN y1 = 4. x1 -0.5 x2 - 1 and y2 = -0.5 x1 + x2 - 0.5
        
        Then these rules can be added to the system using the codes below:
        
        >>> myIT2FLS.add_rule([("x1", Small), ("x2", Small)], 
                              [("y1", {"const":1., "x1":1., "x2":1.}), 
                               ("y2", {"const":1., "x1":2., "x2":-1.})])
        >>> myIT2FLS.add_rule([("x1", Small), ("x2", Big)], 
                              [("y1", {"const":0.5, "x1":1.5, "x2":0.5}), 
                               ("y2", {"const":0.5, "x1":1.5, "x2":-0.5})])
        >>> myIT2FLS.add_rule([("x1", Big), ("x2", Small)], 
                              [("y1", {"const":-0.2, "x1":2., "x2":0.1}), 
                               ("y2", {"const":0., "x1":0.5, "x2":0.1})])
        >>> myIT2FLS.add_rule([("x1", Big), ("x2", Big)], 
                              [("y1", {"const":-1., "x1":4., "x2":-0.5}), 
                               ("y2", {"const":-0.5, "x1":-0.5, "x2":1.})])
        
        """
        self.rules.append((antecedent, consequent))
    
    def copy(self):
        """
        Returns a copy of the IT2FLS.
        """
        o = IT2TSK(self.__t_norm, self.__s_norm)
        o.inputs = self.inputs.copy()
        o.outputs = self.outputs.copy()
        o.rules = self.rules.copy()
        return o

    def evaluate(self, inputs):
        """
        Evaluates the IT2 TSK FLS based on the crisp inputs given by the user.

        Parameters
        ----------
        inputs: 
            dictionary
            
            Inputs is a dictionary, which the keys are input variable 
            names as str and the values are the crisp value of the inputs to 
            be evaluated.

        Returns
        -------
        O: 
            dictionary
            
            The output is a dictionary, which the keys are output variable 
            names as str and the values are the crisp output of the system.

        """
        F = []
        B = {out: [] for out in self.outputs}
        for rule in self.rules:
            u = 1
            l = 1
            for input_statement in rule[0]:
                u = self.__t_norm(u, input_statement[1].umf(inputs[input_statement[0]], input_statement[1].umf_params))
                l = self.__t_norm(l, input_statement[1].lmf(inputs[input_statement[0]], input_statement[1].lmf_params))
            F.append([l, u])
            for consequent in rule[1]:
                B[consequent[0]].append(consequent[1]["const"])
                for input in self.inputs:
                    # self.inputs -> Name of the input variables ...
                    # inputs -> Dict of input and value pairs ...
                    # consequent[1] -> dict of input and coefficient pairs ...
                    B[consequent[0]][-1] += consequent[1][input] * inputs[input]
        O = {}
        for output in self.outputs:
            y = array(B[output]).reshape((len(B[output]), 1))
            intervals = hstack([y, y, array(F)])
            o = self.algorithm(intervals)
            O[output] = crisp(o)
        return O

class IT2Mamdani:
    """
    Interval Type 2 Mamadani Fuzzy Logic System.
    
    Parameters
    ----------
    Parameters of the constructor function:
        
    t_norm:
        function
        
        T-norm operator which would be used by FLS.
    
    s_norm:
        function
        
        S-norm operator which would be used by FLS.
    
    method="Centroid":
        str
        
        Indicates the type reduction method name and should be one 
        of the methods listed below:
            Centroid, CoSet, CoSum, Height, and ModiHe.
    
    method_params=[]:
        List
        
        Parameters of the type reduction method, if needed.
    
    algorithm="EIASC":
        str
        
        Indicates the type reduction algorithm name and should be 
        one of the algorithms listed below:
            KM, EKM, WEKM, TWEKM, EIASC, WM, BMM, LBMM, and NT.
    
    algorithm_params=[]:
        List
        
        Parameters of the type reduction algorithm, if needed.
    
    Members
    -------
    
    inputs:
        List of str
        
        List of the inputs name as str.
    
    output:
        List of str
        
        List of the outputs name as str.
        
    rules:
        List of tuples (antecedent, consequent)
        
        List of rules which each rule is defined as a 
        tuple (antecedent, consequent)
        
        Both antacedent and consequent are lists of tuples. Each tuple 
        of these lists shows assignement of a variable to an IT2FS. 
        First element of the tuple must be variable name (input or output) 
        as a str, and the second element must be an IT2FS. 
    
    Functions
    ---------
    
    add_input_variable:
        
        Adds an input variable to the inputs list of the IT2 Mamdani FLS.
    
    add_output_variable:
        
        Adds an output variable to the outputs list of the IT2 Mamdani FLS.
    
    add_rule:
        
        Adds a rule to the rules list of the IT2 Mamdani FLS.
    
    copy:
        
        Returns a copy of the interval type 2 mamdani fuzzy logic system.
    
    evaluate:
        
        Evaluates the IT2FLS's output for a specified crisp input. This function 
        is selected based on the constructor function parameter, method, among 5 
        private functions below:
        __Mamdani_Centroid, __Mamdani_CoSet, __Mamdani_CoSum, __Mamdani_Height, and 
        __Mamdani_ModiHe.
        The only input of the evaluate function is a dictionary named inputs 
        in which the keys are input variable names as str and the values are 
        the crisp value of inputs to be evaluated.
        The output of the evaluate function is depended on the method selected 
        while constructing the class. For more information, please refer to 
        the examples.
    
    Notes
    -----
    
    While using the IT2Mamdani class the user must take care of the items listed below:
        
        * The UMF defined for an IT2FS must be greater than or equal with the LMF at all points of the discrete universe of discourse. 
        * The inputs and outputs defined must be compatible while adding the rules and evluating the IT2FLS.

    """
    def __init__(self, t_norm, s_norm, 
                 method="Centroid", method_params=[], 
                 algorithm="EIASC", algorithm_params=[]):
        self.inputs = []
        self.outputs = []
        self.rules = []
        self.__t_norm = t_norm
        self.__s_norm = s_norm
        self.__method = method
        self.__method_params = method_params
        if algorithm == "KM":
            if isThereTypereduction:
                self.__algorithm = typereduction.KM_algorithm
            else:
                self.__algorithm = KM_algorithm
        elif algorithm == "EKM":
            if isThereTypereduction:
                self.__algorithm = typereduction.EKM_algorithm
            else:
                self.__algorithm = EKM_algorithm
        elif algorithm == "WEKM":
            self.__algorithm = WEKM_algorithm
        elif algorithm == "TWEKM":
            self.__algorithm = TWEKM_algorithm
        elif algorithm == "EIASC":
            if isThereTypereduction:
                self.__algorithm = typereduction.EIASC_algorithm
            else:
                self.__algorithm = EIASC_algorithm
        elif algorithm == "WM":
            if isThereTypereduction:
                self.__algorithm = typereduction.WM_algorithm
            else:
                self.__algorithm = WM_algorithm
        elif algorithm == "BMM":
            self.__algorithm = BMM_algorithm
        elif algorithm == "LBMM":
            self.__algorithm = LBMM_algorithm
        elif algorithm == "NT":
            self.__algorithm = NT_algorithm
        elif callable(algorithm):
            self.__algorithm = algorithm
        else:
            raise ValueError("The algorithm, " + algorithm + ", is not implemented yet!")

        self.__algorithm_params = algorithm_params
        if method == "Centroid":
            self.evaluate = self.__Mamdani_Centroid
        elif method == "CoSet":
            self.evaluate = self.__Mamdani_CoSet
        elif method == "CoSum":
            self.evaluate = self.__Mamdani_CoSum
        elif method == "Height":
            self.evaluate = self.__Mamdani_Height
        elif method == "ModiHe":
            self.evaluate = self.__Mamdani_ModiHe
        else:
            raise ValueError("The method, " + method + ", is not implemented yet!")

    def __repr__(self):
        # TODO!
        pass

    def add_input_variable(self, name):
        """
        Adds new input variable name.
        
        Parameters
        ----------
        
        name:
            str
            
            Name of the new input variable as a str.
        """
        self.inputs.append(name)

    def add_output_variable(self, name):
        """
        Adds new output variable name.
        
        Parameters
        ----------
        
        name:
            str
            
            Name of the new output variable as a str.
        """
        self.outputs.append(name)

    def add_rule(self, antecedent, consequent):
        """
        Adds new rule to the rule base of the IT2FLS.
        
        Parameters
        ----------
        
        antecedent:
            List of tuples
            
            Antecedent is a list of tuples in which each tuple indicates 
            assignement of a variable to an IT2FS. First element of the 
            tuple must be input variable name as str, and the second 
            element of the tuple must be an IT2FS.
            
        consequent:
            List of tuples
            
            Consequent is a list of tuples in which each tuple indicates 
            assignement of a variable to an IT2FS. First element of the 
            tuple must be output variable name as str, and the second 
            element of the tuple must be an IT2FS.
            
        """
        self.rules.append((antecedent, consequent))
    
    def copy(self):
        """
        Returns a copy of the IT2FLS.
        """
        o = IT2Mamdani(self.__t_norm, self.__s_norm, 
                    self.__method, self.__method_params, 
                    self.__algorithm, self.__algorithm_params)
        o.inputs = self.inputs.copy()
        o.outputs = self.outputs.copy()
        o.rules = self.rules.copy()
        return o
    
    def __meet(self, domain, it2fs1, l, u, t_norm):
        umf = lambda x, params: t_norm(it2fs1.umf(x, it2fs1.umf_params), u)
        lmf = lambda x, params: t_norm(it2fs1.lmf(x, it2fs1.lmf_params), l)
        it2fs = IT2FS(domain, umf, [], lmf, [])
        return it2fs
    
    def __join(self, domain, it2fs1, l, u, s_norm):
        umf = lambda x, params: s_norm(it2fs1.umf(x, it2fs1.umf_params), u)
        lmf = lambda x, params: s_norm(it2fs1.lmf(x, it2fs1.lmf_params), l)
        it2fs = IT2FS(domain, umf, [], lmf, [])
        return it2fs
    
    def __Mamdani_Centroid(self, inputs):
        B = {out: [] for out in self.outputs}
        for rule in self.rules:
            u = 1
            l = 1
            for input_statement in rule[0]:
                u = self.__t_norm(u, input_statement[1].umf(inputs[input_statement[0]], input_statement[1].umf_params))
                l = self.__t_norm(l, input_statement[1].lmf(inputs[input_statement[0]], input_statement[1].lmf_params))
            for consequent in rule[1]:
                B_l = self.__meet(consequent[1].domain, consequent[1], l, u, self.__t_norm)
                B[consequent[0]].append(B_l)
        C = {out: IT2FS(B[out][0].domain) for out in self.outputs}
        TR = {}
        for out in self.outputs:
            for B_l in B[out]:
                C[out] = join(B_l.domain, C[out], B_l, self.__s_norm)
            TR[out] = Centroid(C[out], self.__algorithm, B_l.domain, 
                               alg_params=self.__algorithm_params)
        return C, TR
    
    def __Mamdani_CoSet(self, inputs):
        F = []
        G = {out: [] for out in self.outputs}
        for rule in self.rules:
            u = 1
            l = 1
            for input_statement in rule[0]:
                u = self.__t_norm(u, input_statement[1].umf(inputs[input_statement[0]], input_statement[1].umf_params))
                l = self.__t_norm(l, input_statement[1].lmf(inputs[input_statement[0]], input_statement[1].lmf_params))
            F.append([l, u])
            for consequent in rule[1]:
                G[consequent[0]].append(consequent[1])
        TR = {}
        for out in self.outputs:
            TR[out] = CoSet(array(F), G[out], self.__algorithm, 
                            G[out][0].domain, alg_params=self.__algorithm_params)
        return TR
    
    def __Mamdani_CoSum(self, inputs):
        B = {out: [] for out in self.outputs}
        for rule in self.rules:
            u = 1
            l = 1
            for input_statement in rule[0]:
                u = self.__t_norm(u, input_statement[1].umf(inputs[input_statement[0]], input_statement[1].umf_params))
                l = self.__t_norm(l, input_statement[1].lmf(inputs[input_statement[0]], input_statement[1].lmf_params))
            for consequent in rule[1]:
                B_l = meet(consequent[1].domain, consequent[1], l, u, self.__t_norm)
                B[consequent[0]].append(B_l)
        TR = {}
        for out in self.outputs:
            TR[out] = CoSum(B[out], self.__algorithm, 
                            B[out][0].domain, alg_params=self.__algorithm_params)
        return TR
    
    def __Mamdani_Height(self, inputs):
        B = {out: [] for out in self.outputs}
        for rule in self.rules:
            u = 1
            l = 1
            for input_statement in rule[0]:
                u = self.__t_norm(u, input_statement[1].umf(inputs[input_statement[0]], input_statement[1].umf_params))
                l = self.__t_norm(l, input_statement[1].lmf(inputs[input_statement[0]], input_statement[1].lmf_params))
            for consequent in rule[1]:
                B_l = self.__meet(consequent[1].domain, consequent[1], l, u, self.__t_norm)
                B[consequent[0]].append(B_l)
        TR = {}
        for out in self.outputs:
            TR[out] = Height(B[out], self.__algorithm, 
                             B[out][0].domain, alg_params=self.__algorithm_params)
        return TR
    
    def __Mamdani_ModiHe(self, inputs):
        B = {out: [] for out in self.outputs}
        for rule in self.rules:
            u = 1
            l = 1
            for input_statement in rule[0]:
                u = self.__t_norm(u, input_statement[1].umf(inputs[input_statement[0]], input_statement[1].umf_params))
                l = self.__t_norm(l, input_statement[1].lmf(inputs[input_statement[0]], input_statement[1].lmf_params))
            for consequent in rule[1]:
                B_l = self.__meet(consequent[1].domain, consequent[1], l, u, self.__t_norm)                           
                B[consequent[0]].append(B_l)
        TR = {}
        for out in self.outputs:
            TR[out] = ModiHe(B[out], self.__method_params, self.__algorithm, 
                             B[out][0].domain, alg_params=self.__algorithm_params)
        return TR
    
    
TSK = IT2TSK

Mamdani = IT2Mamdani


