# PR170 source, dependency, and prospective tree applicability

## Result and limits

**PASS_PROSPECTIVE_DATA_ONLY_COMBINATION.** The final data check completed 226 assertions with exit code zero. It reproduces the previously published PR168 dependency combination and extends it by the exact complete PR170 addition set. The resulting prospective tree is `88e905acddc86450c2c637908ccc7e8b3057859c`, containing 24,523 file entries. It preserves all 22,212 entries of the observed main and all preceding dependency-stage entries, including their Git object IDs and modes.

This result concerns an explicitly specified future combination. **PR170 has not been integrated into main by this work.** None of the six prerequisite PRs was observed merged. No Lean command, existing verification driver, Git object-writing command, source mutation, remote mutation, retarget, Ready action, review submission, branch operation, or merge was performed. This specialist does not supply a new mathematical review or replace the prerequisite owners' acceptance gates.

Agent #2/session `acfe54025bfc` owns PR170 delivery under the parent's accepted claim. The original mathematical/source branch writer remains Agent #1. This specialist authored none of the reviewed mathematics. PR168 delivery remains Agent #16/session `02ac12cc16be`; the actual main-write role remains ACTIVE under Agent #31/session `02893e4f368d`. No transfer is inferred.

## Immutable inputs and actual lineage

| Role | Commit | Root Git tree |
| --- | --- | --- |
| PR170 head H | `5e67f08231c1973cb4908c167dbd8e08b3ee50fa` | `31e6a07993ac3c38c8448c05d99b8ad005fe95ed` |
| PR170 stacked base P / PR168 head | `7f23ce839fcc88acb235b1816c2c57dc12e16a33` | `af415391950e87bcda23e0ef8cbaccdbc3e1ac71` |
| Directly read main B | `74a1c3922eb7af438fe40b23d2105ad07556e3f5` | `ba552a911841c2f2654cb4481c92e559e42d2a9b` |

The local immutable Git metadata is consistent with the remote PR head/base observations. Each entire input tree was independently reconstructed by encoding Git tree records and hashing them, without storing a Git object. The resulting IDs exactly match each commit's recorded root tree.

P is a real ancestor of H: `git merge-base P H` returns P. There are exactly three subsequent commits in the selected ancestry path:

1. `7208d7314afe8391db964980f094374c866f9114`, parent P: run tracking and actual clock work.
2. `1c65552f079e1ce4061c69be5488573c59e5a207`, parent `7208d731...`: the frozen full mathematical source checkpoint.
3. H, parent `1c65552f...`: retained independent verification and evidence.

The best common ancestor of B and H is `d299c930273adccb1d1ef8288c23c8c9ce8aeace`. A direct main-to-H tree replacement would therefore be inappropriate. The correct intended operation preserves main and combines the branch history under the established integration protocol.

PR170 remains open and non-draft, with base `research/agent-1/periodic-cycle-adapter-20261017T0100Z`. PR168 remains open and non-draft, based on the guarded-path research branch. PR146/147/150/154/166 were also observed open and unmerged at their pinned heads. Direct `git/ref/heads/main` still returns B. PR146's PR response exposed an older `base.sha`; the direct target ref, not that stale PR metadata field, supplies the observed main identity.

## Complete PR170 scope and identity

The native P-to-H delta, which is also the relevant three-dot delta because P is an ancestor, is exactly **569 additions, zero modifications, and zero deletions**. The GitHub file-list path/blob set agrees with the native tree delta. Every restored file was hashed independently against its H Git blob. The full set contains 190 unique blobs and 5,535,769 file bytes, counting repeated retained copies at each path.

Five additions are the four accepted Lean roots and their scoped registry. The other 564 are contribution evidence under `proofs/contributions/agent-1/periodic-eighteen-return-20261017/`, including original author attempts, retained failures, exact source snapshots, review drivers, command records, manifests, logs, and explanatory documents. Nothing in this report relabels a failed source attempt as an accepted module.

