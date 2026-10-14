# Correlated language return pass — final status

**No decimal Lychrel witness or positive inductive language was found.**
Eight fixed transition-table families were completely excluded, with an
independent ordinary-integer replay of every class-elimination witness.
The last safe-ancestry refinement remains **UNKNOWN**. All subprocesses have
stopped. No original research file outside this directory was modified.

The method and proof are in `METHOD_AND_PROOF.md`. Unlike the excluded moving
suffix operation, this method retains full-word right-context information
and reconstructs output through complete carry paths. It is not an additive,
group, XOR, or allowed-one-tile score. Each completed kernel search permits
**every choice of terminal acceptance flags on its fixed transition table**.

| Transition table | Pair states | Canonical terminal classes | Complete product states | Result |
|---|---:|---:|---:|---|
| Observation D0 | 5 | 42 | 103 | Empty kernel |
| Observation D1 | 38 | 405 | 959 | Empty kernel |
| Observation D2 | 533 | 5,850 | 13,622 | Empty kernel |
| Observation D3 | 7,813 | 85,930 | 113,813 | Empty kernel |
| Observation D4 | 75,311 | 828,408 | 1,167,291 | Empty kernel |
| D0 × ordinary image-one context | 621 | 6,818 | 172,899 | Empty kernel |
| D1 × ordinary image-one context | 3,950 | 43,437 | 1,093,189 | Empty kernel |
| D0 × safe image-one context | 649 | 7,126 | 182,258 | Empty kernel |

All **978,016** listed class exclusions were independently replayed by
`check_eliminations.py`, which imports neither discovery code nor the carry
transducer. It verifies actual integer reversal/addition and separately
checks complete canonical-class coverage in each saved transition table.
These are all-length exclusions of these eight tables, not exclusions of
all automata of these sizes and not termination claims about any seed.

The completed D4 proof has 792,894 arithmetic implication witnesses and
35,514 direct palindrome roots; its largest elimination rank is ten. Its
75,311-state automaton records the residuals of five palindrome-predecessor
observations, at times 0 through 4. Independent implementation controls
covered 22,000 ordinary integer words at each observation depth.

The original D4 500,000-state and image-refined D1 1,000,000-state cap records
remain saved with UNKNOWN status. Separate compact continuations completed
both products in 21.65 and 11.38 seconds respectively. Report fields for
unknown live-class counts are null. Earlier raw progress logs printed zero
for a missing field; that is not a computed empty kernel and is superseded
by the explicit reports and completed continuations.

## Exact splice and tested ancestry repair

D4 identifies the pair word of 1675, `((6,13), no center)`, with
`((5,0,5,13,17), no center)`. Both reach pair state 125. The saved obstruction
chain exploits this and other equalities; it switches between different
integers within classes and is not an ordinary orbit of 196.

The latter word's canonical realization, 5,059,984,000, is not itself a
reverse-add output. However another realization has genuine ancestry:

`1,513,900,000 → 1,513,993,151 → 3,027,986,302`.

Both ordinary one-step and two-step image membership therefore retain the
splice. The middle integer is a palindrome. Exact inverse enumeration found
unique predecessor pair words `(2,10,2,6,18)` and then `(1,5,1,3,9)`, all of
even length with no center. Root independently confirmed this uniqueness by
enumerating all 3,580,398 canonical words of the possible input lengths using
ordinary integer arithmetic (`root_inverse_audit.cpp` and its JSON result).

Define `S0=Canonical` and `S_(r+1)=G(S_r minus B)`. This enforces palindrome
avoidance at every prior generating step. The known splice belongs to S1
but **does not belong to S2**. Thus safe two-step ancestry demonstrably repairs
this particular information loss. This is a concrete positive separation,
not an inductive Lychrel certificate.

The S1 image DFA was completed: 54 NFA states, 595 subset states, 475 states
after minimization. Its D0 product has the independently excluded 7,126-class
kernel above.

For S2, the exact output NFA was completed and saved as
`safe_image2_nfa.json`: 6,746 raw states, 6,680 useful states. The first
determinization hit 100,000 subsets. A separate bounded continuation reached
**1,000,000 discovered subsets, with 232,512 processed**, in 13.69 seconds;
the largest processed subset had 43 NFA states. Its stated limits were
1,000,000 subsets and 240 seconds. It stopped at the subset cap, so no S2 DFA
kernel was computed. The status is **UNKNOWN**, with no surviving-class or
nonexistence claim. The completed NFA and code are retained; the enormous
incomplete subset scratch was not retained. No further refinement followed.

The remaining positive problem is precise: obtain and verify a nonempty
safe forward-closed language retaining enough safe-ancestry correlations.
Removing the exhibited splice alone does not establish this. The present
S2 NFA supplies an exact regular constraint, not a claimed invariant.

## Source reproduction

Run from the project root. The saved cap results and the completed extended
results are separate files.

```sh
python3 main_existence_attempt/return_pass/language/residual_kernel.py --max-depth 4 --seconds 180 --product-cap 500000
python3 main_existence_attempt/return_pass/language/compact_kernel.py --depth 4 --cap 3000000 --seconds 300
python3 main_existence_attempt/return_pass/language/check_eliminations.py --max-depth 4 --extended
python3 main_existence_attempt/return_pass/language/image_ancestry.py
python3 main_existence_attempt/return_pass/language/compact_kernel.py --depth 1 --image1 --cap 3000000 --seconds 180
python3 main_existence_attempt/return_pass/language/check_eliminations.py --max-depth 1 --image1 --extended
python3 main_existence_attempt/return_pass/language/safe_ancestry.py
python3 main_existence_attempt/return_pass/language/continue_safe2.py
python3 main_existence_attempt/return_pass/language/check_eliminations.py --max-depth 0 --prefix safe1_
```

The four `independent_replay*` JSON files record source-table and certificate
hashes. The research is not Lean-formalized, externally peer reviewed, or
claimed novel. No solution of decimal Lychrel existence is asserted.
