cmake_minimum_required(VERSION 3.21)
project(AEGIS LANGUAGES CXX)

option(AEGIS_ENABLE_CUDA  "Enable CUDA if available" ON)
option(AEGIS_BUILD_PYTHON "Build Python bindings"    ON)
option(AEGIS_BUILD_TESTS  "Build and run C++/Python tests" ON)  # <-- add

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# CUDA (best-effort)
if (AEGIS_ENABLE_CUDA)
  include(CheckLanguage)
  check_language(CUDA)
  if (CMAKE_CUDA_COMPILER)
    enable_language(CUDA)
    add_compile_definitions(AEGIS_HAVE_CUDA=1)
  endif ()
endif ()

# Python artifacts location
set(AEGIS_PY_OUT ${CMAKE_BINARY_DIR}/python/aegis)

# pybind11 if building Python bindings
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

# ---- Testing (root handles CTest) ------------------------------------------
include(CTest)
if (AEGIS_BUILD_TESTS)
  enable_testing()

  if (BUILD_TESTING AND AEGIS_BUILD_PYTHON)
    find_package(Python3 COMPONENTS Interpreter REQUIRED)
    add_test(
      NAME python_import_hello
      COMMAND
        ${Python3_EXECUTABLE}
        -c
        "import sys; sys.path[:0]=['${CMAKE_BINARY_DIR}/python','${CMAKE_SOURCE_DIR}/python']; import aegis; print(aegis.hello())"
    )
    set_tests_properties(python_import_hello
      PROPERTIES PASS_REGULAR_EXPRESSION "hello from forge_core")
  endif ()
endif ()
