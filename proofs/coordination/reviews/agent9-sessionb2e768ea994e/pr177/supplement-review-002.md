# PR #177 — independent readback of supplemental audit 002

**Reviewer:** Agent #9 scoped evidence/integration reviewer.  
**Readback time:** 2026-10-17 05:26 UTC.  
**Source H:** `6f48ca108dee4c07588f8c5582bcfef55388537f`.  
**Base B:** `74a1c3922eb7af438fe40b23d2105ad07556e3f5`.  
**Disposition:** **PASS for the new supplemental verification obligation, with the precise coverage and classification limits below.**

The corrected literal audit and the exactly reused safe-definition audit provide the previously pending supplemental evidence. No further Lean invocation or repeated 19-module build is required by this readback. This is an inspection of Agent #1's actual execution, not a claim that Agent #9 compiled the source. It does not reopen unchanged source semantics or substitute for delivery-owner actions.

The frozen checkpoint-001/evidence-review files were not modified. All new files are beneath `agent9-pr177/supplement-review-002/`. Agent #9 remains delivery owner, Agent #1 verification publisher, Agent #107 source owner, and Agent #31 the acknowledged main writer. No source/main/remote mutation or ownership acquisition occurred here. The follow-up continued the existing assignment; no new reasoning-effort configuration is claimed.

## 1. Executed and reused operations

| Evidence item | Actual execution status | Result | Qualification |
|---|---|---:|---|
| `supplement-001/SafeDefinitionAudit` | Executed by Agent #1 | Exit 0 | Successful independent safe-declaration traversal |
| `supplement-001/LiteralEndpointAudit` | Executed by Agent #1 | Exit 1 | Unknown formatting option `pp.width`; failed attempt preserved |
| `supplement-002/SafeDefinitionAudit` | `REUSED_EXACT_SUCCESS` | Original exit 0 | Same audit source, log, compiler, source closure, object pins, and prior report |
| `supplement-002/LiteralEndpointAudit` | Executed afresh by Agent #1 | Exit 0 | Only the unsupported formatting-option line was removed from the generated Lean program |
| `readback.py` | Executed by Agent #9 | Exit 0 / `PASS` | Python-only full parsing, identity checks, and result reconciliation; no Lean process |

All actual Lean argv arrays use the pinned binary at `/workspace/scratch/f8aedc6d7adf/runtime-agent6/lean-4.19.0-linux/bin/lean` with `--trust=0 -j1 -DElab.async=false`. The initial successful safe audit took approximately 22.56 seconds; the corrected literal audit took approximately 3.22 seconds. The repeated command entry in result 002 is correctly labeled reused, including its original path and elapsed time. It must not be counted as a second safe-audit execution.

The reviewed runner uses a restricted environment containing its explicit `PATH`, `LANG`, and `LEAN_PATH` pointing to the prior fresh source/object directory. It invokes Lean via an argv array with the supplement directory as working directory. The result records actual command arguments, exit codes, generated-source hashes, and log hashes. The environment construction is supported by the inspected runner; it is not a separate environment dump in the result JSON.

## 2. The retained failure and the bounded repair

`supplement-001/RESULT.json` remains **FAIL**. Its first substantive error is:

```text
LiteralEndpointAudit.lean:7:0: error: unknown option 'pp.width'
```

The failure is in the generated evidence program's formatting configuration. It is not a failure in a theorem, axiom whitelist, or original PR source. Although the failed invocation emitted substantial diagnostic output afterwards, its literal audit is not reused as successful evidence.

The exact Lean source difference for literal attempt 002 is deletion of:

```lean
set_option pp.width 120
```

All module imports, module-origin theorem selection, calls to actual `#print axioms`, and all nine literal endpoint `#check` commands remain. The Python runner additionally permits exact reuse of the prior successful safe audit, checks the complete source/object/compiler/report identity before that reuse, and corrects the summary parser to accept a multiline axiom-union list. Its count logic and whitelist obligations are not reduced.

The first attempt's source, logs, traceback, result, manifest, console log, and the original runner are preserved unchanged under `snapshots/`. The corrected runner and complete second-attempt evidence are preserved separately. No original failed receipt has been rewritten into a pass.

## 3. Source, object, and runtime provenance

Both supplement records bind to the same actual prior strict-run report:

`trust0-run-001/verification.json`, SHA-256 `9d66b372ee5800806dc96c284c59f25d52520c2433b192eda02744c6f733caaa`.

That prior report identifies exact H, `source_tree_clean=true`, overall/project PASS, and 19 successful strict source-module commands plus the successful `ProjectAudit` command. The earlier review already inspected that execution. This readback checks the specific chain needed for reuse:

- All 19 source records are identical across both supplements and the prior report.
- All reconstructed source bytes match the prior `build_sha256` values and the actual exact-H checkout source hashes.
- Both supplements contain the same 19 `.olean` hashes; every presently retained object matches its pin.
- The safe-audit source and log in attempts 001 and 002 are byte-identical and match the successful command's recorded hashes.
- Both supplements identify the same prior-report digest and compiler-file map.
- The actual compiler and all four listed runtime shared-library files match the five recorded hashes.
- Both manifests are complete for their listed outputs: all six entries from attempt 001 and all five from attempt 002 match their byte counts and SHA-256 values.

The runner captures object hashes before supplemental work and checks them again after a successful attempt, along with the source, compiler, and prior report. Attempt 002 verifies the retained success's object pins against its current pins before reuse. This is a consistent retained-build provenance chain. The original strict verifier did not record `.olean` hashes in its manifest; the supplement's hashes must not be retroactively described as initial compiler-output receipts. No object file is copied into this review deliverable.

## 4. Safe-declaration audit: complete coverage and full axiom lists

The actual safe-audit program traverses all constants whose recorded module of origin belongs to the selected 19-module closure. For every declaration that is neither `isUnsafe` nor `isPartial`, it:

1. Rejects a safe custom `.axiomInfo` declaration.
2. Selects theorem, definition, or opaque declarations for dependency auditing.
3. Rejects project `implemented_by` or `extern` hooks on the selected declarations.
4. Collects transitive axioms with `Lean.collectAxioms` and rejects every axiom outside `propext`, `Classical.choice`, and `Quot.sound`.
5. Prints a named result and complete-count summary.

The readback independently parsed **every full bracketed axiom list**, including continuation lines. It did not merely inspect each first printed line or trust the final summary. It also checked that no non-whitespace log content remained outside recognized declaration, unsafe/partial, and summary records.

| Selected safe category | Actual complete entries |
|---|---:|
| Theorem | 1,453 |
| Definition | 414 |
| Opaque | 0 |
| Total transitive-axiom entries | **1,867** |
| Entries whose axiom list spans multiple lines | **163** |

All names are unique. The theorem name set equals the full prior canonical theorem-origin audit. Every parsed list is limited to the allowed foundational axioms, and their actual union is exactly `{Classical.choice, Quot.sound, propext}`. No safe custom axiom, disallowed theorem/definition dependency, project `implemented_by`, or project `extern` rejection appears. All those checks actually executed in the successful safe audit; they are not inferred only from a keyword scan.

The new seven modules account for **115 theorems and 50 safe definitions**:

| Module | Theorems | Safe definitions |
|---|---:|---:|
| `Agent107DFA` | 13 | 17 |
| `Agent107DFAAlphabet` | 27 | 5 |
| `Agent107DFAArithmetic` | 2 | 0 |
| `Agent107DFABoolean` | 24 | 15 |
| `Agent107DFAChecker` | 20 | 6 |
| `Agent107DFAHorn` | 6 | 0 |
| `Agent107DFARelation` | 23 | 7 |

This includes the actual safe executable definitions `DFA.run`, `DFA.accepts`, `boolImplies`, `allFin`, `checkStarts`, `checkEdges`, `checkTerminals`, `checkHorn`, `centerCode`, `checkRow`, `checkOneHot`, `BooleanDFA.dest`, `BooleanDFA.toDFA`, `stateAt`, `stateIndex?`, and `liftRelation`. In particular, `BooleanDFA.toDFA` has only `propext` and `Quot.sound`; `stateIndex?` and `liftRelation` have only `propext`. Their generated unsafe implementation helpers are classified separately below.

The audit is scoped to theorem/definition/opaque declaration categories in the registered source closure. It is not a claim to audit every standard-library declaration, every category of kernel metadata, all of main, or generated machine-code semantics.

## 5. Literal theorem and endpoint audit

The corrected literal program selects theorem constants by their actual module of origin in the seven new modules and calls Lean's real command elaborator for `#print axioms` on each identifier. It does not fabricate textual output from the previous summary. The successful log contains **115 unique printed theorem results**, matching the safe audit's entire new-module theorem set, including private helpers and generated equation theorems. Every printed axiom set agrees with the independently parsed safe-audit entry for the same theorem.

The log also contains all nine actual `#check` type outputs from the scoped registry:

1. `Agent107.FoldedDFA.horn_prefix_invariant`
2. `Agent107.FoldedDFA.horn_accepting_output`
3. `Agent107.FoldedDFA.checkHorn_iff`
4. `Agent107.FoldedDFA.Encoding.checkOneHot_iff`
5. `Agent107.FoldedDFA.Encoding.BooleanDFA.transition_iff`
6. `Agent107.FoldedDFA.Encoding.stateIndex?_stateAt`
7. `Agent107.FoldedDFA.Encoding.liftRelation_stateAt`
8. `Agent107.FoldedDFA.horn_next_closed`
9. `Agent107.FoldedDFA.horn_canonical_step`

The actual namespace and `?` spellings are preserved. No endpoint was dropped, replaced by a weaker statement, or replaced by an assumed instance. This review checks the supplemental evidence coverage, not a fresh mathematical reinterpretation of those already reviewed statements.

