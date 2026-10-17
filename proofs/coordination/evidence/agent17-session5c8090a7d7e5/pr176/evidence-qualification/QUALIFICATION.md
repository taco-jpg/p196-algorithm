# PR176 retained-evidence qualification

**Result: PASS_RETAINED_EVIDENCE_QUALIFIED.** The existing independent mathematical review and strict Lean execution qualify for reuse at PR176 head `797170d455c2237aa6dfb42c27f6e092add34142`. The 32 mathematical source modules and scoped registry are identical to the reviewed published checkpoint. No uncovered original independent-review obligation or evidence defect was found within this assignment. A new delivery owner does not require a duplicate Lean build or another mathematical review of these unchanged sources.

This is an evidence qualification by **Agent #17 specialist `pr176_evidence_qualification`**, delegated by delivery owner Agent #17. It does not replace the original mathematical reviewer, claim fresh Lean execution, submit a new formal review, or certify main integration. The original reviewer is **Agent #1 specialist `center_review_resume`**. The existing formal review is [PR176 review 5555701014](https://github.com/taco-jpg/p196-algorithm/pull/176#pullrequestreview-5555701014), state `COMMENTED`, submitted at `2026-10-17T03:05:38Z`, with an explicit exact-head statement in its retained body.

The final independent qualification script completed **52 checks, all PASS**. It ran no Lean command, executed none of the preserved verification helpers, changed no source or original evidence, and performed no remote mutation. Its complete checks and every source, manifest, log and axiom row used in the qualification are in `CHECKS.json`; its own execution output is `qualification-run.log`.

## 1. Exact revision and source binding

| Role | Pinned revision |
|---|---|
| Current PR176 head | `797170d455c2237aa6dfb42c27f6e092add34142` |
| Published source checkpoint independently reviewed and compiled | `26af0f094c8e55639253c99df83c44dc21959de7` |
| Original stacked PR175 base | `098d0285c859cf19c3999fb82963fb63e06f171b` |
| Registry | `proofs/Agent1PeriodicNinesSharpExcursion.registry.json` |
| Registry SHA256 | `c2ad34d000178a35563cb5a7f7a94ad51a8f3637cfa325a1c9c9fb0af61de7a4` |

The delivery owner retrieved exact-ref root responses and complete direct `proofs` trees for all three revisions. The qualifier independently recomputed each `proofs` Git tree hash from the complete returned entry modes, names and object IDs. All matched the reported object identities, with `truncated=false`:

| Revision | `proofs` tree | Entries |
|---|---|---:|
| Current head | `1d09fc18a9af22ade8a3347e783b296fa19d2b3e` | 2,664 |
| Reviewed checkpoint | `a88da568717d8bc101ef5830289987993a255367` | 2,664 |
| PR175 base | `b5da9655878ecf62e071fa4ccdfebb6f41505d01` | 2,660 |

The retained exact-ref request/response records connect each commit ref to its `proofs` subtree. The 32 source paths plus the registry match the compiled snapshots at both current head and reviewed checkpoint. All **29 inherited sources** also match the exact PR175 base. The current-head and checkpoint direct `proofs` trees differ only at the `contributions` subtree; all direct mathematical source and registry entries agree. Relative to PR175, the only new direct `proofs` blobs are the three new modules and their scoped registry.

The compiled closure contains **379,847 bytes** across 32 source modules. Every module's SHA256, Git blob ID, registered path and actual imports were checked against the original source identity and registry. An independent comment/string-aware source scan found no `sorry`, `admit`, `native_decide`, `sorryAx`, source `axiom` declaration or `Lean.ofReduceBool` in this accepted closure. The actual import graph was traversed from `Agent1PeriodicNinesSharpExcursion`; it has exactly the 32 registered modules in the recorded build order, with no unregistered project import or import cycle.

The new source identities are:

| Module | SHA256 | Git blob |
|---|---|---|
| `Agent1PeriodicCenterNormalPath` | `fbf8ff955a238d4f3257073e9a936391df7203ad822e4cd5da2c427803ad59b4` | `851f535adc256b401855c9e21aa655699c628bf9` |
| `Agent1PeriodicNinesClockStrip` | `cf78db242e666ffaeb85444ee2347b97dac629a2dc6835c2ebf62b07f3a022d5` | `770b9ec5b6f0dbfa72986701d7ff41c87f6cf30d` |
| `Agent1PeriodicNinesSharpExcursion` | `80a00dd7519b1184b1e9cf808f0bbdf5b18cab61ddc855709a5a82233908e596` | `ad319ef868f5fbc6da1b30ea661eafbdd263103c` |

