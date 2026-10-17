# PR 148: independent review of the new exact-source execution evidence

## Decision

**PASS — the new execution evidence discharges the previously uncovered clean full-closure compilation and declaration/axiom inspection gate for PR 148 at `7360b12a0a5889761c845a56a4b8d8a1df5f39b5`. Existing independent semantic review reuse remains QUALIFIED.**

This is a **NEW_EXECUTION_NOT_ORIGINAL_ARCHIVE_RECOVERY**. The original reported independent execution archive remains **NOT_RECOVERED**. This decision does not authenticate or reconstruct that missing archive, equate its reported counts with the new audit, or confer a repository-wide result. No new mathematical source repair or redundant mathematical review was needed.

The parent, Agent #4 / session `87258c67b0f5`, authored the new outer drivers and executed the compiler. The genuine independent nonauthor reviewer `/root/pr155_independent_review` inspected the procedures before execution and subsequently inspected the complete retained evidence. The reviewer did not run Lean, author or modify the execution scripts, modify source or registry files, or write remotely. This division of work is preserved in the decision.

The earlier `SEMANTIC_REUSE_AND_EXECUTION_OBLIGATIONS.md` is retained unchanged as the preexecution checkpoint. Its PENDING execution status describes that earlier stage; this final report resolves the concrete execution obligations listed there. The source/review identity findings in that checkpoint remain applicable.

## Exact scope and reusable semantic evidence

The source is the real detached, clean worktree at H148, not a checkout with merely equivalent selected files at some other HEAD. The reviewer independently rechecked the actual HEAD and clean tracked state after the run, and compared all 30 frozen input files three ways: Git H148, the checkout, and the preserved `inputs/repository` snapshot. Every byte, registered SHA-256, size, and Git blob identity agreed. The original research, final semantic review, task, historical drafts and failed/successful author attempts remain preserved under their original labels.

The retained implemented-source independent review is `proofs/contributions/agent-51/spectral-overflow-saturation-20261016/review/FINAL_REVIEW.md`, SHA-256 `a518fc3264ee25c719c5df954b9d51a7d24b094fc159b4f3239c8bb345dbe986`. Its explicit source and task pins match H148. Its semantic PASS covers the actual universal overflow-saturation statement and its even/odd corollaries, while expressly reserving the full clean execution gate. The independent reuse qualification in the earlier checkpoint examined that separation and the actual source-facing statements; it did not substitute the preimplementation contract review for implemented-source review.

The registry SHA-256 is `7622d9321f96acecb583ac1958cc72691fa5e3da92fc044908464d4d6fd767e3`. It selects exactly these five modules:

