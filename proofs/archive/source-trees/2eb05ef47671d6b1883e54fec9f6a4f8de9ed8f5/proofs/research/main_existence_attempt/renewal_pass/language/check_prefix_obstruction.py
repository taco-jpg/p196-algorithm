"""Replay the complete carry obstruction independently of its generator.

The proof exhausts all local decimal possibilities, including the one odd
center case. Integer controls are separate from that unrestricted proof.
Only standard-library modules are imported.
"""
from collections import defaultdict
from pathlib import Path
import hashlib
import itertools
import json

HERE = Path(__file__).resolve().parent


def local_choices(state):
    h, a, b, t, started = state
    answers = []
    # Quotients and remainders are derived using integer equality, rather
    # than importing or calling the discovery transducer.
    for q in range(19):
        if not started and q == 0:
            continue
        for inner in range(2):
            upper_digit = q + inner - 10*b
            lower_outgoing = int(q+a >= 10)
            lower_digit = q+a-10*lower_outgoing
            if not 0 <= upper_digit <= 9:
                continue
            assert 0 <= lower_digit <= 9
            emitted = lower_digit + (t if h else upper_digit)
            target = [h, lower_outgoing, inner, upper_digit if h else -1, True]
            answers.append(dict(source=q, output=emitted, target=target))
    return answers


def verify_frontier(record):
    paths = [dict(state=[0, 0, 0, -1, False], source_prefix=[]),
             dict(state=[1, 0, 1, 1, False], source_prefix=[])]
    for output, layer in zip(record['output_prefix'], record['layers']):
        next_paths = []
        for row in paths:
            for edge in local_choices(row['state']):
                if edge['output'] == output:
                    next_paths.append(dict(state=edge['target'],
                                           source_prefix=row['source_prefix']+[edge['source']]))
        assert [{k: row[k] for k in ('state', 'source_prefix')} for row in layer] == next_paths
        paths = next_paths
    return paths


def reverse(n):
    result = 0
    while n:
        result = result*10+n % 10
        n //= 10
    return result


