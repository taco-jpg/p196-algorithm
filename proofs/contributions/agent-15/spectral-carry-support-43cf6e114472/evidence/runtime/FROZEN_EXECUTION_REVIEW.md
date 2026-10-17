# Independent execution review: actual carry support at coefficient nine

**Verdict: PASS_INDEPENDENT_EXECUTION_AXIOMS_AND_UNELIDED_PUBLIC_PRINTS.** The complete eight-module project source closure at commit `5d02e88f13f59f6fcd09cf75d8c7f188c6645727` was rebuilt independently with official Lean 4.19.0 and trust level zero. Every selected-module constant received a signature and an actual `#print axioms` audit. All safe mathematical declarations satisfy the specified foundational axiom policy. All new safe public declarations and the critical prerequisites also received actual complete, unelided `#print` output.

Reviewer: **support_runtime**, a genuine independent nonauthor subagent of Agent #15. The reviewer authored no target Lean declaration, changed no target Lean source, and performed no source publication or integration action. The parent relays attributed coordination through issue #61; this report is not an independent human review or a separate GitHub account's approval. The separate nonauthor semantic review remains required for acceptance of the original mathematical claim. The successful mechanical receipt deliberately retains `semantic_acceptance: SEPARATE_REVIEW_REQUIRED`.

## 1. Frozen source and task identity

The reviewed task is `agent15-spectral-carry-support-43cf6e114472`, protected by claim commit `3de89d0bd03534c92f65886a29b7996525571ff5` and task-record blob `2707332dbc4dc1274bb8470b15e17f6350618bba`. The frozen source commit is `5d02e88f13f59f6fcd09cf75d8c7f188c6645727`, tree `f0594cce1d8b4888561edb4ed22770ab4a6a991a`, on the parent's contribution branch `formalize/agent-15/spectral-carry-support-43cf6e114472`.

The parent reported remote publication and ref readback before authorizing this gate. The reviewer independently resolved the immutable commit and tree locally and compared the compiled source bytes with the committed blobs. No explicit network fetch was needed by this reviewer. The canonical gate's Git commands disable optional locks, prompts, lazy fetching, and replacement objects. Exact commands and outputs are preserved in [the frozen input manifest](freeze-inputs-001/manifest.json) and [the gate receipt](frozen-5d02e88f-attempt-001/verification.json).

The new source is `proofs/contributions/agent-15/spectral-carry-support-43cf6e114472/ActualCarrySupport.lean`, blob `c0e5562e1661570546bced3dca82dd4fb459fa5f`, SHA256 `4c06522efae7aa254b6281003d042e49f6b60162d01d00881d50052c7a73c646`. The exact source bytes, public-export list, contract, and claim record are retained.

The four spectral dependencies retain their original pin `e8d706dc8a67248e1531b0b828fbe05ff50052ed`; the three legacy decimal modules retain pin `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5` and their original flattened source paths. Each source had to match both its original dependency pin and its corresponding blob in the final source commit. The strict [source map](freeze-inputs-001/source-map.json) names every repository path explicitly, so flattened historical names cannot be confused with actual module import names.

| Module | Bytes | Verified Git blob |
| --- | ---: | --- |
| SpectralWeights | 4445 | `40afa93196976972e5c0f6772a18e50c1e635a3f` |
| BinaryCode | 2655 | `35ba9bee5afb9bb47f39738e44860a02ea9b2469` |
| ChargeSymmetry | 3240 | `f69efd4bc0642759dddf99834d5d093c929761a5` |
| SourceFormula | 5059 | `1db4a109629abddf355d12e8a14f2cfb0e26a39b` |
| LychrelDigitSums | 218799 | `8a865176625283648a8a20dd2411ed77670eb0a2` |
| IncomingCarrySensitivity | 12041 | `9ccc745471fd509fb68652fef40454478087e92e` |
| RawSymmetryObstruction | 23848 | `9d4250f3e5daa5ff26f097a7e12ce98830dd9e89` |
| ActualCarrySupport | 10166 | `c0e5562e1661570546bced3dca82dd4fb459fa5f` |

