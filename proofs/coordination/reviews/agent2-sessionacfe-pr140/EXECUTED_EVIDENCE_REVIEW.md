# Independent review of PR140 executed verification evidence

**Review status: the exact `run-001` proof/audit evidence passes this independent evidence review.** The owner also resolved the replay-wrapper optimization finding with a narrowly scoped explicit guard; I independently inspected that change and its bounded negative-check receipt. The original execution and later guard check remain separately identified below.

**Reviewer:** the genuine `/root/audit_coverage` specialist for Agent #2/session `acfe54025bfc`. This specialist reviewed the source and audit design before execution, then independently inspected the actual wrapper, generated audits, complete retained log data, and receipts. This specialist did **not** execute Lean, author the mathematical source, modify an audit, or perform a second build. The only specialist-authored files are this document and `AUDIT_DESIGN_REVIEW.md`.

**Ownership remains unchanged:** Agent #29/session `1f13321af678` owns delivery; Agent #11/session `c68b` owns combined semantic/integration review; Agent #102 owns mathematical source; Agent #31 owns main. This evidence review supplies no main-write claim or merge authorization and does not replace Agent #11's review.

## 1. Exact scope and outcome

The execution receipt records:

- PR source head: `1c1bff874c915d90d2820090e028b40002145375`.
- Observed main base: `74a1c3922eb7af438fe40b23d2105ad07556e3f5`.
- Input kind: exact-commit source snapshot, not a full repository checkout.
- Fresh contribution build: thirteen registered modules.
- Literal audit: 140 distinct explicit theorem targets, including both names containing `?`.
- Module-origin audit: 403 distinct theorem constants, all thirteen selected modules represented.
- Unsafe implementation axiom records: 26 distinct records, retained explicitly.
- Executable dependency audit: sixteen specified roots, each nonempty, each with `forbidden=0`.
- Commands: eighteen recorded commands, all with exit code zero. These consist of two toolchain introspection commands, thirteen contribution-module compilations, and three audit compilations.
- Sum of recorded command durations: 20.220355 seconds. Receipt wall duration: approximately 20.648536 seconds.
- `repository_wide_pass`: `false`.

I independently recomputed hashes and parsed the logs rather than accepting these receipt totals alone. The checks described below produced no discrepancy or disallowed theorem axiom.

The hardcoded head/base fields identify the parent's selected source packet and observed base; this wrapper does not fetch GitHub, construct an H+B tree, or independently certify remote provenance. This review confirms local bytes, executed-command records, generated audit logic, and output consistency. Source acquisition provenance and combined-tree adequacy remain separate evidence obligations owned by the parent and Agent #11.

## 2. Inputs, compiler, and retained-file integrity

The registered source registry SHA-256 is:

```text
a74dbe385c0b1ea59e68ebe9266df08e27e751b49ce093d6064f75ac3157bd69
```

Its Git blob hash is `1530f8777cae7af40eb341503b702cbf996c0fef`.

For every one of the thirteen registered modules, I checked both the original source snapshot and the build-directory copy against the registry's SHA-256 and Git blob hashes. All 26 file comparisons passed. The registry copy in the execution directory is byte-identical to the source registry. The import graph matches the registry and reaches every registered module from `Agent102ParameterSetControls`; the only direct external contribution import is `Std`.

I checked all 37 entries in the original execution `FILES.json`: each path exists, each byte count matches, and each SHA-256 matches. I also checked every recorded command-log hash independently. The manifest intentionally omits `.olean` files; it binds the reproducible source, audit, log, and receipt evidence, not a binary-object archive. This unchanged manifest describes the original completion snapshot. The later `run-001/runner-as-executed.py` preservation copy and review artifacts were not present in that snapshot and are intended for the owner's separate outer publication inventory; I do not claim that the original 37-entry manifest covers those additions.

The actual runner hash in the receipt matches the inspected pre-repair wrapper bytes:

```text
2736cd8f0a3ba976bbdf70c9d51f1e128b462d61c0846499c9cf0db049209b84
```

The recorded compiler is Lean 4.19.0, commit `6caaee842e94`, Release. The current compiler and all four shared-library files recorded by the run still match their recorded hashes. The Lean executable SHA-256 is:

```text
92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023
```

This verifies the recorded executable/shared-library identity. The wrapper does not individually hash every imported standard-library `.olean`; the established pinned toolchain remains the trusted external foundation rather than an independently rebuilt standard library.

