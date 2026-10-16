#!/usr/bin/env python3
"""Direct ordinary-integer controls for the finite marker count."""
import json
from pathlib import Path


def main():
    package = Path(__file__).resolve().parent
    parameters = json.loads((package / 'controls_parameters.json').read_text())
    rows = []
    total_enumerated = 0
    for width, run in parameters['cases']:
        blocks = max(width // 2 - 1, 0) // run
        selected = [[i for a in range(1+j*run, 1+(j+1)*run)
                     for i in (a, width-1-a)] for j in range(blocks)]
        positions = [i for block in selected for i in block]
        assert len(positions) == 2*run*blocks
        assert len(positions) == len(set(positions))
        assert all(0 < i < width-1 for i in positions)
        assert width % 2 == 0 or width//2 not in positions
        divisors = [[10**i for i in block] for block in selected]
        unmarked = hits = trailing_zero_unmarked = 0
        for n in range(10**(width-1), 10**width):
            marked = any(all(n//divisor % 10 == 9 for divisor in block)
                         for block in divisors)
            unmarked += not marked
            trailing_zero_unmarked += not marked and n % 10 == 0
            if run == 1:
                nxt = n + int(str(n)[::-1])
                hit = str(nxt) == str(nxt)[::-1]
                hits += hit
                assert not (marked and hit), (width, run, n)
        exponent = width-1-2*run*blocks
        assert exponent >= 0
        expected = 9*10**exponent*(10**(2*run)-1)**blocks
        assert unmarked == expected, (width, run, unmarked, expected)
        if run == 1:
            assert hits <= expected
        wrong_count = 9*10**exponent*99**(run*blocks)
        if (width, run) == (6, 2):
            assert wrong_count != unmarked
        total = 9*10**(width-1)
        total_enumerated += total
        rows.append(dict(L=width, r=run, J=blocks, total=total, exact_unmarked=unmarked,
                         source_rhs=expected, selected_positions=selected,
                         free_exponent=exponent, trailing_zero_unmarked=trailing_zero_unmarked,
                         positive_time_one_hits=hits if run == 1 else None,
                         incorrect_per_pair_count=wrong_count if (width,run)==(6,2) else None))
    initial_example = 11
    assert str(initial_example) == str(initial_example)[::-1]
    nxt = initial_example + int(str(initial_example)[::-1])
    assert str(nxt) == str(nxt)[::-1]
    result = dict(status='PASS', scope=parameters['scope'], parameters_file='controls_parameters.json',
                  seed_case_visits=total_enumerated, initial_palindrome_positive_hit_example=[11,22],
                  rows=rows)
    (package/'verification'/'finite-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
