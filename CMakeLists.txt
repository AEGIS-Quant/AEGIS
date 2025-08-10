cmake_minimum_required(VERSION 3.21)
project(AEGIS LANGUAGES CXX)

option(AEGIS_ENABLE_CUDA  "Enable CUDA if available" ON)
option(AEGIS_BUILD_PYTHON "Build Python bindings"    ON)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Try to enable CUDA if available (no hard fail)
if (AEGIS_ENABLE_CUDA)
  include(CheckLanguage)
  check_language(CUDA)
  if (CMAKE_CUDA_COMPILER)
    enable_language(CUDA)
    add_compile_definitions(AEGIS_HAVE_CUDA=1)
  endif ()
endif ()

# Where we’ll place built Python artifacts
set(AEGIS_PY_OUT ${CMAKE_BINARY_DIR}/python/aegis)

# Fetch pybind11 if we’re building Python bindings
if (AEGIS_BUILD_PYTHON)
  include(FetchContent)
  FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG v2.12.0
  )
  FetchContent_MakeAvailable(pybind11)
endif ()

# Modules
add_subdirectory(forge)
add_subdirectory(alpha_foundry)
add_subdirectory(hedge_smith)
add_subdirectory(orca)

include(CTest)
enable_testing()

if (BUILD_TESTING AND AEGIS_BUILD_PYTHON)
  # We only need a Python interpreter
  find_package(Python3 COMPONENTS Interpreter REQUIRED)

  # Run python with both build/python and python on sys.path
  add_test(
    NAME python_import_hello
    COMMAND
      ${Python3_EXECUTABLE}
      -c
      "import sys; sys.path[:0]=['${CMAKE_BINARY_DIR}/python','${CMAKE_SOURCE_DIR}/python']; import aegis; print(aegis.hello())"
  )

  # Pass if the output contains the expected string
  set_tests_properties(python_import_hello
    PROPERTIES PASS_REGULAR_EXPRESSION "hello from forge_core")
endif ()

