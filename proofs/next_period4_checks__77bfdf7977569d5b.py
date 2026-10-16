"""Independent integer arithmetic and previous exhaustive-graph comparisons.

No transition code from the C++ refinement is imported. Each outer input is
realized by a literal finite decimal integer: insert a single central digit
0 or9, whose doubled column coefficient forces the chosen inward carry.
"""
import json
import subprocess
from pathlib import Path


def digits19(n, k):
    q = []
    for _ in range(k):
        q.append(n % 19)
        n //= 19
    assert n == 0
    return q[::-1]


def realize(q, b):
    columns = q + [18 * b] + q[::-1]
    ds = [0] * len(columns)
    for i, x in enumerate(q):
        ds[-1 - i] = min(9, x)
        ds[i] = x - ds[-1 - i]
    ds[len(q)] = 9 * b
    assert ds[-1] > 0
    return int(''.join(map(str, ds[::-1])))


def check(k):
    process = subprocess.Popen(
        ['./next_period4_refine', '--outer-check', str(k)],
        stdout=subprocess.PIPE, text=True)
    count = 0
    for row in process.stdout:
        code, carry, target, overflow = map(int, row.split())
        q = digits19(code, k)
        n = realize(q, carry)
        s = str(n + int(str(n)[::-1]))
        assert len(s) == 2 * k + 1 + overflow
        got = [int(s[i]) + int(s[-1-i]) for i in range(k)]
        assert got == digits19(target, k), (q, carry, got, target)
        count += 1
    assert process.wait() == 0
    assert count == 36 * 19 ** (k - 1)
    return {'outer_width': k, 'integer_additions_checked': count, 'passed': True}


def main():
    out = {'integer_controls': [check(k) for k in range(1, 5)]}
    data = json.loads(Path('next_period4_results.json').read_text())
    previous = json.loads(Path('exist_geom_bulk_two_outer_results.json').read_text())
    two = data['levels'][1]
    assert data['bulk_states'] == previous['bulk_states'] == 15768
    assert data['recurrent_bulk_states'] == previous['recurrent_bulk_states'] == 1168
    assert two['positive_components'] == len(previous['positive_components']) == 25
    assert sorted(x['vertices'] for x in two['cycle_examples']) == sorted(
        x['vertices'] for x in previous['positive_components'])
    out['independent_two_pair_component_sizes_match'] = True
    # Check every emitted candidate against independently implemented local
    # carry recurrences, reflection, center parity, and literal integers.
    from exist_geom_periodic_bulk_graph import valid, nextq
    steps = 0
    for level in data['levels']:
        k = level['outer_width']
        for c in level['cycle_examples']:
            p = c['period']
            assert sum(c['clock']) == c['growth'] > 0
            assert c['growth'] % 8 == 0
            assert len(c['bulk']) == len(c['outer_pairs']) == len(c['phases']) == p
            for t in range(p):
                nt = (t + 1) % p
                q = tuple(c['bulk'][t]); h = c['clock'][t]
                assert valid(q, c['phases'][t])
                assert nextq(q, h) == tuple(c['bulk'][nt])
                assert (c['phases'][t] + h) % 8 == c['phases'][nt]
                outer = c['outer_pairs'][t]
                targets = []
                for b in (0, 1):
                    n = realize(outer, b)
                    s = str(n + int(str(n)[::-1]))
                    targets.append(([int(s[i])+int(s[-1-i]) for i in range(k)],
                                    len(s) - (2*k+1)))
                assert (c['outer_pairs'][nt], h) in targets
                steps += 1
    out['candidate_cycle_steps_checked'] = steps
    out['scope'] = 'Necessary-condition model, not a finite exterior or existence proof.'
    Path('next_period4_check_results.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