## 6. Unsafe/partial implementation classification

The generated program uses a single condition:

```lean
if info.isUnsafe || info.isPartial then
```

It reports that combined category as `UNSAFE_IMPLEMENTATION`. There are **3,940 unique records** in this category, and the complete list is preserved in `UNSAFE_OR_PARTIAL.json`. The precise supported wording is therefore **“3,940 declarations classified by Lean as unsafe or partial”**. The log does not record which Boolean condition was true for each declaration, and it must not be rewritten as “3,940 unsafe axioms” or as proof that no partial runtime helper exists.

All 3,940 names fall into the following implementation-name families:

| Name family | Count |
|---|---:|
| Compiler stage helpers containing `._cstage` | 3,907 |
| Specialized implementation helpers containing `._spec_` | 17 |
| Recursive runtime helpers ending `._unsafe_rec` | 13 |
| Elaborated implementation helpers containing `._elambda_` | 3 |

This family classification is inferred from exact names; the unsafe-or-partial status itself is supplied by Lean's actual environment flags. All 20 unsafe implementation axioms reported in the prior theorem-only audit are present in this larger set. None is in any accepted transitive theorem or safe-definition axiom list. The two generated `BooleanDFA.toDFA._elambda_1` and `._elambda_2` entries are kept distinct from the safe `BooleanDFA.toDFA` definition, which was actually audited.

As a corroborating source check, the exact 19 source modules were scanned with nested comments and strings masked. There is no explicit source token `unsafe`, `partial`, `axiom`, `sorry`, `admit`, `sorryAx`, `native_decide`, `implemented_by`, or `extern`. This source scan does not replace the environment/dependency audit; it supports the classification that the reported implementation helpers were not newly introduced unchecked source declarations.

The unavailable per-Boolean split is a wording/diagnostic limit, **not a new acceptance gate**. The proof obligations concern the safe accepted chain, which has now been fully audited in the stated declaration categories. No new Lean run is requested merely to split that runtime-helper count.

## 7. Decision and remaining work

**PASS:** the new safe-definition and literal-theorem/endpoint evidence is correctly bound to exact H, preserves the earlier failure, distinguishes reused success from fresh execution, and contains no disallowed dependency in the accepted audited chain. All previously pending supplemental checks in this assignment are now covered.

No mathematical-source repair, additional build, additional semantic review of unchanged source, or rerun of the successful safe audit is required by this result. The root delivery owner should reuse it together with Agent #1's independently reviewed strict-run PASS and the existing semantic review.

The remaining actions are delivery obligations already tracked outside this narrow supplement: publish the complete source-specific execution/repair/readback evidence; complete the known author-registry namespace correction through Agent #107 or an acknowledged narrow handoff; reconcile historical status descriptions; refresh H/B and platform gates; and perform the eligible Ready/guarded merge through the acknowledged main writer. This supplemental PASS neither grants source/main ownership nor reports that a Ready transition or merge occurred.

## 8. Exact artifacts and reproducibility of this readback

| Artifact | SHA-256 |
|---|---|
| Original supplement result | `a75027e5c2f0151bcd17f86ba0f78ad1e4141b69f1d1a8a80dead09906307b21` |
| Corrected supplement result | `8ba902b4b355d7d4c289f19723406433c5a645520602b8a660be3174bd1242e2` |
| Reused safe-audit source | `1eb6f60e11448252ddb320ae5f8724128b90a162fca913a5361fd2289c8c3438` |
| Reused safe-audit log | `0e62a11d297f1f20a98449ef192c72cf6b0e67835db79335da2decd1ae1f4565` |
| Corrected literal-audit source | `37e6bc3afdcf84d1359a610b27190d74d47d2854c0f224b203d7c051e549eba6` |
| Corrected literal-audit log | `c9d79d74f6401539b6df5ac63b22e279fe3c1ae0c4e753b96c2691164ae52733` |
| Corrected Agent #1 runner | `1aeedfea7977790e0eea844532e33809ce0976a83df754d00aca8c56275daf5f` |
| Executed Agent #9 readback program | `47aa7315089b7d591ab1edbf0b5f999e3d1f3f337ea942ed5ee0d2aa7a8806ab` |
| Agent #9 readback result | `0436072ead2ea06f846ff9eb5069d0e0ef7910e3e6ed5206c0d213752f40a380` |

The exact independently executed program is `readback.py`; its actual command was `python3 -B /workspace/scratch/b2e768ea994e/agent9-pr177/supplement-review-002/readback.py`. It writes only beneath its own directory, snapshots the read evidence, validates complete lists and identities, and never invokes Lean. `READBACK_RESULT.json` records its PASS. `PARSED_SAFE_DECLARATIONS.json` and `PARSED_LITERAL_THEOREMS.json` preserve every parsed dependency list. `FILES.json` inventories all deliverable files. Source-object/compiler binaries are referenced and hashed but are not copied into the deliverable.
