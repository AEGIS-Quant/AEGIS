import sys
from pathlib import Path

# Repo root = .../aegis
root = Path(__file__).resolve().parents[2]

# Try common build dirs (match your presets)
candidates = [
    root / "build" / "ci-debug" / "python",
    root / "build" / "ci-release" / "python",
    root / "build" / "default-debug" / "python",
    root / "build" / "default-release" / "python",
]

# Always add the source package too
sys.path[:0] = [str(p) for p in candidates if p.exists()] + [str(root / "python")]