| New root | Git blob | Direct project imports |
| --- | --- | --- |
| `Agent1PeriodicEighteenBand.lean` | `cd5773a38e64e5dc3abb41caa34b24eba8dc6679` | `Agent1PeriodicQuotient`, `RunAncestry` |
| `Agent1PeriodicEighteenTrack.lean` | `609c440ce9d11ddedc3d92fc29f4288913583a04` | `Agent1PeriodicGuardedPath`, `Agent1PeriodicReturnClock`, `RunAncestry` |
| `Agent1PeriodicEighteenClock.lean` | `63fb386451790b3b2c104e9bd531ec94d444cfed` | `Agent1PeriodicWidthPath` |
| `Agent1PeriodicEighteenReturn.lean` | `c9a8a873c4b802fa11b06855b3247338343d7354` | The three new modules above and `Agent1PeriodicCycleGuard` |
| `Agent1PeriodicEighteenReturn.registry.json` | `f6de97470b5649503599ca4c4c4a67ef4644c062` | Exact 31-module scoped project |

All additions are ordinary file blobs. Preserve the original mode: 568 paths use `100644`; `registry-preflight/lean-trust0.sh` uses **`100755`**. That wrapper explicitly invokes the pinned Lean 4.19.0 binary with `--trust=0 -j1 -DElab.async=false`. Its mode must survive any eventual tree construction even when a recovered file cache uses different local filesystem permissions.

`COMBINATION_CHECK.json` records every path, before/after object, mode, reconstructed byte count, SHA256, and Git blob. `proposed-tree-additions.json` is a reviewable exact construction specification: start from prerequisite tree `fe482076...`, retain all its entries, and add precisely the 569 listed `(path, mode, blob)` records. No unspecified overwrite or deletion is authorized by that specification.

## Qualification of the existing PR168 combination evidence

The immutable published packet is at coordination commit `b0b4e46202a492e7d5726560baba439c91efb802`, path `proofs/coordination/reviews/agent16-session02ac12/pr168/`. Its lossless `EVIDENCE_PACKAGE.json` has Git blob `be60aef62b0836311251cf0c53aefa1033929a11`.

The checker validates that exact outer blob, then decompresses each package member as data and verifies all 33 members against byte count, SHA256, and Git blob. The package retains the prior native `git merge-tree --write-tree` and diagnostic `commit-tree` commands, their exit statuses and outputs, stage deltas, source pins, and preservation details. Those historical commands were read; they were **not executed** by this specialist. Prior diagnostic commit IDs remain unreferenced diagnostic evidence, not merge commits.

The present check reads the bounded actual input trees and actual commit ancestry, implements three-way file identity decisions in memory, and encodes the resulting trees independently. Every stage exactly reproduces the published native tree and complete delta:

| PR | Exact head | Added paths | Reproduced resulting tree | Existing delivery owner |
| --- | --- | ---: | --- | --- |
| 146 | `159ed83569f5cc4d058557c2b24b28839552b75a` | 293 | `d7f318d76f05fea5a5ac8328090524c91bc6572c` | Agent #16/session `2b1962844ca1` |
| 147 | `e77289c5f58a3238f53c0f3c6951a73515c5d7d2` | 327 | `1ed0983bc0bec94f3ca5e0b80be5a6a8db405a5e` | Agent #17/session `0abe49735fe9` |
| 150 | `946c69edf3d2e6a87f5516db1fd0091eae29e663` | 403 | `7b3e2b7b53d4fae2068be44dc01069ebce961cf8` | Agent #17/session `0abe49735fe9` |
| 154 | `ebcaf723d61f9513c8bae30440d02ba4a46343b4` | 193 | `ffeeb654e1cae781eeac9848f876b8c4d2882ed2` | Agent #20/session `86350e418736` |
| 166 | `cb753e1f5e6edf409bbf8c35c8a90c63a52545d1` | 231 | `6ab0228f154fa1a31b68089f7bec5ff02da788ae` | Agent #10/session `2a8fba7b8570` |
| 168 | P | 295 | `fe482076a7a4bfab705a2f64a94133da3f489b4e` | Agent #16/session `02ac12cc16be` |
| 170 | H | 569 | `88e905acddc86450c2c637908ccc7e8b3057859c` | Agent #2/session `acfe54025bfc` |

This is a tested ordering, with a dependency branch at PR150/PR154; it need not be described as a single linear source-branch lineage. The existing owners retain their own mathematical and delivery obligations.

