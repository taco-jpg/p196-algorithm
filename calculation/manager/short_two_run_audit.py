#!/usr/bin/env python3
"""Independent exact decimal-prefix audit for literal two-run short returns.

Reuses the mathematical relation of the existing Lean PrefixModel and
SevenColumnProjection.forwardPrefix. No A120 terminal-neutral boundary is
imposed. Every negative is a finite-prefix computation, not a Lean claim.
"""
import argparse
import ast
from itertools import product
import re
from pathlib import Path
import json
import time


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def explicit_three(s, e):
    a, b, c = s
    l1, d0 = divmod(a, 10)
    l2, d1 = divmod(b + l1, 10)
    d2 = (c + l2) % 10
    r2, h2 = divmod(c + e, 10)
    r1, h1 = divmod(b + r2, 10)
    g, h0 = divmod(a + r1, 10)
    return ((d0 + h0, d1 + h1, d2 + h2) if not g
            else (d0 + 1, d1 + h0, d2 + h1)), g


def folded(s, e):
    low, carry = [], 0
    for coefficient in s:
        carry, digit = divmod(coefficient + carry, 10)
        low.append(digit)
    high, carry = [0] * len(s), e
    for j in range(len(s) - 1, -1, -1):
        carry, high[j] = divmod(s[j] + carry, 10)
    g = carry
    partner = high if not g else [1] + high[:-1]
    return tuple(x + y for x, y in zip(low, partner)), g


def ordinary_completion(s, e):
    """Realize one arbitrary prefix/carry edge by a canonical ordinary integer.

    Two equal middle pair columns, 0 or 18, force the specified inward carry.
    This checks individual edges; it does not claim simultaneous orbit lifting.
    """
    half = tuple(s) + (18 * e,)
    digits = [max(x - 9, 0) for x in half]
    digits += [min(x, 9) for x in reversed(half)]
    n = sum(x * 10**j for j, x in enumerate(digits))
    require(len(str(n)) == len(digits), 'completion is not canonical')
    m = n + int(str(n)[::-1])
    target = tuple(map(int, str(m)[::-1]))
    result = tuple(target[i] + target[-1-i] for i in range(len(s)))
    return result, len(target) - len(digits)


def local_controls():
    checked = 0
    for a in range(1, 19):
        for b, c, e in product(range(19), range(19), (0, 1)):
            s = (a, b, c)
            expected = ordinary_completion(s, e)
            require(explicit_three(s, e) == expected, 'explicit3/numeric mismatch')
            require(folded(s, e) == expected, 'folded/numeric mismatch')
            checked += 1
    # Every root extension used in the independent direct fifth-column check.
    for x, y, e in product(range(19), range(19), (0, 1)):
        s = (1, 4, 4, x, y)
        require(folded(s, e) == ordinary_completion(s, e), 'prefix5/numeric mismatch')
        checked += 1
    return checked


def three_column_census():
    states = [(a, b, c) for a in range(1, 19)
              for b in range(19) for c in range(19)]
    graph = {s: tuple((e, *explicit_three(s, e)) for e in (0, 1)) for s in states}
    hits = {p: {} for p in range(4, 9)}
    for source in states:
        frontier = {(source, 0): ()}
        for p in range(1, 9):
            future = {}
            for (current, overflow), inputs in frontier.items():
                for e, target, g in graph[current]:
                    if overflow + g <= 2:
                        future.setdefault((target, overflow + g), inputs + (e,))
            frontier = future
            if p in hits and (source, 2) in frontier:
                hits[p][source] = frontier[source, 2]
    expected5 = {(1, 4, 4), (2, 8, 8), (4, 16, 17), (9, 13, 15), (10, 3, 10)}
    require(set(hits[5]) == expected5, 'unexpected period-five prefix orbit')
    require(not hits[4] and not hits[6] and not hits[7], 'unexpected short return')
    return {p: {'returning_prefixes': len(rows),
                'witnesses': [{'prefix': s, 'inputs': e} for s, e in sorted(rows.items())]}
            for p, rows in hits.items()}


def direct_cycles_from_root(root, period=5, overflow=2):
    result = set()
    for inputs in product((0, 1), repeat=period):
        rows, gs = [root], []
        for e in inputs:
            target, g = folded(rows[-1], e)
            rows.append(target)
            gs.append(g)
        if rows[-1] == root and sum(gs) == overflow:
            result.add((tuple(rows[:-1]), inputs, tuple(gs)))
    return result


def extend_correlated(state):
    rows, incoming, gs = state
    period = len(rows)
    lows, old_high_digits = [], []
    for row, e in zip(rows, incoming):
        carry = 0
        for x in row:
            carry = (x + carry) // 10
        lows.append(carry)
        old_high_digits.append((row[-1] + e) % 10)
    result = set()
    for anchor in range(19):
        todo = [(0, anchor, (), ())]
        while todo:
            t, x, coefficients, inputs = todo.pop()
            if t == period:
                if x == anchor:
                    target = tuple(row + (y,) for row, y in zip(rows, coefficients))
                    require(all(folded(target[i], inputs[i]) ==
                                (target[(i+1) % period], gs[i]) for i in range(period)),
                            'full-prefix replay rejected an extension')
                    result.add((target, inputs, gs))
                continue
            for inner in (0, 1):
                if (x + inner) // 10 != incoming[t]:
                    continue
                nxt = (x + lows[t]) % 10
                nxt += old_high_digits[t] if gs[t] else (x + inner) % 10
                todo.append((t + 1, nxt, coefficients + (x,), inputs + (inner,)))
    return result