The complete SHA256 source table is:

| Module | SHA256 |
| --- | --- |
| SpectralWeights | `07b3831f17a0d2e43a7e27cfd8a63d364a98ccbbcef87362a20cfbf24fb49db1` |
| BinaryCode | `8db88d52e00dddbd32610dc09b7f8833f1ec1dc623b82236060b67bd2c9171f9` |
| ChargeSymmetry | `28d11217cf147750ec2d07e64dbc6dabeee7deec7e543987817da611201b60a3` |
| SourceFormula | `be165a538963922f6096e63934e5f3c1010d760cabc9e08baa96a0bb43c105d8` |
| LychrelDigitSums | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` |
| IncomingCarrySensitivity | `52850d75999a8fdad298e2e9da638965472ab6507f88630bf428698576ac631f` |
| RawSymmetryObstruction | `922b660e5b3ac42389cd6ea00885075327d4b44fb315b9cc496e1323890e9c87` |
| ActualCarrySupport | `4c06522efae7aa254b6281003d042e49f6b60162d01d00881d50052c7a73c646` |

[Source hashes in TSV form](source-hashes.tsv) include the exact repository path and original pin for every entry. The actual project import graph is the four-module spectral chain and the three-module decimal chain, joined by `ActualCarrySupport`. The earlier `ChargeControls` module is outside this import closure and was not imported or represented as rebuilt.

## 2. Independent execution and freshness boundary

The gate used a newly created directory, `frozen-5d02e88f-attempt-001/source`, which began with only exact copied source. `LEAN_PATH` pointed exclusively to that directory. The eight project modules were compiled in the actual dependency order:

```text
SpectralWeights
BinaryCode
ChargeSymmetry
SourceFormula
LychrelDigitSums
IncomingCarrySensitivity
RawSymmetryObstruction
ActualCarrySupport
```

Every Lean invocation used `--trust=0 -j1 -DElab.async=false`, including compiler version and prefix identification. No author object, old reviewer object, prebuilt decimal project object, or other project cache was reused in this full gate. The gate took 128.964 seconds and returned exit code zero. All eight source compilation commands returned zero. The foundation `LychrelDigitSums` took 65.146 seconds, and the new module took 0.866 seconds. There were no compiler errors or warnings; the foundation's nonempty log contains its existing explicit axiom-print diagnostics.

The origin audit and the first public-export audit also returned zero. The first frozen mathematical-source attempt passed. The launcher applied an outer 1800-second process-group limit; individual compiler commands also had finite timeouts. The exact Python executable, its hash, all command arguments, minimal environment, start/end times, exit codes, elapsed times, log paths and log hashes are preserved in [gate-invocation-001.json](gate-invocation-001.json), [its progress log](gate-invocation-001.log), and the per-command gate receipt. The infrastructure refuses to overwrite an earlier evidence directory.

The actual compiler was:

```text
/tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean
Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)
```

Its SHA256 was `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. The executable and four top-level Lean shared-library files were hashed before the build and checked again after it. The sole direct external project import, official `Std.olean`, had SHA256 `7d3771da25b893da62564bf8198487ff28f01af5cbd410be88d493a4921b2bb1`. The introspection harness additionally imported official `Lean.olean`, SHA256 `7b09317fc9d21262dbfbb6f014dc40c2809b55e6cbb4f7587211a57ec91f7221`. Their identities remained unchanged.

This is a fresh rebuild of the complete selected **project** closure. The official compiled Lean/Init/Std runtime is reused from the pinned distribution. The review does not claim a rebuild of that runtime, a new independent download authentication, or an independent implementation of Lean. Those runtime and project freshness boundaries are explicitly distinct.

## 3. Complete origin-based declaration audit

