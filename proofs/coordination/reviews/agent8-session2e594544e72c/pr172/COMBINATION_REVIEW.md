# PR #172: pinned integration-combination review

## Outcome and scope

**PASS_PINNED_GIT_COMBINATION.** Git 2.51.1 actually executed `git merge-tree --write-tree B H` in an isolated Agent #8 object store. It returned exit status 0 and the conflict-free tree:

`05c11aa0f150ca8a600d1d7cb2b44a1867462a68`

Every one of the **22,212 leaf entries in B** and every one of the **16,508 leaf entries in H** retains its exact path, Git object ID, object type, and mode in the combination. There are no modifications or deletions relative to either input. The complete inventories were read locally from Git, without API pagination or response truncation.

This is a simulation at the pinned inputs below. It is **not an actual merge, a retarget, prerequisite completion, Lean execution, independent mathematical approval, or acceptance of all main**. Agent #8 remains delivery owner. Agent #1's source ownership, Agent #16's PR #168 responsibility, and Agent #31's main-write role were not changed.

## Exact inputs

| Role | Commit | Root tree |
|---|---|---|
| B: frozen main | `74a1c3922eb7af438fe40b23d2105ad07556e3f5` | `ba552a911841c2f2654cb4481c92e559e42d2a9b` |
| H: PR #172 head | `b8c17a5204ae56ad1fc99d8f9932ca9f57b6ac80` | `a2908ac01835564bfc2bfbf39ad023f0726fa22c` |
| P: existing PR base / prerequisite head | `7f23ce839fcc88acb235b1816c2c57dc12e16a33` | `af415391950e87bcda23e0ef8cbaccdbc3e1ac71` |
| M: actual B/H merge base | `d299c930273adccb1d1ef8288c23c8c9ce8aeace` | `25a1e78123d4a9c1721f850247f8fd2c102301a0` |

Local `git merge-base --all B H` returned exactly M. This independently agrees with the GitHub comparison metadata. Local ancestry checks established that P is an ancestor of H and that M is an ancestor of both B and H. The divergence is 152 commits exclusive to B and 19 exclusive to H.

These are the requested frozen inputs. This review makes no assertion that a later remote main or source head has not advanced.

## Complete change and preservation inventory

| Comparison | Added entries | Modified entries | Deleted entries |
|---|---:|---:|---:|
| M to B | 7,212 | 0 | 0 |
| M to H | 1,508 | 0 | 0 |
| P to H: actual PR #172 scope | 288 | 0 | 0 |
| B to combined tree T | 1,508 | 0 | 0 |
| H to combined tree T | 7,212 | 0 | 0 |

The two branches' additions since M have **zero intersecting paths**. Therefore the exact Git merge result is a deterministic additive union. The full combined tree has **23,720 leaf entries**.

The direct endpoint comparison B to H has 7,212 absent-on-H entries and 1,508 absent-on-B entries. Those 7,212 entries are not deletions in the integration: the three-way result preserves them all. The complete endpoint comparison is retained in `changes-B-H.json`; the actual integration delta is `changes-B-T.json`.

The complete P-to-H inventory exactly matches all 288 supplied `pr-files.json` entries, including status and blob identity. The driver independently recomputed Git blob hashes from all 288 materialized files under `../source`, matching those exact objects. No unread/truncated API file list was treated as the full source change inventory.

### Why prerequisite integration must precede any retarget

An immediate integration of H into this B would introduce **1,508 entries**, comprising **1,220 prerequisite-chain entries plus the 288 PR #172 entries**. It would not be a 288-file contribution against current B.

A second actual local command, `git merge-tree --write-tree B P`, succeeded with exit status 0 and produced the hypothetical prerequisite-integrated tree U:

`6fc2fc5a35b7d6f1e3026b8a603f8a91f1314332`

U has 23,432 leaf entries and preserves every entry of both B and P. The entire U-to-T delta is **identical, entry for entry, to P-to-H**: exactly the same 288 additions, with the same modes, types, and blob IDs.

This establishes the source-shape consequence of integrating the pinned prerequisite first. It does not establish that PR #168 has actually merged. No synthetic merge commit, branch ref, or remote mutation was created. After real prerequisite integration, the delivery owner must refresh the actual target and H, recompute the applicable combination, and inspect the actual retargeted diff before acting.

### Additions to B by contribution directory

| Directory | Added leaf entries |
|---|---:|
| `proofs/` directly | 26 |
| `proofs/contributions/agent-1/periodic-cycle-adapter-20261017/` | 291 |
| `proofs/contributions/agent-1/periodic-guarded-path-20261017/` | 43 |
| `proofs/contributions/agent-1/periodic-nine-cycle-20261017/` | 285 |
| `proofs/contributions/agent-1/periodic-outer-catalog-20261016/` | 128 |
| `proofs/contributions/agent-1/periodic-return-clock-20261016/` | 191 |
| `proofs/contributions/agent-1/periodic-return-core-20261016/` | 398 |
| `proofs/contributions/agent-1/periodic-width-projection-20261016/` | 146 |

The 26 direct `proofs/` additions comprise 19 Lean files and 7 registry files. Only two of those Lean modules and one registry belong to the immediate P-to-H PR #172 delta. The other 17 Lean files, six registries, and associated contribution records are inherited prerequisite-chain content. The full path inventories are retained, not collapsed into this summary.

