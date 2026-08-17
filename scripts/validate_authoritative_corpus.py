#!/usr/bin/env python3
"""Compatibility entry point for the authoritative three-set validator.

The former primary/secondary/pending partition is historical and no longer
represents the manuscript-facing corpus. Keep this filename as a compatibility
shim so older automation cannot silently validate obsolete denominators.
"""

from __future__ import annotations

import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT / "scripts" / "validate_three_set_corpus.py"), run_name="__main__")
