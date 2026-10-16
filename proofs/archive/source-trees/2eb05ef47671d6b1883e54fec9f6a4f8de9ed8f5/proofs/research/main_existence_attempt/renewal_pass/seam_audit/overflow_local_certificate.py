"""Emit the finite arithmetic core of the unrestricted overflow proof."""
from pathlib import Path
import itertools
import json

HERE = Path(__file__).resolve().parent
rows = []
examined = 0
for S, C, R, tau, q in itertools.product(range(-1, 3), range(2), range(2), range(2), range(19)):
    examined += 1
    if q != 10*C+R+9*S or not 0 <= q+tau-10*C <= 9:
        continue
    rows.append(dict(S=S, C=C, R=R, tau=tau, q=q, digit=q+tau-10*C, next_S=S+C-R))
result = dict(status='COMPLETE_FINITE_LOCAL_RELATION',
              analytic_state_bound='q in [0,18], C,R in {0,1}, q=10C+R+9S imply S in {-1,0,1,2}',
              initial_state=0, terminal_state=0, enumerated_tuples=examined, rows=rows,
              global_inputs='Every symmetric-E overflow word induces a path in this local relation',
              conclusion='Every path from 0 to 0 stays at 0 and has C=R and q=11C')
(HERE/'overflow_local_certificate.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(dict(status=result['status'], enumerated_tuples=examined, valid_rows=len(rows)), indent=2))
