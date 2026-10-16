#!/usr/bin/env python3
"""PRECLAIM_SCOUT / FINITE: Group II p=5..9 overflow-boundary diagnostics."""
import hashlib
import importlib.util
import json
from pathlib import Path

root = Path(__file__).resolve().parent
helper = root.parents[1] / 'groupII-overlap-20261016/controls/groupII_controls.py'
assert hashlib.sha256(helper.read_bytes()).hexdigest() == '50e73312a3a89a8f90a7d8fc6a40b3280724c764c5e433a2a10734ead2f28f31'
spec = importlib.util.spec_from_file_location('groupII_controls', helper)
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
rows = []
cores = [(u,v) for u in range(5,9) for v in [5,6] if u+v<=13]
for r in list(range(1,11)) + [30,100]:
    for p in range(5,10):
        for u,v in cores:
            a0 = c.component(r,p,u,v)
            q0 = c.phi(a0)
            na, aa = c.integer_trajectory(a0,2)
            nq, qq = c.integer_trajectory(q0,2)
            redundant = c.phi(aa[1])
            norm_a1, carry_a1 = c.normalize(aa[1])
            norm_q1, carry_q1 = c.normalize(qq[1])
            norm_red, carry_red = c.normalize(redundant)
            e = c.sparse_difference(norm_q1,norm_red)
            defect = c.sparse_difference(qq[2],c.phi(aa[2]))
            expected_e = [[r+1,1],[r+2,1],[r+4,-1],[r+5,-1]]
            expected_defect = [[r+1,1],[r+3,-1],[r+4,-1],[r+6,1]]
            assert e == expected_e
            assert defect == expected_defect
            assert [len(x) for x in aa] == [2*r+6,2*r+6,2*r+7]
            assert [len(x) for x in qq] == [2*r+7,2*r+7,2*r+8]
            assert c.normalize(aa[0])[1][-1] == 0
            assert c.normalize(qq[0])[1][-1] == 0
            assert carry_a1[-1] == carry_q1[-1] == carry_red[-1] == 1
            assert c.phi(norm_a1) == norm_red
            assert all(x<=9 for x in c.phi(norm_a1))
            assert c.coefficient_step(redundant) == c.phi(aa[2])
            assert all(not c.palindromic(n) for n in nq[1:])
            rows.append({'r':r,'p':p,'u':u,'v':v,'component_integers':na,
                         'whole_integers':nq,'component_words':aa,'whole_words':qq,
                         'normalized_digit_defect':e,'second_pair_defect':defect,
                         'normalization_overlap_without_extra_carry':True})
out = {'status':'PRECLAIM_SCOUT_FINITE_PASS_NOT_LEAN_PROOF','spacers':list(range(1,11))+[30,100],
       'cores':cores,'p_values':list(range(5,10)),'cases':len(rows),'ordinary_additions':4*len(rows),
       'scope':'One canonical realization of each component and whole profile; no universal theorem or ownership claim.',
       'rows':rows}
(root/'p5-overflow-scout.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
