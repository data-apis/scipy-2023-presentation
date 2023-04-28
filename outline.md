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

    * Extensions (optional)

      * Linear algebra

      * FFT

* Current status of implementations:

    * Two versions of the standard have been released, 2021.12 and 2022.12.
      * 2021.12 is usable subset of array functionalities.
      * 2022.12 highlights are complex number support and fft extension.

    * The standard includes all important core array functionality and
      extensions for linear algebra and Fast Fourier Transforms.

      * Somehow list all functions? (can do for talk. Not sure about paper)

    * NumPy and CuPy have complete reference implementations in submodules
      (numpy.array_api).

      * numpy.array_api is a standalone, **strict** implementation of the
        standard (meaning functionality that is not guaranteed by the spec
        raises an exception). It uses a separate Array object from np.ndarray.
        It's not to be used by end users, but rather by libraries to test that
        their array API usage is portable.

      * cupy.array_api is similar

    * NumPy, CuPy, and PyTorch have near full compliance and have plans to
      approach full compliance

      * NumPy 2.0 (to be released late 2023), will have full array API
        compliance, including some breaking changes.

      * CuPy will follow NumPy.

      * PyTorch has open issues to address any dependencies between array
        API.

    * array-api-compat is a wrapper library designed to be vendored by
      consuming libraries like scikit-learn that makes NumPy, CuPy, and
      PyTorch use a uniform API.

      * To be used by array consumer libraries like scipy or scikit-learn.

      * `import array_api_compat.numpy as np` is just like NumPy except all
        array API functions are wrapped to ensure full spec compliance.

      * Non-spec functions are also included in the compat (there are no
        strictness constraints, unlike with `numpy.array_api`).

      * Primary usage is like

        ```py
        from array_api_compat import array_namespace

        def your_function(x, y):
            xp = array_api_compat.array_namespace(x, y)
            # Now use xp as the array library namespace
            return xp.mean(x, axis=0) + 2*xp.std(y, axis=0)
        ```

      * Supports vendoring. No hard dependencies.

      * Compat wrappers for NumPy, CuPy, and PyTorch. Support for other
        libraries planned (JAX, Dask, ...)

      * Currently successfully used in scikit-learn's
        `LinearDiscriminantAnalysis` API
        (https://github.com/scikit-learn/scikit-learn/pull/22554)

        * TODO: Get benchmarks from Thomas

    * The array-api-tests package is a rigorous and complete test suite for
      testing against the array API and can be used to determine where an
      array API library follows the specification and where it doesn’t.

      * All behavior specified by the spec is rigorously tested.

      * Implemented with pytest + hypothesis. Test cases are generated
        automatically to ensure all corner cases are tested.
        `hypothesis.extra.array_api` has been implemented to support
        generating array for any array API compatible library.

      * First known example of a full featured Python test suite that
        functions against multiple different libraries.

* Future work

    * Add full compliance to NumPy, as part of NumPy 2.0.

      * Planned for late 2023.

      * NumPy development team is fully on board, including breaking changes.

      * NEP 50 fixes type promotion issues (no more value-based casting).

      * Will also use opportunity to apply spec principles to non-specified
        functions (e.g., using positional-only arguments throughout the NumPy
        API).

    * Focus in 2023 is on improving adoption by consuming libraries, such as
      SciPy and scikit-learn.

      * SciPy 2.0 discussion for fully supporting array API.
        https://github.com/scipy/scipy/issues/18286

      * Scikit-learn added support to `LinearDiscriminantAnalysis`. More
        functions planned.

    * Reporting website that lists array API compliance by library.

      * TODO (Athan)

    * Work is being done to create a similar standard for dataframe libraries.
      This work has already produced a common dataframe interchange API.

      * [Minimal to no discussion of this in paper. One slide for talk]