The wrapper creates a new output directory with `exist_ok=False`, writes the exact source copies into its new build directory, and asserts that no `.olean` is present before compilation. Its commands use `--trust=0 -j1 -DElab.async=false`, an explicit build-directory `LEAN_PATH`, and a 180-second per-command timeout. It invokes subprocesses directly without a shell and passes only `PATH`, `LANG`, and `LEAN_PATH`. Failed commands or timeouts raise a failure, retain the log, and cannot reach the final `PASS` assignment under the supported assertion-enabled invocation.

## 3. Literal audit: complete names and enforced axiom policy

The wrapper's input-name parser uses `\S+`, and its output parser captures the complete name inside single quotes. Neither rejects or truncates `?`. It requires 140 unique input targets, exact equality with the 138 registry endpoints plus two extras, exactly 140 parsed output reports, and equality of the output-name set with the expected set. It then rejects any literal axiom outside `{propext, Classical.choice, Quot.sound}`.

I independently parsed every complete line of `logs/LiteralAudit.log`, required every line to match the expected report grammar, checked the exact name set and axiom sets, and compared the result with `literal-results.json`. All checks passed. In particular:

| Literal theorem | Reported axiom set |
|---|---|
| `Agent102.getElem?_word_of_mem_spansFrom` | `propext`, `Classical.choice`, `Quot.sound` |
| `Agent102.getElem?_word_of_covers` | `propext`, `Classical.choice`, `Quot.sound` |

Both are also present in the module-origin output. The union over all 140 literal outputs is exactly the three permitted foundational axioms. All ten concrete `_certificate` theorems report an empty axiom set; their corresponding semantic `_exact` theorems remain separately included in the literal and module-origin checks.

## 4. Module-origin audit: complete selection and no forbidden theorem axiom

The generated `build/ModuleOriginAudit.lean` imports the real closure root and Lean, selects exactly the thirteen registered modules, and rejects any missing selected imported module before enumerating constants. Selection uses Lean's imported-module origin, not a namespace-prefix or restricted name parser.

For each selected `.thmInfo` constant, `Lean.collectAxioms` computes the transitive axiom dependency set; the generated Lean command throws an error if any member is outside the unchanged three-axiom allowlist. A safe custom `.axiomInfo` declaration is rejected. Unsafe implementation `.axiomInfo` entries are logged separately, as in the published template.

The Python wrapper requires one full-module summary, matching theorem-row count, nonempty unique theorem names, and inclusion of every literal target. The Python expression used to count origin rows does not reconstruct wrapped axiom lists; **the axiom-policy enforcement occurs inside the executed Lean audit before each success row is emitted**. This is not a bypass. For independent corroboration, I reparsed all complete bracketed axiom lists across line breaks and checked each set directly.

Results by Lean-recorded module origin:

| Module | Audited theorem constants | Unsafe implementation records |
|---|---:|---:|
| `Agent102RunDefs` | 25 | 2 |
| `Agent102AffineArithmetic` | 37 | 0 |
| `Agent102RunWord` | 49 | 0 |
| `Agent102RunEndpoints` | 42 | 1 |
| `Agent102AffineRuns` | 29 | 2 |
| `Agent102ParameterIntervalDefs` | 9 | 9 |
| `Agent102ParameterIntervalAlgebra` | 50 | 0 |
| `Agent102ParameterIntervalCompact` | 18 | 5 |
| `Agent102AffineInequalityIntervals` | 14 | 0 |
| `Agent102PiecewiseCounts` | 39 | 5 |
| `Agent102AffineRunParameterSets` | 33 | 2 |
| `Agent102ParameterSetDecisions` | 24 | 0 |
| `Agent102ParameterSetControls` | 34 | 0 |
| **Total** | **403** | **26** |

These are imported-environment origin counts, including generated equation, auxiliary-proof, and datatype theorem constants. They are not the handwritten theorem counts from the design report.

All 403 complete axiom lists are subsets of the allowed set. Their union is exactly `{propext, Classical.choice, Quot.sound}`. No `sorryAx`, user axiom, native-decision oracle, or any of the 26 unsafe implementation axiom names occurs in those theorem dependency lists.

The 26 implementation records are not suppressed, reclassified as foundational axioms, or claimed to be rejected. Their names describe generated specializations of standard list/array operations and derived representation/equality machinery; the exact source review found no user-written `unsafe` or `axiom` declaration. Representative records include `List.flatMapTR.go._at.Agent102.word._spec_1`, `List.mapTR.loop._at.Agent102.ParameterSets.equalityRegions._spec_1`, and `Array.foldrMUnsafe.fold._at.Agent102.ParameterSets.fastInterAll._spec_2`. The complete ordered list in `verification.json` exactly matches the 26 unique log records. This is evidence of the preserved implementation boundary, not certification of machine-code implementations.

## 5. Executable traversal: no vacuous pass for the declared scope

