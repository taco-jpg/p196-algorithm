#!/usr/bin/env python3
"""Agent 103 T10: independent decimal B-cycle reproduction for G in {2,4}.

At one spatial cut, each phase records low carry L, reverse carry requirement H,
and (only on overflow phases) previous-column reverse digit Y.  For a column
coefficient a and guessed deeper reverse carry z, the independent constraints are

    divmod(a+z,10).quotient = H
    a_next = (a+L)%10 + (Y if overflow else (a+z)%10).

The next spatial cut records floor((a+L)/10), z, and (a+z)%10 where needed.
Temporal coefficient closure is imposed after one complete phase cycle.  The
physical first column requires a>0 at EVERY phase; ordinary later columns allow
a=0.  The first-column flag is kept separate from the ordinary visited-state set.
An accepting neutral cut has L+H=1 and Y=9L on every overflow phase.

No imports from repository solvers.  All necklaces are tested directly; no head
prefilter, depth limit, or assumed periodicity reduction is used.  State/time
caps produce explicit UNDECIDED and nonzero exit status.
"""
import argparse
import itertools
import json
from math import isfinite
import resource
import time


def necklaces(length, weight):
    for ones in itertools.combinations(range(length), weight):
        values = [0] * length
        for t in ones:
            values[t] = 1
        word = tuple(values)
        if all(word <= word[k:] + word[:k] for k in range(1, length)):
            yield word


class ColumnSystem:
    def __init__(self, overflow):
        self.g = overflow
        self.p = len(overflow)
        self.shifts = []
        shift = 0
        self.accept_shift = []
        for bit in overflow:
            self.shifts.append(shift)
            self.accept_shift.append(shift)
            shift += 6 if bit else 2
        self.width = shift
        self.initial = sum(((bit << 1) | (4 if bit else 0)) << k
                           for bit, k in zip(overflow, self.shifts))

    def transitions(self, state, positive=False):
        # Store the entire next interface in one Python arbitrary-precision int.
        # Per phase: L at bit 0, H at bit 1, Y at bits 2..5 if overflow.
        data = []
        for bit, shift in zip(self.g, self.shifts):
            block = state >> shift
            data.append((block & 1, (block >> 1) & 1,
                         (block >> 2) & 15 if bit else None))
        choices = []
        for t, (low, high, prev_digit) in enumerate(data):
            table = []
            for a in range(19):
                options = []
                if not positive or a:
                    nextlow, lowdigit = divmod(a + low, 10)
                    for deeper in range(2):
                        required, highdigit = divmod(a + deeper, 10)
                        if required != high:
                            continue
                        b = lowdigit + (highdigit if prev_digit is None else prev_digit)
                        code = nextlow | (deeper << 1)
                        if prev_digit is not None:
                            code |= highdigit << 2
                        options.append((b, code << self.shifts[t]))
                table.append(options)
            choices.append(table)
        emitted = set()
        # The DFS uses independently derived local tables, not normalization calls.
        for anchor in range(1 if positive else 0, 19):
            stack = [(0, anchor, 0)]
            while stack:
                phase, coefficient, packed = stack.pop()
                if phase == self.p:
                    if coefficient == anchor:
                        emitted.add(packed)
                    continue
                for b, chunk in choices[phase][coefficient]:
                    stack.append((phase + 1, b, packed | chunk))
        return emitted

    def accepting_carry(self, state):
        carry = []
        for bit, shift in zip(self.g, self.shifts):
            block = state >> shift
            low, high = block & 1, (block >> 1) & 1
            if low + high != 1:
                return None
            if bit and (block >> 2) & 15 != 9 * low:
                return None
            carry.append(str(low))
        return ''.join(carry)

    def exhaust(self, state_cap, seconds):
        start_time = time.monotonic()
        frontier = self.transitions(self.initial, positive=True)
        seen = set(frontier)
        depth, edge_count = 1, len(frontier)
        accepted = {}
        returned_initial = self.initial in seen
        while frontier:
            future = set()
            for state in frontier:
                e = self.accepting_carry(state)
                if e is not None:
                    accepted.setdefault(e, depth)
                successors = self.transitions(state)
                edge_count += len(successors)
                future.update(successors - seen)
                if len(seen) + len(future) > state_cap:
                    return {'status': 'CAPPED-UNDECIDED', 'depth': depth,
                            'states': len(seen) + len(future), 'accepted': accepted}
                if time.monotonic() - start_time > seconds:
                    return {'status': 'TIMEOUT-UNDECIDED', 'depth': depth,
                            'states': len(seen) + len(future), 'accepted': accepted}
            if self.initial in future:
                returned_initial = True
            seen.update(future)
            frontier = future
            depth += 1
        return {'status': 'EXHAUSTED', 'depth': depth, 'states': len(seen) + 1,
                'edges': edge_count, 'accepted': accepted,
                'initial_boundary_revisited': returned_initial,
                'seconds': round(time.monotonic() - start_time, 6)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--g')
    parser.add_argument('--cap', type=int, default=1_000_000)
    parser.add_argument('--seconds', type=float, default=600)
    args = parser.parse_args()
    if args.cap < 1 or not isfinite(args.seconds) or args.seconds <= 0:
        parser.error('positive state cap and finite positive seconds required')
    if args.g is not None:
        if not args.g or any(ch not in '01' for ch in args.g):
            parser.error('--g must be a nonempty binary word')
        words = [tuple(int(x) for x in args.g)]
    else:
        words = (g for weight in (2, 4) for p in range(weight, 4 * weight + 1)
                 for g in necklaces(p, weight))
    tally = {}
    cases = 0
    states_total = 0
    accepts = []
    max_record = None
    initial_revisits = 0
    start_time = time.monotonic()
    for word in words:
        text = ''.join(map(str, word))
        result = ColumnSystem(word).exhaust(args.cap, args.seconds)
        result.update(g=text, P=len(word), G=sum(word))
        print(json.dumps(result, sort_keys=True), flush=True)
        cases += 1
        states_total += result['states']
        tally[result['status']] = tally.get(result['status'], 0) + 1
        initial_revisits += result.get('initial_boundary_revisited', False)
        if result['accepted']:
            accepts.append((text, result['accepted']))
        if max_record is None or result['states'] > max_record['states']:
            max_record = result
    summary = dict(cases=cases, statuses=tally, accepted=accepts,
                   total_states=states_total, max_case=max_record,
                   initial_boundary_revisited_cases=initial_revisits,
                   seconds=round(time.monotonic() - start_time, 6),
                   peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print('SUMMARY ' + json.dumps(summary, sort_keys=True), flush=True)
    return 0 if tally.get('EXHAUSTED', 0) == cases else 2


if __name__ == '__main__':
    raise SystemExit(main())
