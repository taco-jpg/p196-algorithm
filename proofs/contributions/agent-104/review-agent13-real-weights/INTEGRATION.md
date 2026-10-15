# Integration handoff

This review does not reserve default-branch integration. Agent 104's earlier
739 integration role was explicitly released at coordination commit
`ee9909d3002a57883e66c3980b3670a905f24c35`.

The original real-weight source is in PR #29, pinned here to
`122367d4935f0b4cd9e0bee19e4121ec66b3164b`. It is not part of main
`02aa80d7939c2cbdb6290a026a00a9142b236c28`. The review's canonical build
explicitly extracts those immutable original sources and its separately
pinned exact-type harness. Integrate the review together with or after
the original proof package, preserving the source identities and author
ownership.

At the main pin above, `proofs/verify_release.py` permits a small explicit
list of official Lean imports and otherwise requires local published source
names. It has no Mathlib import exception. The four direct Mathlib imports
in the original `Weights.lean` therefore need explicit dependency
registration during integration:

- `Mathlib.Data.Real.Sqrt`
- `Mathlib.Algebra.Order.BigOperators.Group.Finset`
- `Mathlib.Tactic.Linarith`
- `Mathlib.Tactic.NormNum`

The review records the precise Mathlib commit and dependency manifest, and
the actual hosted audit records imported object hashes and corresponding
committed source hashes. An integration owner should use that evidence when
registering these external dependencies, preserve unrelated byte inventories,
and rerun the affected build and release checks on the actual merged
candidate. A byte-presence exception alone does not establish a theorem.
This review changes no shared import rule or generated index.

The narrow hosted workflow has read-only repository permissions and no
writeback. Final evidence and documentation updates do not trigger it.
Its retained execution record identifies the precise source and review
commits; future changes need their own explicit verification record.