The audit enumerated every environment constant attributed to the eight selected modules, rather than filtering by a convenient namespace or a short theorem allowlist. It required each entry to be in Lean's checked environment, recorded its kind and safety flags, retained its signature, collected its transitive axioms, and executed a real `#print axioms` command for it. It also verified the presence of every required explicit export and prerequisite.

| Origin module | All declarations | Safe | Safe public | Safe private | Implementation only |
| --- | ---: | ---: | ---: | ---: | ---: |
| SpectralWeights | 58 | 38 | 33 | 5 | 20 |
| BinaryCode | 36 | 25 | 19 | 6 | 11 |
| ChargeSymmetry | 28 | 17 | 17 | 0 | 11 |
| SourceFormula | 43 | 34 | 31 | 3 | 9 |
| LychrelDigitSums | 1915 | 1131 | 1058 | 73 | 784 |
| IncomingCarrySensitivity | 101 | 92 | 89 | 3 | 9 |
| RawSymmetryObstruction | 187 | 152 | 149 | 3 | 35 |
| ActualCarrySupport | 42 | 36 | 36 | 0 | 6 |
| **Total** | **2410** | **1525** | **1432** | **93** | **885** |

The actual origin-based `#print axioms` output contains exactly 2410 distinct entries. The complete [JSON inventory](frozen-5d02e88f-attempt-001/declarations.json), [TSV inventory](declaration-coverage.tsv), and [signature/axiom log](frozen-5d02e88f-attempt-001/logs/all-declarations.log) retain private helpers, imported project declarations, generated safe declarations, and implementation artifacts.

All 1525 safe declarations have transitive axioms contained in exactly the permitted set: `propext`, `Classical.choice`, and `Quot.sound`. No safe entry is an `axiomInfo` declaration. The distribution is:

| Safe transitive axiom set | Declarations |
| --- | ---: |
| none | 382 |
| `propext` | 79 |
| `propext`, `Quot.sound` | 917 |
| `propext`, `Classical.choice`, `Quot.sound` | 147 |

The complete live-source scan found no `sorry`, `admit`, `sorryAx`, `native_decide`, `Lean.ofReduceBool`, explicit mathematical axiom, explicit unsafe/partial construct, or `skipKernelTC`. Nested comments and strings were masked before the scan, and both the masked source and scan results are retained for all eight files. This scan supplements the actual trust-zero compilation and transitive axiom check; it is not used as a substitute for them.

### Compiler artifacts are a separate evidence class

The 885 implementation entries consist of 871 definitions and 14 `axiomInfo` entries. Of those 885, 862 are flagged unsafe and 23 are flagged partial. Fifty-one implementation entries have nonempty raw axiom lists, including compiler specialization names and `lcProof`; their complete lists are preserved. They are **not** presented as safe mathematics, and their names are **not** added to the permitted foundational axiom set. No such name occurs in the collected axiom set of any of the 1525 safe declarations.

For example, compiling the ordinary safe `outgoing` list map produces the unsafe implementation artifact `List.mapTR.loop._at.P196.Agent15.SpectralSupport.outgoing._spec_1`, represented by Lean as an unsafe `axiomInfo`, plus associated compilation stages. The safe `outgoing` definition itself has no axioms. All six implementation entries originating in `ActualCarrySupport` are separately recorded; all 36 safe entries from that module satisfy the mathematical policy.

This distinction follows actual `ConstantInfo` safety/partial flags and kernel-checked source, not merely a name-pattern exemption. The [implementation-only inventory](implementation-artifacts.json) retains every raw record and the separate raw implementation axiom union. It would be false to say that every raw implementation axiom list contains only the three allowed foundational names; the accepted statement is explicitly about the complete safe mathematical closure.

## 4. Public exports and exact prerequisite output

The reviewer independently extracted 22 explicit public declarations from the frozen new source: two definitions and twenty theorems. The resulting list exactly matches the parent's proposed list, including the legitimate identifier `outgoing_getElem?`. The origin audit additionally found 14 safe generated public declarations attributed to `ActualCarrySupport`. Two of these have the prior spectral namespace (`oddCharge.eq_1` and `evenCharge.eq_1`), which illustrates why origin-based enumeration matters.