The generated executable audit preserves all five forbidden names:

```text
List.range
List.replicate
Agent102.word
Agent102.wordAt
Agent102.ParameterSets.CountExpr.value
```

It checks the forbidden list before testing module membership. It rejects an absent root, a root without an imported-module origin, a root outside the selected modules, and an absent encountered constant. Each selected declaration contributes its type's and available value's used constants to the pending traversal. A per-root visited set prevents duplicate counting.

The wrapper requires exactly sixteen summary records, the exact requested root set, and a strictly positive project-constant count for every root. Exact record count plus exact set equality prevents a duplicated success row from replacing an omitted root. Independently, I checked every project-dependency row, required unique declarations per root, reconciled each row count with its summary, and verified that the root itself appears in its visited project declarations. All sixteen roots passed these stronger output consistency checks.

All names below have prefix `Agent102.ParameterSets.`:

| Root suffix | Project declarations | External frontier records | Forbidden |
|---|---:|---:|---:|
| `CountExpr.pieces` | 33 | 47 | 0 |
| `comparisonRegion` | 35 | 47 | 0 |
| `ltRegion` | 36 | 47 | 0 |
| `leRegion` | 36 | 47 | 0 |
| `eqRegion` | 39 | 47 | 0 |
| `equalityRegions` | 59 | 53 | 0 |
| `palindromeRegions` | 60 | 54 | 0 |
| `equivalentRegions` | 17 | 29 | 0 |
| `hasEqualParameter` | 60 | 53 | 0 |
| `hasUnequalParameter` | 60 | 53 | 0 |
| `everyParameterEqual` | 61 | 54 | 0 |
| `everyParameterUnequal` | 61 | 54 | 0 |
| `hasPalindromicParameter` | 61 | 54 | 0 |
| `hasNonpalindromicParameter` | 61 | 54 | 0 |
| `everyParameterPalindromic` | 62 | 55 | 0 |
| `everyParameterNonpalindromic` | 62 | 55 | 0 |
| **Total per-root records** | **803** | **803** | **0** |

The totals count a declaration again when it is reached from a different root. They are not counts of globally distinct declarations.

I parsed all 1,622 executable-log lines: 803 project dependency records, 803 external frontier records, and sixteen summaries. No line was unclassified. No logged dependency matched a forbidden name. Every project record names a selected module. Every external frontier record belongs to one of these five modules:

```text
Init.Prelude
Init.Data.Int.Basic
Init.Data.Int.DivMod.Basic
Init.Data.List.Basic
Init.Data.Nat.Basic
```

The expected solver machinery is visibly reached, including `widthExpr`, `spanExprs`, `spanExprsFrom`, `agreementRegion`, `overlapRegion`, interval intersection/complement/pruning, and inhabitedness. The sixteen root checks therefore cover substantive implementation declarations rather than just a nominal import or an empty root list.

## 6. Honest scope boundaries

The receipt explicitly identifies the executable audit as a traversal of selected project declaration types and bodies, with external library declarations recorded as frontier nodes. It expressly excludes arbitrary `comparisonRegion` callback implementations. This wording matches the generated code and observed logs.

The audit is not an unrestricted standard-library or machine-code runtime dependency audit, a complexity proof, or an audit of every executable definition in the thirteen modules. It also is not a standalone check of `ParameterSets.test`, which was optional and was not added as a seventeenth root.

The older `Agent102.equalOnTail` and `Agent102.palindromicOnTail` functions deliberately expand `wordAt`; they remain outside the no-expansion executable-root claim. Their mathematical specification theorems are still included in the full theorem audits. No forbidden name was removed or exempted to conceal this distinction.

The fresh thirteen-module run verifies this contribution's selected closure. It does not demonstrate an actual integration with all of base B, rebuild the entire repository, establish decimal reverse-add iteration closure, instantiate a realizable infinite safe family, or solve P196. Those claims are not made by this receipt.

## 7. Exact evidence hashes

Paths in this table are relative to `/workspace/scratch/acfe54025bfc/pr140/`. They identify the reviewed original run evidence. The optimization repair has a separate identity in Section 8.

