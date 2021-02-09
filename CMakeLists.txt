cmake_minimum_required(VERSION 3.1)
project(template)
# include (CTest)



# make compilers strict, comment these in, if you believe your code is bullet proof!
# if(MSVC)
#     add_compile_options(/W4 /WX)
# else()
#     add_compile_options(-Wall -Wextra -pedantic -Werror)
# endif()

# run static checks using clang-tidy
# set(CMAKE_CXX_CLANG_TIDY
#   clang-tidy;
#   -header-filter=.;
#   -checks=*;
#   -warnings-as-errors=*;)


# run static checks using cpp-check
# set(CMAKE_CXX_CPPCHECK
#   cppcheck;
#   --std=c++11;
#   --inconclusive;
#   --error-exitcode=1;
# )


include_directories(include) # set include directory of all targets to the 'include' folder, this is similar to '-I include' in gcc
add_library(matlib src/my_math.cpp) # define library called queue that can imported into other targets via 'target_link_libraries'

add_executable(main src/main.cpp) # define executable named main for experimenting and debugging code


# tests are added by declaring a target, in this case 'tests'.
# additional tests can be added by expanding the test cases in 'src/tests.cpp' or an additional target via 'add_executable'
enable_testing()
add_executable(tests src/tests.cpp)
target_link_libraries(tests matlib)
add_test(usage_test tests)

