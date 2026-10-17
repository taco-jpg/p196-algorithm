# Independent review of the PR165 local transition-table repair

## Verdict and exact scope

**PASS for the exact repaired source blob `b7e822320361fa7c5bd2b443cc7156f73c995a78` and its two-project-module dependency closure.**

The reviewer is the genuine delegated agent `/root/pr165_independent_review`, commissioned by Agent #19 in session `8ff2ac434c0b`. The reviewer did not author or modify the project repair. The reviewer independently read the original and repaired source, the entire imported project module, the original finite discovery experiment, the role safeguards, and `AGENTS.md`. The reviewer wrote only independent verification and review artifacts. There were no source-branch writes, remote review submissions, Ready transitions, merges, or runtime changes by this reviewer.

The accepted result remains a local six-row classification with six concrete executable decoder equalities. The source still describes an incremental WIP checkpoint. This review does not establish an accepted-word recurrence or counting theorem for every `r`, ordinary-number predecessor realizability, a uniform depth bound, or a 196 reachability or exclusion result. It does not certify a combined tree with current `main` or complete PR165's broader integration gates.

## Exact inputs

Original PR head: `cb273afa5b2827e3427d7098e2e13564701d349a`.

| Input | Git blob | SHA-256 |
|---|---|---|
| Original `ResidualFivePredecessorFilter.lean` | `73887468f8915540fc76a9654116d54db24b593e` | `e5e1187f750ce73181c6294c724052eaca1d6f30d81d7533c266a79b5bf58aee` |
| Repaired `ResidualFivePredecessorFilter.lean` | `b7e822320361fa7c5bd2b443cc7156f73c995a78` | `6c685db9d906e15ffa734c3e0382d31221e487992de94d1618a77ff424e530a7` |
| `Agent105DecoderLocal9df76b.lean` | `e03c9a6cc7aadb7e882c47417411e3e091264683` | `820d28d68005208ac21dd498dcd27660b58d2d147de265dbcd0cf0d7c250e872` |

The target path is `proofs/contributions/agent-103/residual-five-predecessor-filter-count-20261016/ResidualFivePredecessorFilter.lean`. Its only project import is the original decoder at `proofs/contributions/agent-103/residual-five-third-gate-20261016/vendor/Agent105DecoderLocal9df76b.lean`; that module imports official `Std`. Exact source snapshots, repository paths, command arguments, environments, exit codes, timings, and log hashes are retained in [the successful attempt](attempt-002/result.json) and its [file manifest](attempt-002/FILES.json).

All seven theorem headers match the original byte for byte. Everything from the comment introducing the six executable equalities through the end of the target file also matches the original byte for byte. The [exact repair patch](attempt-002/inputs/repair.patch) changes only the proof of `validEdge_sum_nine_iff`.

## Mathematical and executable assessment

The theorem quantifies over `u v a b : Nat` and `E : Edge`, with exactly the original assumptions `u + v = 9`, `a ≤ 1`, and `b ≤ 1`. Naturality and the sum equation already imply `u,v ≤ 9`; neither positivity nor an additional digit-range premise has been introduced. Zero digits remain permitted.

Writing `q = E.coeff`, `lo = E.low`, and `hi = E.high`, the original validity relation is precisely:

```text
q ≤ 18, lo ≤ 1, hi ≤ 1,
q + a = u + 10*lo,
q + hi = v + 10*b.
```

The two complete column equations and the sum premise give `2*q + a + hi = 9 + 10*(lo+b)`. Since `a` and `hi` are bits, parity forces `a+hi=1`, and consequently `q=4+5*(lo+b)`. Among the resulting eight combinations of `a,b,lo`, two contradict nonnegativity of `u` or `v`. The remaining six are exactly:

| `a` | `b` | `u` | `v` | `q` | `lo` | `hi` | Existing endpoint suffix |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0 | 0 | 4 | 5 | 4 | 0 | 1 | `decodePair_sum_nine_00` |
| 0 | 1 | 9 | 0 | 9 | 0 | 1 | `decodePair_sum_nine_01a` |
| 0 | 1 | 4 | 5 | 14 | 1 | 1 | `decodePair_sum_nine_01b` |
| 1 | 1 | 5 | 4 | 14 | 1 | 0 | `decodePair_sum_nine_11` |
| 1 | 0 | 0 | 9 | 9 | 1 | 0 | `decodePair_sum_nine_10a` |
| 1 | 0 | 5 | 4 | 4 | 0 | 0 | `decodePair_sum_nine_10b` |

The repair proves the forward implication by extracting and splitting the four bit cases and closing the resulting arithmetic goals with `simp_all` and `omega`. In the reverse implication, each of the six rows is substituted and its closed arithmetic conjunction is proved by kernel `decide`. No assumption, quantified variable, conclusion, import, or decoder definition changes.

The imported decoder's uniqueness, soundness, completeness, successful-result, and failed-result theorems were reviewed together with the private candidate-membership proof. `decodePair` still searches the original four candidate edges and checks the full `ValidEdge` relation. Truncated subtraction can generate a candidate, but cannot bypass either complete equation. `decodeCenter` still uses `q = u + 10*b - a` and checks `q ≤ 18`, evenness, and the complete center equation. These definitions and specifications accept arbitrary natural inputs; the local theorem supplies its own narrower assumptions.

The six advertised equalities continue to invoke the original `decodePair_complete`. The independent audit additionally proves all six equalities directly with `by decide`, exercising the actual executable definitions through the kernel. Four supplementary kernel controls cover an input digit of 10, rejected center subtraction truncation, an odd center coefficient, and a coefficient above 18. All ten control proofs have empty axiom sets. A separate enumeration checked 3,040 arithmetic tuples and reproduced exactly the six rows; it is supplementary finite evidence. The original discovery counts for `r=0..11` remain an experiment, with no promotion to an all-`r` recurrence theorem.

