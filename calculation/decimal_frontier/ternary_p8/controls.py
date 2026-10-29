#!/usr/bin/env python3
"""Mandatory existing base-9 and base-13 controls, from committed repository."""
from importlib.util import spec_from_file_location,module_from_spec
from pathlib import Path
src=Path(__file__).resolve().parent.parent/'ternary_overflow'/'independent.py'
spec=spec_from_file_location('a13_existing_controls',src)
m=module_from_spec(spec);spec.loader.exec_module(m)
m.published_controls()
print('MANDATORY EXISTING BASE-9 AND BASE-13 CONTROLS PASS')
