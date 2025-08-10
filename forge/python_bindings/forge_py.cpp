#include "forge/forge.h"
#include <pybind11/pybind11.h>

namespace py = pybind11;

// Builds a Python extension module named "_forge"
PYBIND11_MODULE(_forge, m) {
  m.doc() = "AEGIS forge Python bindings (minimal)";
  m.def("hello_core", &forge::hello, "Return string from C++ forge_core");
}