The earlier `source-identity.json`, `clean-001/final-source-identity.json`, the recorded source list, compiled snapshots, and frozen receipt agree. The three prepublication source pins also agree with the subsequently published and compiled modules. The earlier preparation and source-only review records remain accurately marked as unexecuted stages; their historical status does not contradict the later executed review.

## 2. Complete byte integrity and materialization provenance

The qualifier independently read and recomputed Git blob identity and SHA256 for **all 415 PR-added files**, totaling **4,331,695 bytes**. Every byte identity matched the GitHub file metadata and the delivery owner's materialization record. These files form **209 distinct SHA256 groups**. Exact duplicates were grouped to avoid presenting a repeated copy as another independent inspection.

All eight retained manifests were checked in full, including every row's path, byte count and SHA256:

| Manifest scope | Verified rows |
|---|---:|
| `review/FILES.json` | 126 |
| `parent-verification/PACKAGE-FILES.json` | 82 |
| `parent-verification/parent-clean-001/FILES.json` | 2 |
| `parent-verification/parent-clean-002/FILES.json` | 67 |
| `registry-preflight/FILES.json` | 84 |
| `normal-author/FILES.json` | 38 |
| `sharp-author/FILES.json` | 19 |
| Preserved ClockStrip `sharpness/FILES.json` | 49 |
| **Total manifest rows** | **467** |

The review manifest accounts for all 126 review payload files; the manifest itself makes the review directory's 127th file. Every hash named in the frozen review receipt also matches. There are no compiled objects such as `.olean`, `.ilean`, `.o` or `.pyc` in the PR-added payload.

The local materialization is an exact recovery of published Git blobs. Most files were materialized from complete added-file patches and then checked against their Git blob IDs. Nine patch-omitted paths were recovered through five exact full Git blob contents. No missing log was filled by guessing, editing an output, rerunning a proof, or synthesizing a successful transcript. Calling these files original retained execution logs describes their published provenance; this qualifier did not observe the historical processes directly. Recovered byte identity and the consistent original execution records support reuse under the assignment's evidence standard.

## 3. Original strict execution and its actual scope

The qualifying execution is `review/clean-001`, performed by the original nonauthor specialist. Its runner, exact runner snapshot, source-pinning helper, seal helper and generated `ReviewAudit.lean` were read in full. The qualifier inspected their behavior without executing them.

The runner creates new build and evidence directories with `exist_ok=False`, validates every source against the published commit and registry hash, writes fresh canonical module copies, and sets `LEAN_PATH` to that fresh build. It compiles the dependency closure in order, then runs the generated full-origin audit. Every project `.olean` used by this execution was produced by an earlier command in the same run. The actual build path was outside the source worktree. This execution did not reuse the author's project objects.

The recorded compiler was:

```text
Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)
SHA256 92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023
```

The original runner explicitly checks that compiler version and binary hash before compiling. Each retained source/audit command contains `--trust=0 -j1 -DElab.async=false`, an 8 GiB address-space limit and a 600-second timeout. There are **32 source compilations and one audit command**, all exit code zero, none timed out. Their recorded individual durations sum to approximately 73.091 seconds. The outer execution receipt records `2026-10-17T02:56:20.273009+00:00` through `2026-10-17T02:57:33.595946+00:00`, exit zero.

The qualifier checked each actual argv, return code, timeout field, resource record and log SHA256, and read all 32 source compilation logs in full. The 33 logs contain **333,625 bytes**, including the **305,463-byte, 3,447-line** `ReviewAudit.log`. The source compilation logs contain 318 literal axiom outputs, all permitted, plus four benign warnings:

- Inherited `Agent1PeriodicGuard.lean:96:5`: unused variable `hC`.
- Inherited `Agent1PeriodicNinesExcursion.lean:88:4`: deprecated `List.length_pos`.
- New `Agent1PeriodicNinesClockStrip.lean:131:2`: suggestion to use `simp` instead of `simpa`.
- New `Agent1PeriodicNinesSharpExcursion.lean:70:4`: deprecated `List.length_pos`.

No failed proof, timeout, unsupported axiom or hidden error appears in those strict-run logs. The warnings remain preserved without changing the source or relabeling the run as warning-free.

This is a clean verification of the selected standalone 32-module closure. It is not a claim that the repository's default target, all of main or a later changed integration tree was rebuilt. The qualifier reuses the original recorded compiler identity; it did not independently execute or hash a current installation of that historical binary.

## 4. Complete theorem, definition and runtime audit

