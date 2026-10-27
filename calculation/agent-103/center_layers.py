#!/usr/bin/env python3
"""Agent103: independent finite layer audit of the p11 decimal center exclusion.

The generic layer relation is re-derived from the normalization equations,
not imported from cauto_fast. It is an independent implementation of the same
mathematical model. The default run checks every finite tail and exact generic
frontier equality, then compares the solver with direct small-word enumeration
and two known-source positive mechanisms (with a transported control each).

The all-trim interpretation uses the neutral-padding/schedule-transport results
of Agents 7 and 107; the balanced-gauge corollary is credited to Agent110.
The transport helper below is only a positive-control fixture, not a competing
claim of that theorem. No base-10 existence or Lean verification is asserted.
"""
import hashlib
import itertools
import json
import sys
from pathlib import Path

def normalize(base, word, entry):
    digits = []
    carry = entry
    for coeff in word:
        carry, digit = divmod(coeff + carry, base)
        digits.append(digit)
    return digits, carry


def raw_center(base, word, entry, overflow):
    d, exit_carry = normalize(base, word, entry)
    if exit_carry != 1 - entry:
        return None
    if overflow:
        d.append((base - 1) * entry)
    return [x + y for x, y in zip(d, reversed(d))]


def pad(base, word, count):
    return [base - 1] * count + list(word) + [base - 1] * count