There is one relevant ancestry nuance. The original PR168 helper recorded the default single result from `git merge-base`. With all prior parents taken into account, PR168 has **two** best common ancestors: `2d5cfe447811155e93cef173192e96f64ec824e1` and PR154 head `ebcaf723d61f9513c8bae30440d02ba4a46343b4`. Their common ancestor is `8f9249c855418eaadf9bb68bd645948d15777b5b`. Combining those ancestor trees as data is conflict-free and yields effective ancestor tree `f6bc1edd8769ba6d125a1b91008aad69da48e30a`. Using that effective ancestor still reproduces the original native result `fe482076...` exactly. The previously retained native merge result is therefore supported; the original single merge-base field should not be quoted as the complete common-ancestor set.

Five inherited documentation/script snapshots in P/H are older than the corresponding prerequisite-stage versions: the guarded-path README, outer-catalog README, catalog-review README, catalog-review `compare_lean_data.py`, and width-projection README. For every one, H equals P exactly, so PR170 does not propose a change. The three-way result keeps the already integrated prerequisite version. Their older versions remain in source history. The precise old/new blob identities are retained in the JSON report. No blanket ours/theirs selection or source loss occurs.

## Import closure and proof-evidence applicability

The registry describes exactly 31 project modules. This checker binds the bytes of every one to an actual H tree entry and to the prospective tree, validates SHA256 and Git blob against the registry, reads their actual import lines, and checks that dependency traversal from `Agent1PeriodicEighteenReturn` reaches exactly those 31 modules. Every project import resolves inside that pinned closure; the external foundation is the pinned toolchain's `Std`.

There are **27 unchanged inherited project modules and four new modules**. Twenty-two of the 31 already have their exact bytes in B. The five inherited closure modules absent from B are `Agent1PeriodicOuter`, `Agent1PeriodicWidthPath`, `Agent1PeriodicReturnClock`, `Agent1PeriodicGuardedPath`, and `Agent1PeriodicCycleGuard`; the prospective prerequisite stack supplies them. The four remaining absent modules are PR170's own additions. This is why adding only the four new files to current main would not supply the reviewed import closure.

The actual scoped verifier is `proofs/verify_project__214bf7673efe116b.py`, Git blob `21131b03dfa516eb19a0a7a4df4f2a41020d4db1`. It is unchanged across B, P, H, and the candidate. Its retained copy `verification/canonical-verifier.py` has identical bytes. The default-named `proofs/verify_project.py`, `proofs/ACCEPTED_BUILD.json`, `proofs/SOURCE_MAP.json`, and the CycleNumeric, ReturnClock, and GuardedPath registries are also preserved at their pinned identities. Registry provenance matches P and H.

PR170 supplies an explicit scoped registry and preserved execution evidence; it does not modify the global accepted-build catalogue. The retained README's scoped reproduction command selects `--project agent1-periodic-eighteen-return --registry proofs/Agent1PeriodicEighteenReturn.registry.json`. This result must not be represented as a default-target or repository-wide Lean build.

The source-identity conditions needed to reuse the already retained PR170 parent fresh31 and separate nonauthor staged27+4 execution are satisfied for this candidate. Actual command success, independence, raw axiom audit, retained failures, public declarations, and the parent source-checkpoint addendum are separately qualified by the evidence specialist. This report does not independently declare those semantic/build obligations passed merely from source hashes. It establishes that no source, import, registry, or actual checker change in the proposed combination invalidates qualifying prior scoped evidence.

The PR168 build/review evidence remains scoped to PR168's 30-module cycle-adapter project; it is not substituted for PR170's 31-module audit. Likewise, this report does not repeat a satisfied PR168 proof build or assume that the current PR168 owner has acquired main. No imported definitions were changed.

## Exact remaining gate and authorized next action

The observed state supports a precise external dependency: **actual prerequisite integration into main, followed by revalidation against the actual current target under the acknowledged writer**. The prospective tree alone cannot certify actual integration of PR168, preservation of the eventual merge parents, future check results, or a target base that has not yet been produced.

The delivery owner can now publish/send the complete exact-head packet to the existing prerequisite owners and main writer through the authorized coordination path. The writer must complete or obtain each prerequisite owner's outstanding gate, actually integrate the prerequisite stack while preserving source history and evidence, and verify each actual target outcome. No additional user permission is implied by this technical gate, and no authority to seize the occupied main role is supplied.

For PR170, retarget only after the prerequisite result is actually on main and the intended full diff has been inspected. If all frozen inputs and target content remain as specified, the expected post-prerequisite PR170 diff is exactly the same **569 additions / zero modifications / zero deletions**. Any real difference requires precise reconciliation and revalidation of affected evidence. Refresh H, P, direct main, ownership, platform checks, material review findings, toolchain assumptions, and import/registry/checker pins immediately before the serialized mutation.

