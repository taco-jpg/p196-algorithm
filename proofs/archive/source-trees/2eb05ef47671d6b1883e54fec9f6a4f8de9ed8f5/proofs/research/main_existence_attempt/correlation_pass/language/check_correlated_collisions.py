"""Independent collision replay; imports no search or transducer module.

Raw observer signatures are reconstructed recursively from entire output
prefixes, rather than discovery state ids or cached transition tables.
"""
from collections import Counter
from functools import lru_cache
from pathlib import Path
import argparse
import hashlib
import itertools
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / 'main_existence_attempt/return_pass/language'


def run(filename):
    source = HERE / filename
    data = json.loads(source.read_text())
    nfa_path = SOURCE / 'safe_image2_nfa.json'
    d4_path = SOURCE / 'observation_depth4.json'
    assert data['nfa_sha256'] == hashlib.sha256(nfa_path.read_bytes()).hexdigest()
    assert data['observer4_sha256'] == hashlib.sha256(d4_path.read_bytes()).hexdigest()
    nfa = json.loads(nfa_path.read_text())
    d4 = json.loads(d4_path.read_text())
    d0 = json.loads((SOURCE/'observation_depth0.json').read_text())
    transition = [dict(row) for row in nfa['transitions']]

    def subset(p):
        states = set(nfa['initial'])
        for q in p:
            out = set()
            for state in states:
                out.update(transition[state].get(q, ()))
            states = out
        return tuple(sorted(states))

    def table_state(table, p):
        state = 0
        for q in p:
            state = table['delta'][state][q]
        return state

    @lru_cache(maxsize=None)
    def signature(depth, p):
        if depth == 4:
            return table_state(d4, p)
        # State stores each still-possible complete high-carry choice. Keep
        # emitted prefixes literally, then independently classify each at
        # the previous observation level. No discovery ids are used.
        paths = {(0, 0, 0, -1, False, ()), (1, 0, 1, 1, False, ())}
        for q in p:
            following = set()
            for overflow, low_carry, high_carry, pending, started, emitted in paths:
                if not started and q == 0:
                    continue
                for inner_high in range(2):
                    if q+inner_high < 10*high_carry or q+inner_high >= 10*(high_carry+1):
                        continue
                    low_digit = (q+low_carry) % 10
                    high_digit = (q+inner_high) % 10
                    output_pair = low_digit + (pending if overflow else high_digit)
                    following.add((overflow, (q+low_carry)//10, inner_high,
                                   high_digit if overflow else -1, True,
                                   emitted+(output_pair,)))
            paths = following
        residuals = frozenset(((h, a, b, pending, started), signature(depth-1, emitted))
                             for h, a, b, pending, started, emitted in paths)
        return table_state(d0, p), residuals

    def reverse(n):
        out = 0
        while n:
            out = 10*out + n%10
            n //= 10
        return out

    def integer(p, c):
        assert (p and 1 <= p[0] <= 18) or (not p and c is not None and c > 0)
        assert all(type(q) is int and 0 <= q <= 18 for q in p)
        assert c is None or c in range(0, 19, 2)
        digits = [max(0, q-9) for q in p]
        if c is not None:
            digits.append(c//2)
        digits.extend(min(9, q) for q in reversed(p))
        return sum(d*10**i for i, d in enumerate(digits))

    def folded(n):
        digits = str(n)
        return (tuple(int(digits[i])+int(digits[-1-i]) for i in range(len(digits)//2)),
                None if len(digits)%2 == 0 else 2*int(digits[len(digits)//2]))

    trace = data['trace']
    n = 196
    for t, row in enumerate(trace):
        assert row['step'] == t and row['integer'] == str(n)
        p, c = folded(n)
        assert list(p) == row['pairs'] and c == row['center']
        assert list(subset(p)) == row['subset']
        n += reverse(n)
    seen = set()
    counts = Counter()
    max_hit = 0
    for row in data['collisions']:
        t, depth = row['trace_step'], row['depth']
        assert (t, depth) not in seen
        seen.add((t, depth))
        target = trace[t]
        p, c = tuple(row['pairs']), row['center']
        tp = tuple(target['pairs'])
        assert c == target['center']
        actual_subset = subset(p)
        assert actual_subset == subset(tp) == tuple(row['subset'])
        assert signature(depth, p) == signature(depth, tp)
        # Current S2 acceptance is checked as a property of the COMPLETE
        # subset and center, rather than only of one chosen terminal path.
        j = 0 if c is None else c//2+1
        assert any(nfa['terminal_masks'][u] >> j & 1 for u in actual_subset)
        n = integer(p, c)
        for h in range(1, row['first_palindrome']+1):
            n += reverse(n)
            assert (n == reverse(n)) == (h == row['first_palindrome'])
        assert row['first_palindrome'] > depth+1
        max_hit = max(max_hit, row['first_palindrome'])
        counts[depth] += 1
    assert len(seen) == data['excluded_trace_classes']
    for depth, count in counts.items():
        assert data['furthest_excluded_trace_step_by_depth'][str(depth)] == max(
            t for t, k in seen if k == depth)
    completed = data['completed_enumeration_lengths']
    assert completed == list(range(max(completed)+1))
    # Complete enumeration cardinality, independently derived. The corpus
    # is deliberately not deduplicated by the search before candidate count.
    corpus = json.loads((ROOT/'main_existence_attempt/ancestry_direct_pass/language/terminal_acceptance_result.json').read_text())
    if data['status'] == 'BOUNDED_REFINEMENT_COMPLETE_NO_INVARIANT':
        enumeration = 1 + sum(18 * 19**(length-1) for length in completed if length)
        assert data['candidates'] == enumeration + len(corpus['proofs'])
    else:
        enumeration = None
    result = dict(status='INDEPENDENT_COMPLETE_COLLISION_REPLAY_VERIFIED',
                  collision_count=len(seen), counts_by_depth=dict(sorted(counts.items())),
                  largest_first_palindrome=max_hit,
                  checked_196_trace_words=len(trace),
                  completely_enumerated_pair_prefixes=enumeration,
                  raw_signature_cache_entries=signature.cache_info().currsize,
                  nfa_sha256=hashlib.sha256(nfa_path.read_bytes()).hexdigest(),
                  observer4_sha256=hashlib.sha256(d4_path.read_bytes()).hexdigest(),
                  certificate_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  positive_invariant_found=False, global_family_status='UNKNOWN')
    out = HERE / (source.stem+'_audit.json')
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', default='correlated_cegar_result.json')
    args = parser.parse_args()
    run(args.certificate)
