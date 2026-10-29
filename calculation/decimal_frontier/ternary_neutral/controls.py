#!/usr/bin/env python3
"""Required positive controls and nonneutral cross-check, from the same repo.
This deliberately uses the already-published agent-13 control engine, not
neutral_proof.py, so no experimental file outside the repository is needed.
"""
from importlib.util import spec_from_file_location,module_from_spec
from pathlib import Path
base=Path(__file__).resolve().parent.parent/'ternary_overflow'
for name in ('proof','independent'):
    spec=spec_from_file_location('a13_'+name,base/(name+'.py'))
    m=module_from_spec(spec);spec.loader.exec_module(m)
    if name=='proof':
        assert m.certify()==(20,16,13,5,100)
        print('PREVIOUS ALL-BASE NONNEUTRAL PROOF PASS')
    else:
        m.published_controls()
        print('MANDATORY B9/B13 CONTROLS PASS')
