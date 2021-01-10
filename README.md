# 270191U025-Software-Architecture-assignment-template

## ONLY FOR TEACHERS (REMOVE THIS FROM ASSIGNMENT)

This repository contains a template for C++ based assignements in the 'Software Architecture' course.
The template provides the students with an CMake based build system.

### Assignment

TODO add description here, what files are expected, what should the code do, etc

### Getting Started

Configure project using system's default compiler:

```bash
mkdir build && cd build && cmake configure .
```

To build all targets:

```bash
cmake --build .
```

Running tests:

```
ctest --verbose
```

If one or more test cases fail you will get an report similar to:

```bash
more stuff ^^^^

[ctest] ../src/tests.cpp(20): FAILED:
[ctest]   REQUIRE( q.empty() == true )
[ctest] with expansion:
[ctest]   false == true
[ctest]
[ctest] ===============================================================================
[ctest] test cases: 2 | 2 failed
[ctest] assertions: 4 | 2 passed | 2 failed
```
