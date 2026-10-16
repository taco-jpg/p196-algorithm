# Agent #312 — M99-C312 block-indexed guard criterion

Status: WIP / proposed Lean formalization.

This contribution sharpens the guard-preservation correction identified by PR #53 and PR #65. The existing SevenStepOrbit.seven_return_iff is a time-zero theorem. The new block_return_iff is its arbitrary-index form: if boundaryAt q L a = initial, then a seven-step return at a is equivalent to the five guarded controls at a,a+1,a+3,a+5,a+6.

The theorem two_block_return proves the exact safe composition rule: a reset at time 0 plus an independently supplied first block guard and second block guard implies a reset at time 14. Crucially, the second guard is an explicit hypothesis; no recurrence is inferred.

The source has not been compiled in this run because the available CaaS execution was blocked by TooManyActiveSessionsError. Therefore this contribution is WIP, not LEAN-CHECKED. The mathematical proof is a direct specialization of run_actual and BoundaryTransducer.seven_return_iff.

This does not establish palindrome avoidance, an infinite return sequence, or existence of a decimal Lychrel number. It only removes an invalid recurrence assumption and supplies the precise conditional interface needed for repeated returns.
