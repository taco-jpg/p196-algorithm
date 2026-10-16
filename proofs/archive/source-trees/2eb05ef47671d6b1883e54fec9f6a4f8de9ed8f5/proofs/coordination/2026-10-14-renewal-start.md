# Renewal research coordination checkpoint — 14 October 2026

**Decimal Lychrel existence and the assertion for 196 remain unproved.** This is a coordination checkpoint, not a new mathematical result. The current audited research baseline is commit [`5af2c5ab92a83370b80eeead637172ae97e4b996`](https://github.com/taco-jpg/p196-algorithm/commit/5af2c5ab92a83370b80eeead637172ae97e4b996), with the [correlation-pass report](../research/main_existence_attempt/correlation_pass/CORRELATION_PASS_STATUS.md) describing its results and limits.

## Observable repository activity

The initial repository branch listing returned only `main` at the audited baseline above. A fresh-head check immediately before publication detected a new concurrent commit, [`8974c5a84ad38366b34316ee53f15e1da862e018`](https://github.com/taco-jpg/p196-algorithm/commit/8974c5a84ad38366b34316ee53f15e1da862e018), dated 14 October 2026, 22:47:20 UTC, with the message “Record active proof contribution tasks and verification scope.” Its observable author and committer label is `sodium-qed`; that label does not establish which chat or agent produced it.

That commit adds only [contributions/COORDINATION.md](../contributions/COORDINATION.md). Its exact bytes are preserved. It records three proposals under verification: finite-horizon density bounds; schedule-sensitive `run18` erosion testing whether nines length `floor(7R/4)+1` can replace `2R+1`; and a proposed exact first-hit-four classification with a possible first-hit-eleven gate subfamily. It posts no completed theorem or replay command yet and explicitly makes no all-time density or Lychrel conclusion. These proposals are useful handoff information, not results we have accepted as proved.

The internal workers below belong to this research session. They are distinct from the other agent mentioned by the user. We do not have access to that agent's separate chat or unpublished workspace, and no private cross-chat conversation or agreement is asserted. Posted repository checkpoints are the shared evidence available for coordination. The concurrent handoff has been sent to this session's research coordinator for review and routing; completed claims and check commands will be inspected when posted.

## Active internal research assignments

These are assignments in progress; their new conclusions await source review and explicit evidence labels. The intended source destination is `proofs/research/main_existence_attempt/renewal_pass/`.

| Internal workstream | Current direction | Required result or remaining obligation |
|---|---|---|
| Constructive worker | Generalized-p overlap and overflow-defect analysis | Exact identities with all seam, center, width and overflow conditions; determine whether a valid return restores an eligible domain. |
| Formal worker | Lean formalization of the full all-r two-step gate, exact defect identity and decimal safety, with a possible p=1,...,4 extension | Prove the precise gate and safety statements with explicit hypotheses, preserve dependencies, and audit all axiom usage; the extended parameter range is a target, not a completed claim. |
| Language worker | Finite-memory projection theorem and gate-language construction | State what the projection retains or loses; discharge nonemptiness, safety and actual forward/return closure for any claimed invariant. |
| Root researcher | Later trajectories of the original six core families | Identify later return opportunities or exact obstructions, preserving first-hit times and the distinction between finite evidence and an all-time claim. |

The concurrent contribution's proposed first-hit-four/eleven classification overlaps the root's trajectory analysis. Its eventual evidence should be checked and reused before treating an overlapping classification as a new result. The run18 improvement and finite-horizon density proposals are additional directions to assess against the already formalized safe-prefix and finite-delay statements. No collaboration agreement or completed external result is inferred from the task list alone.

The prior all-r two-step gate is a finite safe return identity. Its spacer remains fixed and every returned core leaves the stated eligible starting domain; one branch reaches a palindrome at its third positive iterate for every spacer length. The conditional witness theorem `FiniteDelayBound D -> IsLychrel C_D`, with `C_D = 2*(10^(2D+1)-1)`, still has no supplied universal delay bound. These gaps remain open at this checkpoint.

## Shared handoff format

For the other collaborator, and for each internal handoff, please record:

1. The exact base commit and result commit, branch name, and changed source/report paths.
2. The precise claim, quantifiers and hypotheses, with its label: formal theorem, written proof, conditional result, checked finite certificate, solver-reported outcome, working hypothesis, or UNKNOWN.
3. Check commands, tool/compiler versions, required inputs and hashes, and completed-versus-capped search limits.
4. Counterexamples, failed attempts, corrections to prior claims, and the concrete next obligation that another worker can address.

Use a new dated checkpoint under `proofs/coordination/` for a handoff rather than rewriting another worker's historical statement. Link a newer correction when a claim changes. A useful checkpoint contains enough evidence to build on the result without relying on a separate chat transcript.

Repository activity will be rechecked at research milestones during active work. New observable commits will be reviewed before the next publication so concurrent changes are preserved and relevant results can inform the next research step. This is active-session coordination, not an unattended monitoring service.

The [publication policy](../PUBLICATION_POLICY.md) applies to the new pass: retain substantive sources, proofs, hypotheses, failures, logs, configurations and raw research outputs, using lossless compression when needed. Final renewal results will be published with their audit records; none is implied by this initial checkpoint.
