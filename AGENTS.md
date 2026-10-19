# Rules for contributors (people and agents)

The repository has one branch, `main`, and it must always pass `python3 tools/verify.py` (the full check,
run nightly by GitHub Actions).

1. **One branch, verified pushes.** Commit directly to `main`; never create branches, pull requests or tags, never
   force-push or rewrite history. Before every push run
   `git fetch && git rebase origin/main && python3 tools/verify.py --changed`; it must end with `ALL CHECKS PASSED`
   (rerun it if the rebase brought in new commits). `--changed` checks the repository rules everywhere, but builds and
   audits only the files you added or changed and the files that import them, so it takes minutes, not hours.
   GitHub Actions repeats this check on every push and checks the whole repository every night; a red run must be
   fixed or reverted at once. One commit = one complete result or one fix. Discussion and task claims happen in
   GitHub issues (one `[task]` issue per task; issue #61 for coordination). If you cannot run `verify.py --changed`,
   do not push: post the patch in the task issue instead.
2. **Every Lean file is part of a registered result.** A new result is a new directory `lean/P196/<ResultName>/`
   plus one entry in `lean/registry.json` with: `scope` (one paragraph, including what is *not* claimed),
   `roots`, `modules`, `endpoints` (the theorems a reader should trust). `verify.py` rejects unregistered files.
3. **No duplicates.** Import existing modules instead of copying them; `verify.py` rejects byte-identical files.
   Before proving something, search `RESULTS.md` and `lean/registry.json` for an existing statement.
4. **No escape hatches.** No `sorry`, `admit`, custom `axiom` or `native_decide`. Allowed axioms: `propext`,
   `Classical.choice`, `Quot.sound`.
5. **Commit results, not process.** No logs, review transcripts, evidence bundles, base64 archives, probe files or
   failed attempts in the repository. Keep those locally.
6. **Update `RESULTS.md`** with the new result in the right topic section.
7. **Computation** goes in `calculation/`: release zips named `lychrel196_v<N>[_<suffix>].zip`, math packages
   `math_v<N>.zip`, and the single engine page `196-Engine-Fixed.html`.

8. **Build budget.** Every Lean file must compile on one core with at most **8 GB of memory and 20 minutes**
   (check with `/usr/bin/time -v lake env lean <file>` on Linux, `/usr/bin/time -l` on macOS). `verify.py` must run on
   an ordinary 16 GB machine, which is also what GitHub Actions has. A heavier proof is not accepted as one file:
   split the certificate into several files that each stay within budget, make the checker cheaper (e.g. a
   Boolean checker function proved correct once, then `decide +kernel` or `rfl` on compact data), or open an issue
   before committing it. See "Heavy proofs" below.

### Heavy proofs

A correct proof that needs more than the build budget is still valuable, but it cannot be on `main`, because then
nobody with an ordinary machine (and no CI run) could verify `main`. Order of preference:

1. **Split it** into files that each fit the budget (most certificate proofs are a list of independent cases).
2. **Make the check cheaper**: prove a Boolean checker correct once, then evaluate it on the data with
   `decide +kernel` / `rfl`, instead of elaborating a huge `decide` term.
3. If neither works, open an issue `[heavy] <statement>` with the file, its peak memory and time, and the machine it
   was checked on. The owner decides whether to set up a separate heavy-proof check on a large machine.

Toolchain: Lean 4.19.0 (pinned in `lean/lean-toolchain`), no Mathlib.
