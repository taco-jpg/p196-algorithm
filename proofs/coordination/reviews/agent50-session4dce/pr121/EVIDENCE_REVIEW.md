# Agent #50 — PR121 retained-evidence review

## Verdict

**QUALIFIED_RETAINED_EVIDENCE at `5c4d394f20b70547aa7cb8dd14091bcd391e424c`. No intrinsic source-identity, retained-file, execution-scope, or axiom-audit blocker was found.**

The newly written data-only evidence checker passed **601 checks with zero findings**. It verified every entry in six explicit retained-file inventories, comprising **200 file references**. The complete PR patch reconstructs all 92 added files and all 10,638 added lines exactly. There are no deleted lines.

A separate, independently written finite arithmetic checker also passed. It reproduced all retained case counts and all 19 detailed boundary traces. These computations are supplementary finite diagnostics. **This review executed zero Lean commands and zero repository scripts.** The historical Lean executions below are reused retained evidence, not new executions by Agent #50.

This is a delegated read-only evidence review for Agent #50's accepted PR121 delivery task. It does not acquire source ownership, accept another contribution's delivery ownership, resolve PR97's integration dependency, or authorize a target mutation. Parent Agent #50 remains the named delivery owner. Agent #5's source attribution and existing PR97 ownership are preserved.

## Exact scope and identities

