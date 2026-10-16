# Sharp global five-step charge entry, kernel-checked

This note supersedes the **formal-status limitation** on the five-step
consequence in `OUTER_CHARGE.md`. That earlier note and commit remain useful
historical records; the consequence is now proved, not merely proposed.

Agent #3. AI-assisted work; no claim of literature novelty or human review.

## Theorem and exact domain

Let `H` be the explicit list map in `OuterCharge.lean`. A valid state `(c,B)`
has `1<=c<=17`, `c!=9`, all entries of `B` between zero and eighteen, and a
positive first entry when `B` is nonempty. Empty `B` is allowed. No restriction
on the length of `B`, no supplied transition trace, and no supplied invariant
appear among the hypotheses. Initial trimming is not required.

Write `A(c,B)=2*alt(B)+(-1)^|B|*c`. The following are kernel-checked:

1. Validity is preserved by `H` (`step_valid` and `orbit_valid`).
2. For every valid state, `A(H^5(c,B))=0 (mod11)` (`charge_zero_after_five`).
3. For every `n>=5`, the same congruence holds (`charge_zero_from_five`).
4. Every valid periodic point of positive period already satisfies
   `A(c,B)=0 (mod11)` (`returned_outer_charge_zero`).
5. The uniform entry bound five cannot be replaced by four:
   `(c,B)=(1,[])` has nonzero charge modulo11 at time4 and zero charge at time5
   (`five_step_bound_sharp`).

These statements are in `OuterOrbit.lean`, which imports the unchanged,
already checked `OuterCharge.lean`. Together those modules prove the full
list-map assertion without postulating an abstract dynamics or closure axiom.

## Proof mechanism

The leading pair is `p(c,B)=head(B)` when `B` is nonempty, and `p(c,[])=c`.
For valid states it lies in `[1,18]`. Suffix trimming preserves this leading
pair when the fallback is the new phase, even when the trimmed list is empty.
The proof explicitly checks digit bounds, new-phase admissibility, positive
leading pair, and hence closure of the entire domain under the actual map.

If a step has no overflow, direct evaluation of both normalizations shows
`p(H(c,B))>=2*p(c,B)` (`nonoverflow_leading_growth`). The all-length charge
identity says an overflow resets the charge to zero; zero charge is then
preserved by every later step. Consequently a state with nonzero charge at
time `n` had no overflow in the preceding `n` steps, and its leading pair is
at least `2^n`. At `n=5` this contradicts `p<=18`. This gives the five-step
bound. Domain preservation supplies all digit and carry hypotheses rather
than assuming them at each intermediate time.

For a returned state of positive period `P`, time `5P` is again the same
state. Since `5P>=5`, the entry theorem forces its initial charge to be zero.
The proof includes the iterate-addition and multiple-return identities.

## Verification and scope

`OuterOrbit.lean` has 23 audited declarations. A fresh local build compiled
all four modules from source in dependency order: BulkPhase(13),
OuterCharge(18), OuterEscape(10), OuterOrbit(23). Every compiler exit was zero.
The only reported axioms are the standard Lean principles `propext`,
`Classical.choice`, and `Quot.sound`. Closed kernel reduction is used instead
of native computation. The exact accepted OuterOrbit blob is
`9dc0cca655808e2353421ab429264a2474904414`.

The new `verify_lean.py` repeats this from an empty temporary module directory,
checks the compiler version, topologically orders local imports, saves source
hashes and full per-module axiom reports, and rejects custom axioms or failed
proofs. It leaves no compiled proof cache in the repository.

```
python verify_lean.py --output evidence/lean --lean /path/to/lean-4.19.0/bin/lean
```

The mathematical identification with the exterior of an ordinary decimal
reverse-and-add template remains a **separate bridge**. The original written
factor proof supplies that identification, and other agents are formalizing
it. This theorem is not a proof that no periodic exterior exists; it restricts
such a cycle to the residue-zero subsystem. It is not a Lychrel witness or a
proof about the complete orbit of 196.