All 36 safe public declarations originating in the new module and all 12 critical prerequisites received real literal `#print` and `#print axioms` commands: 48 distinct declarations. The initial pass used `pp.all`. It produced 120 visible `⋯` elisions in large proof bodies because the pinned Lean pretty-printer still defaults `pp.maxSteps` to 5000. Its successful compiler/axiom result and complete original output remain unchanged and preserved.

A separate supplemental print pass used `pp.all true`, explicit proof/deep-term printing, and a finite `pp.maxSteps 1000000`. It printed the same 48 declarations and axioms, returned zero in 10.928 seconds, and contained **zero** `⋯` elisions. The pinned official option source, exact generated harness, command, input hashes and complete output are retained in [the supplemental receipt](supplemental-public-print-001/verification.json) and [the complete unelided print log](supplemental-public-print-001/full-public-prints.log).

The supplement reused only objects from this successful independent fresh build. Every reused project source/object and compiler/official import hash was checked before and after it. This is explicitly a presentation supplement, **not** a second full project rebuild. No mathematical source changed. The report therefore distinguishes 2410 origin axiom prints, 48 initial public/prerequisite prints, and 48 unelided supplemental prints; repeated presentations are not additional mathematical results.

The explicit new exports have the following transitive axiom sets:

| New explicit declaration in `P196.Agent15.SpectralSupport` | Axioms |
| --- | --- |
| `outgoing` | none |
| `actualCharge` | none |
| `outgoing_length` | `propext` |
| `outgoing_getElem` | `propext` |
| `outgoing_getElem?` | `propext` |
| `outgoing_last` | `propext`, `Quot.sound` |
| `outgoing_binary` | `propext`, `Quot.sound` |
| `outgoing_reverse_iff` | `propext`, `Quot.sound` |
| `actualCharge_zero_iff` | `propext`, `Classical.choice`, `Quot.sound` |
| `outgoing_reflected_eq_of_nonnine` | `propext`, `Quot.sound` |
| `actualCharge_nonzero_iff_nine_asymmetry` | `propext`, `Classical.choice`, `Quot.sound` |
| `actualCharge_zero_of_no_nine` | `propext`, `Classical.choice`, `Quot.sound` |
| `canonical_actualCharge_zero_iff` | `propext`, `Classical.choice`, `Quot.sound` |
| `canonical_outgoing_reflected_eq_of_nonnine` | `propext`, `Quot.sound` |
| `canonical_actualCharge_nonzero_iff_nine_asymmetry` | `propext`, `Classical.choice`, `Quot.sound` |
| `canonical_actualCharge_zero_of_no_nine` | `propext`, `Classical.choice`, `Quot.sound` |
| `actualCharge_width_zero` | `propext` |
| `actualCharge_width_one` | `propext` |
| `Controls.nine_zero_charge` | none |
| `Controls.even_overflow_zero_charge` | none |
| `Controls.odd_free_center` | none |
| `Controls.odd_nine_asymmetry` | none |

The twelve separately printed prerequisites are:

- `DecimalDigits.carry`.
- `DecimalDigits.carry_bounded`.
- `DecimalDigits.columnSum`.
- `DecimalDigits.columnSum_bounded`.
- `DecimalDigits.columnSum_symmetric`.
- `DecimalDigits.Canonical`.
- `RawSymmetryObstruction.nonnine_binary_div`.
- `P196.Agent15.SpectralCarry.Binary`.
- `P196.Agent15.SpectralCarry.carryCharge`.
- `P196.Agent15.SpectralCarry.carryCharge_zero_iff`.
- `P196.Agent15.SpectralCarry.carryCharge_eq_odd_source_sum`.
- `P196.Agent15.SpectralCarry.carryCharge_eq_even_source_sum`.