## Independent verification and trust boundary

The successful independent attempt ran from `2026-10-17T05:13:17.447938+00:00` through `2026-10-17T05:13:25.647688+00:00`. It created a new output directory, copied only pinned source inputs, and independently rebuilt both project modules in order. No project `.olean` objects were copied or reused. The official toolchain's standard library was used without rebuilding Lean itself.

The runtime was the retained official Lean 4.19.0 release, commit `6caaee842e94`, with executable SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Its exact version and binary hash were verified, and the retained installation record identifies the official release URL. That record explicitly describes its archive hash as a local hash, not an independently published upstream checksum. The runtime was read and executed, never modified.

Every Lean build and audit used `--trust=0 -j1 -DElab.async=false`, with `LEAN_PATH` restricted to that attempt's fresh source directory and a 120-second process limit. Only one Lean process ran at a time.

| Command | Exit code | Result |
|---|---:|---|
| Build `Agent105DecoderLocal9df76b.lean` | 0 | Fresh dependency object |
| Build `ResidualFivePredecessorFilter.lean` | 0 | Fresh target object; all seven advertised endpoints checked |
| Run `IndependentAudit.lean` | 0 | Complete origin inventory, transitive axiom audit, and ten kernel controls |

The audit uses `Environment.getModuleIdxFor?` and actual imported module names, so generated and private declarations are included. It enumerated **127 declarations and 50 theorem constants**: 27 theorems from the decoder module and 23 from the repaired module. It collected axioms transitively from the kernel environment for every theorem and checked every other safe declaration. The combined theorem axiom set is exactly `{propext, Classical.choice, Quot.sound}`. No custom axiom declarations were present. Literal `#print axioms` evidence also covers all seven advertised endpoints and all four executable roots.

`ValidEdge`, `ValidCenter`, `decodePair`, and `decodeCenter` are safe definitions with **empty axiom sets**. The inventory separately records 47 unsafe compiler-stage implementation helpers, all from the unchanged decoder module and ending in `_cstage1` or `_cstage2`. These are implementation definitions rather than mathematical axioms; they are not used as proof oracles. The checked safe roots and all ten controls remain axiom-free. No `sorryAx`, unsupported mathematical axiom, `native_decide`, `ofReduceBool`, or `skipKernelTC` occurs in the accepted proof evidence. Keyword scans supplement the transitive audit; they do not replace it.

The full successful audit log has SHA-256 `752a26d380e00797e450f9a789fce01d2ea543be88ab764b0175b6238ceaf4ba` and is retained at [IndependentAudit.log](attempt-002/IndependentAudit.log).

## Failed attempts and driver assessment

The author's earlier candidate `8794cab2f2e4be4c21de9d566cbdee56e7b4e06f` failed with a heartbeat timeout in the unsplit forward arithmetic proof. Its resulting `sorryAx` belongs to failed elaboration evidence and is not an accepted dependency. The reviewer inspected and retained this historical evidence without treating it as independent verification or rerunning that unchanged failure.

Independent `attempt-001` freshly built both project modules successfully but its audit exited 1 because the reviewer added the unsupported formatting option `pp.width`. The attempt is retained in full. Only this option was removed from the reviewer's audit file; no project source changed. Independent `attempt-002` then rebuilt both modules in another empty directory and completed the audit with exit 0. The successful audit output is byte-identical to the first audit's output after removing that single formatting-error line. The first attempt's completion-looking diagnostic output was never treated as PASS.

The author replay driver was independently inspected and retained as `context/reviewed_author_driver.py`, SHA-256 `4282b8273d297e8b7d82f0ec26dbb874d575486603e4ca807fa3ae45c08bbecd`. Its source pins, fresh output directory, ordered module compilation, restricted `LEAN_PATH`, exact compiler hash/version checks, complete theorem-origin audit, literal endpoints, and failure preservation are suitable for the stated two-module verification. It accepts explicit repository, compiler, and output paths. Its Python assertions require ordinary, unoptimized Python execution. Its theorem-origin audit permits logging unsafe implementation axioms, but none exists in the exact reviewed modules; the independent audit rejects every project axiom declaration outright. This author driver was assessed as infrastructure evidence, not used to impersonate independent authorship.

The independent [replay driver](verify_independent.py) uses explicit failure checks and an independently maintained [audit source](IndependentAudit.lean). Replays require the exact pinned files, the stated Lean binary, and a new output directory. Neither driver alone verifies platform-required checks, source-write ownership, broader PR completeness, or the intended combination with a moving target branch.

## Handoff and preservation

The exact-source review is handed to Agent #19 as the named delivery owner for the isolated repair/evidence scope. Agent #103's active source ownership, the pending publication/handoff decision, PR142's separate prerequisite work, and the current main-writer protocol remain applicable. No source publication, Ready transition, or merge is asserted by this report. Any changed target or dependency bytes require checking the affected obligations against the new exact source.

`review.json` is the final machine-readable review summary. `FILES.json` inventories all local review files other than itself, including both successful and failed attempt records. The planned publication payload **excludes generated `.olean` objects** because they are reproducible build products, and **excludes `context/ROLE_ORIGINAL.txt`** because it is the operational user assignment rather than research evidence. The local manifest may still list these explicitly excluded files; such entries do not claim that their bytes were published. All mathematical source snapshots, both audit attempts, drivers, substantive logs, results, and their hashes are preserved for publication. No retained local evidence was deleted.
