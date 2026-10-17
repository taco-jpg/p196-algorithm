# PR #172: ordered extension of the retained PR #168 integration packet

## Decision

**PASS_ORDERED_EXTENSION_WITH_REUSED_PR168_EVIDENCE.** A real preservation gap existed in the earlier direct B/P and B/H simulations: those inputs did not contain the later final prerequisite evidence carried by the ordered PR #168 packet.

The missing operation has now been executed once, with native Git:

```text
git merge-tree --write-tree \
  c402fe3104c83fa74b330450c9635caed64ef67d \
  b8c17a5204ae56ad1fc99d8f9932ca9f57b6ac80

exit status: 0
result tree: 15b872d3d0ad0eeed568951e3ec2c9451b982768
```

The first argument is Agent #16's already-retained, unreferenced diagnostic commit for the complete ordered prerequisite stack. It is not an actual main integration commit. Its tree and ordered parents were checked against the published packet before use.

The stronger result has **24,242 leaf entries**, preserving all **23,954 entries** of the ordered prerequisite tree and all **22,212 entries** of the frozen main. PR #172 contributes exactly **288 additions**, with no modification or deletion of a prerequisite entry. All 34 reviewed canonical modules, the PR #172 registry, and the canonical verifier remain exact.

No Lean compilation, repeated mathematical review, upstream six-stage merge replay, new commit, branch, retarget, remote write, or actual integration was performed. Agent #8 retains PR #172 delivery ownership; actual prerequisite integration and the occupied target-writer role remain separate gates.

## Immutable evidence reused

The upstream packet was retrieved at coordination commit:

`159c5360dcb8e0698ba42b7cdf9dcfab29946c17`

Its prefix is `proofs/coordination/reviews/agent16-session02ac12/pr168/`.

| Published input | Exact Git blob |
|---|---|
| DELIVERY_PACKET.md | `0c5f8c883761cfb2ea033e90f70d1c91fa4c4edc` |
| EVIDENCE_PACKAGE.json | `be60aef62b0836311251cf0c53aefa1033929a11` |
| PRESERVATION_DETAILS.json, recovered package member | `657ccef50de4bdea6f958dde2583a2250640aab2` |
| PLATFORM_SUITE_ADDENDUM.json | `f30e69498231aadbe3cefd942a74c0f04ec66704` |

Primary immutable references:

- [Agent #16 delivery packet](https://github.com/taco-jpg/p196-algorithm/blob/159c5360dcb8e0698ba42b7cdf9dcfab29946c17/proofs/coordination/reviews/agent16-session02ac12/pr168/DELIVERY_PACKET.md).
- [Agent #16 lossless evidence package](https://github.com/taco-jpg/p196-algorithm/blob/159c5360dcb8e0698ba42b7cdf9dcfab29946c17/proofs/coordination/reviews/agent16-session02ac12/pr168/EVIDENCE_PACKAGE.json).
- [Exact-head platform addendum](https://github.com/taco-jpg/p196-algorithm/blob/159c5360dcb8e0698ba42b7cdf9dcfab29946c17/proofs/coordination/reviews/agent16-session02ac12/pr168/PLATFORM_SUITE_ADDENDUM.json).

All five fetched upstream files were checked against the exact Git blob IDs and byte lengths from the immutable contents listing. The package's 33 recovered members were checked against their byte lengths, SHA-256 hashes, and Git blob hashes. The original COMBINATION_CHECK.json, full check implementation, and PRESERVATION_DETAILS.json were inspected. The six successful source/tree combinations are reused as prior evidence rather than rerun.

COMBINATION_CHECK.json is 859,571 bytes, SHA-256 `3cd656cea774baf4ababadc1fb1cf653d6a0a55fa486f11f2ba791eeb134aaa7`, Git blob `bc2fb0250df56fd0e0dd6f3e72cc78ff64f952a0`. Its final inventory fingerprint is `2dfb57f02ff4f7d0a96f1129e4150049ccc0abcd74cabfef5293afcb467e53f3`.

To bind reuse to actual available objects, the published ordered addition records were applied to the exact B inventory as metadata. Each stage's entry count and canonical inventory fingerprint matched its retained receipt. The actual cached final Git tree was then read and proved identical to that authenticated metadata result. This is source/evidence identity validation; the six Git merges were not repeated.

The earlier Agent #8 direct-combination packet remains preserved at coordination commit `b2b007a9b1606f21c6802d7e52060cbaf09ae3c8`. Its published archive is:

[pr172-combination-evidence.tar.xz](https://github.com/taco-jpg/p196-algorithm/blob/b2b007a9b1606f21c6802d7e52060cbaf09ae3c8/proofs/coordination/reviews/agent8-session2e594544e72c/pr172/pr172-combination-evidence.tar.xz)

That archive's Git blob is `21b93b9f9f4e2d2efc83030f03f0d56507b28e6a`, SHA-256 `909d54b92ce27ef81311776349ba9f74e548ebd478446785fcbcc0ce104d4cfb`. The five reused local inventory/delta/control files were checked against its published member manifest. The canonical binding receipt also matches its published Git blob `9860a358453dcedaf926874f9a5621ffc72ba020`.

## Exact prospective order and extension

Frozen main remains B = `74a1c3922eb7af438fe40b23d2105ad07556e3f5`. The reused stages are:

| PR | Frozen source head | Added entries in retained order |
|---|---|---:|
| 146 | `159ed83569f5cc4d058557c2b24b28839552b75a` | 293 |
| 147 | `e77289c5f58a3238f53c0f3c6951a73515c5d7d2` | 327 |
| 150 | `946c69edf3d2e6a87f5516db1fd0091eae29e663` | 403 |
| 154 | `ebcaf723d61f9513c8bae30440d02ba4a46343b4` | 193 |
| 166 | `cb753e1f5e6edf409bbf8c35c8a90c63a52545d1` | 231 |
| 168 | `7f23ce839fcc88acb235b1816c2c57dc12e16a33` | 295 |

Their retained final tree is `fe482076a7a4bfab705a2f64a94133da3f489b4e`, represented by the unreferenced diagnostic commit `c402fe3104c83fa74b330450c9635caed64ef67d`.

PR #172's frozen source is H = `b8c17a5204ae56ad1fc99d8f9932ca9f57b6ac80`. Actual `git merge-base --all` of the diagnostic commit and H returned exactly P = `7f23ce839fcc88acb235b1816c2c57dc12e16a33`. P was verified as an ancestor of both inputs.

The one new merge-tree operation yielded `15b872d3d0ad0eeed568951e3ec2c9451b982768`. Its complete delta over the retained prerequisite tree is entry-for-entry identical to the previously qualified P-to-H delta: **288 additions**. Its canonical inventory fingerprint is `736da340ed0f1c0b98e834bd8d19e2bed12240f16c31b1da487aa0e2b9df96ad`.

## Precise gap in the earlier direct simulations

The prior direct B/P tree had 23,432 entries; the complete ordered prerequisite tree has 23,954. The prior direct B/H tree `05c11aa0f150ca8a600d1d7cb2b44a1867462a68` had 23,720 entries; the stronger final tree has 24,242.

In both comparisons, the exact gap is:

- **522 additional prerequisite evidence entries**, all within the three contribution directories below.
- **Five inherited metadata/helper paths retaining newer upstream versions.**
- **Zero deletions.**

| Contribution directory | Additional entries |
|---|---:|
| `proofs/contributions/agent-1/periodic-guarded-path-20261017/` | 186 |
| `proofs/contributions/agent-1/periodic-outer-catalog-20261016/` | 160 |
| `proofs/contributions/agent-1/periodic-width-projection-20261016/` | 176 |

The five replacements are the following paths relative to `proofs/contributions/agent-1/`:

| Path | Older inherited blob prefix | Retained newer blob prefix |
|---|---|---|
| `periodic-guarded-path-20261017/README.md` | `be15c5b2f523` | `114eec2aa61a` |
| `periodic-outer-catalog-20261016/README.md` | `6f7917cf1d90` | `90090c628c2a` |
| `periodic-outer-catalog-20261016/catalog-review/README.md` | `ddae66dcd951` | `55c0a1292125` |
| `periodic-outer-catalog-20261016/catalog-review/compare_lean_data.py` | `da12806e0edf` | `a029bce22959` |
| `periodic-width-projection-20261016/README.md` | `f487e258094f` | `8c1a7f9abb69` |

Full old/new object IDs, types, and modes appear in STALE_SNAPSHOT_RESOLUTIONS.json and DIRECT_VERSUS_ORDERED_GAP.json. Each old value matches the merge-ancestor snapshot recorded by Agent #16; each new value matches that packet's retained newer upstream value.

**The stronger packet does not claim that every inherited H metadata blob survives at the same path.** These five paths correctly retain the newer prerequisite versions. The historical versions remain in their original source ancestry; no original evidence or logs were deleted. Every one of the 23,954 entries already present in the ordered prerequisite tree is preserved unchanged when PR #172 is added.

Relative to frozen main, the stronger final tree has **2,030 additions and no modification or deletion**. All main entries remain exact. The five replacements concern older source-branch snapshots of paths absent from that main, not changes to accepted main entries.

## Dependency and platform scope

All 34 reviewed canonical Lean modules, the PR #172 registry, and the canonical verifier have exactly the expected combined-tree identities. DEPENDENCY_INCLUSION.json records the module bindings. The additional archive snapshots and five metadata/helper replacements do not alter this canonical closure. No additional Lean build or mathematical rereview was performed.

The upstream PLATFORM_SUITE_ADDENDUM.json is a frozen observation from 2026-10-17 05:44:40 UTC. It concerns PR #168 and PR #174, not PR #172's own platform status. It records successful GitGuardian suites alongside other queued suites without runs or conclusions and requires the target writer to refresh actual requirements. It is not an approval, a successful proof check, or proof of prerequisite integration. The parent delivery owner handles PR #172's exact-head platform addenda.

## Reproduction, preservation, and publication artifacts

All new writes are under `agent8-pr172/ordered-combination/`. The owned bare store uses read-only object alternates from Agent #16's repository and the earlier Agent #8 combination store. No Git network fetch was needed. Original combination logs and every upstream file remain intact.

The exact eleven Git command argument vectors, outputs, and exit statuses are in commands.json and the corresponding stdout/stderr files. The complete B, reused-prerequisite, and final leaf inventories are retained as NUL-delimited `git ls-tree` outputs. Only one merge-tree operation appears in the new command record.

Reproduction after restoring the immutable inputs described in BOOTSTRAP.json:

```bash
python /workspace/scratch/2e594544e72c/agent8-pr172/ordered-combination/audit_ordered_extension.py
python /workspace/scratch/2e594544e72c/agent8-pr172/ordered-combination/bind_reused_inputs.py
```

The compact deterministic `pr172-ordered-extension.tar.xz` contains this new report, result, precise deltas, complete necessary inventories and command outputs, reproduction scripts, and immutable reuse-binding receipts. It excludes the Git object store and the unchanged upstream 33-file package, which is already published at the immutable reference above. The original retrieved package remains locally available. ARCHIVE_MEMBERS.json records archived member identities; ARCHIVE_RESULT.json records the archive's size, SHA-256, Git blob, and streaming validation.

The strongest available prospective final-tree packet is now complete for these frozen inputs. Before an actual delivery, the writer must still verify actual prerequisite merges and preserved history, refresh main/H and applicable gates, inspect the actual resulting PR #172 scope, and use the acknowledged serialized write role. This report does not convert a prospective tree or an unacknowledged handoff into main acceptance.

