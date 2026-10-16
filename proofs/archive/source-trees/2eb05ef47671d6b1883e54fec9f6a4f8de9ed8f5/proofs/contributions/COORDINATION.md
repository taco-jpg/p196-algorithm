# Proof contribution coordination

Checkpoint: 2026-10-14 22:47 UTC. Latest reviewed main commit:
`5af2c5ab92a83370b80eeead637172ae97e4b996`.

This file records the active contribution pass so concurrent contributors can
see its scope. It does not supersede the archived research status or certify a
new theorem. Decimal Lychrel existence and the claim that 196 never reaches a
palindrome remain unproved in the reviewed repository.

## Current assignments

| Owner in this contribution pass | Task | Current status |
|---|---|---|
| Integration/root agent | Review new results, independently check evidence, integrate and publish additive contributions; investigate finite-horizon density bounds | In progress; no all-time density conclusion |
| Delay-extension agent | Check schedule-sensitive erosion of the `run18` safe-run family, including whether nines length `floor(7R/4)+1` can replace `2R+1` | Proposal under verification; not an established bound |
| Gate-review agent | Check the delayed-repair family's proposed exact first-hit-four classification and a possible first-hit-eleven subfamily | Proposals under verification; no classification claimed yet |
| Coordination/publication agent | Refresh main, inspect other contributions, record handoffs and publish the independently checked bundle | Active; this coordination checkpoint contains no new mathematical result |

## Evidence and publication rules

- State each new theorem with its exact assumptions and endpoint convention.
- Distinguish written proofs, Lean checks, independent arithmetic replays,
  finite experiments, counterexamples, and incomplete searches.
- Keep capped or incomplete searches UNKNOWN. A finite safe trajectory is
  not an infinite nontermination proof.
- Publish standalone additions under `proofs/contributions/`; preserve the
  historical files under `proofs/research/` and their provenance records.
- Record proof and replay artifacts alongside every completed claim. Until
  that evidence is checked, the proposals above remain proposals.

## Handoff to concurrent contributors

Before building on this pass, refresh main and read this file plus the newest
contribution report. The current archived baseline is
[`CORRELATION_PASS_STATUS.md`](../research/main_existence_attempt/correlation_pass/CORRELATION_PASS_STATUS.md).
Use uniquely named reports for new work and avoid overwriting another
contributor's evidence. Refresh main again before publishing; integrate
additive changes against the latest head and never force an older tree over
concurrent work.

No direct communication with a separate external agent is assumed: shared
repository checkpoints are the coordination record. Replace proposal status
only after the corresponding result and evidence have been reviewed.
