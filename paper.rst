.. Make single backticks produce code
.. default-role:: code

:author: Aaron Meurer
:email: asmeurer@quansight.com
:institution: Quansight

=========================
 Array API Specification
=========================

.. TODO: Does the abstract have a word or character limit?

.. class:: abstract

   The Python array API standard (https://data-apis.org/array-api/) specifies
   standardized application programming interfaces (APIs) and behavior for array
   and tensor objects and operations as commonly found in libraries such as NumPy,
   PyTorch, TensorFlow, Dask, and CuPy.

   The establishment and subsequent adoption of the standard aims to reduce
   ecosystem fragmentation and facilitate array library interoperability in user
   code and among array-consuming libraries, such as scikit-learn and SciPy.

   A key benefit of array interoperability for downstream consumers of the
   standard is device agnosticism, whereby previously CPU-bound implementations
   can more readily leverage hardware acceleration via graphics processing
   units (GPUs), tensor processing units (TPUs), and other accelerator devices.

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
the fundamental building blocks--multidimensional arrays (a.k.a. tensors)--that
underpin the scientific Python ecosystem (SPE).

This fragmentation comes with significant costs, from reinvention and re-implementation
of arrays and associated application programming interfaces (APIs) to siloed
technical stacks targeting only one array library to the proliferation of user
guides providing guidance on how to convert between, and interoperate among,
libraries. Too often, the APIs of each library are largely similar, but each
have enough differences that end users have to relearn and rewrite code in
order to work with multiple libraries. This process can be very painful as the
transition is far from seamless.

.. TODO: Consider inserting Figure 2 from Year 1 report

*TODO: add a motivating example*

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

After providing an overview of the Consortium, we discuss standardization
methodology. We then discuss the current status of the array API standard and
highlight the main standardization areas. Next, we introduce additional tooling
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

- *Pure functions.* Functional API design is the dominant pattern among array
  libraries, both in Python and in other frequently used programming languages
  supporting array computation (e.g., MATLAB (TODO: citation) and Julia (TODO: citation)).
  While method chaining and the fluent interface design pattern are relatively
  common, especially among array libraries supporting lazy evaluation and
  operator fusion, functional APIs are generally preferred, mirroring design
  patterns used in underlying implementations, such as those written in C/C++
  and Fortran.

- *Minimal array object.* A standardized array object should have a minimal set
  of attributes necessary for inspection (e.g., shape, data type, size, etc.)
  and should have a minimal set of magic methods (a.k.a. "dunder" methods) to
  support operator overloading.

- *No dependencies.* The array API standard and its implementation should be
  possible in pure Python, without the need for any external dependency outside
  of Python itself.

- *Accelerator support.* Standardized APIs and behavior should be possible to
  implement for both central processing units (CPUs) and hardware-accelerated
  devices, such as graphics processing units (GPUs), tensor processing units (TPUs),
  and field-programmable gate arrays (FPGAs).

- *JIT compiler support.* Standardized APIs and behavior should be amenable to
  just-in-time (JIT) compilation and graph-based optimization (e.g., PyTorch (TODO: citation),
  JAX (TODO: citation), and TensorFlow (TODO: citation)). For APIs and behavior
  which are not amenable, such as APIs returning arrays having data-dependent
  output shapes, the respective APIs and behavior should be specified as
  optional extensions. Moreover, copy-view mutation semantics (as, e.g.,
  supported by NumPy) should be considered an implementation detail and, thus,
  not suitable for standardization.

- *Distributed support.* Standardized APIs and behavior should be amenable to
  implementation in array libraries supporting distributed computing (e.g., Dask (TODO: citation)).

- *Consistency.* Except in scenarios involving backward compatibility concerns,
  naming conventions and design patterns should be consistent across
  standardized APIs.

- *Extensibility.* Conforming array libraries may implement functionality which
  is not included in the array API standard. As a consequence, array consumers
  should bear responsibility for ensuring that a given API is standardized and its
  usage is portable across specification-conforming array libraries.

- *Deference.* Where possible, the array API standard should defer to existing,
  widely-used standards. For example, the accuracy and precision of numerical
  functions should not be specified beyond the guidance included in IEEE 754 (TODO: citation).

- *Universality.* Standardized APIs and behavior should reflect common usage
  among a wide range of existing array libraries. Accordingly, with rare
  exception, only APIs and behavior having prior art within the SPE may be
  considered candidates for standardization.

Methods
=======

Once we formalized goals and design principles, we sought to understand the Python data API landscape 

TODO: discuss problems for standardization in more detail (in-place operations, copy-view semantics, fancy indexing); focus less on listing particular APIs; discuss at a high level "categories" of functions (e.g., stats, creation, manipulation), as otherwise the lists are likely to be stale in a few years time.

Features
========

*TODO: write an introduction here.*

Array Object
------------

*TODO: introduce the array object. See NumPy paper (https://www.nature.com/articles/s41586-020-2649-2) and the section on NumPy arrays.*

*TODO: consider including something akin to Fig 1 in NumPy paper. May also want to include type promotion.*

Interchange Protocol
--------------------

*TODO: rephase to emphasize interoperability and the desire to convert an array of one flavor to another flavor. We should be able to cut down the content found in this section.*

As discussed in the non-goals section, array libraries are not expected to
support mixing arrays from other libraries. Instead, there is an interchange
protocol that allows converting an array from one library to another.

To be useful, any such protocol must satisfy some basic requirements:

- Interchange must be specified as a protocol, rather than requiring a
  specific dependent package. The protocol should describe the memory layout
  of an array in an implementation-independent manner.

- Support for all dtypes in this API standard (see `Data Types`_ below).

- It must be possible to determine on which device the array to be converted
  resides (see `Device Support`_ below). A single protocol is preferable to
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

Device Support
--------------

*TODO: we should be able to cut down this section. Can we add a PyTorch example here to demonstrate moving an array to a different device and why this is desirable?*

The standard supports specifying what device an array should live on. This is
implemented by explicit `device` keywords in creation functions, with the
convention that execution takes place on the same device where all argument
arrays are allocated. This method of specifying devices was chosen because it
is the most granular, despite its potential verbosity. Other methods of
specifying devices such as context managers are not included, but may be added
in future versions of the spec.

The primary intended usage of device support in the specification is geared
towards array consuming libraries. End users who create arrays from a specific
array library may use that library's specific syntax for specifying the device
relative to their specific hardware configuration. For an array consuming
library, the important things they need to be able to do are

- Create new arrays on the same device as an array that's passed in.

- Determine whether two input arrays are present on the same device or not.

- Move an array from one device to another.

- Create output arrays on the same device as the input arrays.

- Pass on a specified device to other library code.

Consequently, the specified device syntax focuses primarily on getting the
device of a given array and setting the device to the same device as another
array. The specifics of how to specify actual devices are left unspecified.
These specifics differ significantly between existing implementations, such as
CuPy and PyTorch.

The syntax that is specified is

- A `.device` property on the array object, which returns a device object
  representing the device the data in the array is stored on. Nothing is
  specified about the device object other than that it must support basic `==`
  equality comparison within the same library.

- A `device=None` keyword for array creation functions, which takes an
  instance of a device object.

- A `.to_device()` method on the array object to copy an array to a different
  device.

In other words, the only specified way to access a device object is via the
`.device` property of an existing array object. The specifics of how to
specify an actual device depends on the actual array library used, and is
something that will be done by end users, not array library consumers.

This also means that the following are currently considered out-of-scope for
the array API specification:

- Identifying a specific physical or logical device across libraries

- Setting a default device globally

- Stream/queue control

- Distributed allocation

- Memory pinning

- A context manager for device control

All functions should respect explicit `device=` assignment, preserve the
device whenever possible, and avoid implicit data transfer between devices.

Array Methods and Attributes
----------------------------

*TODO: consider rolling up into the "Array Object" section above.*

All relevant Python double underscore (dunder) methods (e.g., `__add__`,
`__mul__`, etc.) are specified for the array object, so that people can write
array code in a natural way using operators. Each dunder method has a
corresponding functional form (e.g., `__add__` :math:`\leftrightarrow`
`xp.add()`). For consistency, this is done even for operators that may seem
unnecessary, like `__pos__` :math:`\leftrightarrow` `positive()`. Operators
and their corresponding functions behave identically, except that operators
accept Python scalars (see `Type Promotion`_ below), while functions are only
required to accept arrays.

In addition to the standard Python dunder methods, the standard adds a some
new dunder methods:

- `x.__array_namespace__()` returns the corresponding
  array API compliant namespace for the array `x`. This solves the problem of
  how array consumer libraries determine which namespace to use for a given
  input. A function that accepts input `x` can call `xp =
  x.__array_namespace__()` at the top to get the corresponding array API
  namespace `xp`, whose functions are then used on `x` to compute the result,
  which will typically be another array from the `xp` library.

- `__dlpack__()` and `__dlpack_device__()` (see the `Data Interchange`_
  section above).

Array Functions
---------------

Aside from dunder methods, the only methods/attributes defined on the array
object are `x.to_device()`, `x.dtype`, `x.device`, `x.mT`, `x.ndim`,
`x.shape`, `x.size`, and `x.T`. All other functions in the specification are
defined as functions. These functions include

- Elementwise functions. These include functional forms of the Python
  operators (like `add()`) as well as common numerical functions like `exp()`
  and `sqrt()`. Elementwise functions do not have any additional keyword
  arguments.

- Creation functions. This includes standard array creation functions
  including `ones()`, `linspace`, `arange`, and `full`, as well as the
  `asarray()` function, which converts "array like" inputs like lists of
  floats and object supporting the buffer protocol to array objects. Creation
  functions all include a `dtype` and `device` keywords (see the `Device
  Support`_ section above). The `array` type is not specified anywhere in the
  spec, since different libraries use different types for their array objects,
  meaning `asarray()` and the other creation functions serve as the effective
  "array constructor".

- Data type functions are basic functions to manipulate and introspect dtype
  objects such as `finfo()`, `can_cast()`, and `result_type()`. Notable among
  these is a new function `isdtype()`, which is used to test if a dtype is
  among a set of predefined dtype categories. For example, `isdtype(x.dtype,
  "real floating")` returns `True` if `x` has a real floating-point dtype like
  `float32` or `float64`. Such a function did not already exist in a portable
  way across different array libraries. One existing alternative was the NumPy
  dtype type hierarchy, but this hierarchy is complex and is not implemented
  by other array libraries such as PyTorch. The `isdtype()` function is a rare
  example where the consortium has specified a completely new function in the
  array API specification—most of the specified functions are already widely
  implemented across existing array libraries.

- Linear algebra functions. Only basic manipulation functions like `matmul()`
  are required by the specification. Additional linear algebra functions are
  included in an optional `linalg` extension (see `Optional Extensions`_
  below).

- Manipulation functions such as `reshape()`, `stack()`, and `squeeze()`.

- Reduction functions such as `sum()`, `any()`, `all()`, and `mean()`.

- Four new functions `unique_all()`, `unique_counts()`, `unique_inverse()`,
  and `unique_values()`. These are based on the `np.unique()` function but
  have been split into separate functions. This is because `np.unique()`
  returns a different number of arguments depending on the values of keyword
  arguments. Functions like this whose output type depends on more than just
  the input types are hard for JIT compilers to handle, and they are also
  harder for users to reason about.

Note that the `unique_*` functions, as well as `nonzero()` have a
data-dependent output shape, which makes them difficult to implement in graph
libraries. Therefore, such libraries may choose to not implement these
functions.

Data Types
----------

*TODO: consider rolling into the "Array Object" section above.*

Data types are defined as named dtype objects in the array namespace, e.g.,
`xp.float64`. Nothing is specified about what these objects actually are
beyond that they should obey basic equality testing. Introspection on these
objects can be done with the data type functions (see `Array Functions`_
above).

The following dtypes are defined:

- Boolean: `bool`.
- Integer: `int8`, `int16`, `int32`, `int64`, `uint8`, `uint16`, `uint32`, and
  `uint64`.
- Real floating-point: `float32` and `float64`.
- Complex floating-point: `complex64` and `complex128`.

These dtypes were chosen because they are the most widely adopted set across
existing array libraries. Additional dtypes may be considered for addition in
future versions of the standard.

Additionally, a conforming library should have "default" integer and
floating-point dtypes, which is consistent across platforms. This is used in
contexts where the result data type is otherwise ambiguous, for example, in
creation functions when no dtype is specified. This allows libraries to
default to 64-bit or 32-bit data types depending on the use-cases they are
aiming for. For example, NumPy's default integer and float dtypes are `int64`
and `float64`, whereas, PyTorch's defaults are `int64` and `float32`.

See also the `Type Promotion`_ section below for information on how dtypes
combine with each other.

Broadcasting
------------

*TODO: consider rolling into the "Array Object" section above.*

*TODO: examples.*

All elementwise functions and operations that accept more than one array input
apply broadcasting rules. The broadcasting rules match the commonly used
semantics of NumPy, where a broadcasted shape is constructed from the input
shapes by prepending size-1 dimensions and broadcasting size-1 dimensions to
otherwise equal non-size-1 dimensions (for example, a shape `(3, 1)` and a
shape `(2, 1, 4)` array would broadcast to a shape `(2, 3, 4)` array by
virtual repetition of the array along the broadcasted dimensions).
Broadcasting rules should be applied independently of the input array data
types or values.

Indexing
--------

*TODO: consider rolling into the "Array Object" section above.*

*TODO: examples.*

Arrays should support indexing operations using the standard Python getitem
syntax, `x[idx]`. The indexing semantics defined are based on the common NumPy
array indexing semantics, but restricted to a subset that is common across
array libraries and does not impose difficulties for array libraries
implemented on accelerators. Basic integer and slice indexing is defined as
usual, except behavior on out-of-bounds indices is left unspecified. Multiaxis
tuple indices are defined, but only specified when all axes are indexed (e.g.,
if `x` is 2-dimensional, `x[0, :]` is defined but `x[0]` may not be
supported). A `None` index may be used in a multiaxis index to insert size-1
dimensions (`xp.newaxis` is specified as a shorthand for `None`). Boolean
array indexing (also sometimes called "masking") is specified, but only for
instances where the boolean index has the same dimensionality as the indexed
array. The result of a boolean array indexing is data-dependent, and thus
graph-based libraries may choose to not implement this behavior.

Integer array indexing is not specified, however a basic `take()` is specified
and `put()` will be added in the 2023 version of the spec.

Note that views are not required in the specification. Libraries may choose to
implement indexed arrays as views, but this should be treated as an
implementation detail by array consumers. In particular, any mutation behavior
that affects more than one array object is considered an implementation detail
that should not be relied on for portability.

As with other APIs, extensions of these indexing semantics, e.g., by
supporting the full range of NumPy indexing rules, is allowed. Array consumers
using these will only need to be aware that their code may not be portable
across libraries.

It should be noted that both 0-D arrays (i.e., "scalar" arrays with shape `()`
consisting of a single value), and size-0 arrays (i.e., arrays with `0` in
their shape with no values) are fully supported by the specification. The
specification does not have any notion of "array scalars" like NumPy's
`np.float64(0.)`, only 0-D arrays. Scalars are a NumPy-only thing, and it is
unnecessary from the point of view of the specification to have them as a
separate concept from 0-D arrays.

Type Promotion
--------------

*TODO: I don't think we need the type promotion diagram here. Main concern is that this is likely to be stale at some point in the future if and when new dtypes are added.*

*TODO: consider rolling into the "Array Object" section above.*

*TODO: examples.*

.. figure:: dtype_promotion_lattice.pdf

   The dtypes specified in the spec with required type promotions, including
   promotions for Python scalars in operators. Cross-kind promotion is not
   required.

Elementwise functions and operators that accept more than one argument perform
type promotion on their inputs, if the input dtypes are compatible.

The specification requires that all type promotion should happen independently
of the input array values and shapes. This differs from the historical NumPy
behavior where type promotion could vary for 0-D arrays depending on their
values. For example (in NumPy 1.24):

.. code:: python

   >>> a = np.asarray(0., dtype=np.float64)
   >>> b = np.asarray([0.], dtype=np.float32)
   >>> (a + b).dtype
   dtype('float32')
   >>> a2 = np.asarray(1e50, dtype=np.float64)
   >>> (a2 + b).dtype
   dtype('float64')


This behavior is bug prone and confusing to reason about. In the array API
specification, any `float32` array and any `float64` array would promote to a
`float64` array, regardless of their shapes or values. NumPy is planning to
deprecate its value-based casting behavior for NumPy 2.0 (see `Future Work`_
below).

Additionally, automatic cross-kind casting is not specified. This means that
dtypes like `int64` and `float64` are not required to promote together. It
also means that functions are not required to accept dtypes that imply a
cross-kind cast: for instance floating-point functions like `exp()` or `sin()`
are not required to accept integer dtypes, and arithmetic functions and
operators like `+` and `*` are not required to accept boolean dtypes. Array
libraries are not required to error in these situations, but array consumers
should not rely on cross-kind casting in portable code. Cross-kind casting is
better done explicitly using the `astype()` function. Automatic cross-kind
casting is harder to reason about, can result in loss of precision, and often
when it happens it indicates a bug in the user code.

Single argument functions and operators should maintain the same dtype when
relevant, for example, if the input to `exp()` is a `float32` array, the
output should also be a `float32` array.

For Python operators like `+` or `*`, Python scalars are allowed. Python
scalars cast to the dtype of the corresponding array's dtype. Cross-kind
casting of the scalar is allowed in this specific instance for convenience
(for example, `float64_array + 1` is allowed, and is equivalent to
`float64_array + asarray(1., dtype=float64)`).

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

Current Status of Implementations
=================================

Two versions of the array API specification have been released, v2021.12 and
v2022.12. v2021.12 was the initial release with all important core array
functionality. The v2022.12 release added complex number support to all APIs
and the `fft` extension. A v2023 version is in the works, although no
significant changes are planned so far. In 2023, most of the work around the
array API has focused on implementation and adoption.

Strict Minimal Implementation
-----------------------------

The experimental `numpy.array_api` submodule is a standalone, strict
implementation of the standard. It is not intended to be used by end users,
but rather by array consumer libraries to test that their array API usage is
portable.

The strictness of `numpy.array_api` means it will raise an exception for code
that is not portable, even if it would work in the base `numpy`. For example,
here we see that `numpy.array_api.sin(x)` fails for an integral array `x`,
because in the array API spec, `sin()` is only required to work with
floating-point arrays.

.. code:: python

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

Compatibility Layer
-------------------

*TODO: we don't need to go in the weeds here, listing API renames and each instance of incompat behavior. We can focus on the problems the compat layer is intended to solve, at a high level, and how it helps downstream libraries, such as sklearn and SciPy. Main point is that this is a shim layer which allows standardization consumption to be independent of individual array library release schedules.*

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

Compliance Testing
------------------

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

*TODO: I think we can remove the following paragraph.*

Utilizing hypothesis offers several advantages. Firstly, it allows writing
tests in a way that more or less corresponds to a direct translation of the
spec into code. This is because hypothesis is a property-based testing
library, and the behaviors required by the spec are easily written as
properties. Secondly, it makes it easy to test all input combinations without
missing any corner cases. Hypothesis automatically handles generating
"interesting" examples from its strategies. For example, behaviors on 0-D or
size-0 arrays are always checked because hypothesis will always generate
inputs that match these corner cases. Thirdly, hypothesis automatically
shrinks inputs that lead to test failures, producing the minimal input to
reproduce the issue. This leads to test failures that are more understandable
because they do not incorporate details that are unrelated to the problem.
Lastly, because hypothesis generates inputs based on a random seed, a large
number of examples can be tested without any additional work. For instance,
the test suite can be run with `pytest --max-examples=10000` to run each test
with 10000 different examples (the default is 100). These things would all be
difficult to achieve with an old-fashioned "manual" test suite, where explicit
examples are chosen by hand.

The array-api-tests test suite is the first example known to these authors of
a full featured Python test suite that runs against multiple different
libraries. It has already been invaluable in practice for implementing the
minimal `numpy.array_api` implementation, the `array-api-compat` library,
and for finding discrepancies from the spec in array libraries including NumPy,
CuPy, and PyTorch.

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
