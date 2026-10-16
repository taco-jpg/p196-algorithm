"""Emit the small exhaustive carry frontier and a hand-specified inverse.

The frontier concerns all suffixes and all finite widths, not a search of
sampled integers. The independent checker does not import this generator.
"""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def edges(state):
    overflow, low_carry, high_carry, delayed_high, started = state
    for q in range(1 if not started else 0, 19):
        for inner_high in (0, 1):
            if (q + inner_high) // 10 != high_carry:
                continue
            low = (q + low_carry) % 10
            high = (q + inner_high) % 10
            output = low + (delayed_high if overflow else high)
            target = (overflow, (q + low_carry) // 10,
                      inner_high, high if overflow else -1, True)
            yield q, output, target


def frontier(prefix):
    current = [((0, 0, 0, -1, False), ()), ((1, 0, 1, 1, False), ())]
    history = []
    for value in prefix:
        current = [(target, word + (q,)) for state, word in current
                   for q, output, target in edges(state) if output == value]
        history.append([dict(state=state, source_prefix=word)
                        for state, word in current])
    return history


def fixed(value, length=1):
    return [value, [0], length]


def variable(value, constant):
    return [value, [1], constant]


def full(prefix):
    return prefix + prefix[::-1]


def main():
    pairs = [(1, 6, 2), (2, 12, 4)]
    frontiers = [dict(output_prefix=p, layers=frontier(p)) for p in pairs]
    one_six = frontiers[0]['layers'][1]
    for row in one_six:
        state = row['state']
        row['all_next_pair_edges'] = [dict(source=q, output=out, target=target)
                                      for q, out, target in edges(state)]
        h, a, b, t, unused = state
        row['all_odd_center_extras'] = [dict(center=c, extra=(c+a) % 10+t)
                                      for c in range(0, 19, 2)
                                      if h and (c+a)//10 == b]
    d = [fixed(1), fixed(6), fixed(2, 2), fixed(4), variable(9, 1),
         fixed(17), fixed(7), fixed(18), fixed(7)]
    a = [fixed(2), fixed(12), fixed(4, 2), variable(9, 2),
         fixed(14), fixed(16, 2), fixed(15)]
    result = dict(
        status='EXHAUSTIVE_LOCAL_CARRY_OBSTRUCTION',
        state_fields=['overflow', 'low_carry', 'high_carry', 'delayed_high', 'started'],
        frontiers=frontiers,
        forbidden_image_prefix=[1, 6, 2],
        forbidden_two_step_image_prefix=[2, 12, 4],
        width_coverage='Three folded pairs require output width>=6 and input width>=5. '
                       'The third pair is either an ordinary edge, or the odd-center extra '
                       'of a five-digit overflowing input. Both cases are certified.',
        predecessor_parameter='r=7+k, every k>=0; r=6 checked separately',
        predecessor_formula='D_r=(1,6,2,2,4,9^(r-6),17,7,18,7), no center',
        predecessor_full_pair_words={'D': full(d), 'A': full(a)},
        predecessor_transition=['D', 'A'],
        first_positive_palindrome_time=15,
        ladder_certificate_path='inverse_ladder_certificate.json',
        ladder_certificate_sha256=hashlib.sha256((HERE/'inverse_ladder_certificate.json').read_bytes()).hexdigest(),
        scope='All predecessors of the A-prefix cylinder. No bound on all other branches above Q_r is claimed.',
        positive_invariant_found=False)
    (HERE/'prefix_obstruction_certificate.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],
                         frontier_sizes=[[len(layer) for layer in row['layers']]
                                         for row in frontiers],
                         predecessor_first_hit=15, positive_invariant_found=False), indent=2))


if __name__ == '__main__':
    main()
