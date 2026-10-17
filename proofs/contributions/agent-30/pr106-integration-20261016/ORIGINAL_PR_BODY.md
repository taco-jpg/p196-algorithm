## Why this change is needed

The preserved congruence-family note gives a written example of an artificial sparse entry jump that can satisfy residue and coarse growth checks while violating the quantitative carry restriction of actual decimal reverse-add. Its all-parameter obstruction had not been a Lean theorem.

This PR formalizes that arithmetic gap using the unchanged Lychrel196.step, DecimalMass.digitSum, DecimalDigits.Canonical, and DecimalQuantitativeMass.decimalLength.

## Proved core

For every ordinary natural n, including zero:
- digitSum(step n) <= 2*digitSum(n);
- 2*digitSum(n) <= digitSum(step n) + 9*decimalLength(n).

For y_k = 11*(10^k-1), k>=2, the source has exact width k+2 and digit sum 9k. The package additionally proves reverse10(y_k)=9*y_k, step(y_k)=10*y_k, and the actual first edge 2*(10^k-1) -> y_k for k>=1.

For R>=3, put k=7*R/4+1, a=k+2 and c=10^a+990*a+(if a%2=1 then89 else989). The core proves

`digitSum(c)+36 < 9*a <= digitSum(step(y_k))+36`

and therefore c != step(y_k). The R=3 / a=8 boundary is explicit; the general target bound is digitSum(c)+44<=9*a for a>=9.

This formalizes the original note's Section 3, not an infinite orbit or a result resolving 196. The complete artificial path remains outside this PR.

## Source and verification

Published core source: 2085103344800254e6d05d6c52e4a850a6246f26.
Four new modules / 24 public named theorems:
- proofs/Agent106CarryBudget.lean
- proofs/Agent106CongruenceSeed.lean
- proofs/Agent106SparseTarget.lean
- proofs/Agent106CongruenceObstruction.lean

All four passed author Lean 4.19.0 with explicit --trust=0, -j1, -DElab.async=false. Failed attempts, exact sources and compiler logs are retained in proofs/contributions/agent-106/congruence-carry-budget-20261016T2131Z/development/.

A genuine separate same-session specialist has completed the independent core semantic review and is running a fresh whole-core rebuild and exhaustive module-origin audit. The fixed original foundation already passed its separate fresh build / 986-theorem audit with only propext, Classical.choice, Quot.sound. Unsafe implementation placeholders are reported separately; no source sorry/admit/native_decide or custom theorem axiom is introduced.

## Draft completion work

- Finish the already-claimed modulo99 and entry-growth/width controls in a separate fifth source module.
- Publish the independent complete receipt, full public endpoint registry and portable replay.
- Run the parent's separate exact-published-source final replay, obtain a formal attributed PR review, and hand off to the serialized integration owner.

No main-write slot is held by this author.

Original written source: commit 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5, proofs/contributions/2026-10-15-congruence-family-obstruction/CONGRUENCE_PATHS.md, blob fc8bef244f236095de36b9319f07147f23d41d1a.
Ownership claim: coordination 2d9f553521404c98c119ed92e4c0538dce17aea4.
Coordination: https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6225263639 .
