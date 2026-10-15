# Agent #115 — independent review of `agent103-broader-return-formal`

Task `agent115-review-agent103-broader`, claimed on `p196/coordination` at
`3f870221e402ada2bf798730881d1ed1c8e76447`. This is a **review (replication)**:
no new theorem is claimed. Owner of the reviewed package: Agent #103.

**Status: stage-2 verdict PASS; stage-1 corollaries pending.** The written
bound (eq. (2) of `COMPONENT_SPECIFIC_BOUND.md`) is formalized by the stage-2
endpoints in `BroaderBound`; their complete 50-module import closure has been
rebuilt from source and audited, and the statements checked (below). The
weaker stage-1 corollaries in `BroaderScalarBound` additionally import the full
scalar certificate closure, which is still compiling; their verdict will be
added when that finishes.

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

## Stage-2 verdict: PASS

**Fresh build.** All 50 modules of the `BroaderBound` import closure compiled
from source with exit status 0 (`build/build_report_stage2_snapshot.json`,
logs in `build/logs-stage2/`). The host container restarted once during the
run (after 44 of the 90 modules of the full closure). The run was resumed in the
same build directory with `--resume`, which reuses a module only if its recorded
exit was 0 and both its copied source and its object still have the SHA-256
recorded by this same build; all 44 passed that check and the remaining modules
were compiled. No object from any other build was used. Driver hashes: run 1
`26774c23…eb804` (committed at `6b5901d`), resumed run `6b448c86…c4de4c4`
(identical except for the `--resume` option). The slowest modules were
`BJobChecks8` (1,748 s), `BJobChecks7` (1,613 s) and `BJobChecks12` (1,324 s),
peak memory under 1 GB each.

**Axiom audit.** `audit/Agent115AuditStage2.lean` enumerates every theorem whose
defining module is one of the 50 modules and runs `Lean.collectAxioms`:
**4,243 theorems**, transitive union exactly `{propext, Classical.choice,
Quot.sound}` (`audit/axiom_inventory_stage2.tsv`). The four endpoints and
`BroaderHierarchy.finite_root_bound` use all three; `return_forces_clock`,
`returns_clock_segment`, `root2_realization`, `returnIn_root` and
`actual_broader_root_path` use `propext, Quot.sound`; `returnOK_root` uses none.
The 138 axiom-kind constants defined in these modules are all compiler-generated
specializations (names ending `_spec_N`, `_lambda_N`, `_elambda_N`); none occurs in
any theorem's axioms.

**Statement fidelity.** Exact types are in `audit/Agent115AuditStage2.log`.

- `returns_le_90_plus_warmup : Admissible L q → 2 ≤ L →
  (∀ k ≤ R, pairAt q L (7k) = (4,4)) → R ≤ 90 + warmup L`, with
  `pairAt q L t = ((iterPairs q L t).2 0, (iterPairs q L t).2 1)` (first two
  coefficients of the actual pair-word orbit) and `warmup L = (14 − L + 2)/3`.
  For `L ≤ 14` this is `⌈(14−L)/3⌉`; for `L > 14` it is 0. This is eq. (2)
  of `COMPONENT_SPECIFIC_BOUND.md` exactly, with its convention that `R` counts
  returns after the time-0 occurrence.
- `returns_le_94` (any start time `a`), `wide_returns_le_90` (width at least 14
  at time `a`) and `no_95_returns` follow as stated in the README.
- `FoldedDecimal.Admissible` is the exact realizable mirrored pair-word predicate
  (positive outside coefficient, coefficients ≤ 18, symmetric, even centre), and
  `iterPairs` is the actual pair-word update with overflow-dependent width; both
  come from the unchanged pinned base. The hypotheses impose no safety, branch or
  deeper-column period assumption, matching "all three return branches and
  arbitrary switching".
- `BroaderClock.two_column_step`, `returnOK_root` (kernel `decide`) and the root
  bridge (`states`, `encodeB`, `root2_realization`, `returnIn_root`,
  `actual_broader_root_path`) were read; the endpoints carry no remaining
  certificate premise, so their meaning does not depend on the tables, and the
  tables' provenance was checked separately (above).

## Pending

- Stage-1 corollaries in `BroaderScalarBound` (`returns_le_94_plus_warmup`,
  `returns_le_98`, `wide_returns_le_94`, `no_99_returns`): waiting for the scalar
  closure (`JobData*`, `JobChecks*`, `ScalarHierarchy`, `ScalarPeriods`,
  `RootBridge`, `ScalarBound`) to finish compiling, then the full 90-module audit.
