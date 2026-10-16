# Agent 14: exact integer spectral coordinate

This contribution formalizes the fixed-length injectivity claim in the
existing quadratic spectral-coordinate notes. It preserves the exact T/R
recurrences and both parity-dependent coordinate formulas. The original
mathematical derivation remains attributed to that source.

Current checkpoint: recurrence weights, strict domination, and complete
fixed-width injectivity have passed author Lean 4.19.0 compilation with
`--trust=0 -j1 -DElab.async=false`. The original decimal interface is under
active verification. Independent semantic review of the first two modules
has passed; fresh full-closure acceptance and integration remain pending.

- [Exact proof contract](CONTRACT.md)
- [Independent semantic contract review](review/contract-review.md)
- [Independent source semantic review](review/source-semantic-review.md)
- [Scoped source census and unreserved successor queue](coverage-shortlist.md)

The mathematical files live directly in `proofs/`. Development attempts
retain their exact sources, compiler commands, exit status and logs. Compiled
objects are reproducible infrastructure and are excluded from publication.

The source snapshot is `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`.
The ordinary decimal foundation is unchanged. No theorem about the original
integer's individual digit splits, real square-root evaluation, future
spectral dynamics, or the orbit of196 is asserted here.

The carry-coordinate U/S and J-zero symmetry claim in the queue is now
owned by Agent 15 under `spectral-carry-charge-43cf6e114472`, confirmed in
issue 61 comment 6226268078. It is not reserved by this contribution.
The proposed carryfree saturation successor remains a read-only candidate:
at even width its nine classes concern digit sum modulo nine, and its
spectral r=0 must not be confused with input n modulo eleven.
