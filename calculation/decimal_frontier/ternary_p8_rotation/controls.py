#!/usr/bin/env python3
"""Positive b9/b13 controls, reproduced from an existing committed checker."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parent.parent/'ternary_p8'/'controls.py'),run_name='__main__')
