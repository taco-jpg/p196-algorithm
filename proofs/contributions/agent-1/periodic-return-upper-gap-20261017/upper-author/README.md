# ReturnUpper author receipt

Accepted claim: `ffb0ae839ea8fcfeb71aacdbc9cc3d1afb2349d5`.
Author: Agent1 specialist `cap4_existing_theorems`. Root remains sole Git
writer; this receipt records the author increment, not independent review.

Frozen canonical source: `proofs/Agent1PeriodicReturnUpper.lean`.
SHA-256:
`ff200fa0dbfd1d01ded585f2c182dd65e1fe296f881e1408e219aff166aecd97`.
The exact final source is also retained in `attempt-003/`.

The three public declarations, in namespace `Agent1.Periodic`, are:

- `quotient_path_lower_potential`: every exact valid quotient path satisfies
  the original Agent8 lower-potential bound with both outside endpoints and
  its actual `quotientClockSum`.
- `quotient_return_initial_upper_gap`: a positive full-tuple return with
  initial phase `[14,14,4,4]` satisfies `N + 2 ≤ 4 * quotientClockSum ... N`.
- `quotient_return_initial_upper_gain`: the existing positive natural gain
  satisfies `C=8*G`, signed delta `G`, `16*G≤N`, and `N+2≤32*G`.

The local finite lemma checks the unchanged scalar exterior formulas under
positive outside at most 18, binary actual incoming carry, overflow one,
and target outside nine or ten. It gives the last edge's two-unit gap.
The open adapter uses `Agent8.exterior_bounds` directly; it neither changes
ReturnClock nor duplicates its private clock-total helper. The final proof
uses the existing ReturnCore outside restriction and the separately authored
`quotient_return_initial_last_clock` from InitialIncoming.

No generic lower3 theorem, equality-cycle classification, exponent lift,
arbitrary-path realization, safe infinite orbit, or return existence is
asserted.

## Preserved attempts

| Attempt | Actual result |
| --- | --- |
| `attempt-001` | Preliminary source compilation failed: unknown constant `Nat.cast_zero`. Exact source, command, dependency pins, compiler output and failure status retained. No audit acceptance is asserted. |
| `attempt-002` | Corrected local gap and open adapter compile and complete module audit passed. Nine theorem constants, one required public endpoint, no definitions; this is a partial source snapshot. |
| `attempt-003` | Final three-export source compiled and complete module-origin audit passed. Fourteen theorem constants, all three required public endpoints, no safe or unsafe definitions and no custom axioms. The axiom union is exactly `propext`, `Classical.choice`, `Quot.sound`. |

All executed Lean commands use pinned Lean 4.19.0 commit `6caaee842e94`,
`--trust=0 -j1 -DElab.async=false`, and a 4 GiB address-space limit.
Final compile: exit 0, 0.667 seconds, 460816 KiB maximum RSS.
Final audit: exit 0, 1.620 seconds, 776660 KiB maximum RSS.
Exact measured values, executable hash, working directory and `LEAN_PATH`
are retained in each `commands.json`; these rounded figures are summaries.
The final source prints axioms for every public declaration.

Forty dependency objects were reused for attempt 003 after source hashes
were matched to the frozen ReturnCore/ReturnClock registries and the exact
InitialIncoming source. The dependency records also retain every reused
object's hash. InitialIncoming is the first passing author object from
`incoming-author/attempt-001`, source SHA
`acf7b30677c467b30f7ef978effa8506fb75ead9cf2512d8c1af97f09318edda`.
The remaining objects come from the retained parent clean ReturnClock and
ReturnCore builds named explicitly in `dependencies.json`.

This is **not a fresh full-closure rebuild or independent review**. Those
acceptance stages belong to root and the independent reviewer. After the
environment restart, sealing rechecked the frozen source, attempt results,
logs, and dependency source/object hashes without rerunning Lean.

`manifest.json` inventories the publication evidence, excluding itself and
compiled runtime objects. `runtime-objects.json` records those objects
separately. All failed and partial attempts remain intact. No Git mutation
or external issue message was made by this author during sealing.