def period_five_extension():
    root = (1, 4, 4)
    states = direct_cycles_from_root(root)
    require({s[1] for s in states} ==
            {(0, 1, 0, x, y) for x, y in product((0, 1), repeat=2)},
            'not all four correlated third-column carry words are present')
    records = {3: sorted(states)}
    for width in (4, 5, 6):
        future = set()
        for state in states:
            future.update(extend_correlated(state))
            require(len(future) <= 100000, 'CAPPED-UNDECIDED')
        states = future
        records[width] = sorted(states)
    direct4, direct5 = set(), set()
    for suffix in product(range(19), repeat=1):
        direct4.update(direct_cycles_from_root(root + suffix))
    for suffix in product(range(19), repeat=2):
        direct5.update(direct_cycles_from_root(root + suffix))
    require(direct4 == set(records[4]), 'direct fourth-column comparison failed')
    require(direct5 == set(records[5]), 'direct fifth-column comparison failed')
    require(len(records[4]) == 12 and not records[5], 'unexpected extension result')
    return {'levels': {k: {'prefix_and_input_states': len(v),
                          'distinct_temporal_prefixes': len({s[0] for s in v}),
                          'states': v} for k, v in records.items()},
            'direct_initial_words_tested': {4: 19, 5: 361},
            'temporal_input_words_per_initial': 32, 'status': 'EXHAUSTED'}


def hierarchical_catalogs():
    """Regenerate complete temporal rows and compare every Lean data literal."""
    def choices(p, q, x):
        outputs = [folded(p + (x,), e)[0] for e in (0, 1)]
        return sorted({out[-1] for out in outputs if out[:-1] == q})

    def extensions(rows):
        result = []
        for initial in range(19):
            todo = [(0, initial, ())]
            while todo:
                t, x, prefix = todo.pop()
                prefix += (rows[t] + (x,),)
                if t + 1 == len(rows):
                    if prefix[0] == prefix[-1] and prefix[0][0] > 0:
                        result.append(prefix)
                else:
                    for y in reversed(choices(rows[t], rows[t+1], x)):
                        todo.append((t+1, y, prefix))
        return result

    def weight(rows):
        return sum(int(a[0] >= 10 or (a[0] == 9 and b[0] == 10))
                   for a, b in zip(rows, rows[1:]))

    source = (Path(__file__).resolve().parents[2] / 'lean/P196' /
              'ManagerShortTwoRunReturns/ShortCatalog.lean').read_text()
    literal = {(int(p), int(k)): ast.literal_eval(data) for p, k, data in
               re.findall(r'def catalog(\d+)_(\d+) : List Rows :=\n  (\[[^\n]*\])', source)}
    expected = {5: (10, 5, 5, 20, 0), 6: (12, 3, 0), 7: (7, 0)}
    observed = {}
    for period, counts in expected.items():
        rows = [((),) * (period + 1)]
        observed[period] = []
        for columns, count in enumerate(counts, 1):
            rows = [out for old in rows for out in extensions(old) if weight(out) == 2]
            require(len(rows) == count, 'hierarchical count mismatch')
            decoded = json.loads(json.dumps(rows))
            require(decoded == literal.get((period, columns)), 'Lean catalog literal mismatch')
            observed[period].append(len(rows))
    require(len(literal) == 10, 'unexpected Lean catalog coverage')
    return observed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Optional detailed JSON audit output')
    args = parser.parse_args()
    started = time.monotonic()
    output = {'local_numeric_edges': local_controls(),
              'three_column_G2_census': three_column_census(),
              'period_five': period_five_extension(),
              'hierarchical_catalogs': hierarchical_catalogs()}
    # Existing actual seven-step return is a mandatory weight-scope control.
    n = 770
    for _ in range(7):
        n += int(str(n)[::-1])
    require(n == 176176, 'existing ordinary period-seven witness changed')
    output['ordinary_period7_control'] = {'source': 770, 'target': n, 'width_gain': 3}
    output['seconds'] = time.monotonic() - started
    if args.output:
        args.output.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'numeric_local_edges': output['local_numeric_edges'],
                      'G2_returning_prefixes': {p: a['returning_prefixes'] for p, a in
                                               output['three_column_G2_census'].items()},
                      'P5_extension_states': {k: a['prefix_and_input_states'] for k, a in
                                              output['period_five']['levels'].items()},
                      'hierarchical_catalogs': output['hierarchical_catalogs'],
                      'seconds': output['seconds'], 'status': 'EXHAUSTED-PASS'}, sort_keys=True))


if __name__ == '__main__':
    main()
