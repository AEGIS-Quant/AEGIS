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
