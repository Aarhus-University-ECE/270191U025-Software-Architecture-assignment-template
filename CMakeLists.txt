cmake_minimum_required(VERSION 3.1)
project(template)

include_directories(include) # set include directory of all targets to the 'include' folder, this is similar to '-I include' in gcc
add_library(queue src/queue_array.cpp src/queue_linked_list.cpp) # define library called queue that can imported into other targets via 'target_link_libraries'

add_executable(main src/main.cpp) # define executable named main for experimenting and debugging code


# tests are added by declaring a target, in this case 'tests'.
# additional tests can be added by expanding the test cases in 'src/tests.cpp' or an additional target via 'add_executable'
enable_testing()
add_executable(tests src/tests.cpp)
target_link_libraries(tests queue)
add_test(usage_test tests)