| Evidence | SHA-256 |
|---|---|
| `run-001/runner-as-executed.py` | `2736cd8f0a3ba976bbdf70c9d51f1e128b462d61c0846499c9cf0db049209b84` |
| `run-001/verification.json` | `36c2340c03fb03c2735ab51187b94e3ec2e98f1aebdfec98d50d076e8b336250` |
| Original `run-001/FILES.json` | `1c366c3c08fd9e93ec416c3d3bcbddec85cfa24663ce78a04915ffd1e047cab6` |
| `run-001/literal-results.json` | `5b169351bf1e57e7fed2f35dd34586ed9b3655467f109143d7b1c16977a46ed6` |
| `run-001/build/LiteralAudit.lean` | `d01b5243de23b4a753a32fbe451aaf6b8a1aa83c9236ba847d90658e59d35bdc` |
| `run-001/build/ModuleOriginAudit.lean` | `884420c221549223a830fbb815d552744925cb0e812e51ecbbc7ffc97c75e1e3` |
| `run-001/build/ExecutableDependencyAudit.lean` | `6e4b00981ac0a856f1951b8aeb4d22b89ce63984e17abb73bd5bc73690631a56` |
| `run-001/logs/LiteralAudit.log` | `e9aa2670e5c2ff82620c784b84190cd0389f8d1a9b483dadb5d57de300196cfe` |
| `run-001/logs/ModuleOriginAudit.log` | `7cac8bfae7cf92356a4506878f949ef7adf83ac4113e8d4f034a3c4adf0e8164` |
| `run-001/logs/ExecutableDependencyAudit.log` | `058bc10174b40ca2489f219fa44cd7a4dd8c62c21b3a549f7d2ee9b6d606a482` |
| Inspected source-parser helper | `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a` |

The original module-origin template hash is `2ea57e7a511fbf4d9f34eee9e06011b3812980c38de17d9e32f8c4f2dd67a486`; the original executable template hash is `9c77a3858196f12fec1cba67d3f94944e0de6d6053bc21ca91baa6dfcb083417`. The adapted hashes above match `verification.json`.

## 8. Replay-wrapper finding and owner repair

The actual executed wrapper uses Python `assert` for several critical preconditions and output checks. Running it with `-O`, `-OO`, or an optimization-enabling environment would disable those checks. This is a concrete replay robustness finding. It does not invalidate the already inspected `run-001` output: this specialist independently repeated the relevant source/hash, name-coverage, axiom-set, nonvacuity, and log-consistency checks without running Lean.

The owner preserved the exact originally executed wrapper as `run-001/runner-as-executed.py`. I independently recomputed its hash and confirmed equality with the original `verification.json` runner hash. The current `run_exact_verification.py` differs from that preserved file by exactly these two lines at the beginning of `main()`:

```python
    if not __debug__:
        raise RuntimeError("Python optimization disables verification assertions; run without -O and without PYTHONOPTIMIZE.")
```

This is an explicit runtime branch, not an `assert`, and therefore remains effective when Python disables assertions. It executes before argument parsing, output-directory creation, source preparation, and any Lean subprocess. The ordinary assertion-enabled verification path is otherwise unchanged. The guard also applies to `-OO` and optimization enabled through the environment because those modes make `__debug__` false; only the owner's actual `-O` invocation is claimed as executed evidence.

The owner recorded this bounded negative check in `optimization-guard-check.json`:

```text
python3 -O /workspace/scratch/acfe54025bfc/pr140/run_exact_verification.py
  --lean /tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean
  --output /workspace/scratch/acfe54025bfc/pr140/must-not-exist-optimized-output
  --prepare-only
```

The receipt records exit code **1**, empty stdout, the expected optimization-rejection traceback, and `output_created=false`. I independently inspected the receipt, matched its wrapper hash to the current file, and checked that the named output path does not exist. The rejection occurs before Lean execution. This is an intentionally retained failed precondition check, not a failed mathematical build or a replacement proof result.

| Later replay evidence | SHA-256 |
|---|---|
| Current `run_exact_verification.py` | `4d19f706f98320d7243418e45b216eb7e564eebf5d923f715e7ca8f80a1652a8` |
| `optimization-guard-check.json` | `5a518fd809d7a35d29bd3722daabab886272f92ca94dd80c5053af311059ccda` |

The original `verification.json` and its 37-entry `FILES.json` retain their original hashes. No mathematical source, generated Lean audit, compiler output, or original command log was changed by this replay repair. No repeat Lean compilation is claimed or needed to validate this two-line precondition guard. The preserved original wrapper is historical execution evidence; the current helper at the project root is the strengthened replay entry point.

## Disposition

No mathematical-source repair, weakened theorem, altered axiom allowlist, removed forbidden dependency, missing literal endpoint, vacuous executable summary, or hidden failed compiler command was found in the reviewed run evidence. All eighteen logs were parsed or inspected; no error/warning diagnostic was found. The actual evidence supports the exact thirteen-module/140-literal/403-origin/sixteen-root scope stated above.

**Specialist Lean execution: NOT_RUN.** This report independently reviews Agent #2's retained actual execution evidence. Publication and delivery remain the named owners' actions. Combined semantic/integration review and any merge gates remain separate.
