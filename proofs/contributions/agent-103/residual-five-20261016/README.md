# Agent #103 — residual digit-five family

Task: `agent103-residual-five-20261016`.

## First source checkpoint: Lean-checked inverse shape

`ResidualFiveShape.lean` formalizes the two-step inverse structure described
in section 4 of the preserved `p196_all_palindromes_and_eight_families.md`.
The arithmetic uses the unchanged `Lychrel196.orbit`, `DecimalDigits.Canonical`,
and Agent #119's `Agent119.EightFamilies.V`. This is a formalization of the
written necessary structure, not an exclusion of the residual family.

The public interface `Agent103.ResidualFive.middle_no_overflow_five` says:
if the pair sums at time `s+1` equal the digit word of `fam 5 r`, their width is
`2*r+4`, and the addition from time `s` has terminal carry zero, then all pair
sums at time `s` are `fiveSourceDigit r`, and
`orbit 196 (s+1) = 33 * 10^(2*r+2) + 22`.
The pair word is exactly `[2,12] ++ replicate (2*r) 9 ++ [12,2]`.
The generic inverse lemma also permits any zero-run length, including zero.

Only the terminal carry is zero. The earlier addition has internal carries.
Uniqueness here concerns the symmetric pair-sum word and the intermediate
integer, not a unique choice of the individual source digits.

## Evidence and dependency identity

The frozen source SHA256 is
`592f4af76ee78c92f24dddf91042f0fc2c918944dd181d7e058eb3c57330ffa6`.
Lean 4.19.0 compiled it successfully; the exported endpoint axiom reports are
included under `evidence/shape/`. They contain only `propext`,
`Classical.choice`, and `Quot.sound`.

The five reused source modules are pinned to Agent #119's exact source commit
`913441a936a437e5f4b82d03d7e7fae32da877af`. Their original checker has passed
a fresh five-module build and all 233 module-origin Agent #119 theorem checks.
The original source paths, SHA256s, Git blob identities and current-tree
equivalents are recorded in `evidence/baseline/restore.json` and
`evidence/baseline/verification.json`.

This incremental checkpoint does not yet claim a complete combined clean
rebuild or independent execution review. The author has frozen the checked
source and a separate specialist has begun its semantic review and rebuild.
The next checkpoint adds original-orbit occurrence conditions, the exact
six-step modulo-99 witness, a combined entry point and portable clean replay.

Agent #119's eight-family theorem explicitly excludes `d=5`; it is reused,
not reproduced. Agent #423's modular results will be imported unchanged
through a verified import adapter: their entire original foundation body is
byte-identically embedded in the pinned continuation foundation. Adapter
evidence is preserved separately and does not declare a new arithmetic model.

The status of 196 and exclusion of this residual family remain open here.
No main integration is performed by this source branch.
