# Agent #1: retained failed formalization attempts

## Attempt 1: well-founded digit extraction with ordinary decide

Exact source is retained in Git commit
`13594a41c4a08ccbf3ac9bb12795b2914f997421`, path
`proofs/contributions/2026-10-15-safe-high-return/SafeHighWitness.lean`.
Run: https://github.com/taco-jpg/p196-algorithm/actions/runs/38682098335
Job: 116248693146. The complete job log is available through that run.

The Python controls passed. Official Lean 4.19.0 installed successfully.
Compiler: `Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)`.
Downloaded archive SHA-256:
`6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`.

The compiler exited 1. All five intended theorem declarations failed:
ordinary `decide` could not reduce the well-founded recursive digit extractor.
The emitted axiom reports contained `[propext, sorryAx, Quot.sound]` because
Lean recovered from tactic errors; **none is an accepted theorem**. Source
containing no literal `sorry` did not prevent this failed-build artifact.

Repair under test: use structurally recursive `digitsAux fuel n` and define
`digits10 n := digitsAux n n`. This is not a fixed-width approximation;
positive division by ten strictly decreases the remaining number. No axiom,
unsafe evaluation, or compiler-backed decision tactic is introduced.
The revised source is still PENDING until a successful compiler run is read.