| Field | Value |
|---|---|
| Repository | `taco-jpg/p196-algorithm` |
| Pull request | [PR121](https://github.com/taco-jpg/p196-algorithm/pull/121) |
| Reviewed evidence head | `5c4d394f20b70547aa7cb8dd14091bcd391e424c` |
| Frozen mathematical source | `5b4238ebe95f5fb80512d1b1ad3dbe3b062279a3` |
| Observed stacked base | `5bbd70c486b3c274cfc9bf244cc92e551419d5d8` |
| Observed base branch | `research/agent-5/digit-streams-20261016T2108Z` |
| Parent delivery task | `agent50-session4dce-pr121-delivery-20261016` |
| Parent accepted coordination | `e4ce3f5a62aff79d132f8815f9a329876649a40f` |
| Delegated reviewer | Agent #50, `/root/pr121_evidence_check` |
| Reasoning configuration supplied by parent | `ultra` |
| Remote mutations by this reviewer | None |
| Source edits by this reviewer | None |
| New Lean executions | 0 |

The [top-level registry](https://github.com/taco-jpg/p196-algorithm/blob/5c4d394f20b70547aa7cb8dd14091bcd391e424c/proofs/Agent5OrdinaryStreamPrefix.registry.json), [top-level verification record](https://github.com/taco-jpg/p196-algorithm/blob/5c4d394f20b70547aa7cb8dd14091bcd391e424c/proofs/Agent5OrdinaryStreamPrefix.verification.json), and all 92 changed files were fetched at the exact reviewed head. Twenty additional exact-head files supplied the thirteen external registered modules, the canonical verifier, its prior audit template, and five original arithmetic provenance snapshots. All 112 downloaded file bodies matched their GitHub Git blob IDs after independent local recomputation.

The top-level registry SHA256 is `e866196ef123c8c79232fa2d0aba72d5662bcd06faaadd2295c55d17ae9e3061`. Every one of its fifteen mathematical source paths matches the expected SHA256 and Git blob. Every one of the fifteen separate strict-review snapshots has the same identity. Source imports match the registry, the root closure has fifteen modules, and the graph is acyclic. The six retained theorem contract strings and their SHA256 hashes also match the actual source contracts.

## Complete archive and manifest reconciliation

| Inventory | Referenced files | Result |
|---|---:|---|
| `PUBLICATION.json` | 91 | PASS |
| `verification/canonical-published-source/FILES.json` | 18 | PASS |
| `review/strict-replay-01/FILES.json` | 29 | PASS |
| `author/raw-prefix/artifact-index.json` | 6 | PASS |
| `author/arithmetic/MANIFEST.sha256` | 17 | PASS |
| `review/REVIEW_MANIFEST.sha256` | 39 | PASS |

These are 200 references across inventories, with some repeated files. They are not 200 distinct contributions. `PUBLICATION.json` covers precisely the other 91 changed files and deliberately does not include itself.

### Canonical source snapshots: no omission requiring restoration

The [canonical archive manifest](https://github.com/taco-jpg/p196-algorithm/blob/5c4d394f20b70547aa7cb8dd14091bcd391e424c/proofs/contributions/agent-5/ordinary-stream-prefix-20261016/verification/canonical-published-source/FILES.json) enumerates exactly 18 artifacts: its verification record, all sixteen module/audit logs, and generated `source/ProjectAudit.lean`. Every enumerated file exists and its byte count and SHA256 match.

That manifest expressly retains registered mathematical sources at their canonical repository paths, while excluding reproducible compiled objects. Therefore the absence of fifteen duplicate source files in the canonical archive is an intentional documented scope, not a missing manifest entry. All fifteen canonical repository source paths and all fifteen separate review snapshots were fetched and checked. There is **no PR97-style additive source restoration to perform for PR121's canonical archive**.

The separate strict replay has all 29 artifacts listed in its `FILES.json`, including fifteen mathematical source snapshots and `ProjectAudit.lean`. The four original Agent #6 archive paths and alternate `ExteriorCore` snapshot named by provenance also reproduce the exact registered source hashes. No registered source adapter is used.

## What the retained Lean evidence actually covers

| Retained execution | Actually fresh project source compilation in that historical run | Other imported project objects | Recorded result |
|---|---|---|---|
| Agent #5 parent's canonical published-source run | All 15 registered modules, in complete dependency order | No reused project object cache in the new output directory | 15 module commands plus complete audit, all 16 exit 0 |
| Separate nonauthor Agent #5 specialist's strict run | `RawPrefixStreams` and `OrdinaryStreamStep` | 13 explicitly attributed and source-hash-recorded objects | Two module commands plus complete audit, all 3 exit 0; 2 preflights also exit 0 |
| Raw-prefix author run | `RawPrefixStreams` | Nine coordinate objects and four arithmetic objects from the author baseline | First attempt exit 0, five explicit export axiom reports |
| Arithmetic author baseline and wrapper records | Four arithmetic modules; separately the one wrapper and its small audit | Nine coordinate objects; the wrapper additionally inherits the raw-prefix object | All recorded source compilations and audits exit 0 |

The canonical record is [retained here](https://github.com/taco-jpg/p196-algorithm/blob/5c4d394f20b70547aa7cb8dd14091bcd391e424c/proofs/contributions/agent-5/ordinary-stream-prefix-20261016/verification/canonical-published-source/verification.json), with SHA256 `742937cdfcc106812ef4cfb24652cbc7462b4b3e406be0e26e25652617e4ceea`. It reports the exact frozen source commit and `source_tree_clean=true`. The inspected unchanged canonical verifier creates a nonexistent output directory, copies and hashes the registered source, constrains the project import path to that new source directory, compiles every module in dependency order, generates the exhaustive audit, checks source stability, and rehashes the compiler files. Its retained command arrays use `-j1 -DElab.async=false`; they do not contain `--trust=0`.

The separate [strict replay record](https://github.com/taco-jpg/p196-algorithm/blob/5c4d394f20b70547aa7cb8dd14091bcd391e424c/proofs/contributions/agent-5/ordinary-stream-prefix-20261016/review/strict-replay-01/verification.json) has SHA256 `3c08d98fb198270d4a347f34818ab3b2454060eb2102750a3851a5663c56466c`. Its three proof/audit command arrays contain `--trust=0 -j1 -DElab.async=false`. Its own status and fields explicitly state that only two modules were freshly compiled and thirteen were inherited. The reviewer recorded the thirteen object hashes at import and verified the nine prior recorded coordinate-object hashes; the four arithmetic hashes are attributed to the author's separately recorded fresh arithmetic compilation.

All retained command log references checked here resolve to exact matching bytes. The wrapper's historical log name is explicitly relocated to retained `attempt01/compile.log` through its receipt. The baseline receipt and inherited-artifact record copies agree byte for byte. The raw module's author object hash agrees with the wrapper's subsequent inheritance record.

**The thirteen imported `.olean` bytes are intentionally unretained and were not freshly rehashed or recompiled by this review. `--trust=0` alone does not establish rechecking imported theorem proofs.** The qualifying source-compilation evidence for the complete project closure is the separate retained canonical run's fresh compilation of all fifteen registered sources. Standard toolchain imports remain part of the pinned Lean runtime.

The original verifier's `agent: Agent #1` metadata is preserved. The top-level record explicitly names `Agent #5 parent` as the actual canonical executor. These distinct identities are accurately labeled. The separate reviewer is identified as a nonauthor specialist in the same Agent #5 session; this does not by itself establish a separate GitHub account or satisfy an independently required platform approval.

## Actual complete theorem and axiom audit

Both raw `ProjectAudit.log` files have SHA256 `e88d8b7a819c3528fc69862f5cf385ac189112cb7e49730236bb8f438b3e8549` and are byte-identical. The independently parsed multiline output contains 267 unique theorem records and all six fixed exports. The complete structured reviewer declaration list agrees exactly with the parsed raw output.

The generated audit source is retained consistently in all three locations with SHA256 `9383d1c8429c90b25c78e9bfa1f2dac3386defc6b274389ec89c9cc26c2e638c`. It selects all fifteen module origins, checks the six exports, rejects custom safe axiom declarations, and computes transitive theorem axiom dependencies with `Lean.collectAxioms`. Its actual allowed-axiom body matches the published prior canonical template.

| Selected module origin | Theorem declarations in raw audit |
|---|---:|
| `OuterFinite` | 10 |
| `TARGET` | 0 |
| `ExteriorFactorizationProof` | 59 |
| `DigitDefinitions` | 10 |
| `AdicDigits` | 23 |
| `FractionDigits` | 26 |
| `CoordinateStreams` | 5 |
| `CoordinateThreshold` | 36 |
| `CoordinateOnlyStreams` | 10 |
| `ExteriorCore` | 12 |
| `ExteriorBridge` | 24 |
| `ExteriorProjection` | 11 |
| `ExteriorArithmetic` | 32 |
| `RawPrefixStreams` | 8 |
| `OrdinaryStreamStep` | 1 |

The total is **267**: 179 from the coordinate dependency context, 79 from the four arithmetic modules, eight from `RawPrefixStreams`, and one from `OrdinaryStreamStep`. A selected module with zero theorem declarations is still part of the source and import closure.

Every parsed theorem axiom set is a subset of `{propext, Classical.choice, Quot.sound}`; the union is exactly that set. The three separately recorded unsafe implementation declarations do not occur in any theorem axiom set. They remain visible in the report and are not relabeled as accepted mathematical axioms. The comment-aware source scan found no forbidden source declaration or shortcut in the fifteen registered source modules. This scan supplements the retained transitive audit and does not replace it.

## Pinned runtime fingerprints

The retained compiler version is Lean 4.19.0, commit `6caaee842e94`, Release. Canonical and strict records contain identical fingerprints for the compiler executable and four shared-library paths. This review freshly read those five existing authorized runtime files as data, using bounded blocks, and all five hashes matched.

The executable SHA256 is `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. No compiler was launched for this fingerprint check. The historical resource-recovery record describes removal of a reproducible downloaded archive; those removed bytes cannot be freshly checked here. Its preserved extracted runtime is consistent with the newly checked fingerprints. No historical source, proof log, or other session's data was removed by this review.

## Independently recomputed finite controls

The new `check_boundary_controls.py` imports only Python standard-library modules. It does not import or execute the retained repository script. Low digits are calculated using the inverse of 9 modulo `10**k`, and high digits use successive exact integer quotients. The implementation was written for this evidence review after inspection of the original definitions and the finite-control script.

| Finite family | Observed cases | Retained count matched |
|---|---:|---|
| Bounded coefficient words | 64,008 | Yes |
| Canonical ordinary realizations, a subset of the bounded family | 51,984 | Yes |
| Structural zero-head cases | 3,360 | Yes |
| Empty exterior cases | 168 | Yes |
| Empty middle cases | 9,144 | Yes |
| Negative adic-numerator cases | 32,592 | Yes |
| Longer patterns | 384 | Yes |

All 19 detailed retained boundary traces also match. Every bounded and longer-pattern case is preserved, including its parameters, actual prefix, independently calculated stream sum, and result, in `checks/boundary-cases-01.csv`: **64,392 rows**, 4,903,722 bytes, SHA256 `3bf7c1714475017fd5302cebd1861d0aea504c683bff22a346238113ecef8473`.

The counts overlap as indicated and must not be added to claim more unique tests. None of these finite computations supplies a universal theorem, later shape persistence, an arbitrary longer prefix, all-time safety, palindrome avoidance, or a conclusion about 196.

## Limits, remedy decision, and delivery handoff

No missing manifest-referenced file or mismatched source byte was found. Exact recovery candidates were located and checked for the arithmetic provenance records, but no additive restoration is necessary. No proof, source, registry, verifier, or remote branch was changed.

The new work consists of data acquisition, byte-identity and reference reconciliation, source/import/contract comparisons, raw retained command/log analysis, full raw axiom-census parsing, five runtime file hashes, and finite integer computations. Historical compilation is reused. This report does not claim that a new combined tree with current main was built, that PR97 is integrated, that a platform requirement passed, or that PR121 was merged.

The parent owns the next integration action and the exact PR97 ownership/publication blocker disposition. This completed delegated review supplies qualified retained evidence for H and does not change those external dependencies.

## Retained deliverables

- `checks/check_evidence.py`: complete independently written retained-evidence checker.
- `checks/evidence-check-01.json`: all 601 results, every manifest/file reference, source map, retained command array, and parsed theorem record.
- `checks/evidence-check-01.log`: complete raw checker output.
- `checks/check_boundary_controls.py`: complete independently written finite checker.
- `checks/boundary-check-01.json` and `.log`: full finite-check results and raw output.
- `checks/boundary-cases-01.csv`: all 64,392 bounded and long-pattern case rows.
- `raw-pr-patch-complete.json`: complete connector diff used by the checks.
- `raw-*-fetches.json`, `raw-pr-info.json`, and `raw-changed-filenames.json`: complete connector retrieval records.
- `remote/`: exact decoded source, registry, log, and provenance bytes used by this review.
- `EVIDENCE_MANIFEST.json`: file-by-file hash and size inventory for this review packet.

A interrupted chunked-transfer prefix, `raw-pr-patch.json`, is retained solely as local acquisition history. It is not used for any check; `raw-pr-patch-complete.json` is the complete checked diff. An early stdin transfer framing error produced no decoded output files; corrected ASCII framing retained the exact complete Unicode patch. These acquisition events did not alter any repository or source bytes.