class CenterLayers:
    """Outside-in layer constraints re-derived from normalization equations.

    State at each time is (left incoming carry, right outgoing carry,
    previous right digit if this time overflows, pending shifted coefficient
    if this time trims).  Whole-word widths enter only at the middle boundary.
    """
    def __init__(self, base, e, g, v):
        self.base, self.e, self.g, self.v = base, tuple(e), tuple(g), tuple(v)
        self.period = len(self.e)
        if not self.period or not (len(self.g) == len(self.v) == self.period):
            raise ValueError('bad period')
        if any(x not in (0, 1) for x in self.e + self.g + self.v):
            raise ValueError('binary streams and trim schedule required')
        if sum(self.g) != 2 * sum(self.v) or not sum(self.v):
            raise ValueError('unbalanced or zero trim schedule')
        self.segments = []
        for end in range(self.period):
            if not self.v[end]:
                continue
            start = (end + 1) % self.period
            times = [start]
            while not self.v[times[-1]]:
                times.append((times[-1] + 1) % self.period)
            self.segments.append(tuple(times))
        self.cache = {}

    def initial(self):
        return tuple((self.e[t], 1 - self.e[t],
                      (self.base - 1) * self.e[t] if self.g[t] else -1, -1)
                     for t in range(self.period))

    def widths(self, m0):
        result = [m0]
        for t in range(self.period - 1):
            result.append(result[-1] + self.g[t] - 2 * self.v[t])
        if min(result) < 1:
            return None
        return result

    def _segment_choices(self, times, state, types, first_layer):
        # type: 0 generic pair; 1 odd middle; 2 even middle;
        #       3 overflow-created middle; 4 inactive.
        key = (times, tuple(state[t][:3] for t in times), state[times[-1]][3],
               tuple(types[t] for t in times), first_layer)
        if key in self.cache:
            return self.cache[key]
        b, h = self.base, self.base - 1
        results = []
        need = h if first_layer else state[times[-1]][3]

        def visit(k, coeff, start_coeff, assignments):
            t = times[k]
            left, right, previous_digit, pending = state[t]
            kind = types[t]
            branches = []
            if kind <= 2:
                if not 0 <= coeff <= 2 * h:
                    return
                left_out, left_digit = divmod(coeff + left, b)
                if kind == 1:
                    if left_out != right:
                        return
                    out_coeff = (left_digit + previous_digit if self.g[t]
                                 else 2 * left_digit)
                    branches.append((left_out, right, left_digit, out_coeff))
                else:
                    for inward in ((left_out,) if kind == 2 else (0, 1)):
                        right_out, right_digit = divmod(coeff + inward, b)
                        if right_out != right:
                            continue
                        out_coeff = left_digit + (previous_digit if self.g[t] else right_digit)
                        branches.append((left_out, inward, right_digit, out_coeff))
            else:
                if coeff != -1:
                    return
                branches.append((left, right, previous_digit,
                                 2 * previous_digit if kind == 3 else -1))
            for lo, ri, digit, cp in branches:
                triple = (lo, ri, digit if self.g[t] else -1)
                assigned = assignments + ((t, triple),)
                if k + 1 == len(times):
                    if cp == need:
                        results.append((start_coeff, assigned))
                else:
                    visit(k + 1, cp, start_coeff, assigned)

        allowed = range(2 * h + 1) if types[times[0]] <= 2 else (-1,)
        for c0 in allowed:
            visit(0, c0, c0, ())
        results = tuple(results)
        self.cache[key] = results
        return results

    def advance(self, frontier, types=None, first_layer=False):
        if types is None:
            types = (0,) * self.period
        output = set()
        for state in frontier:
            pieces = [self._segment_choices(times, state, types, first_layer)
                      for times in self.segments]
            if any(not opts for opts in pieces):
                continue
            for selected in itertools.product(*pieces):
                target = [list(x) for x in state]
                for times, (start_coeff, assignments) in zip(self.segments, selected):
                    for t, triple in assignments:
                        target[t][:3] = triple
                    target[(times[0] - 1) % self.period][3] = start_coeff
                output.add(tuple(tuple(x) for x in target))
        return output

    def fixed_width(self, m0):
        widths = self.widths(m0)
        if widths is None:
            return {'m0': m0, 'valid_widths': False, 'counts': [], 'feasible': False}
        halfs = [(m + 1) // 2 for m in widths]
        out_halfs = [(m + g + 1) // 2 for m, g in zip(widths, self.g)]
        frontier = {self.initial()}
        counts = [1]
        for j in range(max(out_halfs)):
            types = []
            for m, half, out_half in zip(widths, halfs, out_halfs):
                if j < half - 1:
                    types.append(0)
                elif j == half - 1:
                    types.append(1 if m % 2 else 2)
                else:
                    types.append(3 if j < out_half else 4)
            frontier = self.advance(frontier, tuple(types), j == 0)
            counts.append(len(frontier))
            if not frontier:
                break
        return {'m0': m0, 'valid_widths': True, 'counts': counts,
                'feasible': bool(frontier)}


def check_period11_layers():
    machine = CenterLayers(10, map(int, '10100110011'), map(int, '11100010000'),
                           map(int, '11000000000'))
    frontier = {machine.initial()}
    generic = []
    sets = [frontier]
    for j in range(5):
        frontier = machine.advance(frontier, first_layer=(j == 0))
        digest = hashlib.sha256(repr(sorted(frontier)).encode()).hexdigest()
        generic.append({'layer': j + 1, 'states': len(frontier), 'sha256': digest})
        sets.append(frontier)
    if sets[4] != sets[5]:
        raise AssertionError('generic frontier did not stabilize at layer 4')
    finite = [machine.fixed_width(m) for m in range(1, 13)]
    if any(row['feasible'] for row in finite):
        raise AssertionError('unexpected p11 center')
    return {'generic_layers': generic, 'fixed_frontier_layer': 4,
            'finite_tails': finite, 'tail_classes': [11, 12],
            'conclusion': 'p11 specified e/g: no symmetric center of any length'}


def brute_closed(base, e, g, v, m0):
    for half in itertools.product(range(2 * base - 1), repeat=(m0 + 1) // 2):
        original = list(half) + list(half[:m0 // 2][::-1])
        current = original
        for entry, overflow, trim in zip(e, g, v):
            current = raw_center(base, current, entry, overflow)
            if current is None or len(current) <= 2 * trim:
                break
            if any(x != base - 1 for x in current[:trim] + (current[-trim:] if trim else [])):
                break
            if trim:
                current = current[trim:-trim]
        else:
            if current == original:
                return True
    return False


def positive_controls():
    # The core solver is standard-library-only. Source certificate parsing is
    # used only by these integration controls.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import neutral_band_search as mirror
    checked = []
    for base, original in mirror._lean_certs():
        if base not in (2, 26):
            continue
        e = [mirror.e1(base, edge[0]) for edge in original]
        g = [mirror.gam(base, edge[0], edge[1]) for edge in original]
        old_v = [edge[5] for edge in original]
        for target in (old_v, [int(t == 0) for t in range(len(original))]):
            heights = [0]
            for previous, desired in zip(old_v, target):
                heights.append(heights[-1] + previous - desired)
            if heights[-1] != 0:
                raise AssertionError('unbalanced positive-control schedule')
            shift = -min(heights)
            heights = [h + shift for h in heights[:-1]]
            edges = []
            for t, (B, C, B2, C2, u, v) in enumerate(original):
                edges.append((B, pad(base, C, heights[t]), B2,
                              pad(base, C2, heights[(t + 1) % len(original)]),
                              u, target[t]))
            if not mirror.cycleOK(base, edges, edges[0][0], edges[0][1]):
                raise AssertionError('invalid transported source control')
            result = CenterLayers(base, e, g, target).fixed_width(len(edges[0][1]))
            if not result['feasible']:
                raise AssertionError(('known positive rejected', base, target))
            checked.append({'base': base, 'v': target, 'm0': len(edges[0][1]),
                            'frontiers': result['counts']})
    return checked


def selftest():
    checked = positives = 0
    for base in (2, 3):
        for P in ((2, 3, 4) if base == 2 else (2, 3)):
            for gs in itertools.product((0, 1), repeat=P):
                if sum(gs) != 2:
                    continue
                for es in itertools.product((0, 1), repeat=P):
                    for trim_time in range(P):
                        vs = [int(t == trim_time) for t in range(P)]
                        machine = CenterLayers(base, es, gs, vs)
                        for m0 in range(1, 6):
                            expected = brute_closed(base, es, gs, vs, m0)
                            actual = machine.fixed_width(m0)['feasible']
                            if expected != actual:
                                raise AssertionError(('layer/brute mismatch',
                                                      base, es, gs, vs, m0,
                                                      expected, actual))
                            checked += 1
                            positives += int(expected)
    return {'exhaustive_direct_cases': checked,
            'direct_positive_cases': positives,
            'known_source_controls': positive_controls()}


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if mode not in ('all', 'p11', 'selftest'):
        raise SystemExit('usage: center_layers.py [all|p11|selftest]')
    if mode in ('all', 'p11'):
        print(json.dumps(check_period11_layers(), sort_keys=True))
        print('P11 ALL-WIDTH CENTER LAYER AUDIT PASSED (COMPUTED)')
    if mode in ('all', 'selftest'):
        print(json.dumps(selftest(), sort_keys=True))
        print('CENTER LAYER SELFTEST PASSED')
