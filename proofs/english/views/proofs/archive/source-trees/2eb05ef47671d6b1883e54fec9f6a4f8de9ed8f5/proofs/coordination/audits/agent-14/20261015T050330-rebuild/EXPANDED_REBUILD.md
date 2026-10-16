# Agent #14 — expanded independent rebuild checkpoint

Checkpoint: 2026-10-15T05:28:10Z. This is direct execution during the audit, not a repetition of collaborator build claims.

## Newly discharged verification obligations

1. `HighReturnRank.lean`: a fresh Lean 4.19.0 compilation completed with exit 0. All five exported theorem axiom queries passed. The concrete `finite_check` over 900 vertices and two controls is axiom-free; the four soundness/rank corollaries use only `propext` and `Quot.sound`. This certifies the necessary prefix graph, not by itself its arithmetic correspondence.
2. Agent #8's `PeriodObstructions`, `ActualWordBridge`, and `AllPhaseRefinement`: all three modules compiled in an initially empty project build directory. Exit codes are 0, with respectively 24, 26, and 5 printed transitive axiom queries. Only standard logical axioms occurred.
3. Agent #6's `ExteriorCore`, `ExteriorCapTwo`, and `ExteriorCoverage`: all three modules compiled in that same independently populated build directory, using only freshly built local dependencies. Exit codes are 0, with respectively 2, 3, and 5 printed axiom queries. Only `propext` and `Quot.sound` occurred.

No project compiled object was imported from the source artifact or another agent's build. Sources were compared with the pinned artifact before compilation and hashed before/after each successful run. The runtime is the official Lean 4.19.0 release previously recorded in SNAPSHOT.md; no runtime shim was required here.

## Exact scope of the mathematical conclusions

`HighReturnRank.no_four_edges` excludes four consecutive edges in its checked finite graph. The separate Agent #105 actual-orbit bridge is source- and existing-evidence-inspected in this audit; that eight-module chain has not yet been freshly rebuilt by Agent #14.

Agent #8's canonical whole-word orbit has no two-step return to the same complementary template with positive initial/final outer gaps. `no_repeatable_six_step_periodic_template_return` excludes a six-step return with BOTH gaps nondecreasing in any of the eight periodic even phases. The six-phase twelve- and eighteen-step lemmas constrain hypothetical return gains; they do not construct a return. The actual-word bridge discharges normalization, actual-width, exterior-transition, and overflow-count obligations in the word model. Transport into the repository's ordinary-integer orbit is a distinct obligation; later Agent #109 contributions must be assessed separately, not silently included in this build.

`P196.Agent6.capTwo_uniform_escape` proves every canonical periodic exterior initially of length at most two exceeds that length at some time at most seven. Canonical means even phase in 2..16, coefficients at most 18, positive nonempty head, and trimming already applied. `capTwo_coverage` supplies the finite decoder representation, removing the earlier decoder premise. This does not state arbitrary-length escape or prove that every ordinary decimal orbit is represented by this exterior model.

These are rigorous supporting obstructions. None supplies a fixed positive finite seed with an infinite palindrome-free orbit.

## New local source access, with exact provenance

The existing Agent #9 pinned-source workflow at `6c0101e9d6fb78463acc4c15ac5d74558a9c81cc` explicitly checks out `f49d2fa2319d34e3f97fc94e49523c3ed3e056f4`. Its completed run is 38684576316; artifact 11949148116 is `agent9-proof-snapshot-f49d2fa`.

Downloaded ZIP SHA-256: `3ed67ac75f5d02ef33cfa6896f7367a94e8abea877e598a4234a61d06769eaa4`.
Contained source archive SHA-256: `c0b2a6ad3df7089b3b369ee5218365fe05bcb63e4a88933ddfbb060d5bc34c6c`.
All 2,695 manifest-listed source files matched their SHA-256 records and Git blob identities. This is integrity evidence for a finite pinned inventory, not 2,695 mathematical verifications. The archive predates the initial main snapshot by several commits and does not implicitly include later branch contributions.

## Selected exact source hashes

Paths for the first three expanded modules: `proofs/contributions/2026-10-15-agent8-complementary-bulk/`.

| File | SHA-256 |
|---|---|
| PeriodObstructions.lean | 83102a949036799a929ba72d74ce9d76bc2a11cb3adf61e0bc06b6013b22991a |
| ActualWordBridge.lean | 3123e8f86fe751e61307ea528390bd265515a8d69c731f51e2808fb78d0a6ec6 |
| AllPhaseRefinement.lean | 97c48b0eaaeff5c058f664019d03c1484c8f992e78b756e51186acfe6bc93740 |

Paths for the next three: `proofs/contributions/agent6-complementary-bulk/`.

| File | SHA-256 |
|---|---|
| ExteriorCore.lean | 4f4f31795a5198bffccf86ba1b7beed33da43e93063dfd0253266e8d1626d8e2 |
| ExteriorCapTwo.lean | cbf5d410dd436f524c84856901116ba946e328ebb5796cd0b56135b684d286d3 |
| ExteriorCoverage.lean | 459a9ee9aa87f28affbda6ce632df6ef87d63b19f2f853cdc1fecc88ec860e8c |

Rank source: `proofs/contributions/2026-10-15-high-return-rank-formal/HighReturnRank.lean`, SHA-256 `76ce0aefdcf8ed6bea047c5d8b718d23ab02bfaf18bfb96211f8fa13269218d8`, Git blob `7b7d025866a478b46e5c3a73168fdf4902133372`.

## Executed commands and limits

Each expanded module was compiled in dependency order with:

```sh
LEAN_PATH=/absolute/path/to/empty-project-build /path/to/lean-4.19.0/bin/lean -j1 -o MODULE.olean MODULE.lean
```

The recorded 05:27 batch completed all three Agent #6 modules, including the 30.288-second cap-two check, before the outer 45-second tool-call deadline interrupted the subsequent Agent #5 `ExteriorClock` attempt. There is no completed log or accepted exit status for that interrupted attempt; it is not counted as verified. Agent #2 `ExteriorCharge` was not reached in that batch. This is an execution limit, not evidence that either mathematical statement is false. Successful logs, exact commands, source/object hashes, and timing records remain retained for publication with the complete audit bundle.

Correction to the wording in LEAN_REBUILD.md: all five witness theorems are axiom-free; every one of the 70 family theorems uses `propext` or `propext` plus `Quot.sound`. The earlier phrase suggesting some family theorems were axiom-free was imprecise. It does not affect the accepted standard-axiom result.
