# Reduced-core independent review: PASS

Reviewer: genuine Agent #1 specialist `/root/verification_plan`. The reviewer
prepared this contribution's registry and authored some earlier dependency
modules, but authored neither `Agent1PeriodicEighteenLabel` nor
`Agent1PeriodicReturnReducedCore`. No mathematical source edits are made by
this review.

Parent authorization covered a staged fresh build: first the 46 published
dependencies at `1c65552f079e1ce4061c69be5488573c59e5a207`, then the two new
modules at published commit `e84dfed51f9dfd48995ddc4920f5bf2bd6b80f82`.
The final audit completed over all 48 modules. The registry SHA256 is
`02854c6cf0631e0605ddb83a859ff98f1347bb8130120d7101357b4cfe4e9c06`.

The baseline build directory starts empty and receives only the exact Lean
source files. No external project objects are reused. Commands use the
official pinned Lean 4.19.0 executable with `--trust=0 -j1
-DElab.async=false`, an explicit `LEAN_PATH` pointing only at this fresh
build, a 16 GiB address-space limit, and a 1200-second per-command timeout.
Actual command exits and logs are retained under `baseline-001`.

The staged helpers were adapted from the EighteenReturn independent review.
Their provenance is recorded separately. Nested comments and strings are
masked before every public declaration scan; `scanner-controls.json`
records the regression checks for the previously discovered documentation
false positive. The origin audit checks every selected theorem and safe
definition, inventories compiler implementation entries separately, and
rejects custom axioms or disallowed dependencies. Literal `#print axioms`
commands are added to the generated audit for discovered public theorems.

After publication, `pin_published.py` independently compared the final
registry and every selected source byte to the specified published commit,
resolved actual imports, checked exact closure and public declarations, and
pinned the new source identities. The append driver verified every baseline
source and object hash before using those objects from this same review.

All 50 actual Lean commands exited zero: 46 fresh dependency compilations,
their full audit, two published new-module compilations, and the final full
audit. The final audit checked 2,267 theorem constants and 587 safe
definitions. The theorem axiom union is `Classical.choice`, `Quot.sound`,
and `propext`; safe definitions use only `Quot.sound` and `propext`.
Literal `#print axioms` output was checked for 184 public Agent1 theorems,
including both new endpoints. The Label endpoint is axiom-free; ReducedCore
uses precisely the three approved logical axioms. The new modules contain
58 theorem constants, eight safe definitions, and 24 separately inventoried
compiler runtime definitions. No custom mathematical axioms or unsafe
opaque constants were found.

## Retained reporting failure and correction

The baseline driver exited one after all 47 baseline Lean commands passed.
Its Python postcheck had been strengthened to reject every unsafe compiler
implementation axiom, so it rejected 32 inherited runtime specializations.
The failed script snapshot and `REVIEW_REQUIRED` inventory remain unchanged
under `baseline-001`.

`review_inventory.py` made a separate classification-only check, recorded
under `baseline-inventory-review-001`. All 32 entries exactly match the
published ReturnCore38 inventory at the pinned foundation, with matching
source pins. None occurs in any audited theorem or safe-definition axiom
set. No Lean command, mathematical source, or proof was changed to make
this correction. The final append audit requires this exact inherited
inventory and rejects additions. Its 12,193 runtime definitions are
separately inventoried; every `_unsafe_rec` entry has an audited safe base.

The final runner's `failed_audit_preserved: false` is its append-stage retry
flag: no append audit failed. The baseline Python postcheck failure is
explicitly preserved and disclosed in `frozen-receipt.json`.

## Source interpretation

The new label lemma says that the total `outerComponent` function can return
130 only when its phase is `[18,18,18,18]`; it needs no catalog membership
premise. The final result reuses the existing full-return core theorem,
then eliminates label 130 by the constant-eighteen no-return theorem.

The final result keeps initial original validity, initial `outerCatalog`
membership, an exact quotient path, positive path length, and equality of
all three endpoint blocks as explicit premises. Its conclusion uses one
constant label in `[8,129]` for every state through the endpoint, retaining
membership in the existing `returnCore`. It neither proves catalog coverage
for arbitrary valid inputs nor excludes either remaining label, constructs
a return, or makes an assertion about 196. Positivity excludes the trivial
zero-length path; full tuple equality is stronger than returning only the
phase or width.

No semantic gap was found in the two frozen new statements or their use of
the original definitions. `frozen-receipt.json`, the source identities,
exact command records, logs, runtime inventories, and `FILES.json` retain
the evidence. This is a scoped contribution review; it does not assert a
repository-wide accepted build or publication by the reviewer.
