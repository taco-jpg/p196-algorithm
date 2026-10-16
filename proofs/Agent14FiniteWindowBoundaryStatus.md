# Agent #14 — finite nonperiodic boundary window

Status: WIP / UNEXECUTED. The complete proof attempt in `Agent14FiniteWindowBoundary.lean` has not been compiled or axiom-audited. The proposed bound is not an accepted result.

## Exact proposed extension

The imported `Slot`, `Tile`, four scalar fiber lemmas, 和 `shift` are Agent #9's unchanged definitions/theorems from blob `03c2e377b669b90d39cf5dc4c2983acee18eea27`.

`StepWindow H outer inner` requires the exact tile equation only for `j < H`. The same coefficient function occurs at `j` 和 `j+1`. It does not impose a final-to-first equality, fabricate a periodic extension, or require the finite data to extend to an infinite valid trace. The functions have domain `Nat`, but all constraints are restricted to the finite window.

The proposed generic endpoint rules out a width-`n` path with an outside constant over the window, a six or twelve tail constant over the same window, 和 all adjacent column relations valid for `H = 2*n+1`. The outside must differ from both the regular tail slot 和 its exceptional predecessor. The two orientations are separate cases, never simultaneous tail assumptions.

## Proof attempt 和 index audit

Predecessor classification at `j` uses inner-column tiles at `j` 和 `j+1`, so the fixture requires `j+1 < H`. Erasing the exceptional letter at time `j+1` uses two such classifications, so it requires `j+2 < H`. These local proofs reuse the exact previously proved scalar fibers rather than an unverified evaluator.

The induction removes one spatial layer, shifts every surviving trace once, 和 shortens the usable horizon by two. From an original horizon `2*(n+1)+1`, the shifted width-`n` problem has horizon `2*n+1`. For each remaining index `j`, `j < 2*n+1` guarantees `j+2 < 2*(n+1)+1`. The zero-width case retains one actual time slot; the width-one case uses direct predecessor classification. No optimality is claimed for this conservative horizon.

The one-slot control explicitly supplies the physical-outside-to-six tile with coefficients `q=6`, `r=12`, `e=1`, `qNext=3`. The endpoint coefficient does not return to six. A corresponding `StepWindow 1` witness is included to catch an erroneous proof that excludes all nonempty finite windows by silently adding cyclic closure. These controls are also UNEXECUTED.

## Required execution

First run the source-pinned M99-A04 replay in a new directory using the accompanying manifest 和 a trusted Lean4.19.0 installation. Then stage this exact file from its patch commit into that same freshly built dependency directory; compile it with `-j1 -DElab.async=false`. Preserve its source hash, compiler identity, exit status, object hash, 和 all ten printed transitive axiom answers. Any error or forbidden dependency rejects the candidate. The existing replay PASS, if obtained, would not by itself cover this additional module.

## Current limit 和 next dependency

This file concerns the abstract exact cut relation. A finite-window application to actual pair iterates must separately derive every tile, the physical outside, 和 the aligned tail using only finite-time schedule/width/band hypotheses. The imported Agent #112 `actual_tile` is pointwise 和 can supply those tiles; its global infinite-trace wrappers must not be applied by inventing an infinite schedule. That pointwise finite arithmetic transport is the next concrete proof-development step.

No ordinary-orbit bound, arbitrary certificate exclusion, decimal Lychrel existence, or statement about196 is accepted by this file. The runtime import/execution blocker from the M99-A04 review remains unresolved.

Agent #14
