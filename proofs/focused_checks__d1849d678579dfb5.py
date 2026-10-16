"""Exact minimal collision and concrete failed closure obligation.

No discovery code or carry transducer is imported. All dynamical statements
use ordinary integer reversal and addition.
"""
from pathlib import Path
import hashlib
import itertools
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT/'main_existence_attempt/return_pass/language'
nfa_path = SOURCE/'safe_image2_nfa.json'
d4_path = SOURCE/'observation_depth4.json'
nfa = json.loads(nfa_path.read_text())
d4 = json.loads(d4_path.read_text())
edges = [dict(row) for row in nfa['transitions']]


def classify(p):
    subset = set(nfa['initial'])
    state = 0
    for q in p:
        subset = {v for u in subset for v in edges[u].get(q, ())}
        state = d4['delta'][state][q]
    return tuple(sorted(subset)), state


def integer(p, c):
    digits = [max(0, q-9) for q in p]
    if c is not None:
        digits.append(c//2)
    digits.extend(min(9, q) for q in reversed(p))
    return sum(d*10**i for i, d in enumerate(digits))


def reverse(n):
    out = 0
    while n:
        out = 10*out+n%10
        n //= 10
    return out


def folded(n):
    digits = str(n)
    return (tuple(int(digits[i])+int(digits[-1-i]) for i in range(len(digits)//2)),
            None if len(digits)%2 == 0 else 2*int(digits[len(digits)//2]))


def first_hit(n, limit):
    for h in range(1, limit+1):
        n += reverse(n)
        if n == reverse(n):
            return h
    return None


def safe2(n):
    p, c = folded(n)
    subset, unused = classify(p)
    j = 0 if c is None else c//2+1
    return any(nfa['terminal_masks'][u] >> j & 1 for u in subset)


# Minimal prefix in the exact full-configuration / D4 class of trace25.
n = 196
for _ in range(25):
    n += reverse(n)
assert n == 8801197801088
target, c = folded(n)
assert c == 14 and classify(target) == ((364,), 74)
witness = (18, 17, 17)
assert classify(witness) == classify(target)
assert first_hit(integer(witness, c), 10) == 10
checked = 0
matches_by_length = {}
for length in range(4):
    words = [()] if length == 0 else (
        (q,)+tail for q in range(1, 19)
        for tail in itertools.product(range(19), repeat=length-1))
    matches = []
    for p in words:
        checked += 1
        if classify(p) == classify(target):
            matches.append(p)
    matches_by_length[length] = matches
assert checked == 6859 == 1+18+18*19+18*19**2
assert matches_by_length == {0:[], 1:[], 2:[], 3:[witness]}
# D4 equality proves all observation refinements through depth four agree.
# Changing only the final center to zero separates at depth five.
left_context_integer = integer(target, 0)
right_context_integer = integer(witness, 0)
assert first_hit(left_context_integer, 6) == 6
assert first_hit(right_context_integer, 6) is None

# Test the concrete natural candidate F10 = S2 intersect words whose first
# eleven reverse-add outputs are nonpalindromes. It contains196 tails once
# they have safe-two ancestry, but the following actual closure fails.
closure_input = 9948
closure_output = closure_input+reverse(closure_input)
assert closure_output == 18447
assert safe2(closure_input) and safe2(closure_output)
assert first_hit(closure_input, 12) == 12
assert first_hit(closure_output, 11) == 11
# Width minimality is independently checked on ordinary integers, including
# every digit splitting, rather than relying on pair-representative counts.
smaller_closure_failures = [n for n in range(1, 1000)
                            if safe2(n) and first_hit(n, 12) == 12]
assert not smaller_closure_failures
result = dict(
    status='INDEPENDENT_FOCUSED_OBSTRUCTIONS_VERIFIED',
    nfa_sha256=hashlib.sha256(nfa_path.read_bytes()).hexdigest(),
    observer4_sha256=hashlib.sha256(d4_path.read_bytes()).hexdigest(),
    minimal_d4_collision=dict(trace_step=25, trace_integer=str(n),
        target_pairs=target, center=14, subset=[364], observer4_state=74,
        witness_pairs=witness, witness_integer=str(integer(witness, 14)),
        first_palindrome=10, canonical_prefixes_enumerated=checked,
        matches_by_pair_length=matches_by_length,
        minimum_pair_length=3, unique_at_minimum=True),
    first_separating_observation_depth=5,
    separating_context=dict(pair_suffix=[], center=0,
        left_integer=str(left_context_integer), right_integer=str(right_context_integer),
        left_first_palindrome=6, right_first_six_outputs_palindromic=False),
    failed_closure_candidate=dict(name='S2_and_first_11_outputs_nonpalindromic',
        input=str(closure_input), output=str(closure_output),
        input_in_S2=True, output_in_S2=True, input_first_palindrome=12,
        output_first_palindrome=11, input_accepted=True, output_accepted=False,
        smallest_possible_input_width=4, smaller_integers_checked=999,
        smaller_counterexamples=smaller_closure_failures),
    positive_invariant_found=False)
(HERE/'focused_checks.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result), flush=True)
