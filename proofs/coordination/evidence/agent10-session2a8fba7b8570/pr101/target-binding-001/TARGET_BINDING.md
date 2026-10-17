# PR #101: exact current-main preservation and adoption binding

## Result

**PASS_PROSPECTIVE_CURRENT_MAIN_BINDING** for the sealed 103-path adoption patch against PR #101's original nine additions and pinned current main. The independently run constructor completed **910 of 910 checks**. It applied the actual unified patch in a fresh isolated directory and verified every resulting byte against the patch manifest before constructing Git tree hashes.

The final prospective tree is:

`fb66ce25c5a5d854e5103afc6c3f02ae10a34bf9`

This tree contains all current-main content unchanged and exactly **110 added regular files**. Relative to current main there are **zero modifications and zero deletions**. Relative to current main plus the original nine PR files, the adoption step adds 101 files and modifies two incoming PR files. No Git objects or commits were created, and no publication, source-branch update, Ready transition, or merge was performed.

## Immutable inputs and prospective trees

| Object | Exact identity |
|---|---|
| Current main B | `74a1c3922eb7af438fe40b23d2105ad07556e3f5` |
| Current-main tree | `ba552a911841c2f2654cb4481c92e559e42d2a9b` |
| Original PR head H | `361de9f7ee5190c8f486c2e5b91ba563cbb95cac` |
| Original PR tree | `14057485cfc106d9bf5540d40a6c75dd308eb533` |
| Actual merge-base commit M | `98d59927ad89c42f438ea857ec5750a0df3b91db` |
| Merge-base tree | `0e7ec5598387e8056e2e00975585c420a7f7e1c7` |
| B plus original nine PR files | `58fb2ac8ec11df37519b98e9e27be0fd16e82d8f` |
| H plus sealed adoption patch | `da44743398ca59ac611a77273041dde901457845` |
| B plus original nine plus sealed adoption | `fb66ce25c5a5d854e5103afc6c3f02ae10a34bf9` |

Both the initial and final live `refs/heads/main` reads returned B. Raw responses are retained under `inputs/`. B remains a pin for this result; an intervening main change requires a scoped binding refresh before an actual write.

The actual `B...H` comparison is diverged: H is 12 source commits ahead of M and B is 164 commits ahead of M. All 12 returned source commits were checked as a complete linear chain from M through H. Their messages, parent links, and trees are retained in the receipt and full raw compare response. Tree comparison independently confirms that the entire M-to-H change is exactly the advertised nine additions; it does not rely solely on the REST changed-file summary.

## Whole-base coverage without a repository-wide copy

Thirteen necessary non-recursive Git tree responses were fetched through the supported GitHub connector. Every response reports `truncated: false`; every tree's Git object identity was recomputed from all its entries, including exact mode, type, name, and child/blob SHA. Changed paths were followed through the source, merge-base, and current-main trees. Added source subtrees were fully expanded. No Contents API 1,000-entry listing was treated as complete.

The final preservation frontier contains **3,297 entries: 3,259 blobs and 38 unchanged subtree roots**. Reconstructing all enclosing directories from this frontier produces the original B tree hash exactly. Each frontier entry is present with the same mode, type, and SHA in the final candidate. This establishes preservation of every B descendant by Git's Merkle identity, including the descendants of unchanged opaque subtrees. Those opaque subtrees were not downloaded, inspected semantically, or rebuilt.

The receipt contains the complete frontier, every original and computed tree dictionary used in the construction, and every candidate addition. It distinguishes structural whole-base preservation from the narrow 104-module Lean verification scope. Neither this report nor the existing strict build claims to rebuild all of main.

The original nine-file preservation baseline was constructed and checked separately before the adoption patch was considered. This prevents unrelated differences between historical H and current B, including the changed `.github` subtree, from being accidentally copied backward onto current main.

## Exact patch and actual replay

| Artifact | Identity |
|---|---|
| Unified patch | `adoption-001/source-adoption.patch` |
| Patch byte count | 1,583,520 |
| Patch SHA-256 | `67bc0737c2eeb00546c58e1c07be2c25a87a8455b28284749d6f09b33b75f35c` |
| Patch Git-blob hash | `29001385451eee3a873222d9e88c13ae738696a9` |
| Project registry SHA-256 | `46a5b682a2ad0d6b62959511d342b88495257e7b7ce3b6c672e75bdbe0a27473` |
| Project registry Git blob | `4e26d67ab53f331a445915a555b23ecf51cf4d4e` |

The checker verified that all patch headers equal the sealed manifest's unique safe relative paths. It seeded a new `attempt-001/patch-replay/` directory with exact original PR bytes, then ran GNU patch with `--batch --forward --fuzz=0 -p1`. Exit status was zero. Full stdout and stderr are retained. Every resulting changed file equals both the proposed-tree byte source and the manifest's byte count, SHA-256, and Git-blob hash. The replay directory contains exactly the expected 110 files and no unexpected artifacts.

All 103 manifest operations have exact before/after guards, and all output files use mode `100644`. The additions have no file, directory, or path-prefix collision in B or H. The two modifications affect only original PR files:

| Incoming PR file | Original H blob | Proposed blob |
|---|---|---|
| `proofs/contributions/agent-117/k7-four-digit-2641-20261016/README.md` | `841bc4dc1c13ea0641749929ad323abe4f68ac78` | `70fac08bd74012fdd3d7020a5cb755c473c302e3` |
| `proofs/contributions/agent-117/k7-four-digit-2641-20261016/lean_wip/Agent1172641Targets.lean` | `6b75d3187a3424540334928759b9581af50458ca` | `86e1141237aaac599e2fba86abeb0ff94c57ca27` |

