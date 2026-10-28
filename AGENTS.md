# Rules for contributors (people and agents)

The repository has one branch, `main`, and it must always pass `python3 tools/verify.py` (the full check, run
nightly by GitHub Actions). The goal is one thing: find a Lychrel number in base 10 (see `OPEN_PROBLEMS.md`).
Everything below exists to keep `main` correct while 20 agents work in parallel without waiting for each other.

## 1. Pushing (no pull requests, no branches, no tags)

Commit directly to `main`. Never create branches, pull requests or tags; never force-push or rewrite history.

    git fetch && git rebase origin/main && python3 tools/verify.py --changed     # must end with ALL CHECKS PASSED
    git push origin HEAD:main

- If the push is rejected because someone else pushed first: `git fetch && git rebase origin/main` and push again.
  Re-run `verify.py --changed` only if the new commits changed a file that your files import. Otherwise push at once.
- One commit = one complete result (or one fix). Do not push a result in slices.
- If you cannot run `verify.py --changed`, do not push Lean files: post the patch in your task comment on issue #474.
- A red GitHub Actions run on your commit is yours to fix or revert immediately.

## 2. Files you add (nobody edits a shared file)

- **Lean result:** a new directory `lean/P196/<ResultName>/` and one registry fragment
  `lean/registry.d/<ResultName>.json` of the form `{"<ResultName>": {"id": ..., "title": ..., "scope": ...,
  "roots": [...], "modules": [...], "endpoints": [...]}}`. `scope` is one paragraph that also says what is **not**
  claimed. `endpoints` are the theorems a reader should trust. `verify.py` rejects unregistered Lean files.
  Do not edit `lean/registry.json` (frozen legacy part).
- **Result note:** `results/<ResultName>.md`, at most 15 lines: the claim, the label (see 4), the scope, the paths of
  the code or Lean files. Do not edit `RESULTS.md`; the maintainer assembles it from `results/`.
- **Computation:** code and compact data under `calculation/<topic>/`; release zips and the engine page as before
  (`lychrel196_v<N>[_<suffix>].zip`, `math_v<N>.zip`, `196-Engine-Fixed.html`). Every computed claim ships the
  command that reproduces it.
- **Report:** only if a result needs more than 15 lines: `reports/<ResultName>.md`. No other documents.

## 3. Coordination: issue #474 only, no manager

- Before starting, read the last 40 comments of #474 and `OPEN_PROBLEMS.md`. Pick a task nobody holds.
- Claim with one comment: `CLAIM agent-<N>: <task id from OPEN_PROBLEMS.md or one line> -> <expected output>`.
- When done, one comment: `DONE agent-<N>: <commit hash> <one line>`. If you give up: `RELEASE agent-<N>: <task> <why>`.
- A claim with no DONE after 24 hours may be taken by someone else. No other comments, no `[task]` issues, no reviews.

## 4. What counts as a result

A commit must change what is known: a new theorem or certificate; a decided item from `OPEN_PROBLEMS.md` (an
UNDECIDED becomes COMPUTED, PAPER PROOF or LEAN-VERIFIED); or a bug fix. Not accepted:

- a re-verification of a result already on `main`, unless it finds a discrepancy (then report the discrepancy);
- one more slice of a census whose other slices are not done (finish the census, then push once);
- a restatement of an existing result with a new name; search `results/`, `RESULTS.md` and the registry first;
- logs, transcripts, probe files, failed attempts, evidence bundles, base64 archives. Keep those locally.

Label every claim exactly one of: LEAN-VERIFIED, COMPUTED (exhaustive program run, state caps stated), PAPER PROOF,
UNDECIDED. A negative result must state its exact scope (bases, periods, widths, caps).

## 5. Lean rules

- No `sorry`, `admit`, custom `axiom` or `native_decide`. Allowed axioms: `propext`, `Classical.choice`, `Quot.sound`.
  No meta-programming that could bypass the kernel (`set_option debug.*`, `run_cmd`/`run_elab`/`run_meta`, `addDecl`,
  `implemented_by`, `@[extern]`, `unsafe`, `elab`, `#eval`). `verify.py` replays every built module with lean4checker.
- No duplicates: import existing modules instead of copying; `verify.py` rejects byte-identical files.
- **Build budget:** every Lean file compiles on one core with at most **8 GB and 20 minutes**
  (`/usr/bin/time -v lake env lean <file>`). Split big certificates, or prove a Boolean checker correct once and run
  it with `decide +kernel` / `rfl` on compact data (see `lean/P196/LatticeBand/Base9.lean` for the pattern).
  A proof that cannot fit is not committed; describe it in a `[heavy]` comment on #474 with peak memory and time.
- Toolchain: Lean 4.19.0 (pinned in `lean/lean-toolchain`), no Mathlib.
