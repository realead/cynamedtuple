# cynamedtuple

Memory efficient and fast `namedtuple` implementation using `Cython`.

## Installation

To install last released version:

    pip install cynamedtuple

As `cynamedtuple` uses `Cython` under the hood, right C-compler/tool-chain is needed in order to be able to create `cynamedtuple`s.

To install the most current version use:

    pip install https://github.com/realead/cynamedtuple/zipball/master

The necessary `Cython`-module will be installed as well, if not already in the installation.


## Usage

When providing the types of fields, the resulting tuple is not only named but also typed, i.e. the underlying fields backed by corresponding c-types thus needing less memory:

    from cynamedtuple import typed_namedtuple
    MyStruct = typed_namedtuple("MyStruct", dict(a="int", b="int", c="int"), defaults=[2,3])
    s = MyStruct(5)
    print(s.a, s.b, s.c)      # results in 5 2 3
    print(s[0], s[1], s[-1])  # results in 5 2 3

For Python versions with non-ordered `dict`s (i.e. prior to Py3.6), version with name-type-pairs iterable can be used:

    ...
    typed_namedtuple("MyStruct", [("a","int"), ("b","int"), ("c","int")])
    ...


When the fields cannot be statically typed, `untyped_namedtuple` can be used, which uses slightly less memory and is somewhat faster than Python's original `namedtuple`:

    from cynamedtuple import untyped_namedtuple
    MyStruct = untyped_namedtuple("MyStruct", ["a", "b", "c"], defaults=[2,3])
    s = MyStruct(5)
    print(s.a, s.b, s.c)      # results in 5 2 3
    print(s[0], s[1], s[-1])  # results in 5 2 3


## Performance

Let's compare the performance of the following implementation

    P=collections.namedtuple("P",["a", "b"])
    T=cynamedtuple.typed_namedtuple("T", [("a", "int"), ("b", "int")])
    U=cynamedtuple.untyped_namedtuple("U", ["a", "b"])

with the built-in (unnamed) `tuple`.

### Memory usage

Memory usage depends on the used types, using `int` instead of Python's integer means 3-4 times smaller memory footprint. For `1e7` elements in a list following memory was used:

| Class     | Used memory (in MB)|
|-----------|--------------------|
|typed(T)   |         308        |
|untyped(U) |         927        |
|Python's(P)|        1082        |
|tuple      |        1006        |


### Timings

#### Creation

For creation of `1e6` elements, typed cynamedtuple is almost as fast as usual tuple and about 4 times faster than Python's `namedtuple`:

| Class      |        Times       |
|------------|--------------------|
|typed(T)    |       128 ms       |
|untyped(U)  |       171 ms       |
|Python's(P) |       504 ms       |
|tuple       |       118 ms       |


#### Accessing fields

For accessing a field, typed and untyped versions are about 30% faster than Python's `namedtuple` but slightly slower than the usual `tuple`:

| Class     |        Times       |
|-----------|--------------------|
|typed(T)   |       51.5 ns      |
|untyped(U) |       45.5 ns      |
|Python's(P)|       68.4 ns      |
|tuple      |       49.9 ns      |


#### Accessing via index

Warning: `cynamedtuple`s aren't optimized for access via index - it is linear in number of fields, thus should not be used if there are many fields.


## Producing pyx-code

Under the hood cynamedtuple uses string code snippets from Cython (aka `cython.inline`), and with that some constrains come into play:

  * Cython doesn't not yet supporting any cimports/includes from string code snippets
  * it is not possible to define any types via `ctypedef` e.g. `ctypedef int myint` and use them in a `cynamedtuple`, thus the types of `cynamedtuple` are limited to the built-in types.

A workaround is to use `typed_namedtuple_cycode` to produce the Cython code and to build a cython module from it. Use `cython_header`-argument to insert needed definitions, e.g.

     typed_namedtuple_cycode("A", (("a", "myint"),), cython_header = ["ctypedef int myint"])

will yield the following cython-code:

    ctypedef int myint
    cdef class A:
        cdef public myint a
        def __init__(self,a):
            self.a = a
        def __getitem__(self, i):
            if i==0 or i==-1: return self.a
            raise IndexError('tuple index out of range')

There is also `untyped_namedtuple_cycode`-function as well.


## Trivia:

  * This project was inspired by the following SO-question: https://stackoverflow.com/q/65159938/5769463.
  * While Python's `namedtuple` was an inspiration, `cynamedtuple`isn't a simple drop-in replacement.
  * While cnamedtuple (https://pypi.org/project/cnamedtuple/) is all about speed, `cynamedtuple` is more about smaller memory footprint.


## History:

   *  0.1.0: 13.12.2020:
       * introducing basic functionality
