add_library(forge_core STATIC
  src/forge.cpp
)
target_include_directories(forge_core PUBLIC include)

if (AEGIS_BUILD_PYTHON)
  pybind11_add_module(forge_py
    python_bindings/forge_py.cpp
  )
  target_link_libraries(forge_py PRIVATE forge_core)
  set_target_properties(forge_py PROPERTIES OUTPUT_NAME "_forge")
  set_target_properties(forge_py PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${AEGIS_PY_OUT}
  )
endif ()

# ---- C++ unit tests ---------------------------------------------------------
if (AEGIS_BUILD_TESTS)
  include(FetchContent)
  FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG v1.14.0
  )
  set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
  set(BUILD_GMOCK OFF CACHE BOOL "" FORCE)
  set(BUILD_GTEST ON  CACHE BOOL "" FORCE)
  FetchContent_MakeAvailable(googletest)

  add_executable(test_forge_sanity tests/test_sanity.cpp)
  target_link_libraries(test_forge_sanity PRIVATE gtest_main)
  target_compile_features(test_forge_sanity PRIVATE cxx_std_20)
  add_test(NAME forge.sanity COMMAND test_forge_sanity)
endif()
