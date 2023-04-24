Here is the outline from the talk proposal:

* A motivating example, adding array API standard usage to a real-world scientific data analysis script so it runs with CuPy and PyTorch in addition to NumPy.
* History of the Data APIs Consortium and array API specification.
* The scope and general design principles of the specification.
* Current status of implementations:
    * Two versions of the standard have been released, 2021.12 and 2022.12.
    * The standard includes all important core array functionality and extensions for linear algebra and Fast Fourier Transforms.
    * NumPy and CuPy have complete reference implementations in submodules (numpy.array_api).
    * NumPy, CuPy, and PyTorch have near full compliance and have plans to approach full compliance
    * array-api-compat is a wrapper library designed to be vendored by consuming libraries like scikit-learn that makes NumPy, CuPy, and PyTorch use a uniform API.
    * The array-api-tests package is a rigorous and complete test suite for testing against the array API and can be used to determine where an array API library follows the specification and where it doesn’t.
* Future work
    * Add full compliance to NumPy, as part of NumPy 2.0.
    * Focus on improving adoption by consuming libraries, such as SciPy and scikit-learn.
    * Reporting website that lists array API compliance by library.
    * Work is being done to create a similar standard for dataframe libraries. This work has already produced a common dataframe interchange API.
