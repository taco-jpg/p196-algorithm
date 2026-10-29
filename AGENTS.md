# COORDINATION MOVED TO ISSUE #475 (read this before posting anything)

**Issue #474 is FULL: GitHub disables commenting after 2500 comments (HTTP 403 since 2026-10-29 06:02 UTC). Post ALL CLAIM / DONE / RELEASE / ALERT / FEED / COMBINE / BREAK / SUMMARY lines in issue #475 ("DISCUSSION ROOM 2") instead. Wherever these instructions say "#474", read "#475". The last 40 FEED/COMBINE lines are on pages 20-25 of #474's comments (read-only); current focus is target T* in docs/FOCUS_SWARM.md.**

# MISSION (owner, read before anything else)

**We are here to PROVE that a decimal Lychrel number exists. We are not here to fill the repository with results.**
The deliverable is one thing: a mathematically complete argument -- ideally Lean-checked -- that some base-10 number
never reaches a palindrome. A pile of computed facts, horizon measurements, exclusions or formats without a decimal
instance is not a partial success; it is noise that hides the one result that matters. Before you push anything ask:
"Does this make an all-time proof strictly closer? Which exact lemma does it supply?" If you cannot answer in one
sentence, do not push it. Prefer one hard attempt at a missing lemma over ten easy computations. Quality over quantity.

# OWNER DIRECTIVE (read this first; it overrides every earlier definition of "progress")

**Finite-horizon replays are worthless here. Do not produce them, push them, or post them as ALERT/DONE.**
"The orbit of seed S survives 20,000 (or 100,000, or 10^6) steps without a palindrome", "uniform in Q for T steps",
"all Q >= q0 for the first T steps" -- for ANY horizon T such seeds exist trivially (196 itself survives millions of
steps). They are public knowledge, prove nothing, and cost everyone review time. Earlier prompts that said
"a 20,000-step replay counts as progress" were wrong; ignore them.

**The only things that count:**
1. A decimal certificate: a template family T(m) (exterior + band + centre, symbolic length parameter m) with a
   finite checked edge cycle T(m) -> ... -> T(m') for m' > m, covering ALL m >= m0, so the orbit is non-palindromic
   for ALL steps. Post ALERT only for this, and include the exact statement of what is proved for all steps.
2. A theorem (PAPER PROOF or LEAN-VERIFIED) that closes a specific gap of the known mechanisms for ALL time (e.g.
   a periodic repair of the defect that finite-horizon families consume, an invariant of the pair-word dynamics,
   a sound growing-centre format together with an actual decimal instance).
3. A reduction of the open problem to a finite computation that you then actually carry out.

If your mechanism loses a defect budget every cycle, your job is to find the REPAIR that restores it forever, not to
measure how long it lasts. If you cannot close a mechanism, say exactly which single lemma is missing and attack it.
Do not push exclusion results or horizon measurements. Do not ask the owner anything.

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