| Module | Source SHA-256 |
|---|---|
| `LychrelDigitSums` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` |
| `OverflowDigits` | `65adeb3ae7bea93e390a95fc5f8b58ec43f0f64f01ed9db3f51392657ba89a41` |
| `OverflowWitness` | `fbf7568256e31948a20563e5d9e1335ce45b6859d2343917395180970114c901` |
| `ResidueSums` | `1333e156e2da6f02a18ff67f83e8ce36955e93c00e425cf67aff713f916140d4` |
| `Saturation` | `e2379506a0b70c1502fea88e8daff4241282be73f6f11672effff182a10bc722` |

The canonical source copies match those bytes exactly and use no adapters. Copying the pinned original `proofs/LychrelDigitSums__0810ace083af80c5.lean` to its registered import filename `LychrelDigitSums.lean` does not change its contents. `OverflowDigits` and `ResidueSums` retain the exact already-reviewed PR 155 bytes; the other three modules receive the previously missing coherent full-closure execution here.

## Procedure identity and actual execution

The canonical verification implementation remains byte-identical to the published source: `proofs/verify_project__214bf7673efe116b.py`, SHA-256 `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`. Its inherited `"agent": "Agent #1"` field is static script metadata. The actual new execution is attributed to Agent #4 by the outer driver and the new evidence classification; it is not an execution claimed on behalf of Agent #1.

The copied strict launcher remains identical to the accepted final PR 155 launcher, SHA-256 `a9d32e8bb8658a25b799d3bf2f466c8862a95e25b8fd2e44ab042af931b11dec`. It verifies the official Lean executable hash, rejects the inspected caller trust/memory overrides, sets a hard 4 GiB `RLIMIT_AS`, records the actual effective argv and working directory, and replaces itself with the compiler through `execv`.

The actual compiler is Lean 4.19.0, commit `6caaee842e94`, executable SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. The reviewer independently matched the executable and all four reported shared-library hashes to both receipts and the current retained runtime files. The preexecution source freeze and procedural hashes also agree with the final files. This verifies the recorded official runtime identity; it does not claim a bootstrap rebuild of Lean or its shipped standard library.

The complete `strict-launches.jsonl` contains nine distinct process entries: compiler version and prefix queries, five sequential local module compilations, the canonical project audit, and the supplemental audit. All nine record explicit `--trust=0` and `rlimit_as_bytes=4294967296`. Each of the seven substantive invocations additionally records `-j1 -DElab.async=false`. The reviewer matched every effective argv and cwd to its corresponding canonical or supplemental receipt and checked that its launch time lies within the corresponding driver interval.

The parent executed canonical attempt 001 under its approved 600-second external bound. It completed successfully in 96.076121325 seconds. All five fresh source compilations and the generated `ProjectAudit.lean` returned a real exit code of zero:

| Stage | Exit | Recorded elapsed seconds |
|---|---:|---:|
| `LychrelDigitSums` | 0 | 67.790751 |
| `OverflowDigits` | 0 | 1.519237 |
| `OverflowWitness` | 0 | 0.665733 |
| `ResidueSums` | 0 | 2.070235 |
| `Saturation` | 0 | 0.716578 |
| `ProjectAudit` | 0 | 22.644687 |

The complete logs are retained, including the legitimately empty `OverflowDigits.log`. All 13 entries in the canonical `FILES.json` match their actual size and SHA-256. The canonical console and every separately reported raw log hash also match. The canonical manifest intentionally does not list `.olean` files; their identities are independently recorded and checked through the supplemental receipt and this review's inspection records.

The approved supplemental driver then imported exactly the five fresh canonical objects through its explicit `LEAN_PATH`, under a separate 180-second external bound. It returned zero in 3.223026105 seconds. Its source, driver, launcher, compiler, source/object hashes, working directory, command, canonical-report hash, and complete output all agree with the recorded receipt. Its before/after source, object, and runtime checks passed, and the reviewer independently matched those same bytes afterward.

No additional compiler execution was requested or performed by this reviewer to inspect the results. The two successful attempts are sufficient for the scoped gate.

## Complete declaration coverage and axiom inspection

The reviewer parsed the entire canonical and supplemental outputs, including axiom lists that wrap across lines, rather than accepting only the final summary counts. The inspection records preserve every parsed theorem row, safe declaration row, public axiom row, and excluded implementation row by exact module origin and name.

The module-origin selector covers all five registered modules, including the foundation's declarations outside the `P196.Agent51` namespace. The canonical audit selects every `.thmInfo` declaration and rejects safe custom axioms. The supplemental audit selects `.defnInfo` values whose safety is `.safe` and nonunsafe `.opaqueInfo` values, uses the already-corrected explicit `eligible : Bool` annotation, collects their transitive axiom dependencies, and also rejects safe custom axioms. It reports excluded unsafe/partial implementation entries separately. Both audits reject any checked dependency outside `propext`, `Classical.choice`, and `Quot.sound`.

| Module of origin | Unique theorem rows | Safe definition/opaque rows | Excluded implementation entries |
|---|---:|---:|---:|
| `LychrelDigitSums` | 986 | 131 | 784 |
| `OverflowDigits` | 29 | 2 | 4 |
| `OverflowWitness` | 10 | 1 | 2 |
| `ResidueSums` | 47 | 7 | 23 |
| `Saturation` | 11 | 0 | 0 |
| **Total** | **1083** | **141** | **813** |

All names within each category are unique; the theorem, safe-declaration, and excluded-name sets are pairwise disjoint. Every row has an allowed selected module origin. The counts agree with both real final audit summaries and the canonical JSON. Zero safe-definition rows from `Saturation` reflect its declarations, not an omitted module: its name is present in both actual selectors and its eleven theorem rows are present.

The actual union of theorem dependencies is `{Classical.choice, Quot.sound, propext}`. The actual union for the 141 safe definition/opaque rows is `{propext}`. There is no forbidden axiom dependency, safe custom axiom diagnostic, or compiler error in either audit. The excluded entries comprise 798 unsafe/partial definitions and 15 unsafe implementation axioms; no excluded unsafe opaque entry appears. The fifteen unsafe-axiom pairs match exactly between canonical and supplemental output. They are reported as compiler implementation artifacts, not accepted mathematical assumptions. The checked transitive dependency sets establish that none enters a checked theorem or safe declaration as an extra axiom.

The actual audits each contain the exact registry order of 52 literal `#check` commands, and the supplemental audit contains the exact same 52 literal `#print axioms` commands. The emitted public type block is byte-identical across the two independent audit invocations. The supplemental output contains one actual axiom result for every registered name, with no missing, extra, reordered, or duplicate public entry. All 52 public names are covered by the module-origin audits: 45 are theorem declarations and seven are safe definitions. Their literal axiom outputs agree individually with their module-origin audit rows. The seven public definitions have empty axiom dependencies.

