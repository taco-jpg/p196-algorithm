# PR #168 — retained independent evidence qualification

## Decision

**PASS_REUSABLE** for the three new cycle-adapter modules and their exact 30-module build/audit closure at PR head `7f23ce839fcc88acb235b1816c2c57dc12e16a33` (H). The retained independent review and execution evidence qualify for reuse. No fresh Lean run or duplicate independent review is required merely because Agent #16 has accepted delivery ownership.

This decision follows inspection of retained source bytes, actual command records, substantive raw output, the audit implementation, complete evidence manifests, exact Git object identity, and the actual submitted GitHub review. It is not inferred from a badge or PR description. All **28 qualification checks passed**, with machine-readable results in `checks.json` and substantive execution output in `check_reuse.log`.

This is an evidence-reuse qualification, not a claim of a new proof compilation, a new semantic review of every dependency, current-main integration verification, platform approval, or completed merge. The delivery owner remains Agent #16. The combined current-main tree, dependency delivery, ownership, and merge requirements remain with the parent delivery task.

## Exact identities

| Item | Identity |
| --- | --- |
| Repository / PR | `taco-jpg/p196-algorithm` / #168 |
| Reviewed current PR head H | `7f23ce839fcc88acb235b1816c2c57dc12e16a33` |
| Original reviewed source checkpoint S | `6f169320a7a750ea7978093c4cd05140d5d6cc73` |
| Actual submitted review | [COMMENT review 5555324338](https://github.com/taco-jpg/p196-algorithm/pull/168#pullrequestreview-5555324338) |
| Review state / commit | `COMMENTED` / H |
| Review submission | `2026-10-17T01:19:12Z`, GitHub account `sodium-qed` |
| Final registry Git blob | `6bda231e3e4c1e4ac4bfabcbb62016de4a04fd7e` |
| Final registry SHA256 | `239a98f425775ffa41298e1776e7618aed4793f064115f8571f4a29bc0dabac7` |
| Reviewer frozen receipt SHA256 | `8a8b48e385b9208917e86a57035253a335add0168ee7ce355593f63b96e45914` |
| Independent audit log SHA256 | `cd47cbf9f2d1084370e43693e7fa347679b55473861fc785dae4882e3da0e994` |
| Independent command-results SHA256 | `841fe2adc88cc1a6dfb4cdf8ee69b6be4486e0bb611e6f5da4be4ff154e0415f` |
| Source-identity receipt SHA256 | `b6eae334b9f0c5a6b5436267018169b10f5106226048cf425901fab3314bd6dc` |

The actual review was read from the supported GitHub REST review resource, not reconstructed from a conversation comment. Its `commit_id` is H and its state is `COMMENTED`. The exact response is retained as `actual-review-5555324338.json`; the separately retrieved review listing is retained as `actual-pr-reviews.json`.

### The three new mathematical sources

| Source | Git blob SHA1 | SHA256 |
| --- | --- | --- |
| `proofs/Agent1PeriodicCyclePath.lean` | `74012aada269a04ca03bf2cbf2309590e518f009` | `196f04ef0d9ca89e0eb6151905c0f3abf217eefcf8469c32269e0954423384a9` |
| `proofs/Agent1PeriodicCycleGuard.lean` | `3b2ab9ce3628125fb44379bac8ee574c88ae850c` | `357d626233997cd7b1d9b2606c63f196814854abd29f7e72a1a51254c9aa2041` |
| `proofs/Agent1PeriodicCycleNumeric.lean` | `920e7a58f61eba4a913e12ac4d3dd92d0883ce41` | `4cbf4ee50c819e71ee09d108ab62fd703af1287507b969988a09e61b3fe2c527` |

All thirty source paths—not only these three—were compared against the Git trees of both H and S. For each source, the retained compiled-source bytes reproduce the declared SHA256 and Git blob SHA1, and that blob is the source path's blob in both trees. The registry has the same exact byte identity at H and S. `checks.json` contains the complete thirty-row source table.

## Source closure and executed environment

The final registry and the reviewer's source identity record contain the same thirty modules and the same paths, SHA256s, Git blob IDs, and imports. An independent lexical pass masked nested comments and strings, reconstructed literal import edges, and traversed them from `Agent1PeriodicCycleNumeric`. The resulting project closure is exactly those thirty modules; its external source import boundary is `Std`. No unregistered project dependency or unused registered module was found. The recorded compilation order is topological for that closure. The generated audit also imports `Lean` from the toolchain and selects exactly those thirty project modules by module origin.

The retained replay driver was read in full. It creates new build and evidence directories with `exist_ok=False`, copies each pinned source into the empty build directory, verifies the original source against the published source commit, and sets `LEAN_PATH` to that build directory. It records compiler identity, commands, exits, limits, timings, and raw combined stdout/stderr. No retained project `.olean` is used as a source of acceptance. The postcheck verifies that source bytes remained unchanged.

The recorded compiler is official Lean **4.19.0**, commit **`6caaee842e94`**, release for `x86_64-unknown-linux-gnu`; executable SHA256:

`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.

The replay driver enforces that executable hash and version. This task qualifies the existing recorded execution; it did not run, redownload, or independently authenticate a compiler binary. The canonical parent's report separately retains the same executable hash plus four shared-library hash entries.

Each of the independent review's thirty source commands has the form:

```text
/workspace/p196-tools/lean-4.19.0-linux/bin/lean --trust=0 -j1 -DElab.async=false -o <module>.olean <module>.lean
```

The thirty-first command runs `ReviewAudit.lean` with the same explicit trust and threading options and without an object-output argument. All thirty-one commands have recorded exit code zero, `timed_out=false`, and a raw output file whose independently recomputed SHA256 matches its command result. Each command records an 8192 MiB address-space cap and 600-second timeout; the compiler's default stack setting is preserved. The sum of recorded command durations is approximately 77.081 seconds. That is historical execution time, not time spent by this qualification task compiling Lean.

## Substantive audit output

The full `ReviewAudit.log` contains 305,966 bytes. Its entries were parsed independently, including multiline axiom lists; the result is retained in `audit-extracted.json`.

| Coverage | Recount from raw output |
| --- | ---: |
| Project modules with theorem-origin entries | 30 |
| Distinct theorem constants | 1,506 |
| Distinct safe definitions / safe opaques | 243 |
| New-module theorem constants | 31 |
| New-module safe definitions | 2 |
| Public Agent1 theorem types checked | 124 |
| Additional new public definition types checked | 2 |

The thirty-one new theorem constants comprise six from CyclePath, twenty-one from CycleGuard, and four from CycleNumeric. Generated and private proof constants explain why this exceeds the ten public theorem declarations. The two new public definitions are `repeatWordState` and `quotientCycleExponent`.

Every raw theorem axiom list is a subset of `{propext, Classical.choice, Quot.sound}`, and their union is exactly that set. Every safe-definition axiom list uses only `propext`, and the safe-definition union is exactly `{propext}`. Both new public definitions have explicit printed output stating that they depend on no axioms. All twelve advertised new exports have full type output, and all ten public theorems have explicit axiom output in their module logs.

The retained audit implementation traverses environment constants selected by their actual defining module, applies `Lean.collectAxioms` transitively to theorem and safe-definition/opaque declarations, rejects custom safe axioms and any axiom outside the permitted list, and rejects a registered module with no audited theorem. Inspection and raw-log reconstruction agree; no `CUSTOM_AXIOM`, `DISALLOWED_*`, `MODULE_NOT_AUDITED`, `sorryAx`, `Lean.ofReduceBool`, or error output was found. An auxiliary source scan also found no prohibited proof shortcut token in the thirty selected source files. The axiom evidence, rather than the lexical scan alone, supports the logical-trust conclusion.

### Compiler implementation inventory stays separate

The audit retains 976 non-safe compiler/runtime definitions: 945 compilation-stage helpers and 31 `._unsafe_rec` helpers. Every recursion helper's corresponding safe base occurs in the safe-definition audit. Thirteen inherited unsafe implementation axioms occur in `LychrelDigitSums`, with no unsafe opaque and no unclassified non-safe definition. None appears in any checked theorem or safe-definition axiom list. These entries are preserved as implementation inventory, not omitted and not counted as additional allowed mathematical axioms.

## Independence and semantic scope

The real prior review is attributed to Agent #1 specialist `symbolic_scope`. Its formal review, frozen receipt, semantic report, and source-identity record consistently state that this reviewer authored none of the three new cycle-adapter modules. Prior authorship of some already frozen dependency modules is explicitly disclosed. The reviewer rebuilt the full dependency closure, but that execution does not become an independent semantic review of the reviewer's own prior mathematical authorship. Existing dependency acceptance remains a separate upstream obligation of the delivery campaign; this qualification does not replace those earlier reviews.

The supplementary reviewer `/root/research_status` is separately identified as a same-session/account nonauthor specialist. Its semantic report and inspection receipt explicitly say that it performed source inspection only, with no Lean execution. Its three observed source hashes match the final published sources exactly. Its historical registry SHA256 is `8349b90f3ea7c41ab44fccb8c0c37de38ee989789c6cd4d8ce1e79137361886e`, different from the final registry's hash; nevertheless, its entire thirty-module pin map is identical to the final map. The historical observation is not relabeled as final-registry execution evidence.

Neither different specialist names nor the GitHub account establishes a separate eligible GitHub approval. The formal state is COMMENTED, and this report does not promote it to APPROVED. Project-required nonauthor review is supported by the actual identified specialist work and its retained execution; any platform-specific approval requirement must be handled by the delivery owner under the actual repository requirements.

The reviewed result remains conditional on a supplied positive-length full quotient cycle, initial `ValidPeriodic`, literal B/H/w endpoint equalities, and, for palindrome avoidance, explicit safety at every cycle residue. The retained semantic report examines full endpoint repetition, guards before natural subtraction, one global schedule, one positive seed chosen before arbitrary time, canonical width and all in-range column sums, and the successor seed needed to align safety with `IsLychrel` at time zero. It claims no concrete qualifying cycle, unconditional decimal seed, projected-walk realization, or result for 196. The raw checked endpoint types agree with these boundaries. The parent's separate mathematical reading remains complementary delivery work, not a newly imposed duplicate review gate.

## Preservation and historical flags

All 184 paths under the selected `review/`, `complementary-review/`, and `verification/` prefixes match their H-tree Git blobs. Missing local Git objects were recovered through supported GitHub blob reads; local absence was never treated as remote absence. Eighty-three distinct absent evidence blobs were recovered, each validated against its expected Git blob SHA1. The final registry was separately fetched at exact H and similarly validated.

The full manifests verify as follows:

| Manifest | Entries checked | Result |
| --- | ---: | --- |
| `review/evidence-files.json` | 108 | Every size and SHA256 matches |
| `verification/parent-clean-001/FILES.json` | 63 | Every original size and SHA256 matches |
| `verification/parent-clean-001/PACKAGE_FILES.json` | 67 | Every package size and SHA256 matches |
| `complementary-review/FILES.json` | 6 | Every size and SHA256 matches |

The original parent manifest SHA256 is `7208470b86bce64ba8cd9d13624ec80febc592f2034e873646eddf175aa2de77`. The package adds metadata and a checker snapshot without amending the original manifest. The exact canonical checker snapshot has SHA256 `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a` and matches `proofs/verify_project__214bf7673efe116b.py` in both H and S.

The canonical parent independently records thirty source compiles plus ProjectAudit, all exit zero with matching raw-log hashes, and a 1,506-theorem audit. Its thirty source snapshots equal the independent review's source snapshots. Its commands contain **no explicit trust override**; its original `source_tree_clean=true` means the checker's tracked-file status was clean under `git status --porcelain --untracked-files=no`. Both fields remain intact. The explicit trust-zero claim belongs to the separate reviewer run, not retroactively to the parent run.

Historical registry fields still say `FROZEN_AUTHOR_CHECKED_FRESH_REVIEW_PENDING`, and historical catalogue text says parent/fresh review was pending. These are preserved pre-execution status fields. The later actual parent verification, independent execution, frozen receipt, and formal review document completion. They do not justify rewriting original historical flags, and their stale wording is not evidence that the later recorded commands did not run. The scope remains a thirty-module contribution, not a repository-wide accepted catalogue.

## What this task executed and what it reused

Executed here: read-only Git tree/object inspection; supported read-only GitHub evidence retrieval; SHA256 and Git blob SHA1 reconstruction; full manifest checks; literal-import closure and compilation-order reconstruction; raw theorem/definition/runtime inventory parsing; command/exit/log/flag comparisons; exact submitted-review inspection; and preparation of this report and its machine-readable evidence. The shared source repository was not mutated. No Lean compiler, retained replay script, or retained checker was executed.

Reused: the previous nonauthor reviewer's clean thirty-module trust-zero build and ReviewAudit, the canonical parent's separate execution, the two retained semantic reports with their stated scopes, compiler/environment provenance, and reviewer authorship disclosures. No new mathematical claim or platform approval was created.

The first run of this local metadata checker expected five complementary-manifest entries; inspection showed six, all byte-correct. That local expectation was corrected to six. The first output is preserved in `check_reuse-attempt001.log`; it was not a Lean failure or a defect in the submitted evidence. The final local checker returned exit zero and PASS_REUSABLE.

## Delivery consequence

The existing review/build gate for the exact cycle-adapter sources should be treated as satisfied. Preserve the named review reference and exact source/registry hashes in the delivery packet. The next action belongs to the same PR's integration work: finish or verify prerequisite integration, compare this thirty-module source/registry closure with the intended combined tree, and proceed through the actual target-write protocol and applicable platform gates. If the combination leaves all selected source bytes and toolchain assumptions unchanged, this evidence remains reusable; a new merger, unrelated coordination metadata, or an evidence-only commit does not itself create a new Lean or independent-review obligation. A change to a selected source, its import closure, or the relevant environment requires only the corresponding affected revalidation.

## Local deliverables

- `checks.json`: complete check results, thirty source pins/imports, all command comparisons, four manifest results, every selected evidence-file hash, formal-review identity, and qualification limits.
- `check_reuse.py` and `check_reuse.log`: inspectable non-compiling qualification procedure and its final substantive output.
- `audit-extracted.json`: all 1,506 raw theorem entries and 243 safe-definition entries with normalized axiom sets.
- `actual-review-5555324338.json`: exact GitHub review resource proving review state and commit binding.
- `fetched-hashes.json`: verified identities of the eighty-three recovered evidence blobs.
- `retained/`: exact retained evidence bytes and selected source snapshots.
- `SHA256SUMS.json`: hashes for this qualification packet's primary new deliverables.
