# Agent #109 — kernel-only recheck of the 8/17 boundary certificate (WIP)

Task: `agent109-boundary-kernel-recheck`. Original (unmodified):
`proofs/research/main_existence_attempt/boundary_resume/lean/`, whose final
theorems depend on `Lean.ofReduceBool` through 21 `native_decide` checks.

**Status: WIP. No theorem of this directory is accepted yet.**

## Done

* `BoundaryDataK.lean`: the 32 string-encoded tables of `BoundaryData.lean`
  (`graph0..7`, `ranks0..7`, `maps0..7`, `rootRanks0..7`) re-transcribed as
  literal `List Nat`s (string parsing via `String.splitOn`/`String.toNat?` does
  not reduce in the kernel: `decide +kernel` on `parseNats "12 7 345" = …` gets
  stuck). `TranscriptionCheck.lean` evaluates (compiled) all 32 equalities
  `original = transcription`: `true`. This is a transcription control only.
* Generated `*K.lean` replays (same proofs, `decide +kernel`, K tables).
* Individually timed kernel checks (`prof.py`, `prof2.py`, 6 GB cap, 2 cores):

| check | result |
|---|---|
| `fibers_arithmetic_checked` | kernel OK, 31 s |
| `projection0_checked`, `projection1_checked` | kernel OK (≤ 20 s) |
| `root0..7_checked` | kernel OK (root7 6 s) |
| `candidates_complete_checked` | kernel OK, 54 s |
| `bulk_edges_checked` | kernel OK, 2 s |
| `bulk_cycles_checked` | kernel OK, 9 s |
| `derived_targets_checked` | kernel OK, 10 s |
| `projection2_checked` | **out of memory** at 6 GB after 80 s |
| `projection3..7_checked` | not attempted with the naive checker |

## Obstruction and plan

`Sofic.checkProjection` is all-pairs over raw nodes and looks ranks up by
`findIdx`: raw node counts are 24, 76, 324, 910, 2522, 3434, 3434, 3434 for
`graph0..7`, while only 48 … 25,896 pairs share a vertex. Planned replacement:
a checker with proved soundness into the unchanged `Sofic.Projection` predicate
that (i) looks ranks/projections up in balanced binary-tree literals keyed by
an injective node code, (ii) visits only pairs in a source-vertex bucket, with
a checked bucket-completeness condition, and (iii) tests destination-edge
membership in a tree keyed by edge code; split into chunked kernel theorems.
