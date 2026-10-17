# Nine-cycle registry preflight

Accepted task: `ec362fbee11009628944ee14ec6a1d1b29990e2e`. Published source
foundation: `7f23ce839fcc88acb235b1816c2c57dc12e16a33`. The registry specialist
authored neither new mathematical module and performed no Lean execution,
Git mutation, or external publication for this preflight.

The frozen registry is `proofs/Agent1PeriodicNinesCycle.registry.json`, project
`agent1-periodic-nine-cycle`, with sole root `Agent1PeriodicNinesCycle`.
SHA256: `d3fca8aa3b055bd287f347a21d132a02c41c6713cdd754fd42a90bf5afcccc80`.
Its exact actual import closure contains 34 modules: 32 inherited sources
plus `Agent1PeriodicNinesPath` and `Agent1PeriodicNinesCycle`. Catalog and
rank modules are outside this closure.

The five actual public theorem endpoints are:

- `Agent1.Periodic.quotient_path_nines_phase`
- `Agent1.Periodic.quotient_path_nines_entry_sum`
- `Agent1.Periodic.periodic_nines_input_nonpalindrome`
- `Agent1.Periodic.quotient_cycle_nines_safe`
- `Agent1.Periodic.quotient_cycle_nines_positive_seed`

`run-000` validates the 32-module inherited union of CycleNumeric, Phase, and
Nines. The existing CycleNumeric and PhaseCatalog registries supply the
exact source aliases; all 17 duplicate pins agree. Every inherited source
matches the published foundation byte for byte. `run-001` preserves the
provisional actual-source snapshot and registry. `run-002 --author-checked`
pins the frozen sources after checking both authors' successful strict
compile/full-origin audit receipts. All runs passed their executable-source
token scan. The global accepted registry is unchanged.

The Path source SHA256 is
`72518762371d6174e300104d817b0e4cbe7a72d2f0f548ce6b6a9e1c79717866`;
the Cycle source SHA256 is
`2bcd823a039a8fd1e9a4f54c01ae367cb2e46f97b96b9d31e29336342953dafd`.
The authors' full new-module audits cover 23 theorem constants and no safe
definitions or generated runtime entries, with only `propext`,
`Classical.choice`, and `Quot.sound`. `confirm-authors.py` verifies exact
source snapshots, actual compile/audit exits, strict compiler arguments and
identity, and sealed receipts. It does not execute Lean. The authors reused
pinned dependency objects; fresh combined verification remains separate.

The registry is frozen as `FROZEN_AUTHOR_CHECKED_FRESH_REVIEW_PENDING`.
Parent and independent fresh 34-module builds remain pending at this
metadata freeze; no combined verification is asserted here.

The mathematical scope stays conditional. Finite phase persistence assumes
an exact path beginning and ending in four nines and includes length zero.
The positive-seed result additionally assumes original initial validity,
positive path length, and full tuple return. It derives the finite safety
premise, then reuses the existing same-seed cycle soundness theorem. No
qualifying return is constructed, and no unconditional decimal seed,
constant-nine no-return result, or conclusion about 196 is claimed.
