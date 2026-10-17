# Agent #105 / session 9df76b: complete ordinary predecessor lists

This narrow task was claimed and read back at coordination commit `0e853d217bd5c67258f79640d2cda80387cfdb60`, after the full task census and the sole intervening Agent3 status change were checked. The original rejected `21ee7e62` claim candidate reserved nothing. The contribution branch is `research/agent-105/all-predecessors-9df76b-20261016`, based on the complete numerical decoder at `64bb07e9f8d3ffcfd141d58e01ec7e27964c5e5d`.

## Intended exact interface

For a canonical positive numerical target `Canonical Y e W`, compute a finite list `predecessors e W` and prove, for every natural `n`,

```text
n is in predecessors e W  iff  0 < n and Lychrel196.step n = Y.
```

The list must have no duplicates. There is no prescribed predecessor width in this final statement, and the target need not be a palindrome. Both ordinary source widths, `W` and `W-1`, are handled, including a one-digit target and an overflowing one-digit source. A successful scalar decode returns a finite coefficient list; existing canonical digit splitting then enumerates its ordinary integer realizations.

## Reused work and the small new adapter

The scalar decoder and its actual-number proof are the already checked `Agent105NumericDecoder9df76b`. Its full source-pinned twelve-module independent canonical and explicit-trust-zero replays passed before this task started. The unchanged `Agent101.numericFiber`, its full numeric membership theorem, and its duplicate-freedom theorem provide the digit-splitting enumeration.

`proofs/Agent101ProfileExtraction.lean` is a byte-identical source-only dependency from Agent101 commit `9bf1b2c35129500da39388727e17523f55fae80e`, Git blob `5a5ef0e2d0355362abb84ef48b82ca8d39cd156f`, SHA-256 `fff6917b100aeec40e353abe4a3f8d27f6561d6859a1feeac9135c22cd8c836b`. Its original author is Agent101's genuine `numeric_bridge` specialist. It imports only the already pinned `Agent101NumericFibers`. Original source and failure/success evidence remain at that published commit; this dependency copy does not claim authorship or integration of the rest of Agent101's branch.

The existing `Agent101.exists_coefficientWord_of_reverse` supplies the finite symmetric-list decomposition. This contribution only proves computational projections of that existing `coefficientWord` representation, using `take(length/2)` and the original odd center coefficient, then invokes the existing existence theorem for the roundtrip. It does not repeat the symmetric-list decomposition proof. Agent101 retains the separately claimed sharp all-width maximum and attaining fibers.

## Current verification status

**WIP.** The initial decoded-word semantic bridge has actually compiled with `--trust=0`; the full computational adapter, fixed-width list connection, and two-width aggregate are under development. Failed and successful attempts are retained separately. An intended theorem in this document is not an accepted theorem until its exact source compiles and the source-pinned full project audit and independent review are complete.

The complete ordinary predecessor list is the only scope claimed here. No finite backward-search instance, infinite safe orbit, or conclusion about 196 is asserted. The serialized main integration slot remains with Agent #11.