The actual printed definitions preserve the exact existing decimal carry recursion, the existing canonical representation predicate, the zero-or-one `Binary` predicate, and the parity-selected integer `carryCharge`. The checked signatures retain the coefficient bound, symmetry hypothesis where required, actual outgoing indices, canonical wrapper, and explicit no-nine premise. Formal comparison with the original source statement belongs to the separate semantic review. [Endpoint summaries](endpoint-summary.json) provide the convenient signature/axiom index; the supplemental log contains the unelided full declarations and proof bodies.

## 5. Infrastructure provenance and preserved observations

The prior accepted review helper and report remain byte-preserved under `original-infrastructure/`. Three successive new infrastructure versions are retained with exact patches and change descriptions in `infrastructure-001`, `infrastructure-002`, and `infrastructure-003`. They adapt the single-folder resolver to explicit repository paths and dual source pins, strengthen complete new-public print coverage, and support the ordinary question-mark identifier suffix. Python syntax checks passed. The executed helper SHA256 is `f59c1c7b3e3ec240008f7c9635e6e40dc4ec8f8849d5f6fffd53f5b9f8a972b8`. Its exact invocation is retained; no earlier or stale object was relabeled as a fresh result.

The seven historical dependencies received a separate metadata-only source comparison before the author froze the target. That preparation established source identity and import closure, not compilation or mathematical acceptance. The preparation reports are historical checkpoints superseded by this completed execution report; their original bytes remain present. Any changed helper path from an old preparation manifest is reconciled to its exact retained infrastructure snapshot.

Initial ordinary-executor reads could not see the assigned `/dev/shm` workspace. The approved `require_escalated` executor did see it, and all workspace writes and compiler runs used that authorized view. This was an observed executor-view difference; no mount, permission, compiler, or another agent's cache was changed. No execution approval was denied. No cleanup or deletion was attempted, and no reclaimed-space claim is made. The initial failed read observations remain accurately separated from proof or compiler failures.

All new source copies, scan outputs, metadata commands, infrastructure revisions, successful compiler output, implementation inventories, full print output, and the formatting-limit observation are retained. All eleven present compiled products are included in the delivery archive because their total size is modest; their exact identities and regenerable-infrastructure classification are recorded in [the generated-product inventory](generated-product-inventory.json). The reviewer leaves all original files and products intact. The delivery excludes only its own `delivery/` directory to prevent archive recursion.

## 6. Acceptance boundary and handoff

This report establishes the independent execution and axiom gate for the exact frozen carry-support package. It does not substitute for the separately assigned source-semantic verdict or the integration owner's accepted-build decision. The new source and its dependencies must retain the reviewed bytes and pins; a changed mathematical source requires an appropriate new gate. Documentation-only updates do not retroactively make this a build of a different source snapshot.

This review supplies no theorem that coefficient nine alone forces nonzero charge, no converse `J=0 iff no nine`, no charge persistence along an orbit, and no all-time conclusion about 196. Legacy imported declarations receive complete execution/axiom coverage here because they are dependencies, without being promoted to newly established claims about this task.

The primary evidence entry points are [review-summary.json](review-summary.json), [the frozen gate receipt](frozen-5d02e88f-attempt-001/verification.json), [the full origin log](frozen-5d02e88f-attempt-001/logs/all-declarations.log), [the unelided public print log](supplemental-public-print-001/full-public-prints.log), and the final reviewer manifest. The parent owns publication, issue #61 relay, formal review attachment, and any integration handoff.

## 7. Frozen delivery

The complete reviewer directory is frozen after final packaging. The compressed delivery is `delivery/support-runtime-review-5d02e88f.tar.gz`. Its adjacent delivery manifest lists the exact bytes and SHA256 of every archived regular file, including the internal reviewer manifest, and records the archive's global byte count and SHA256. The internal [reviewer manifest](review-manifest.json) excludes only itself and `delivery/`; the external delivery manifest closes that self-reference boundary. All fresh objects, raw unsafe/partial records, complete sources, helper revisions and logs remain included. No file was deleted or silently replaced by a summary.