## Reviewed dependency source inclusion

All **34 reviewed modules** in `../CANONICAL_BINDING_RESULT.json` are present in T at their exact reviewed blob identities and H modes. Of those modules, 25 were already identical at B. The other nine are:

| Canonical path | Source relationship |
|---|---|
| `proofs/Agent1PeriodicOuter.lean` | Inherited from P; absent at B |
| `proofs/Agent1PeriodicWidthPath.lean` | Inherited from P; absent at B |
| `proofs/Agent1PeriodicReturnClock.lean` | Inherited from P; absent at B |
| `proofs/Agent1PeriodicCyclePath.lean` | Inherited from P; absent at B |
| `proofs/Agent1PeriodicGuardedPath.lean` | Inherited from P; absent at B |
| `proofs/Agent1PeriodicCycleGuard.lean` | Inherited from P; absent at B |
| `proofs/Agent1PeriodicCycleNumeric.lean` | Inherited from P; absent at B |
| `proofs/Agent1PeriodicNinesPath.lean` | New in PR #172 |
| `proofs/Agent1PeriodicNinesCycle.lean` | New in PR #172 |

The exact paths and full reviewed/combined identities for all 34 modules are in `dependency-inclusion.json`.

The combined tree also preserves the canonical registry and verifier:

- `proofs/Agent1PeriodicNinesCycle.registry.json`: `efe03f3f3f146d7ddce2e96cb126ea81f710fcc3`.
- `proofs/verify_project__214bf7673efe116b.py`: `21131b03dfa516eb19a0a7a4df4f2a41020d4db1`.

This establishes source inclusion and identity. The parent delivery owner separately determines whether retained Lean evidence and independent review qualify under current policy.

## Acquisition, isolation, and execution evidence

The shared Agent #6 and Agent #12 repositories were queried read-only with lazy fetching disabled. Both contained B; neither contained H or P. Agent #6's repository was not shallow and was selected as a read-only alternate. Its existing transitive alternate was preserved.

The only created Git store is:

`/workspace/scratch/2e594544e72c/agent8-pr172/combination/objects.git`

It references the existing read-only object directory:

`/workspace/scratch/01c8ccabdd45/p196-agent6/.git/objects`

A bounded public Git fetch obtained H/P commit and tree metadata using `--filter=blob:none`, `--no-tags`, `--no-write-fetch-head`, `--no-auto-maintenance`, and the known B as negotiation tip. The ordinary sandbox attempt failed to reach the proxy. The same command then succeeded through the approved `require_escalated` tool path. It fetched 285 packed objects, approximately 359.06 KiB. No unfiltered clone or separate blob-fetch command was performed.

All later audit commands set `GIT_NO_LAZY_FETCH=1`, disable optional locks, and use an empty global Git configuration. The before/after `show-ref` outputs are empty: no branch or tag refs were created. The bare store's initial HEAD is only an unborn placeholder.

GitHub compare metadata was used only as corroborating metadata. Its file array was capped at 300 and the requested commit page contained one entry. A recursive Git Trees API attempt returned a transport error. Neither incomplete response was used as a complete inventory. The successful local `git ls-tree -r -z --full-tree` calls supplied the complete inventories.

## Reproduction and retained files

From the existing workspace, rerun:

```bash
python /workspace/scratch/2e594544e72c/agent8-pr172/combination/audit_combination.py
```

The reviewed driver executes only Git metadata operations and the two isolated merge-tree simulations. It reads the materialized PR sources for hashing and writes its evidence solely within this combination directory. It does not run project scripts or Lean.

- `bootstrap.json`: exact acquisition command, approval-path outcome, cache probes, and limitations.
- `audit_combination.py`: reproducible audit implementation.
- `commands.json`: every audit command's exact argument vector, exit status, and stdout/stderr artifact names.
- `*.stdout` and `*.stderr`: complete raw command outputs, including NUL-delimited full inventories.
- `COMBINATION_RESULT.json`: structured result.
- `inventory-{M,B,P,H,U,T}.json`: complete leaf-entry inventories.
- `changes-*.json`: complete path changes, with before/after object IDs, types, and modes.
- `branch-change-overlap.json`: empty, confirming disjoint branch changes.
- `dependency-inclusion.json` and `registry-and-verifier-inclusion.json`: reviewed source/control binding in T.
- `compare-B-H.json` and `commit-H.json`: corroborating GitHub metadata; the compare file intentionally retains metadata only.

The object store is deliberately partial and relies on the named shared read-only alternates for existing objects. It is not represented as a self-contained full repository archive. No compiled outputs, fresh proof checks, platform acceptance, prerequisite completion, retarget, or actual merge are asserted.

## Deterministic publication archive

`pr172-combination-evidence.tar.gz` retains the complete evidence files and reproducible scripts, excluding `objects.git` and the archive itself. No local originals were removed. Members are sorted; tar ownership and timestamps are normalized; the gzip timestamp is zero. The included `ARCHIVE_MEMBERS.json` records member byte lengths and SHA-256 hashes for every evidence file other than that manifest itself. Its own identity is recorded in the external `ARCHIVE_RESULT.json`, together with the archive's size, SHA-256, Git blob ID, and streaming verification result. `build_archive.py` documents the memory-bounded packaging procedure. The report, result, and commands can also be published as readable plain files alongside the archive.

