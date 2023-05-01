=========================
 Array API Specification
=========================

Abstract
========


Introduction
============

History of the Consortium
=========================

Goals and Non-Goals
===================

The array API specification has the following goals:

- Make it possible for array-consuming libraries to start using multiple
  types of arrays as inputs.

- Enable more sharing and reuse of code built on top of the core
  functionality in the API standard.

- For authors of new array libraries, provide a concrete API that can be
  adopted as is, rather than each author having to decide what to borrow
  from where and where to deviate.

- Make the learning curve for users less steep when they switch from one
  array library to another one.

Additionally, the specification has several non-goals:

- Making array libraries identical so they can be merged. Each library will
  keep having its own particular strength, whether it's offering functionality
  beyond what's in the standard, performance advantages for a given use case,
  specific hardware or software environment support, or more.

- Implement a backend or runtime switching system to be able to switch from
  one array library to another with a single setting or line of code. This may
  be feasible, however it’s assumed that when an array-consuming library
  switches from one array type to another, some testing and possibly code
  adjustment for performance or other reasons may be needed.

- Making it possible to mix multiple array libraries in function calls. Most
  array libraries do not know about other libraries, and the functions they
  implement may try to convert "foreign" input, or raise an exception. This
  behavior is hard to specify. It is better to require the end-user to use a
  single array library that best fits their needs. Note that specification of
  an interchange protocol is within scope, but interchange between array
  libraries is only done explicitly in the specification.

Design Principles
=================

The array API standard has been developed with several design principles in
mind. The most important principle is that the standard only specifies
behavior that is already widely supported by most existing array libraries.
The goal is to minimize the number of backwards incompatible changes required
for libraries to support the specification. This in particular leaves many
things out of scope if they are not already supported by all major array
libraries.

The standard has been developed with following core principles:

* APIs should support accelerators. This means not either not specifying or
  making optional behaviors that are difficult to implement performantly.

* In a similar vein, APIs should support JIT compilers. For example, the type
  of any function's output should only depend on the types of the inputs.

* No value-based casting. The output data type of any function or
  operation should depend only on the input data type(s), not the array
  values.

* No dimension dependent casting. The output data type of any function or
  operation should function independently of the input array dimensionality.
  This also means that 0-D arrays are fully supported. Scalars as a separate
  concept are not specified.

* Functions that can easily be implemented in terms of existing standardized
  functions do not necessarily need to be standardized.

* Copy-view behavior and mutability is not required. Array libraries may
  implement mutation but the behavior of in-place mutation with views is not
  guaranteed by the spec. The `out` keyword is omitted from API definitions.

* Functions with data-dependent output shapes are optional, since Graph-based
  libraries like JAX and Dask cannot easily support them. This includes
  boolean indexing, `nonzero()`, and the `unique_*` functions.

* Type annotations are defined in a basic way in the spec, but libraries may
  extend them. Input types are designed to be simple. For example, functions
  are only required to accept `array` objects. Accepting "array like" types
  like lists of numbers, as NumPy does, is problematic because it complicates
  type signatures, and calling `asarray()` at the top of every function adds
  additional overhead. However, these type signatures are not strict:
  libraries may choose to accept additional input types outside of those that
  are specified.

* The accuracy and precision of numerical functions are not specified beyond
  very basic IEEE 754 rules.

Scope
=====

The scope of the array API specification includes:

- Functionality which needs to be included in an array library for it to
  adhere to this standard.
- Names of functions, methods, classes and other objects.
- Function signatures, including type annotations.
- Semantics of functions and methods, i.e., expected outputs and dtypes of
  numerical results.
- Semantics in the presence of `nan`'s, `inf`'s, and empty arrays (i.e. arrays
  including one or more dimensions of size `0`).
- Casting rules, broadcasting, and indexing.
- Data interchange. i.e., protocols to convert one type of array into another
  type, potentially sharing memory.
- Device support.

To contrast, the following are considered **out of scope** for the array API
specification

- Implementations of the standard are out of scope. Members of the consortium
  have played a role in helping libraries like NumPy, CuPy, and PyTorch
  implement the standard, but this work has been done independently of the
  standard. In particular, the standard is completely independent of any
  specific implementation and does not make reference to or depend on any
  given implementation or Python library (the `array-api-compat` library has
  been produced as a compatibility layer on top of array libraries such as
  NumPy, CuPy, and PyTorch, but this library is provided only as a helper tool
  for array consumer libraries. It is not in any way required to make use of
  the array API).

- Execution semantics are out of scope. This includes single-threaded vs.
  parallel execution, task scheduling and synchronization, eager vs. delayed
  evaluation, performance characteristics of a particular implementation of
  the standard, and other such topics.

- Non-Python API standardization (e.g., Cython or NumPy C APIs).

- Standardization of dtypes not already supported by all existing array
  libraries is out of scope. This includes bfloat16, extended precision
  floating point, datetime, string, object and void dtypes.

- The following topics are out of scope: I/O, polynomials, error handling,
  testing routines, building and packaging related functionality, methods of
  binding compiled code (e.g., `cffi`, `ctypes`), subclassing of an array
  class, masked arrays, and missing data.

- NumPy (generalized) universal functions, i.e. ufuncs and gufuncs.

- Behavior for unexpected/invalid input to functions and methods.

For out-of-scope behavior, array libraries are free to implement or to raise
an error. It is up to array consuming libraries to ensure they write portable
code that doesn't depend on behaviors outside of the specification. The
`numpy.array_api` implementation, discussed below, can be a useful tool for
this.

Features
========

Current Status of Implementations
=================================

Future Work
===========