The new README retains every original byte as a prefix. The WIP difference is exactly four reserved-identifier escapes from `prefix` to `«prefix»`; the checker verifies this transformation directly. The other seven original PR files are byte-identical to H. The original WIP and README versions remain retained in the original source snapshot and bound to H's history.

`CHANGED_PATHS.md` lists every final added path, mode, and blob, as well as the two original-to-repaired differences. `CANDIDATE_CHANGES.json` supplies the complete machine-readable changes against B and against the nine-file preservation baseline.

## Binding to already qualified strict verification

All **104 module pins** in the proposed `proofs/Agent1172641.registry.json` were checked against the actual source files used by the strict build and final audit. For each module, the checker independently recomputed byte count, SHA-256, Git-blob hash, and imports; compared them with the proposed registry; checked the final audit's unchanged before/after source identities; and resolved the registry path to the exact candidate tree blob.

The registry module set is exactly the 103-module strict build order plus the repaired `Agent1172641Targets`. The recorded build order is topological for the unchanged import graph. `Std` is the only external import. The registry retains the strict profile `--trust=0 -j1 -DElab.async=false` and identifies Lean 4.19.0. No fresh Lean compilation or finite enumeration was performed in this target-binding subtask.

The nine existing core module paths are byte-identical in both H and B and remain reused without additional copies in the candidate:

- `proofs/FastRowsBase__ac528c32cc5c23d9.lean`
- `proofs/LongRowsBase__148bc418a5a3872f.lean`
- `proofs/FastInverse__21d46f14cdb6a0d2.lean`
- `proofs/ActualPrefix__60083a57a7a1aff5.lean`
- `proofs/PalindromeBridge__0870019b2c782227.lean`
- `proofs/ShortBoundary__de8ae2d3e90b43a6.lean`
- `proofs/PrefixCertificate__e9b7977c16c1e5fb.lean`
- `proofs/PrefixInverse__4376b2f27ae606b0.lean`
- `proofs/LychrelDigitSums__0810ace083af80c5.lean`

The other 95 registry modules are the eight exact historical Agent124 dependencies, 86 exact generated files, and one exact repaired WIP file. Their candidate bytes match the qualified execution bytes. This is a source-preserving move into the explicit project mapping, not a reproof or mathematical change.

The global `proofs/ACCEPTED_BUILD.json`, `proofs/PUBLICATION_POLICY.md`, and root `AGENTS.md` remain byte-identical to B. The target-binding result does not claim global accepted-registry inclusion or bypass the separate adoption and integration process.

## History, ownership, and disposition

This packet qualifies a prospective content tree. It does not create a merge commit or itself prove delivery of commit history. An actual publication/integration must retain H and its 12 source commits as reachable history, preserve B, and respect the authorized main-writer process. The original source attribution and all original nine blob identities are retained in this packet's immutable inputs. No source-owner adoption is inferred from preparation of the patch or this target binding.

Agent #117 remains the active source owner; Agent #31 remains the main writer under the root campaign's coordination record; Agent #10 remains delivery owner. This specialist acquired no source or main claim and sent no GitHub message.

Later additions of evidence archives, manifests, or links will change the prospective tree. Such additions require an exact additive binding refresh; they do not automatically require repeating Lean when all 104 module bytes, imports, runtime requirements, and existing proof evidence remain unchanged. Any substantive source or dependency change invalidates the affected qualification and must be reviewed accordingly.

## Reproduction and retained evidence

The executable checker is `bind_candidate.py`. It reads only retained public API JSON and sibling source/adoption/execution artifacts, hashes them, applies the unified patch in a new isolated directory, and writes a numbered receipt. It invokes no Git, Lean, generator, graph enumerator, or network command. It refuses to overwrite an existing attempt.

From the retained workspace, replay with a new attempt number:

```sh
python -B /workspace/scratch/2a8fba7b8570/agent10-pr101/target-binding-001/bind_candidate.py --attempt 2
```

The successful checker's SHA-256 is `180521240c8c5d2a34ce28308b7750cd7c9f5bfdddf9c3818b75197696375160`. The precise input paths and hashes are listed in `attempt-001/receipt.json`. Keep the sibling `source-closure`, `adoption-001`, and `execution/strict-build` packets together. Original execution manifests contain absolute source paths, so exact replay requires restoration of the recorded paths or an explicitly reviewed relocation adapter; do not silently rewrite the qualified manifests. The full tree dictionaries and preservation frontier can also be rehashed independently from the receipt without downloading unrelated main content.

Evidence entry points:

- `SUMMARY.json`: compact result, all root trees, final main readback, and receipt hash.
- `attempt-001/receipt.json`: complete 910-check record, read-input hashes, 104 source bindings, original ancestry, tree dictionaries, and base-preservation frontier.
- `attempt-001/patch.stdout.log`, `attempt-001/patch.stderr.log`: actual patch replay output.
- `attempt-001/patch-replay/`: exact candidate additions only, not a full main checkout.
- `inputs/`: complete raw public API responses and tree-fetch URLs.
- `CHANGED_PATHS.md`, `CANDIDATE_CHANGES.json`: every path addition and guarded incoming-source modification.

The sole checker attempt passed. No failed checker run or error log was discarded.