The three final endpoints are explicitly present:

- `P196.Agent51.overflow_saturation`.
- `P196.Agent51.even_overflow_saturation`.
- `P196.Agent51.odd_overflow_saturation`.

Each has exactly the permitted three-axiom set. Their emitted types retain the universal length/residue quantifiers, one shared positive canonical nonpalindromic witness, actual terminal carry one, palindrome next step, exact output width, and literal divided polynomial residue interfaces addressed by the reused semantic review. The count of 52 describes the new registered interface, not every declaration in the substantial historical foundation. The 1083 and 141 category counts are observations of this new traversal; no automatic comparison to the unrecovered historical “117” or “1238 safe declarations” summaries is asserted.

## Resource observations and evidentiary limits

The 4 GiB per-process address-space cap was actually installed and recorded for each compiler launch, and all substantive processes completed successfully under it. That resolves the earlier uncertainty about whether this particular bounded attempt could compile the large foundation and import the audit modules.

The driver's `/proc` observations retained only the Python supervisor. They do **not** provide Lean peak RSS or peak virtual-memory measurements, and no such measurement is claimed. Shared cgroup `oom` and `oom_kill` counts did not increase during the canonical interval, but those shared counters are not attributed as isolated measurements of these processes. The raw observations are retained without reinterpretation. Missing optional per-process profiling is not an unmet mathematical execution gate and does not justify another build.

Fresh source compilation with trust zero supplies the proof-checking evidence; the later import-based audits inspect the resulting environments and their axiom dependencies. The supplemental import does not claim to recheck proof bodies inside already-built objects. The package records that boundary explicitly.

The canonical report correctly retains `catalogue_complete=false` and `repository_wide_pass=false`. This result covers the selected overflow-saturation claim and its exact five-module import closure. It does not prove the entire original spectral report, all-time behavior of the 196 orbit, or every repository claim.

## Evidence identities and final handoff

| Retained artifact | SHA-256 |
|---|---|
| `source-freeze.json` | `3129d916d1e2ae22f98f5fdd523308522fbb624894e35914403e4da78b046454` |
| `canonical-driver-001.json` | `27268066f162cabf7b1e5ac8a11ca914457960e51e3063009d755445821f786b` |
| `canonical-strict-001/verification.json` | `ced91cb4d8a1a7024fd08714cb38dac80ce00793a09c2495fede39a2a5cadd8a` |
| `canonical-strict-001/agent51-overflow-saturation/logs/ProjectAudit.log` | `6686d60ff8792f429c90e4d1dd25673a3a557b88ae7f07c0b4eab09c872d965d` |
| `PublicAndSafeAudit.lean` | `dba2697be8a32bc8b8543ec85a502addee82403910bd7b6fba758264d60da32d` |
| `run_supplement.py` | `35b63d169bbdd8bda97c4103bafd07e07be8bcae76a4fbab0adbfff2f404b581` |
| `supplement-001/result.json` | `187cdd16977be46f3d32eee6cdde638dc41b4ab7f7e12fb82d4656879e729341` |
| `supplement-001/PublicAndSafeAudit.log` | `af46f816a136596c3868bd6f959cee3758160af98ccb691f8f9c865909282e24` |
| `review/canonical-001-inspection.json` | `95dc7dabaa23f4d50a529c81fdb7bb45be12f24da6aa04e747376813867ee79a` |
| `review/supplement-001-inspection.json` | `deb63036e8ffec779f7b339933406a5976b88f76b8a655b674d7c0271dc2e5b9` |

**There are no remaining blockers in this delegated new-execution evidence review.** The source, procedure, compiler/command/exit binding, complete raw output, full module-origin theorem audit, exact public interface audit, and safe-definition audit all satisfy the stated obligations. The existing semantic review can be reused with this newly verified execution corpus.

Agent #28 retains PR 148 delivery, Agent #51 retains the source scope, and Agent #31 retains main-write control. Publication, platform and current-main combination requirements, any actual merge, and post-merge checks remain the responsibility of the authorized delivery/main owners. This reviewer neither performed nor accepted those separate actions. The original missing archive remains NOT_RECOVERED regardless of this successful new reproduction.
