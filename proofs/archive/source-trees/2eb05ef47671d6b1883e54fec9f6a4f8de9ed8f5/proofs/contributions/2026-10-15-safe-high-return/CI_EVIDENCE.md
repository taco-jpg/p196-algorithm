# Additional observed CI evidence

The complete family source, not only the finite witness, passed GitHub Actions
run **38684097931** at source commit
`9096791b36bd8b18985328a6970a4abfc9eb4272`.
The run was observed completed with conclusion `success`.
It rebuilt SafeHighWitness.lean, SafeHighFamily.lean and FamilyAudit.lean
using the pinned official Lean 4.19.0 archive. This supplements the earlier
local audit and the finite-only run in FORMAL_STATUS.md.

The current branch workflow additionally runs all four Python scripts,
including the full producer and independent 59,999-word replay. Its result
must be inspected at the exact new commit before being claimed as passed.

No CI success is an external mathematical peer review or a proof of P196.
