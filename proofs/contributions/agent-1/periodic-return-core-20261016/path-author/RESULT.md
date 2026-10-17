# Exact quotient path: author evidence

Frozen source: `proofs/Agent1PeriodicQuotientPath.lean`, SHA-256
`7735197ffa2a779c6ff1e0d76c2ed338ceb1afef75623adb7f2ce9a62c0d4e67`.

The two exported theorems, in `Agent1.Periodic`, reuse the original
`QuotientPath`, validity theorem, and actual outer catalog edge theorem:

- `quotient_path_valid_catalog B H w N hp hv hs i hi` takes `hi : i ≤ N`
  and proves full original `ValidPeriodic` and physical outside/phase
  membership at state `i`.
- `quotient_path_outer_edge B H w N hp hv hs i hi` takes `hi : i < N`
  and supplies a literal `outerEdges` member whose source is state `i`,
  target is state `i+1`, clock is the actual `rawGamma`, and exceptional
  all-nine label is the actual pair of boundary entry carries.

Here `hp` is the exact path contract, `hv` is initial full validity, and
`hs` is initial outer catalog membership. Propagation includes endpoint
`N` and the empty path. No complete return, component restriction, safety,
exponent guard, or ordinary numeric orbit is asserted by this module.

## Actual checks

Official Lean 4.19.0, compiler SHA-256
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
Both commands used `--trust=0 -j1 -DElab.async=false`, CPU affinity `[0]`,
and a 1500 MiB resident-memory watchdog sampled every 10 ms. Neither
watchdog triggered. No virtual-address limit was imposed.

`attempt-001` compiled the frozen source on its first attempt: exit 0,
0.292 seconds, peak resident memory 447608 KiB. The produced object has
SHA-256 `791ae2b2a6d89af70979e91b1b56d92d273fae51b70ba52a0375647f877adb31`.
Its log includes literal `#print axioms` for both public theorems.

`audit-001` passed on its first attempt: exit 0, 1.865 seconds, peak resident
memory 759384 KiB (sampled high-water mark 759544 KiB). The complete
module-origin audit traversed all five new theorem constants, including
generated support. There are no new definitions, axioms, or executable
helper declarations. Every theorem uses only `propext`, `Classical.choice`,
and `Quot.sound`. Both public types and literal axiom lists were printed.
Audit log SHA-256:
`8ea84ffb0a4144624c6e586e1c5872a4210d8fcafc07f1a637ba5e4e6365de09`.

All exact commands, working directories, `LEAN_PATH`, source snapshots,
driver snapshots, logs, compiler hashes and exit receipts are retained.
There were no failed Lean attempts for this module.

## Dependency qualification

This is incremental author verification, not a fresh independent rebuild.
It reused 25 dependency objects from the complete outer parent clean build
at source commit `6be2aa2273e97ecf15445429827b02feb9bb83c0`, whose receipt
was checked PASS, plus the unchanged WidthPath author object from its
successful `attempt-002` and full `audit-006`. All 26 dependency source and
object hashes are recorded in `attempt-001/dependencies.json`. The fourteen
underlying WidthPath source dependencies were matched to the corresponding
outer clean-build sources before reuse.

Only the owned source and `path-author/` evidence were written. The parent
owns Git publication and combined fresh verification. `FILES.json` hashes
the source and retained text evidence; the generated `.olean` is omitted
from that publication manifest, with its exact hash retained above and in
the receipts.
