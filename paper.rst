.. Make single backticks produce code
.. default-role:: code

:author: Aaron Meurer
:email: asmeurer@quansight.com
:institution: Quansight

===========================================================================================
Python Array API Standard: Toward Array Interoperability in the Scientific Python Ecosystem
===========================================================================================

.. TODO: Does the abstract have a word or character limit?

.. class:: abstract

   The Python array API standard (https://data-apis.org/array-api/) specifies
   standardized application programming interfaces (APIs) and behavior for
   array and tensor objects and operations as commonly found in libraries such
   as NumPy, PyTorch, TensorFlow, Dask, and CuPy (TODO: citations). The
   establishment and subsequent adoption of the standard aims to reduce
   ecosystem fragmentation and facilitate array library interoperability in
   user code and among array-consuming libraries, such as scikit-learn and
   SciPy (TODO: citations). A key benefit of array interoperability for
   downstream consumers of the standard is device agnosticism, whereby
   previously CPU-bound implementations can more readily leverage hardware
   acceleration via graphics processing units (GPUs), tensor processing units
   (TPUs), and other accelerator devices.

   In this paper, we first introduce the Consortium for Python Data API
   standards and define the scope of the array API standard. We then discuss
   the current status of standardization and associated tooling (including a
   library-independent test suite and compatibility layer). We conclude by outlining
   plans for future work.

.. class:: keywords

   Python, Arrays, Tensors, NumPy, CuPy, PyTorch, JAX, Dask

Introduction
============

Today, Python users have a wealth of choice for libraries and frameworks for
numerical computing, data science, machine learning, and deep learning (TODO: citations). New
frameworks pushing forward the state of the art in these fields appear every
year. One unintended consequence of all this activity has been fragmentation in
the fundamental building blocks—multidimensional arrays (TODO: van der walt citation) (also known as tensors)—that
underpin the scientific Python ecosystem.

This fragmentation comes with significant costs, from reinvention and re-implementation
of arrays and associated application programming interfaces (APIs) to siloed
technical stacks targeting only one array library to the proliferation of user
guides providing guidance on how to convert between, and interoperate among,
libraries. Too often, the APIs of each library are largely similar, but each
have enough differences that end users have to relearn and rewrite code in
order to work with multiple libraries. This process can be very painful as the
transition is far from seamless.

.. TODO: Consider inserting Figure 2 from Year 1 report

The Consortium for Python Data API Standards (hereafter referred to as "the
Consortium" and "we") aims to address this problem by standardizing a fundamental array
data structure and an associated set of common APIs for working with arrays,
thus facilitating interchange and interoperability.

Paper Overview
==============

This paper is written as an introduction to the Consortium and the array API
standard. The aim is to provide a high-level overview of the standard and its
continued evolution and to solicit further engagement from the Python
community.

After providing an overview of the Consortium, we first discuss standardization
methodology. We then discuss the current status of the array API standard and
highlight the main standardization areas. Next, we introduce tooling
associated with the standard for testing compliance and shimming incompatible
array library behavior. We conclude by outlining open questions and
opportunities for further standardization. Links to the specification and all
current repository artifacts, including associated tooling, can be found in the
bibliography.

Consortium Overview
===================

History
-------

While the Python programming language was not designed for numerical computing,
the language gained initial popularity in the scientific and engineering
community soon after its release. The first array computing library for
numerical and scientific computing in Python was Numeric, developed in the mid-1990s (TODO: citation).
To better accommodate this library and its use cases, Python’s syntax was
extended to include indexing syntax (TODO: PEP citation).

In the early 2000s, a similar library, Numarray, introduced a more flexible
data structure (TODO: citation). Numarray had faster operations for large
arrays. However, the library was slower for small arrays. Subsequently, both
Numeric and Numarray coexisted to satisfy different use cases.

In early 2005, NumPy was written to unify Numeric and Numarray as a single
array package by porting Numarray’s features to Numeric (TODO: citation). This
effort was largely successful and resolved the fragmentation at the time, and,
for roughly a decade, NumPy was the only widely used array library. Building on
NumPy, pandas was subsequently introduced in 2008 in order to address the need
for a high performance, flexible tool for performing quantitative analysis on
labeled tabular data (TODO: citation).

Over the past 10 years, the rise of deep learning and the emergence of new
hardware has led to a proliferation of new libraries and a corresponding
fragmentation within the PyData array and dataframe ecosystem. These libraries
often borrowed concepts from, or entirely copied, the APIs of older libraries,
such as NumPy, and then modified and evolved those APIs to address new needs
and use cases. While the communities of each individual library discussed
interchange and interoperability, until the founding of the Consortium for
Python Data API Standards, no process for coordination among libraries arose to
avoid further fragmentation and to arrive at a common set of API standards.

.. TODO: consider inserting Figure 1 from year 1 report

The genesis for the Consortium grew out of many conversations among maintainers
during 2019-2020. During those conversations, it quickly became clear that any
attempt to write a new reference library to fix the current fragmentation was
infeasible. Unlike in 2005, too many different use cases and varying
stakeholders now exist. Furthermore, the speed of innovation of both hardware
and software is simply too great.

In May 2020, an initial group of maintainers and industry stakeholders assembled
to form the Consortium for Python Data API Standards to begin drafting
specifications for array and dataframe APIs, which could then be adopted by each
of the existing array and dataframe libraries and by any new libraries which arise.

Objectives
----------

Standardization efforts must maintain a delicate balance between codifying what
already exists and maintaining relevance with respect to future innovation. The
latter aspect is particularly fraught, as relevance requires anticipating
future needs, technological advances, and emerging use cases. Accordingly, if a
standard is to remain relevant, the standardization process must be
conservative in its scope, thorough in its consideration of current and prior
art, and have clearly defined objectives against which continued success is
measured.

To this end, we established the following objectives for the array API standard:

- Increase interoperability such that array-consuming libraries can accept and
  operate on any specification-conforming array library.

- Reduce reinvention and facilitate code sharing and reuse by establishing a
  common set of standardized APIs and behavior.

- Reduce barriers to new array library creation by providing a set of APIs which
  can be adopted as is.

- Reduce the learning curve and friction for users as they switch between array
  libraries.

Notably, of equal importance to the aforementioned objectives is the explicit
omission of the following:

- Make array libraries identical for the purpose of merging them. Different array
  libraries have different strengths (e.g., performance characteristics, hardware
  support, and tailored use cases, such as deep learning), and merging into a
  single array library is neither practical nor realistic.

- Implement a backend or runtime switching system in order to switch from
  one array library to another via a single setting or line of code. While
  potentially feasible, array consumers are likely to need to modify code in
  order to ensure optimal performance and behavior.

- Support mixing multiple array libraries in function calls. Mixing array
  libraries requires defining hierarchies and specifying rules for device
  synchronization and data localization. Such rules are likely to be specific to
  individual use cases and beyond the scope of the array API standard.

Design Principles
-----------------

In order to guide standardization and define the contours of the standardization
process, we further established the following design principles:

**Pure functions.** Functional API design is the dominant pattern among array
libraries, both in Python and in other frequently used programming languages
supporting array computation (e.g., MATLAB (TODO: citation) and Julia (TODO: citation)).
While method chaining and the fluent interface design pattern are relatively
common, especially among array libraries supporting lazy evaluation and
operator fusion, functional APIs are generally preferred, mirroring design
patterns used in underlying implementations, such as those written in C/C++
and Fortran.

**Minimal array object.** A standardized array object should have a minimal set
of attributes necessary for inspection (e.g., shape, data type, size, etc.)
and should have a minimal set of magic methods (a.k.a. "dunder" methods) to
support operator overloading.

**No dependencies.** The array API standard and its implementation should be
possible in pure Python, without the need for any external dependency outside
of Python itself.

**Accelerator support.** Standardized APIs and behavior should be possible to
implement for both central processing units (CPUs) and hardware-accelerated
devices, such as graphics processing units (GPUs), tensor processing units (TPUs),
and field-programmable gate arrays (FPGAs).

**JIT compiler support.** Standardized APIs and behavior should be amenable to
just-in-time (JIT) compilation and graph-based optimization (e.g., PyTorch (TODO: citation),
JAX (TODO: citation), and TensorFlow (TODO: citation)). For APIs and behavior
which are not amenable, such as APIs returning arrays having data-dependent
output shapes, the respective APIs and behavior should be specified as
optional extensions. Moreover, copy-view mutation semantics (as, e.g.,
supported by NumPy) should be considered an implementation detail and, thus,
not suitable for standardization.

**Distributed support.** Standardized APIs and behavior should be amenable to
implementation in array libraries supporting distributed computing (e.g., Dask (TODO: citation)).

**Consistency.** Except in scenarios involving backward compatibility concerns,
naming conventions and design patterns should be consistent across
standardized APIs.

**Extensibility.** Conforming array libraries may implement functionality which
is not included in the array API standard. As a consequence, array consumers
should bear responsibility for ensuring that a given API is standardized and its
usage is portable across specification-conforming array libraries.

**Deference.** Where possible, the array API standard should defer to existing,
widely-used standards. For example, the accuracy and precision of numerical
functions should not be specified beyond the guidance included in IEEE 754 (TODO: citation).

**Universality.** Standardized APIs and behavior should reflect common usage
among a wide range of existing array libraries. Accordingly, with rare
exception, only APIs and behavior having prior art within the ecosystem may
be considered candidates for standardization.


Methods
=======

A foundational step in technical standardization is articulating a subset of
established practices and defining those practices in unambiguous terms. To
this end, the standardization process must approach the problem from two
directions: design and usage.

The former direction seeks to understand both current implementation design
(e.g., APIs, names, signatures, classes, and objects) and semantics (calling
conventions and behavior). The latter direction seeks to quantify API consumers
(e.g., who are the downstream users of a given API?), usage frequency (e.g.,
how often is an API consumed?), and consumption patterns (e.g., which optional
arguments are provided and in what context?). By analyzing both design and
usage, we sought to ground the standardization process and specification
decisions in empirical data and analysis.

Design
------

To understand API design of array libraries within the SPE, we first identified
a representative sample of commonly used Python array libraries. The sample included
the following libraries: NumPy, Dask Array, CuPy, MXNet, JAX, TensorFlow, and PyTorch.
Next, we extracted public APIs for each library by analyzing module exports and
scraping public web documentation. As an example of extracted API data, consider
the following APIs for computing the arithmetic mean.

.. TODO: line wrapping makes this block harder to grok, especially when inferring common kwargs; consider an alternative presentation

.. code:: python

   numpy.mean(a, axis=None, dtype=None, out=None,
       keepdims=<no value>)
   cupy.mean(a, axis=None, dtype=None, out=None,
       keepdims=False)
   dask.array.mean(a, axis=None, dtype=None, out=None,
       keepdims=False, split_every=None)
   jax.numpy.mean(a, axis=None, dtype=None, out=None,
       keepdims=False)
   mxnet.np.mean(a, axis=None, dtype=None, out=None,
       keepdims=False)
   tf.math.reduce_mean(input_tensor, axis=None,
       keepdims=False, name=None)
   torch.mean(input, dim, keepdim=False, out=None)

We then standardized the representation of the extracted public API data for
subsequent analysis and joined individual table data using NumPy as our
reference relation. From the unified representation, we determined
commonalities and differences by analyzing the intersection, and its
complement, of available APIs across each array library. From the intersection,
we derived a subset of common APIs suitable for standardization based on
prevalence and ease of implementation. The common API subset included function
names, method names, attribute names, and positional and keyword arguments.
As an example of a derived API, consider the common API for computing the
arithmetic mean:

.. code:: python

   mean(a, axis=None, keepdims=False)

To assist in determining standardization prioritization, we leveraged usage
data (discussed below) to confirm API need and to inform naming conventions,
supported data types, and optional arguments. We have summarized findings and
published tooling (TODO: repo citation) for additional analysis and exploration,
including Jupyter (TODO: citation) notebooks, as public artifacts available on GitHub.

Usage
-----

To understand usage patterns of array libraries within the SPE, we first
identified a representative sample of commonly used Python libraries
("downstream libraries") which consume the sample of array libraries identified
during design analysis. The sample of downstream libraries included the
following libraries: SciPy, pandas, Matplotlib, Xarray, scikit-learn, and scikit-image,
among others. Next, we instrumented downstream libraries in order to record
Python array API calls (TODO: repo citation). After instrumentation, we
collected traces while running downstream library test suites. We subsequently
transformed trace data into structured JSON for subsequent analysis. From
the structured data, we generated empirical APIs based on provided arguments
and associated data types, noting which downstream library called which
empirical API and at what frequency. We then derived a single inferred API
which unifies the individual empirical API calling semantics. We organized the
API results in human-readable form as type definition files and compared the
inferred API to the publicly documented APIs obtained during design analysis.

The following is an example inferred API for `numpy.arange`, with the docstring
indicating the number of lines of code which invoked the function for each
downstream library when running downstream library test suites.

.. code:: python

   def arange(
     _0: object,
     /,
     *_args: object,
     dtype: Union[type, str, numpy.dtype, None] = ...,
     step: Union[int, float] = ...,
     stop: int = ...,
   ):
     """
     usage.dask: 347
     usage.matplotlib: 359
     usage.pandas: 894
     usage.sample-usage: 4
     usage.scipy: 1173
     usage.skimage: 174
     usage.sklearn: 373
     usage.xarray: 666
     ...
     """
     ...

As a final step, we ranked each API in the common API subset obtained during
design analysis according to relative usage using the Dowdall positional voting
system (TODO: citation) (a variant of the Borda count (TODO: citation) which
favors candidate APIs having high relative usage). From the rankings, we
assigned standardization priorities, with higher ranking APIs taking precedence
over lower ranking APIs, and extended the analysis to aggregated API categories
(e.g., array creation, manipulation, statistics, etc.). All source code, usage
data, and analysis are available as public artifacts on GitHub. (TODO: repo
citations)

.. TODO: consider a figure showing the top 10 common API ranks (see Jupyter notebook for array API comparison).

Array API Standard
==================

.. TODO: consider whether to include an introduction here.

Array Object
------------

An array object is a data structure for efficiently storing and accessing
multidimensional arrays (TODO: citation). Within the context of the array API
standard, the data structure is opaque--libraries may or may not grant direct
access to raw memory--and includes metadata for interpreting the underlying
data, notably 'data type', 'shape', and 'device'.

An array data type describes how to interpret a single array element (e.g.,
integer, real- or complex-valued floating-point, boolean, or other). A
conforming array object has a single data type, where a data type is named
object supporting equality comparison. For operations in which the data type of
the resulting array object is a product of the operand data types, the resolved
data type must follow type promotion semantics, which are independent of array
shape or contained values, but restricted to data types of the same "kind"
(e.g., integer versus floating-point). For example,

.. code:: python

   >>> x1 = xp.ones((2,2), dtype=xp.float32)
   >>> x2 = xp.ones(x1.shape, dtype=x1.dtype)
   >>> y = x1 + x2
   >>> y.dtype == xp.float32
   True
   >>> x2 = xp.ones(x1.shape, dtype=xp.float64)
   >>> y = x1 + x2
   >>> y.dtype == xp.float64
   True
   >>> x1 = xp.ones((2,2), dtype=xp.int8)
   >>> x2 = xp.ones(x1.shape, dtype=xp.uint8)
   >>> y = x1 + x2
   >>> y.dtype == xp.int16
   True

An array shape specifies the number of elements along each array axis (also
referred to as "dimension"). The number of axes corresponds to the
dimensionality (or "rank") of an array. For example, :math:`(10)` is a one-dimensional
array (vector) containing 10 elements; :math:`(3,5)` is a two-dimensional array
(matrix) whose inner dimension contains 5 elements and whose outer dimension
contains 3 elements.

An array device specifies the location of array memory allocation and operation
execution. A conforming array object is assigned to a single logical device,
which is represented by an object supporting equality comparison.

.. TODO: consider adding an example of device support, helping to motivate its use; e.g., copying a PyTorch array from CPU to GPU or vice versa

In order to interact with array objects, one uses "indexing" to access sub-
arrays and individual elements, "operators" to perform logical and arithmetic
operations (e.g., :math:`+`, :math:`-`, :math:`\times`, :math:`\div`, and
:math:`@`), and array-aware functions (e.g., for linear algebra, statistical
reductions, and element-wise computation of transcendental functions).

.. TODO: clean-up the following regarding broadcasting

All elementwise functions and operations that accept more than one array input
apply broadcasting rules. The broadcasting rules match the commonly used
semantics of NumPy, where a broadcasted shape is constructed from the input
shapes by prepending size-1 dimensions and broadcasting size-1 dimensions to
otherwise equal non-size-1 dimensions (for example, a shape `(3, 1)` and a
shape `(2, 1, 4)` array would broadcast to a shape `(2, 3, 4)` array by
virtual repetition of the array along the broadcasted dimensions).
Broadcasting rules should be applied independently of the input array data
types or values.

.. TODO: add broadcasting examples

*TODO: introduce the array object. See NumPy paper (https://www.nature.com/articles/s41586-020-2649-2) and the section on NumPy arrays.*

*TODO: consider including something akin to Fig 1 in NumPy paper. In that figure, may also want to include type promotion example/schematic as part of the figure.*

Interchange Protocol
--------------------

*TODO: we can rephase to emphasize interoperability and the desire to convert an array of one flavor to another flavor. We should be able to cut down the content found in this section.*

As discussed in the non-goals section, array libraries are not expected to
support mixing arrays from other libraries. Instead, there is an interchange
protocol that allows converting an array from one library to another.

To be useful, any such protocol must satisfy some basic requirements:

- Interchange must be specified as a protocol, rather than requiring a
  specific dependent package. The protocol should describe the memory layout
  of an array in an implementation-independent manner.

- Support for all data types in this API standard.

- It must be possible to determine on which device the array to be converted
  resides. A single protocol is preferable to
  having per-device protocols. With separate per-device protocols it’s hard to
  figure out unambiguous rules for which protocol gets used, and the situation
  will get more complex over time as TPU’s and other accelerators become more
  widely available.

- The protocol must have zero-copy semantics where possible, making a copy
  only if needed (e.g. when data is not contiguous in memory).

- There must be both a Python-side and a C-side interface, the latter with a
  stable C ABI. All prominent existing array libraries are implemented in
  C/C++, and are released independently from each other. Hence a stable C ABI
  is required for packages to work well together. The protocol must support
  low level access to be usable by libraries that use JIT or AOT compilation,
  and it must be usable from any language.

To satisfy these requirements, DLPack was chosen as the data interchange
protocol. DLPack is a standalone protocol with a header-only C implementation
that is ABI stable, meaning it can be used from any language. It is designed
with multi-device support and supports all the data types specified by the
standard. It also has several considerations for high performance. DLPack
support has already been added to all the major array libraries, and is the
most widely supported interchange protocol across different array libraries.

The array API specifies the following syntax for DLPack support:

- A `.__dlpack__()` method on the array object, which exports the array as a
  DLPack capsule.

- A `.__dlpack__device__()` method on the array object, which returns the device
  type and device ID in DLPack format.

- A `from_dlpack()` function, which converts an object with a `__dlpack__`
  method into an array for the given array library.

Note that `asarray()` also supports the buffer protocol for libraries that
already implement it, like NumPy. But the buffer protocol is CPU-only, meaning
it is not sufficient for the above requirements.

*TODO: add code example.*

Array Functions
---------------

Aside from dunder methods, the only methods/attributes defined on the array
object are `x.to_device()`, `x.dtype`, `x.device`, `x.mT`, `x.ndim`,
`x.shape`, `x.size`, and `x.T`. All other functions in the specification are
defined as functions. These functions include

- **Elementwise functions.** These include functional forms of the Python
  operators (like `add()`) as well as common numerical functions like `exp()`
  and `sqrt()`. Elementwise functions do not have any additional keyword
  arguments.

- **Creation functions.** This includes standard array creation functions
  including `ones()`, `linspace`, `arange`, and `full`, as well as the
  `asarray()` function, which converts "array like" inputs like lists of
  floats and object supporting the buffer protocol to array objects. Creation
  functions all include a `dtype` and `device` keywords. The `array` type is not specified anywhere in the
  spec, since different libraries use different types for their array objects,
  meaning `asarray()` and the other creation functions serve as the effective
  "array constructor".

- **Data type functions** are basic functions to manipulate and introspect
  dtype objects such as `finfo()`, `can_cast()`, and `result_type()`. Notable
  among these is a new function `isdtype()`, which is used to test if a dtype
  is among a set of predefined dtype categories. For example,
  `isdtype(x.dtype, "real floating")` returns `True` if `x` has a real
  floating-point dtype like `float32` or `float64`. Such a function did not
  already exist in a portable way across different array libraries. One
  existing alternative was the NumPy dtype type hierarchy, but this hierarchy
  is complex and is not implemented by other array libraries such as PyTorch.
  The `isdtype()` function is a rare example where the consortium has
  specified a completely new function in the array API specification—most of
  the specified functions are already widely implemented across existing array
  libraries.

- **Linear algebra functions.** Only basic manipulation functions like `matmul()`
  are required by the specification. Additional linear algebra functions are
  included in an optional `linalg` extension (see `Optional Extensions`_).

- **Manipulation functions** such as `reshape()`, `stack()`, and `squeeze()`.

- **Reduction functions** such as `sum()`, `any()`, `all()`, and `mean()`.

- **Unique functions** are four new functions `unique_all()`,
  `unique_counts()`, `unique_inverse()`, and `unique_values()`. These are
  based on the `np.unique()` function but have been split into separate
  functions. This is because `np.unique()` returns a different number of
  arguments depending on the values of keyword arguments. Functions like this
  whose output type depends on more than just the input types are hard for JIT
  compilers to handle, and they are also harder for users to reason about.

Note that the `unique_*` functions, as well as `nonzero()` have a
data-dependent output shape, which makes them difficult to implement in graph
libraries. Therefore, such libraries may choose to not implement these
functions.

Optional Extensions
-------------------

*TODO: consuming extensions. How to check whether present?*

In addition to the above required functions, there are two optional extension
sub-namespaces. Array libraries may chose to implement or not implement these
extensions. These extensions are optional because they typically require
linking against a numerical library such as a linear algebra library, and
therefore may be difficult for some libraries to implement.

- `linalg` contains basic linear algebra functions, such as `eigh`, `solve`,
  and `qr`. These functions are designed to support "batching" (i.e.,
  functions that accept matrices also accept stacks of matrices as a single
  array with more than 2 dimensions). The specification for the `linalg`
  extension is designed to be implementation agnostic. This means that things
  like keyword arguments that are specific to backends like LAPACK are omitted
  from the specified signatures (for example, NumPy’s use of `UPLO` in the
  `eigh()` function). BLAS and LAPACK no longer hold a complete monopoly over
  linear algebra operations given the existence of specialized accelerated
  hardware, so these sorts of keywords are an impediment wide implementation
  across all array libraries.

- `fft` contains functions for performing Fast Fourier transformations.

Test Suite
==========

The array API specification contains over 200 function and method definitions,
each with its own signature and specification for behaviors for things like
type promotion, broadcasting, and special case values.

To facilitate adoption by array libraries, as well as to aid in the
development of the minimal `numpy.array_api` implementation, a test suite for
the array API has been developed. The `array-api-tests` test suite is a fully
featured test suite that can be run against any array library to check its
compliance against the array API specification. The test suite does not depend
on any array library—testing against something like NumPy would be circular
when it comes time to test NumPy itself. Instead, array-api-tests tests the
behavior specified by the spec directly.

When running the tests, the array library is specified using the
`ARRAY_API_TESTS_MODULE` environment variable.

This is done by making use of the hypothesis Python library. The consortium
team has upstreamed array API support to hypothesis in the form of the new
`hypothesis.extra.array_api` submodule, which supports generating arrays from
any array API compliant library. The test suite uses these hypothesis
strategies to generate inputs to tests, which then check the behaviors
outlined by the spec automatically. Behavior that is not specified by the spec
is not checked by the test suite, for example the exact numeric output of
floating-point functions.

The array-api-tests test suite is the first example known to these authors of
a full featured Python test suite that runs against multiple different
libraries. It has already been invaluable in practice for implementing the
minimal `numpy.array_api` implementation, the `array-api-compat` library,
and for finding discrepancies from the spec in array libraries including NumPy,
CuPy, and PyTorch.

Specification Status
====================

Two versions of the array API specification have been released, v2021.12 and
v2022.12. v2021.12 was the initial release with all important core array
functionality. The v2022.12 release added complex number support to all APIs
and the `fft` extension. A v2023 version is in the works, although no
significant changes are planned so far. In 2023, most of the work around the
array API has focused on implementation and adoption.

*TODO: add brief overviews regarding specification revisions and contents.*

Implementation Status
=====================

.. _numpy.array_api:

Reference Implementation
------------------------

The experimental `numpy.array_api` submodule is a standalone, strict
implementation of the standard. It is not intended to be used by end users,
but rather by array consumer libraries to test that their array API usage is
portable.

The strictness of `numpy.array_api` means it will raise an exception for code
that is not portable, even if it would work in the base `numpy`. For example,
here we see that `numpy.array_api.sin(x)` fails for an integral array `x`,
because in the array API spec, `sin()` is only required to work with
floating-point arrays.

.. code:: pycon

   >>> import numpy.array_api as xp
   <stdin>:1: UserWarning: The numpy.array_api submodule
   is still experimental. See NEP 47.
   >>> x = xp.asarray([1, 2, 3])
   >>> xp.sin(x)
   Traceback (most recent call last):
   ...
   TypeError: Only floating-point dtypes are allowed in
   sin

In order to implement this strictness, `numpy.array_api` employs a separate
`Array` object, distinct from `np.ndarray`.

.. code:: python

   >>> a
   Array([1, 2, 3], dtype=int64)

This makes it difficult to use `numpy.array_api` alongside normal `numpy`. For
example, if a consumer library wanted to implement the array API for NumPy by
using `numpy.array_api`, they would have to first convert the user's input
`numpy.ndarray` to `numpy.array_api.Array`, perform the calculation, then
convert back. This is in conflict with the fundamental design of the array API
specification, which is for array libraries to implement the API and for array
consumers to use that API directly in a library agnostic way, without
converting between different array libraries.

As such, the `numpy.array_api` module is only useful as a testing library for
array consumers, to check that their code is portable. If code runs in
`numpy.array_api`, it should work in any conforming array API namespace.

.. _array-api-compat:

Compatibility Layer
-------------------

*TODO: we don't need to go in the weeds here, listing API renames and each instance of incompatible behavior. We can focus on the problems the compat layer is intended to solve, at a high level, and how it helps downstream libraries, such as sklearn and SciPy. Main point is that this is a shim layer which allows standardization consumption to be independent of individual array library release schedules.*

As discussed above, `numpy.array_api` is not a suitable way for libraries to
use `numpy` in an array API compliant way. However, NumPy, as of 1.24, still
has many discrepancies from the array API. A few of the biggest ones are:

- Several elementwise functions are renamed from NumPy. For example, NumPy has
  `arccos()`, etc., but the standard uses `acos()`.

- The spec contains some new functions that are not yet included in NumPy.
  These clean up some messy parts of the NumPy API. These include:

  *TODO: How complete do we need to be here?*

  - `np.unique` is replaced with four different `unique_*` functions so that
    they always have a consistent return type.

  - `np.transpose` is renamed to `permute_dims`.

  - `matrix_transpose` is a new function that only transposes the last two
    dimensions of an array.

  - `np.norm` is replaced with separate `matrix_norm` and `vector_norm`
    functions in the `linalg` extension.

  - `np.trace` operates on the first two axes of an array but the spec
    `linalg.trace` operates on the last two.

There are plans in NumPy 2.0 to fully adopt the spec, including changing the
above behaviors to be spec-compliant. But in order to facilitate adoption, a
new library `array-api-compat` has been written. `array-api-compat` is a
small, pure Python library with no hard dependencies that wraps array
libraries to make the spec complaint. Currently `NumPy`, `CuPy`, and `PyTorch`
are supported.

`array-api-compat` is to be used by array consumer libraries like scipy or
scikit-learn. The primary usage is like

.. code:: python

   from array_api_compat import array_namespace

   def some_array_function(x, y):
       xp = array_api_compat.array_namespace(x, y)

       # Now use xp as the array library namespace
       return xp.mean(x, axis=0) + 2*xp.std(y, axis=0)

`array_namespace` is a wrapper around `x.__array_namespace__()`, except
whenever `x` is a NumPy, CuPy, or PyTorch array, it returns a wrapped module
that has functions that are array API compliant. Unlike `numpy.array_api`,
`array_api_compat` does not use separate wrapped array objects. So in the
above example, the if the input arrays are `np.ndarray`, the return array will
be a `np.ndarray`, even though `xp.mean` and `xp.std` are wrapped functions.

While the long-term goal is for array libraries to be completely array API
compliant, `array-api-compat` allows consumer libraries to use the array API
in the shorter term against libraries like NumPy, CuPy, and PyTorch that are
"nearly complaint".

`array-api-compat` has already been successfully used in scikit-learn's
`LinearDiscriminantAnalysis` API
(https://github.com/scikit-learn/scikit-learn/pull/22554).

Ecosystem Adoption
------------------

*TODO: discuss adoption of the specification in NumPy, CuPy, PyTorch, et al.*

Discussion
==========

*TODO: discuss implementation implications for array-consuming libraries; namely, dunder array_namespace and dunder dlpack methods.*

- `x.__array_namespace__()` returns the corresponding
  array API compliant namespace for the array `x`. This solves the problem of
  how array consumer libraries determine which namespace to use for a given
  input. A function that accepts input `x` can call `xp =
  x.__array_namespace__()` at the top to get the corresponding array API
  namespace `xp`, whose functions are then used on `x` to compute the result,
  which will typically be another array from the `xp` library.

- `__dlpack__()` and `__dlpack_device__()` (see `Interchange Protocol`_).

*TODO: show examples for how to use the above dunder methods.*

As a motivating example, consider the `LinearDiscriminantAnalysis` class in
scikit-learn. This is a classifier whose code is written in pure Python
against NumPy. In scikit-learn pull request `#22554
<https://github.com/scikit-learn/scikit-learn/pull/22554>`__, the
`LinearDiscriminantAnalysis` code was updated to support the array API
standard. This pull request provides a useful example of what array consuming
libraries will typically require to update pure NumPy code to code that can
consume any array API compliant library.

The biggest takeaway from the pull request is that the majority of NumPy-like
code will remain unchanged, other than renaming `np` to `xp`. `xp` is defined
a the top of each function as `xp = array_namespace(X, y)`, where `X` and `y`
are the input arguments to the function and `array_namespace()` is a function
from the `array-api-compat`_ compatibility layer that returns the array
namespace corresponding to `X`.

However, some changes to the usage of NumPy were necessary. A `selection from
the pull request diff
<https://github.com/scikit-learn/scikit-learn/pull/22554/files#diff-088a77600941874d633e8dbe71804c94c3b9d336a73509e6d2db5b48065d1c8bR500-R516>`__
demonstrates the sorts of changes that were required:

.. Note: see scikit-learn commit 2710a9e7eefd2088ce35fd2fb6651d5f97e5ef8b

.. code:: diff

     Xc = []
     for idx, group in enumerate(self.classes_):
   -     Xg = X[y == group, :]
   -     Xc.append(Xg - self.means_[idx])
   +     Xg = X[y == group]
   +     Xc.append(Xg - self.means_[idx, :])

   - self.xbar_ = np.dot(self.priors_, self.means_)
   + self.xbar_ = self.priors_ @ self.means_

   - Xc = np.concatenate(Xc, axis=0)
   + Xc = xp.concat(Xc, axis=0)

     # 1) within (univariate) scaling by with classes
     #    std-dev
   - std = Xc.std(axis=0)
   + std = xp.std(Xc, axis=0)
     # avoid division by zero in normalization
     std[std == 0] = 1.0
   - fac = 1.0 / (n_samples - n_classes)
   + fac = xp.asarray(1.0 / (n_samples - n_classes))

     # 2) Within variance scaling
   - X = np.sqrt(fac) * (Xc / std)
   + X = xp.sqrt(fac) * (Xc / std)

This highlights the following types of changes that are needed to support the
array API:

- **NumPy behavior only a subset of which is defined in the standard.** The
  array indexing expressions `X[y == group, :]` and `self.means_[idx]` are
  changed to `X[y == group]` and `self.means_[idx, :]`, respectively. This is
  because the standard only guarantees support for boolean indexing when the
  boolean index is the sole index, and multidimensional indexing only when all
  axes are indexed.

- **NumPy functions not included in the standard.** `dot()` is not included in
  the standard, so must be replaced with `@` (it could also have been replaced
  with `matmul()`).

- **NumPy functions that are named differently in the standard.** Here
  `np.concatenate()` must be replaced with `xp.concat()`.

- **Using functions instead of methods.** `Xc.std()` must be replaced with
  `xp.std(Xc)`, because the standard is designed around a functional API
  rather than array methods.

- **No array-likes.** The expression `fac = 1.0 / (n_samples - n_classes)`
  must be wrapped with `asarray()`. This is because it is later passed to
  `xp.sqrt()`, and the standard only requires functions to accept actual array
  types as inputs.

Additional types of changes which are not demonstrated in the above example include

- **Functionality that is not included in the standard at all.** This will
  depend on the specific situation, but it will often be sufficient to add a
  helper function to implement the desired behavior across common array
  libraries. For example, the above scikit-learn pull request added a helper
  function for `take()`, which was not yet included in the standard at the
  time of its writing.

- **Library specific performance optimizations.** For instance, code that
  makes use of stride optimizations might use separate code paths for
  libraries like NumPy that support stride manipulations and libraries like
  JAX that do not (stride manipulations are not part of the array API
  specification because not all libraries support them). Per-array library
  special casing allows optimizing for specific commonly used libraries while
  still keeping the code portable.

The above scikit-learn changes were developed with the help of the strict
minimal `numpy.array_api`_ implementation. This was necessary because the
NumPy APIs used in the previous version of the code are not strictly
disallowed by the standard, but using them would not be portable. The
`numpy.array_api` implementation errors on any code that isn't explicitly
required by the specification. By running the `LinearDiscriminantAnalysis`
code against `numpy.array_api`, the scikit-learn developers were able to find
which parts of the code used NumPy functionality that is not part of the
standard.

The resulting code can now be run against any array API conforming library.
`Figure 1`_ shows the resulting speedups from running
`LinearDiscriminantAnalysis` against NumPy, Torch CPU and GPU (Cuda), and
CuPy. Torch CPU gives a 5x speedup over NumPy for fitting, and Torch GPU gives
a 72x and 37x speedup for fit and predict, respectively. CuPy gives 10x and
17x respective speedups over NumPy.

.. Automatic figure references won't work because they require Sphinx.
.. _Figure 1:
.. figure:: scikit_learn_timings.pdf

   Average timings for scikit-learn's `LinearDiscriminantAnalysis` fit and
   predict on a random classification with 500,000 samples and 300 features on
   NumPy, Torch CPU, Torch GPU, and CuPy backends. Benchmarks were run on a
   Nvidia GTX 3090 and an AMD 5950x.

From an end user point of view, making use of the array API support in
`LinearDiscriminantAnalysis` is trivial: they simply pass in arrays from
whichever array API conforming library they wish to use. For example, a
computation with PyTorch might look like

.. code:: python

   import sklearn
   import torch

   # Array API support in scikit-learn is experimental,
   # but this will not be needed in the future.
   sklearn.set_config(array_api_dispatch=True)

   lda = LinearDiscriminantAnalysis()

   # X and y are data provided by the end user
   X = torch.Tensor(...)
   y = torch.Tensor(...)

   # fitted is a torch Tensor. The computation is done
   # entirely with PyTorch functions.
   fitted = lda.fit(X, y)

Future Work
===========

The focus of the consortium for 2023 is on implementation and adoption.

NumPy 2.0, which is planned for release in late 2023, will have full array API
support. This will include several small breaking changes to bring NumPy
inline with the specification. This also includes, NEP 50, which fixes NumPy's
type promotion by removing all value-based casting. A NEP for full array API
specification support will be announced later this year.

SciPy 2.0, which is also being planned, and will include full support for the
array API across the different functions. For end users this means that they
can use CuPy arrays or PyTorch tensors instead of NumPy arrays in SciPy
functions, and they will just work as expected, performing the calculation
with the underlying array library and returning an array from the same
library.

Scikit-learn has implemented array API specification support in its
`LinearDiscriminantAnalysis` class and plans to add support to more functions.

Work is underway on an array API compliance website. (*TODO*)

There is a similar effort being done by the same Data APIs Consortium to
standardize Python dataframe libraries. This work will be discussed in a
future paper and conference talk.

Conclusion
==========

*TODO*

Bibliography
============

*TODO: Add references*