def folded(n):
    digits = tuple(map(int, str(n)))
    full = tuple(a+b for a, b in zip(digits, reversed(digits)))
    return full[:len(full)//2], full[len(full)//2] if len(full) % 2 else None


def realize(pairs, center):
    digits = [max(0, q-9) for q in pairs]
    if center is not None:
        digits.append(center//2)
    digits.extend(min(9, q) for q in reversed(pairs))
    return sum(d*10**i for i, d in enumerate(digits))


def plus(a, b):
    return a[0]+b[0], a[1]+b[1]


def add(*terms):
    out = defaultdict(int)
    for polynomial, scalar in terms:
        for exponent, coefficient in polynomial.items():
            out[exponent] += scalar*coefficient
    return {e: c for e, c in out.items() if c}


def numerator(runs):
    out = defaultdict(int)
    position = (0, 0)
    for coefficient, affine, constant in runs:
        assert len(affine) == 1 and affine[0] >= 0 and constant >= 1
        end = plus(position, (affine[0], constant))
        out[end] += coefficient
        out[position] -= coefficient
        position = end
    return {e: c for e, c in out.items() if c}, position


def reflection(polynomial, width):
    return {(width[0]-a, width[1]-b): -coefficient
            for (a, b), coefficient in polynomial.items()}


def normalize(runs):
    carries = []
    incoming = 0
    for q, slope, constant in runs:
        assert 0 <= q <= 18
        outgoing = int(q+incoming >= 10)
        assert int(q+outgoing >= 10) == outgoing
        assert 0 <= q+incoming-10*outgoing <= 9
        assert 0 <= q-9*outgoing <= 9
        carries.append([outgoing, slope, constant])
        incoming = outgoing
    Q, length = numerator(runs)
    C, carry_length = numerator(carries)
    assert carry_length == length
    D = add((Q, 1), ({plus(e, (0, 1)): c for e, c in C.items()}, 1), (C, -10))
    return D, plus(length, (0, incoming)), incoming


def explicit(name, r):
    if name == 'D':
        return (1, 6, 2, 2, 4)+(9,)*(r-6)+(17, 7, 18, 7)
    return (2, 12, 4, 4)+(9,)*(r-5)+(14, 16, 16, 15)


def main():
    source = HERE/'prefix_obstruction_certificate.json'
    cert = json.loads(source.read_text())
    forbidden, forced = cert['frontiers']
    assert forbidden['output_prefix'] == [1, 6, 2]
    assert forced['output_prefix'] == [2, 12, 4]
    assert not verify_frontier(forbidden)
    final = verify_frontier(forced)
    assert final == [dict(state=[0, 0, 0, -1, True], source_prefix=[1, 6, 2])]
    assert len(forbidden['layers'][1]) == 4
    next_edge_count = center_count = 0
    lower_bounds = []
    for row in forbidden['layers'][1]:
        state = row['state']
        assert state[0] == 1 and state[3] >= 4
        next_edges = local_choices(state)
        assert next_edges == row['all_next_pair_edges']
        assert all(edge['output'] >= 4 for edge in next_edges)
        next_edge_count += len(next_edges)
        h, a, b, t, unused = state
        center_outputs = [dict(center=c, extra=c+a-10*b+t)
                          for c in range(0, 19, 2) if 0 <= c+a-10*b <= 9]
        assert center_outputs == row['all_odd_center_extras']
        assert all(row['extra'] >= 4 for row in center_outputs)
        center_count += len(center_outputs)
        lower_bounds.append(dict(source_prefix=row['source_prefix'], state=state,
                                 next_pair_min=min(edge['output'] for edge in next_edges),
                                 center_min=min(row['extra'] for row in center_outputs)))
    # An overflowing first output 2 never permits a second output 12.
    first_two = forced['layers'][1]
    assert len(first_two) == 1 and first_two[0]['state'][0] == 0
    # No-overflow terminal handling never emits an additional folded pair.
    # Hence the third pair 4 must be the third ordinary edge above.

    dependency = HERE/cert['ladder_certificate_path']
    assert hashlib.sha256(dependency.read_bytes()).hexdigest() == cert['ladder_certificate_sha256']
    words = cert['predecessor_full_pair_words']
    D, width, overflow = normalize(words['D'])
    A, target_width = numerator(words['A'])
    assert width == target_width and overflow == 0
    assert A == add((D, 1), (reflection(D, width), 1))
    assert numerator(words['D'])[0] == reflection(numerator(words['D'])[0], numerator(words['D'])[1])
    assert A == reflection(A, width)
    assert words['D'][0][0] > 0 and words['A'][0][0] > 0

    # All 5-digit-or-shorter integers include the short odd-center case.
    integer_count = 0
    for n in range(1, 100000):
        input_word = folded(n)[0]
        out_word = folded(n+reverse(n))[0]
        assert out_word[:3] != (1, 6, 2)
        if out_word[:3] == (2, 12, 4):
            assert input_word[:3] == (1, 6, 2)
        integer_count += 1
    # Exhaust all canonical 6- and 7-digit pair words: this compares the
    # local theorem with actual decimal arithmetic for every center type.
    pair_word_count = forced_examples = 0
    for p0 in range(1, 19):
        for tail in itertools.product(range(19), repeat=2):
            p = (p0,)+tail
            for center in (None,)+tuple(range(0, 19, 2)):
                n = realize(p, center)
                assert folded(n) == (p, center)
                output = folded(n+reverse(n))[0]
                assert output[:3] != (1, 6, 2)
                if output[:3] == (2, 12, 4):
                    assert p == (1, 6, 2)
                    forced_examples += 1
                pair_word_count += 1
    assert integer_count == 99999 and pair_word_count == 18*19**2*11

    controls = []
    for r in (6, 7, 8, 11, 37, 128, 1024):
        p = explicit('D', r)
        if r >= 7:
            full = tuple(value for value, slope, constant in words['D']
                         for _ in range(slope[0]*(r-7)+constant))
            assert full == p+p[::-1]
        n = realize(p, None)
        seed = n
        orbit = []
        for time in range(1, 16):
            n += reverse(n)
            if time == 1:
                assert folded(n) == (explicit('A', r), None)
            assert (n == reverse(n)) == (time == 15)
            orbit.append(str(n))
        controls.append(dict(r=r, seed=str(seed), first_hit=15,
                             palindrome=str(n), orbit_sha256=hashlib.sha256('\n'.join(orbit).encode()).hexdigest()))
    result = dict(status='PASS', scope=cert['scope'],
                  certificate_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  frontier_sizes=[[len(layer) for layer in row['layers']] for row in cert['frontiers']],
                  next_pair_edge_count=next_edge_count, odd_center_cases=center_count,
                  minimum_third_pair=4, lower_bounds=lower_bounds,
                  forbidden_image_prefix=[1, 6, 2], forbidden_two_step_image_prefix=[2, 12, 4],
                  all_parameter_D_to_A=True, D_to_A_overflow=overflow,
                  small_integer_controls=integer_count, complete_pair_word_controls=pair_word_count,
                  forced_prefix_examples=forced_examples, D_integer_controls=controls,
                  uses_generator=False, positive_invariant_found=False)
    (HERE/'prefix_obstruction_audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('D_integer_controls', 'lower_bounds')}, indent=2))


if __name__ == '__main__':
    main()
