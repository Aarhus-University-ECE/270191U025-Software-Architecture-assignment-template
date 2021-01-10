# 270191U025-Software-Architecture-assignment-template

## ONLY FOR TEACHERS (REMOVE THIS FROM ASSIGNMENT)

This repository contains a template for C++ based assignements in the 'Software Architecture' course.
The template provides a CMake-based build system that makes it easy that makes it easy to build and test the students code.

The intention is to use this template as the seed project to several other repos, specifically one for each assignment in the course.
An assignement in GitHub classroom provides the students with the appropriate files.

## Assignment

1. Write an abstract class for an integer queue with `enqueue`, `dequeue`, `empty` and `full` (you should consult the material from the Introduction to Programming lecture).

Use the file `queue.hpp` as reference

```cpp
class Queue
{
public:
    virtual void enqueue(int value) = 0;
    virtual int dequeue() = 0;
    virtual bool empty() const = 0;
    virtual bool full() const = 0;
};
```

2. Implement the class using an integer array, see `queue_array.hpp`.

3. Implement the class using an integer list, see `queue_linked_list.hpp`.

## Getting Started

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