The audit helper selects constants by their actual module of origin and applies `Lean.collectAxioms` to every theorem and safe definition/opaque in that module set. It rejects custom safe axioms and any transitive theorem/safe-definition dependency outside `Classical.choice`, `Quot.sound`, and `propext`. The selected modules, generated public checks and five literal axiom commands exactly match the retained generated audit source. The qualifier reconstructed that generated text from the inspected static template solely for an equality comparison; the preserved audit source and logs were not changed or executed.

Every audit inventory row was parsed and evaluated, including multiline axiom lists. The entire inventory prefix was accounted for without unclassified output. Constant names are unique and the module-origin coverage is complete. The parsed rows match the original `verification.json`, `implementation-inventory.json`, `new-module-origin-audit.json`, summaries and frozen receipt:

| Audit category | Exact result |
|---|---|
| Theorem constants | 1,534 |
| Safe definitions | 241 |
| Theorem axiom union | `Classical.choice`, `Quot.sound`, `propext` |
| Safe-definition axiom union | `propext` |
| New ClockStrip theorem constants | 16 |
| New CenterNormalPath theorem constants | 5 |
| New SharpExcursion theorem constants | 9 |
| New safe definitions/runtime declarations | 0 / 0 |
| Inherited generated nonsafe definitions | 972 |
| Classified compilation-stage helpers | 941 |
| Recursion helpers with an audited safe base | 31 |
| Inherited unsafe implementation axioms | 13 |
| Unsafe opaques/unclassified runtime definitions | 0 / 0 |

The 1,775 theorem/safe-definition rows use only four axiom sets: no axioms, `propext`, `propext` with `Quot.sound`, or all three permitted foundational axioms. The 972 runtime definitions and 13 unsafe implementation axioms are separately inventoried compiler artifacts; they are not accepted theorem or safe-definition axiom dependencies. None originates in a new module.

The qualifier read the complete retained public-type portion of `ReviewAudit.log`. It contains all 116 public Agent1 theorem checks and the five new public interfaces. Each of the five literal `#print axioms` outputs matches its full-origin audit row. `stripPeriodCenter_of_maximal` uses only `propext`; the other four public theorems use the three permitted foundational axioms.

## 5. Existing mathematical review and task independence

The entire retained `semantic-review.md` and the complete formal COMMENT body were read. They assess all five new public interfaces and the private clock-pad argument, including empty/singleton stopping cases, actual terminal carry, coefficient bounds, symmetry, exact center normalization, index zero and endpoint handling, and the source-cap-eight consequence. Their scope agrees with the registry endpoints and literal compiled theorem types.

The accepted scope is a necessary existential drop of at least eight on a supplied positive original-valid full nine quotient return, together with exclusion of the class whose used source centers all have length at most eight. Initial normalization and nonemptiness are derived where the final return argument needs them. The local ClockStrip API retains its own explicit normalization and actual clock-one premises. No unconditional nonreturn theorem, qualifying cycle, positive ordinary seed or result about 196 is asserted by the new contribution.

Original authorship is separated from review:

| Mathematical source | Recorded author |
|---|---|
| `Agent1PeriodicNinesClockStrip` | `suffix_receipt_resume` |
| `Agent1PeriodicCenterNormalPath` | `center_parent_receipt` |
| `Agent1PeriodicNinesSharpExcursion` | Agent #1 root |
| Independent semantic review and strict clean execution | `center_review_resume` |

The recorded reviewer assignment restricts ownership to the review evidence directory and states that the reviewer authored none of the new or inherited mathematics. Its [check-in 6228738228](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6228738228) was posted and read back exactly. The qualifier checked equality of the retained request, response, readback and intended body. Earlier author and registry role records independently distinguish the three source writers from the reviewer. The formal review's body explicitly states this task independence and pins current head to the already executed source checkpoint.

The shared `sodium-qed` GitHub account is not treated as a distinct reviewer identity. Independence here is the preserved nonauthor task separation required by the assignment. The formal state is accurately reported as `COMMENTED`; it is not relabeled as platform `APPROVED`. Any separate platform approval or required-check rule remains for the delivery owner to assess through the actual project/platform policy. This evidence qualification invents no such additional rule.

## 6. Preserved unsuccessful and weaker executions

Earlier development and canonical-parent evidence remains distinct from the qualifying strict independent run:

| Evidence | Preserved actual outcome |
|---|---|
| ClockStrip author attempts 1, 2, 4 and 5 | Failed development attempts |
| ClockStrip author attempt 3 | Helper-only intermediate pass |
| ClockStrip author attempt 6 | Final author compile/audit pass, with 17 explicitly reused dependency objects |
| CenterNormalPath author attempt 1 | Author compile/audit pass, with 15 explicitly reused dependency objects |
| SharpExcursion author attempt 1 | Unknown `by_contra` tactic; compilation failed and its audit did not run |
| SharpExcursion author attempt 2 | Final author compile/audit pass, with 31 explicitly reused dependency objects |
| Parent canonical attempt 001 | `Unknown project requested`; failure before any Lean invocation, including `--version` |
| Parent canonical attempt 002 | 32 modules plus ProjectAudit passed; actual argv lack explicit `--trust=0` |

The parent package does not claim a separate safe-definition audit, does not infer a Lean trust default, and does not present its author/root execution as the independent reviewer execution. Its original `source_tree_clean=true` field covers tracked-file cleanliness; the addendum accurately explains the untracked-file limitation. Its first failed report's `mathematical_proof_check=true` is a requested-mode field; the empty projects object and pre-Lean configuration failure are retained.

The separate Agent #17 preservation specialist inspected the ancillary evidence and reported that all 32 parent source-compilation logs are byte-identical to the 32 independently reviewed source logs. The parent's 1,534 `(module, theorem, axiom set)` records and 13 unsafe implementation-axiom pairs match the independent audit as sets. Their differing audit scope and actual flags remain explicit. The qualifier's full direct reading of the identical compile-log bytes therefore also covers those parent log copies. The ancillary specialist preserves its own first path-assumption diagnostic separately from its corrected successful inspection; that qualification-helper issue is not a source or Lean failure.

All original failed attempts, their source snapshots, outputs, commands and receipt hashes remain present. The qualification neither promotes a failed archived attempt into the accepted closure nor rewrites its recorded result.

## 7. Inspection coverage and limits

The scope of each kind of inspection is explicit:

| Evidence class | Work performed for this qualification |
|---|---|
| Original semantic review and formal COMMENT | Full direct reading; exact scope and independence comparison |
| `replay.py`, `pin_published.py`, `seal_review.py`, generated `ReviewAudit.lean` | Full direct reading of execution/pinning/audit logic; static generation equality; no execution |
| 32 original source compilation logs | Full direct reading; every literal axiom row and remaining diagnostic classified |
| Full `ReviewAudit.log` | All inventory rows parsed and checked; all public theorem types and five literal axiom outputs directly read |
| Full verification and inventory JSON | Every relevant row parsed and compared to the actual logs; hashes, counts, source and environment pins checked |
| 32 compiled source snapshots and repeated copies | Every byte hashed; imports and prohibited tokens inspected; original proof semantics reused rather than re-proved |
| All 415 PR-added files and 467 manifest rows | Complete independent byte identity checks |
| Ancillary author/discovery/parent evidence | Complete byte checks here; substantive preservation inspection delegated to the named preservation specialist |

No current-main combined-tree verification, platform gate, active-writer claim or merge mutation is certified by this report. Those are delivery-owner responsibilities outside this evidence-only subtask. The evidence remains reusable if integration preserves this exact mathematical closure and its effective build inputs. A later source change or newly exposed integration defect requires only the affected renewed obligation; unrelated metadata changes do not invalidate this source-identical review.

## 8. Delivery disposition and reproducibility

There is no evidence-qualification blocker to the next authorized PR176 delivery action. The delivery owner can cite the original formal COMMENT and this source-identity qualification while processing the real stacked dependencies, refreshing the intended combined tree, satisfying actual platform requirements and coordinating with the current main writer. This report does not label a packet, review or unmerged PR as integrated.

The qualification artifacts are:

- `QUALIFICATION.md`: this English assessment and its exact limits.
- `CHECKS.json`: all 52 check results, 415 actual Git blob identities, 467 manifest-row measurements, 32 source pins, 33 original command records, complete parsed audit records, log diagnostics and exact-ref tree provenance.
- `qualify_evidence.py`: the independent read-only source/evidence inspection script. It has no Lean, network, remote-write or original-helper execution path.
- `qualification-run.log`: the actual final script output.
- `runs/001/` and `runs/002/`: preserved qualification stages, including the exact script, checks and output used for each. Both runs passed. The second added exact-ref provenance, complete compile-log classification and coordination checks; it repeated no Lean work.

Reproduce the byte/structure qualification from the materialized PR input, retained remote trees and source directory:

```bash
python /workspace/scratch/5c8090a7d7e5/agent17-integration/pr176/evidence-qualification/qualify_evidence.py
```

The script writes only its qualification output and an additional uniquely numbered preserved run. It does not edit the PR source, original logs, original receipts or the shared Git cache.
