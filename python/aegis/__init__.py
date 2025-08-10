"""
AEGIS dev package.

During development, the native extension (_forge) is built into:
  build/python/aegis/_forge*.so

We make the 'aegis' package span BOTH the source tree (python/aegis)
and the build tree (build/python/aegis) by using pkgutil.extend_path.
This keeps binaries out of the source repo and gives clean imports.

Usage after building:
  export PYTHONPATH="$(pwd)/build/python:$(pwd)/python"
  python3 -c "import aegis; print(aegis.hello())"  # -> "hello from forge_core"
"""
from __future__ import annotations

from pkgutil import extend_path

# Make 'aegis' behave like a namespace package across multiple dirs on sys.path.
# This lets Python see aegis/_forge in build/python/aegis alongside this file.
__path__ = extend_path(__path__, __name__)  # type: ignore[name-defined]

# Friendly Python API that calls into the C++ core via pybind11.
try:
    # Re-export as aegis.hello()
    from ._forge import hello_core as hello  # type: ignore[attr-defined]
except Exception as e:
    # Helpful error if the extension isn't built or not on PYTHONPATH
    def hello() -> str:
        raise RuntimeError(
            "aegis._forge not found.\n"
            "Build the project and ensure PYTHONPATH includes BOTH:\n"
            "  - $(repo)/build/python\n"
            "  - $(repo)/python\n"
            "Example:\n"
            '  export PYTHONPATH="$(pwd)/build/python:$(pwd)/python"\n'
            "Then: python3 -c \"import aegis; print(aegis.hello())\""
        ) from e
