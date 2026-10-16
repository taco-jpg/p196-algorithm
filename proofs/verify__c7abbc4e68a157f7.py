#!/usr/bin/env python3
"""Fresh, deterministic controls of Agent8's independent quotient implementation.

This is a finite formula audit, not a proof that any quotient cycle exists.
The emitted digest covers canonical JSON of every tested state, gaps, target,
gains, overflow and literal output. The generator is the complete input catalog;
no unreported per-case output file is required for this replay.
"""
from __future__ import annotations
import hashlib
import json
import random
from pathlib import Path
from complementary_bulk import PHASES, State, direct_pair, pair, realize, small_states, step, trim

GAPS = ((2, 2), (3, 5), (7, 2))
RANDOM_SEED = 19608
RANDOM_STATES = 5000


def main() -> None:
    digest = hashlib.sha256()
    controls = overflows = small = random_count = 0

    def check(s: State) -> None:
        nonlocal controls, overflows
        s.check()
        target, dg, dh, gamma = step(s)
        target.check()
        for g, h in GAPS:
            source = s.word(g, h)
            actual_pair = direct_pair(source)
            expected = target.word(g + dg, h + dh)
            assert actual_pair == expected, (s, g, h, actual_pair, expected)
            n = realize(source)
            literal = n + int(str(n)[::-1])
            digits = tuple(map(int, str(literal)[::-1]))
            assert pair(digits) == actual_pair
            assert len(digits) == len(source) + gamma
            assert digits != digits[::-1]
            assert len(expected) == len(source) + gamma
            record = [s.as_json(), g, h, target.as_json(), dg, dh, gamma, list(actual_pair)]
            digest.update(json.dumps(record, separators=(',', ':')).encode() + b'\n')
            controls += 1
            overflows += gamma

    for s in small_states():
        check(s)
        small += 1
    rng = random.Random(RANDOM_SEED)
    for _ in range(RANDOM_STATES):
        c = rng.choice(PHASES)
        B = tuple(rng.randrange(19) for _ in range(rng.randrange(7)))
        if B and B[0] == 0:
            B = (rng.randrange(1, 19),) + B[1:]
        A = tuple(rng.randrange(19) for _ in range(rng.randrange(7)))
        half = tuple(rng.randrange(19) for _ in range(rng.randrange(5)))
        middle = (2*rng.randrange(10),) if rng.randrange(2) else ()
        C = half + middle + half[::-1]
        s, _, _ = trim(c, B, A, C)
        check(s)
        random_count += 1
    assert small == 28512 and controls == 100536 and random_count == RANDOM_STATES
    print(json.dumps({
        'status': 'PASS',
        'scope': 'finite formula controls, including literal ordinary-integer reverse-and-add',
        'small_trimmed_states': small,
        'small_catalog': 'all eight periodic phases; B,A,C length <=1; C empty or even singleton',
        'random_states': random_count,
        'random_seed': RANDOM_SEED,
        'gap_pairs': GAPS,
        'ordinary_integer_controls': controls,
        'overflow_controls': overflows,
        'canonical_case_stream_sha256': digest.hexdigest(),
        'implementation_sha256': hashlib.sha256(Path(__file__).with_name('complementary_bulk.py').read_bytes()).hexdigest(),
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'periodic_cycle_search': False,
        'lychrel_conclusion': None,
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