If every gate is then satisfied, the acknowledged writer can use the ordinary history-preserving merge method with the exact head guard `expected_head_sha=5e67f08231c1973cb4908c167dbd8e08b3ee50fa`. This specialist has not invoked that action. The actual merged state, main target, integration commit, ordered parents, content/tree preservation, and applicable postchecks must be independently read back before labeling the delivery VERIFIED_ON_TARGET. A merge into the current research base would remain an intermediate-branch merge.

Revisit on an actual prerequisite merge, any selected head/target-source change, an owner qualification update, relevant platform-check change, or Agent31's explicit execution/release/acknowledged handoff. Silence does not transfer the writer role.

## Reproduction and preserved diagnostics

Run the local data-only checker from any working directory:

```sh
python /workspace/scratch/acfe54025bfc/pr170/combination/check_combination.py
```

It uses the existing read-only Git object database at `/workspace/scratch/7efd48098de6/agent1-repo/.git`, with `GIT_NO_LAZY_FETCH=1`, `GIT_OPTIONAL_LOCKS=0`, and `--no-optional-locks`. An equivalent complete local object database can be selected through `PR170_READONLY_GIT_DIR`. It performs only `ls-tree`, `rev-parse`, `merge-base`, and `log` reads; it neither fetches missing objects nor creates a worktree/ref/object. It reads the parent's complete `snapshot/` and `metadata/changed-files.json`; all its outputs remain inside this `combination/` directory.

The checker does not execute recovered source or prior build scripts. Its limited file-level merge algorithm rejects nontrivial path conflicts, and independently hashes directory trees; all encountered stages are conflict-free under those exact decisions. It is sufficient for this specified additive combination and is not a general replacement for native Git merging arbitrary conflicting edits.

Preserved diagnostic failures are local checker issues, not submitted-source or Lean failures. Attempt001 detected one extra terminal newline introduced while materializing the remote package; removing exactly that tool-added byte restored the authoritative package Git blob, recorded in `transport-correction.json`. Attempt002 exposed the overly restrictive assumption that all additions were mode100644; the checker now preserves and explicitly inventories the existing executable wrapper. Attempt004 exposed the incomplete single-ancestor assumption for PR168; the final checker explicitly handles its recursive two-ancestor combination. Failure outputs and reports remain alongside the corrected final run. An earlier read-only attempt to read a missing local new-source blob also failed with lazy fetching disabled; the parent-provided byte-checked snapshot supplied the required content instead.

## Source references

- Exact PR170 metadata: https://api.github.com/repos/taco-jpg/p196-algorithm/pulls/170 ; retained normalized copy `raw_pr170.json`.
- Exact PR168 metadata and current delivery checkpoint: https://api.github.com/repos/taco-jpg/p196-algorithm/pulls/168 and https://github.com/taco-jpg/p196-algorithm/pull/168#issuecomment-6230260699 .
- Existing qualified PR168 packet: https://github.com/taco-jpg/p196-algorithm/blob/b0b4e46202a492e7d5726560baba439c91efb802/proofs/coordination/reviews/agent16-session02ac12/pr168/DELIVERY_PACKET.md .
- Existing lossless PR168 evidence: same commit/path, `EVIDENCE_PACKAGE.json`; exact downloaded Git blob validated above.
- PR168 delivery task: `proofs/coordination/tasks/agent16-session02ac12-pr168-delivery-20261017.json` on `p196/coordination`, retained as `pr168_task.json`.
- Canonical role: `proofs/coordination/roles/integration.json` on `p196/coordination`, observed Git blob `62de1daf0365fc361c8cd633e1858c6118371f4e`; refreshed role and direct main ref in `current-main-role-readback.json`.
- Direct target: https://api.github.com/repos/taco-jpg/p196-algorithm/git/ref/heads/main .
- PR170 exact source/evidence: https://github.com/taco-jpg/p196-algorithm/tree/5e67f08231c1973cb4908c167dbd8e08b3ee50fa/proofs/contributions/agent-1/periodic-eighteen-return-20261017 .
- Source/dependency review references remain distinct: PR170 review5555414572 and PR168 review5555324338. This report submits neither a replacement review nor a same-account approval.
