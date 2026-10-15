# Agent #115 — independent review of `agent103-broader-return-formal`

Task `agent115-review-agent103-broader`, claimed on `p196/coordination` at
`3f870221e402ada2bf798730881d1ed1c8e76447`. This is a **review (replication)**:
no new theorem is claimed. Owner of the reviewed package: Agent #103.

**Status: WIP.** The provenance check below is complete. The fresh from-source
Lean rebuild and the independent axiom audit are running; no build or audit
verdict is recorded yet. `agent103-broader-return-formal` keeps its
LEAN-CHECKED label until this review publishes a verdict.

## Pins

- Reviewed source: `04a36443d5bd0f3c15eeb3dc4ae03d4a45f7a5c2`
  (package `proofs/contributions/agent-103/broader-return-formal/`).
  `git diff 04a3644 2c25511` (current main) is empty for all 90 source files of
  the import closure; the only later change in the package directory is the
  added `SUBAGENT_REVIEW.md`.
- Toolchain: official Lean 4.19.0, release commit `6caaee842e94`, archive
  SHA-256 `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`,
  `bin/lean` SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`,
  downloaded fresh into this review's own workspace. No `/proc/self/exe` shim.
- Base `LychrelDigitSums.lean` SHA-256
  `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`.

## Method

- `build/agent115_build.py` was written for this review, independently of
  Agent #103's `verify_*.py` drivers. Only the module-to-file layout is taken
  from the package. It copies all 90 sources of the closure of
  `BroaderBound` and `BroaderScalarBound` into an empty directory, rejects
  `sorry`/`admit`/`native_decide`/`axiom`/`ofReduceBool`/`implemented_by`/`extern`
  tokens outside comments (base checked by hash), and compiles every module
  from source with `-DElab.async=false`, at most two concurrent `lean`
  processes, recording exit codes, wall time, peak RSS and object hashes.
  No object, log or manifest from any earlier build is reused.
- `audit/Agent115Audit.lean` is an independently written audit. It enumerates
  every theorem constant whose defining module is one of the 90 project modules
  and runs `Lean.collectAxioms` on each, records any `axiom` declared in a project
  module and every unsafe declaration, and prints the exact endpoint types and the
  definitions `pairAt`, `warmup`, `Admissible` and `iterPairs`.

## Completed: generator provenance (item 5 of the claim)

Performed by a separate-context Agent #115 subagent (Python only, single process),
then spot-checked by Agent #115. Scripts and outputs are in `provenance/`.

| Check | Result |
|---|---|
| `component_certificates.json.gz` SHA-256 `ff7a70ee…23b47e` equals the pin in `gen_broader.py`, the original generator and `COMPONENT_SPECIFIC_BOUND.md` §5 | PASS |
| Rerunning `stage2/gen_broader.py` on a copy reproduces all 34 committed `stage2/generated` files byte for byte (Agent #115 re-hashed the pinned files separately) | PASS |
| Copies of the original scalar generators changed only by literal name/offset/root substitutions reproduce all 31 `BJob*` files and both hierarchy files byte for byte | PASS |
| An independent Tarjan/condensation recomputation from the certificate (no repository code) gives jobs 16–30 = the 15 broader jobs and root bound 636 = 22 + 14 + 600 | PASS |
| `SHA256SUMS` files (51/51 and 7/7) | PASS |

`BroaderHierarchy.finite_root_bound` (verbatim):
`(q : Nat → Nat) (L a s n : Nat) (path : Nat → Nat) (ha : Admissible L q) (hL : 14 ≤ L) (hp : ActualPath (ScalarFinite.graph data0) q L 2 a s path n) : n ≤ 636`.

Excluded from this directory: the subagent's temporary copies of the
repository tree and the regenerated Lean files (they are byte-identical to the
committed sources; their hashes are in `provenance/outputs/*.sha256`).

## Pending

1. Fresh rebuild verdict (`build/`).
2. Axiom audit verdict (`audit/`).
3. Statement-fidelity verdict against `COMPONENT_SPECIFIC_BOUND.md` eq. (2).
