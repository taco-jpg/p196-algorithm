"""Independent arithmetic and coaccessibility replay of the finite core."""
from fractions import Fraction
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
path = HERE/'overflow_local_certificate.json'
data = json.loads(path.read_text())
# The analytic bound covers every integer S, not only tested values.
assert Fraction(-11, 9) > -2 and Fraction(18, 9) == 2
expected = set()
for q in range(19):
    for C in (0, 1):
        for R in (0, 1):
            numerator = q-10*C-R
            if numerator % 9:
                continue
            S = numerator//9
            assert -1 <= S <= 2
            for tau in (0, 1):
                digit = q+tau-10*C
                if digit in range(10):
                    expected.add((S, C, R, tau, q, digit, S+C-R))
actual = {(r['S'], r['C'], r['R'], r['tau'], r['q'], r['digit'], r['next_S']) for r in data['rows']}
assert actual == expected and len(data['rows']) == len(actual) == 9
assert data['enumerated_tuples'] == 4*2**3*19 == 608
coaccessible = {0}
while True:
    enlarged = coaccessible | {S for S, C, R, tau, q, digit, target in actual if target in coaccessible}
    if enlarged == coaccessible:
        break
    coaccessible = enlarged
assert coaccessible == {0}
accepted_edges = [row for row in actual if row[0] in coaccessible and row[-1] in coaccessible]
assert len(accepted_edges) == 4
assert all(S == 0 and C == R and q == 11*C for S, C, R, tau, q, digit, target in accepted_edges)
assert all(S in (0, 1) for S, C, R, tau, q, digit, target in actual)
assert all(target == 1 and C == R == tau == 0 and q == 9
           for S, C, R, tau, q, digit, target in actual if S == 1)
result = dict(status='INDEPENDENT_OVERFLOW_CORE_PASS',
              certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
              enumerated_tuples=608, admissible_local_rows=9,
              states_with_local_rows=[0, 1], states_coaccessible_to_zero=sorted(coaccessible),
              zero_return_edges=len(accepted_edges), allowed_q_on_zero_return_paths=[0, 11],
              imports_generator=False, unrestricted_path_length=True)
(HERE/'overflow_local_audit.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
