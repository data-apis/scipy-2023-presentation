Here is the outline from the talk proposal:

* A motivating example, adding array API standard usage to a real-world
  scientific data analysis script so it runs with CuPy and PyTorch in addition
  to NumPy. (https://github.com/data-apis/scipy-2023-presentation/issues/2)

* History of the Data APIs Consortium and array API specification.
  * Q2 2020: Consortium formed
  * Q3 2020: Consortium publicly announced
  * Q2-Q3 2020: standard methodology and tooling developed
  * Q4 2020: First array API RFC published
  * Q1 2021: NEP 47 published
  * Q3 2021: RFC for dataframe interchange protocol published
  * Q4 2021: Array API v2021.12 published
  * Q4 2021: NumPy 1.21 released with numpy.array_api
  * Q1 2022: First release or array API testsuite
  * Q4 2022: Array API v2022.12 published
  * Q1 2023: array-api-compat released
  * Q2 2023: First scikit-learn APIs supporting array API merged

* The scope and general design principles of the specification.
  * Scope (copied from standard):

    - Functionality which needs to be included in an array library for it to adhere
      to this standard.
    - Names of functions, methods, classes and other objects.
    - Function signatures, including type annotations.
    - Semantics of functions and methods. I.e. expected outputs including precision
      for and dtypes of numerical results.
    - Semantics in the presence of `nan`'s, `inf`'s, empty arrays (i.e. arrays
      including one or more dimensions of size `0`).
    - Casting rules, broadcasting, indexing
    - Data interchange. I.e. protocols to convert one type of array into another
      type, potentially sharing memory.
    - Device support.

    Furthermore, meta-topics included in this standard include:

    - Use cases for the API standard and assumptions made in it
    - API standard adoption
    - API standard versioning
    - Future API standard evolution
    - Array library and API standard versioning
    - Verification of API standard conformance

  * Out of scope (copied from standard, note standard also has rationales for
    all of these https://data-apis.org/array-api/latest/purpose_and_scope.html#out-of-scope)

    1. Implementations of the standard are out of scope.

    2. Execution semantics are out of scope. This includes single-threaded vs.
       parallel execution, task scheduling and synchronization, eager vs. delayed
       evaluation, performance characteristics of a particular implementation of the
       standard, and other such topics.

    3. Non-Python API standardization (e.g., Cython or NumPy C APIs)

    4. Standardization of these dtypes is out of scope: bfloat16, complex, extended
       precision floating point, datetime, string, object and void dtypes.

    5. The following topics are out of scope: I/O, polynomials, error handling,
       testing routines, building and packaging related functionality, methods of
       binding compiled code (e.g., `cffi`, `ctypes`), subclassing of an array
       class, masked arrays, and missing data.

    6. NumPy (generalized) universal functions, i.e. ufuncs and gufuncs.

    7. Behavior for unexpected/invalid input to functions and methods.

  * Goals (copied from standard)

    - Make it possible for array-consuming libraries to start using multiple types
      of arrays as inputs.
    - Enable more sharing and reuse of code built on top of the core functionality
      in the API standard.
    - For authors of new array libraries, provide a concrete API that can be
      adopted as is, rather than each author having to decide what to borrow from
      where and where to deviate.
    - Make the learning curve for users less steep when they switch from one array
      library to another one.

  * Non-goals (copied from standard. Note standard also has rationales)

    - Making array libraries identical so they can be merged.

    - Implement a backend or runtime switching system to be able to switch from one
      array library to another with a single setting or line of code.

    - Making it possible to mix multiple array libraries in function calls.

  * Design principles

    * APIs should support accelerators

    * APIs should support JIT compilers (e.g., the type of the output should
      only depend on the types of the inputs)

    * Only specify behavior that is already widely supported by most existing
      array libraries.

    * No value-based casting. The output data type of any function or
      operation should depend only on the input data type(s), not the array values.

    * No dimension dependent casting. The output data type of any function or
      operation should function independently of the input array
      dimensionality. This also means that 0-D arrays are fully supported.
      Scalars as a separate concept are not specified.

    * Functions that can easily be implemented in terms of existing
      standardized functions to not necessarily need to be standardized.

    * Copy-view behavior and mutability. Array libraries may implement
      mutation but the behavior of in-place mutation with views is not
      guaranteed by the spec. The `out` keyword is omitted from API
      definitions.

    * Data-dependent output shapes. Since graph-based libraries (JAX, Dask) cannot easily
      implement them support is optional. Functions: boolean indexing,
      `nonzero`, and `unique_*`.

    * Static typing. Type annotations are defined in a basic way in the spec,
      but libraries may extend. Input types are designed to be simple (e.g.,
      functions only accept `array`, not `array_like`).

    * Accuracy: not specified beyond very basic IEEE 754 rules

    * Complex numbers (XXX: probably don't need to discuss this in too much
      detail. The important bits are already covered by other sections)

* Features

    * Data Interchange mechanism

    * Device support

    * Functions and methods

      * API is functional (only a few attributes on array object + operators)

      * Focus is on functions implemented by most array libraries and found to
        be used heavily in usage data.

      * Positional-only and keyword-only arguments

      * Most APIs are identical to `numpy`.

      * Highlight a few key breaks from NumPy (e.g., `transpose`)

    * Broadcasting

    * Indexing

    * Type promotion.

      * Only certain dtypes are defined but libraries can define
      others.

      * Type promotion should not depend on array *values* or
        *dimensionalities*.

      * Cross kind promotion is not defined (but libraries may choose to
        implement anyway).

      * Python scalars are only defined for array operators. Scalars are cast
        to the array dtype. Cross-kind promotion is allowed in this specific
        instance (e.g., `float64_array + 1`).

    * Extensions

      * Linear algebra

      * FFT

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
