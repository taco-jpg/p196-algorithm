#!/usr/bin/env python3
"""Run exact carry graph proof and the independent integer/matrix checker."""
import json,subprocess,sys
from pathlib import Path
here=Path(__file__).resolve().parent
p=subprocess.run([sys.executable,str(here/'sharp_streak.py'),str(here/'lattice_input.txt')],check=True,capture_output=True,text=True)
print(p.stdout,end='')
assert 'SHARP_RUN_BOUND_3_5_ALL_WIDTH_PASS' in p.stdout
assert json.loads(p.stdout.split('SUMMARY_JSON ',1)[1])==json.loads((here/'bounds.json').read_text())
subprocess.run([sys.executable,str(here/'independent_checker.py'),str(here/'lattice_input.txt'),str(here/'bounds.json')],check=True)
print('SHARP_STREAK_FULL_REPRODUCTION_PASS')
