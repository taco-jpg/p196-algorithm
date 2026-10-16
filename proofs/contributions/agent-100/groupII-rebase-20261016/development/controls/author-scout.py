import json
from pathlib import Path


def pair_step(q):
    carry = 0
    digits = []
    for a in q:
        carry, digit = divmod(a + carry, 10)
        digits.append(digit)
    assert carry in (0, 1)
    if carry:
        digits.append(carry)
    return [a + b for a, b in zip(digits, reversed(digits))]


def shift_one(q):
    return [q[0]] + [q[i] + q[i - 1] for i in range(1, len(q))] + [q[-1]]


cores = [(u, v) for u in range(5, 9) for v in range(5, 7) if u + v <= 13]
rows = []
for r in list(range(1, 13)) + [30, 100]:
    for p in range(5, 10):
        for u, v in cores:
            a0 = [p] + [0] * r + [u, v, v, u] + [0] * r + [p]
            q0 = shift_one(a0)
            a1, q1 = pair_step(a0), pair_step(q0)
            a2, q2 = pair_step(a1), pair_step(q1)
            delta = [1 if i in (r + 1, r + 5) else -1 if i in (r + 2, r + 4) else 0
                     for i in range(len(a2))]
            c = [a + d for a, d in zip(a2, delta)]
            finite_c = lambda i: c[i] if 0 <= i < len(c) else 0
            checks = {
                'actual_widths': len(a2) == 2 * r + 7 and len(q2) == 2 * r + 8,
                'nonnegative': min(c) >= 0,
                'bounded_by_18': max(c) <= 18,
                'symmetric': c == c[::-1],
                'even_center': c[len(c) // 2] % 2 == 0,
                'positive_outer': c[0] > 0,
                'finite_tail_zero': all(finite_c(i) == 0 for i in range(len(c), len(c) + 4)),
                'exact_overlap': shift_one(c) == q2,
                'four_position_formula': all(a2[i] == val for i, val in
                    ((r + 1, 2 * u - 9), (r + 5, 2 * u - 9),
                     (r + 2, 2 * (u + v) - 18), (r + 4, 2 * (u + v) - 18))),
            }
            rows.append({'r': r, 'p': p, 'u': u, 'v': v,
                         'A0': a0, 'Q0': q0, 'A1': a1, 'Q1': q1,
                         'A2': a2, 'Q2': q2, 'Delta': delta, 'CInt': c,
                         'checks': checks, 'passed': all(checks.values())})

out = Path(__file__).with_name('author-scout.jsonl')
out.write_text(''.join(json.dumps(row, separators=(',', ':')) + '\n' for row in rows))
summary = {'rows': len(rows), 'cores': cores,
           'passed': sum(row['passed'] for row in rows),
           'failed': sum(not row['passed'] for row in rows),
           'note': 'Finite integer controls only; no all-r claim. Tail check uses explicit zero extension.'}
Path(__file__).with_name('author-scout-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
assert summary['failed'] == 0
