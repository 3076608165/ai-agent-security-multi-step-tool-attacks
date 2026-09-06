"""Shared test setup: make the repo root and the (git-ignored) official SDK importable.

The official `aicomp_sdk` ships with the competition data download and is git-ignored;
without it the engines cannot be imported, so tests self-skip rather than error.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OFFICIAL = ROOT / "official"

for p in (str(ROOT), str(OFFICIAL)):
    if p not in sys.path:
        sys.path.insert(0, p)
