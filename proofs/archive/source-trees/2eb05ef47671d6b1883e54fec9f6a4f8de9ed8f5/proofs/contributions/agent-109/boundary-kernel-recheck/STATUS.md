# Agent #109 — kernel-only recheck of the 8/17 boundary exclusion

Task: `agent109-boundary-kernel-recheck`. Original (unmodified):
`proofs/research/main_existence_attempt/boundary_resume/lean/`, whose final
theorems depend on `Lean.ofReduceBool` through 21 `native_decide` checks
(`FORMAL_STATUS.txt`: axioms `[propext, Classical.choice, Lean.ofReduceBool, Quot.sound]`).

**Status: LEAN-CHECKED locally (see `build_log.txt` for the fresh from-source
build). Replication/trust upgrade of a historical result, not a new mathematical
claim. Not independently reviewed.**

## Result

`BoundaryCertificateK.no_936_or_9_12_15_exterior` has *the same statement, over
the same constants* as the original `BoundaryCertificate.no_936_or_9_12_15_exterior`
(`AuditK.lean` prints both with full names and type-checks the original
statement against the new proof):

    ∀ (t : Fin 12) (k : Nat), ¬ ReverseClosure.Path
      (BoundaryCertificate.ArithmeticColumn (6 * (k + 1))) (fun _ => 41)
      (BoundaryCertificate.derivedBulkWord t)

and depends only on `propext`, `Classical.choice`, `Quot.sound` — **no
`Lean.ofReduceBool`**. The same holds for `no_24_phase_936_or_9_12_15_exterior`,
`options_complete`, `no_bulk_exterior`, `no_24_phase_bulk_exterior`, and for
`no_finite_exterior` / `no_arithmetic_exterior` stated for `graph0K`, the literal
transcription of `graph0`. Scope is unchanged from the original: an obstruction for
the fixed alternating 8/17 exterior ansatz; the correspondence to all ordinary
orbits remains the original written argument.

## How

1. `BoundaryDataK.lean`: the 32 string-encoded tables re-transcribed as literal
   lists (string parsing via `String.splitOn`/`String.toNat?` does not reduce in
   the kernel). `TranscriptionCheck.lean` compares all 32 with the originals by
   compiled evaluation (`true`); this control is not part of the proof chain.
2. `SoficFast.lean`: a new projection checker with a proved soundness theorem
   `Sofic.Fast.fast_sound` into the **unchanged** `Sofic.Projection` predicate.
   Ranks/projections and destination-edge indices live in binary-search-tree
   literals; only same-vertex node pairs are visited; every raw node is checked
   to lie in its source bucket; edge membership is rechecked by index (`h[i]?`).
   Wrong or unbalanced trees can only make the check fail.
3. `FastData0..7.lean`: tree data (`gen_fast.py`, an untrusted producer).
4. `ProjK<g>p<k>.lean` / `ProjK<g>b<k>.lean`: 217 modules, one `decide +kernel`
   theorem each on a 45-edge (pairs) or 180-edge (buckets) block of the literal
   graph (kernel memory is not reclaimed between declarations of one file; the
   naive all-pairs `checkProjection` exhausted 6 GB already on `graph2`).
   `ProjK<g>.lean` proves the block split by `rfl` and combines blocks
   (`pairsOK_graph_append`), yielding `projection<g>_fast`.
5. `BoundaryCertificateK`, `ArithmeticBridgeK`, `BulkTargetsK`, `BulkDerivationK`:
   the original proofs replayed with `decide +kernel`; definitions not mentioning
   the tables are reused from the original modules.

Kernel `decide` times (2 cores): chunk modules 0.5–25 s each, total ≈ 17 min;
`fibers_arithmetic_checked` ≈ 31 s; `candidates_complete_checked` ≈ 54 s.

## Reproduce

`./build.sh <repo-root>` (official Lean 4.19.0 on PATH, ~8 GB RAM). It copies the
unmodified originals and these sources to an empty directory and rebuilds all
modules from source (≈ 30 min), then prints the axiom audit and scans the new
sources for `sorry/admit/native_decide/ofReduceBool/axiom`. `peak.sh` measures peak
memory of a single module.
