"""Rebuild the standalone Lean 4.19 file from the checked source modules."""
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
base = ROOT / 'research' / 'Lychrel196Research.lean'
if not base.exists():
    base = ROOT / 'Lychrel196Research.lean'
modules = [base] + [HERE / name for name in (
    'MassCriterion.lean', 'ZeroGap.lean', 'UnboundedMass.lean',
    'MassConsequences.lean', 'QuantitativeMass.lean')]
parts = [
    'import Std\n\n/-! Standalone decimal digit-sum research continuation.\n'
    'Checked with Lean 4.19.0 and Std only.\n'
    'Main result: DecimalUnboundedMass.digitSum_unbounded_after.\n'
    'No decimal Lychrel existence claim is made.\n'
    'The base module is retained intact below, followed by five modules. -/\n'
]
for index, path in enumerate(modules):
    source = path.read_text()
    source = re.sub(r'^import[^\n]*\n', '', source, flags=re.MULTILINE)
    parts.append('\n/- Source module: ' + path.name + ' -/\n' + source)
target = HERE / 'LychrelDigitSums.lean'
target.write_text('\n'.join(parts))
print(target)
