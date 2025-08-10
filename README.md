# AEGIS

**AEGIS** (Alpha • Exposure • Greeks • Infrastructure • Strategy) is a modular scaffold for a quant research + risk + execution stack.  
This repository provides a clean **C++20 + CMake** monorepo with **pybind11** bindings and a minimal end-to-end path so you can start adding pricers, Greeks, IV surfaces, and reports without reworking the build.

---

## What’s here (scaffold)
- Monorepo layout: `forge/` (core C++), `alpha_foundry/`, `hedge_smith/`, `orca/`
- Root CMake with optional CUDA detection and pybind11 via `FetchContent`
- Minimal C++ lib `forge_core::hello()` + Python extension `_forge`
- Python package `aegis` that re-exports `hello()` (no binary copies in source)
- CTest that imports the package and verifies the binding

---

## Build & quick test (dev)

```bash
# 1) Configure
cmake -S . -B build -DAEGIS_BUILD_PYTHON=ON

# 2) Build (C++ lib + pybind11 extension)
cmake --build build -j

# 3) Make Python see both the built extension and the source package
export PYTHONPATH="$(pwd)/build/python:$(pwd)/python"

# 4) Smoke test (should print: hello from forge_core)
python3 -c "import aegis; print(aegis.hello())"

# 5) Run the CTest suite
cd build && ctest --output-on-failure

```

## Requirements
- CMake ≥ 3.21
- C++20 compiler (tested with AppleClang 17)
- Python ≥ 3.8 (development headers available)
- (Optional) CUDA toolkit — detected automatically if present

``` 
AEGIS/
├─ forge/
│  ├─ include/forge/forge.h         # public header
│  ├─ src/forge.cpp                 # minimal core impl
│  └─ python_bindings/forge_py.cpp  # pybind11 module (_forge)
├─ alpha_foundry/                   # stub target (research)
│  └─ CMakeLists.txt
├─ hedge_smith/                     # stub target (risk/hedging)
│  └─ CMakeLists.txt
├─ orca/                            # stub target (execution)
│  └─ CMakeLists.txt
├─ python/aegis/__init__.py         # Python package (namespace + wrapper)
├─ CMakeLists.txt                   # root build
├─ CMakePresets.json                # debug/release presets
└─ README.md

```
## Design notes
- Build artifacts stay out of the source tree.
    The Python package uses a namespace-like pattern so aegis._forge lives in build/python/aegis/.
- Monorepo, module-first: each top-level folder owns its targets and bindings.
- Reproducible and CI-ready: single CMake entry point + CTest smoke test.

## License
Apache-2.0