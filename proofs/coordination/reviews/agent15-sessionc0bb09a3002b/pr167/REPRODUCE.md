# Recovering and checking the PR167 delivery evidence

Read `ARCHIVE.json` for the exact archive SHA-256, Git blob, original file count/byte sum, every member identity and recovery command. Verify the compressed file, extract into a new directory, then verify every member byte count and SHA-256 against that manifest. The archive retains complete source snapshots, reports, raw command outputs, API observations, original failed parser attempts and all successful lightweight checkers. No compiled proof objects or runtime installation is needed for archive verification.

## What was actually executed in this delivery

No Lean compilation, mathematical proof replay or source-generating helper was run. The new work consists of exact Git/connector reads, byte hashing, source/import and script parsing, complete retained-log analysis, local `merge-tree`/`commit-tree` calculations and full-tree preservation comparisons.

The actual parent commands were:

```sh
python /workspace/scratch/c0bb09a3002b/agent15-evidence/pr167/verify_integration.py
python /workspace/scratch/c0bb09a3002b/agent15-evidence/pr167/verify_serialized_stack.py
```

Both completed with exit zero. Their full command arguments, outputs and hashes are in `integration-validation/commands.json` and `serialized-stack/commands.json`; initial bare-repository and raw-source merge-tree commands are in `initial-combination-commands.json`. Successful results contain 147 and 115 checks respectively. The evidence-only specialist and static package checker have their own exact scripts, versions, inputs and execution receipts under `review-reuse/` and `package-audit/`. The first retained-review parser failure is intentionally preserved.

The original scripts record their actual absolute local Git location, `/workspace/scratch/c0bb09a3002b/agent15-integration.git`. To repeat their local tree analysis elsewhere, use a fresh isolated bare repository with the listed public commits and their parent/tree objects available, copy the recovered evidence to a fresh work directory, and change only `GIT_DIR` in a working copy of `verify_integration.py` and the `GIT` argument prefix in a working copy of `verify_serialized_stack.py` to that new repository. Retain the original scripts unchanged as evidence and retain the relocated copies and their outputs separately. Run the source-combination checker before the ordered-stack checker. Do not direct new outputs into the sole recovered original evidence tree.

The ordered stack starts at main `74a1c3922eb7af438fe40b23d2105ad07556e3f5`, then uses published heads 146=`159ed83569f5cc4d058557c2b24b28839552b75a`, 147=`e77289c5f58a3238f53c0f3c6951a73515c5d7d2`, 150=`946c69edf3d2e6a87f5516db1fd0091eae29e663`, 154=`ebcaf723d61f9513c8bae30440d02ba4a46343b4`, 167=`502d3f5ea2e516f7cf4342854e1ec865f188d4f3`. The final conditional tree is `dff6792f554a29dbf41ec8c8146db971206d8a8b`. Local hypothetical commit author metadata is deliberately labelled and deterministic; no source or main ref is written.

The complete Git `ls-tree -r -z` outputs are stored as original binary `.stdout` files. They preserve the NUL path boundaries; do not reinterpret them as line-separated text. Their output hashes are in the command records. Source snapshots in `package-audit/head-delta/` contain every one of the 699 added PR files, while `review-reuse/blobs/` is a content-addressed selection used for the independent-evidence qualification. `head-paths.json` maps that latter selection back to published paths.

## Reusing or independently repeating the original mathematical verification

The qualified existing nonauthor review is COMMENT5555257249 at exact H. Its official Lean 4.19.0 executable SHA-256 is `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, release commit `6caaee842e94`. The original independent replay used fresh project objects, explicit `--trust=0 -j1 -DElab.async=false`, default stack, 8192 MiB and 600 seconds per command. All 42 commands/logs and complete audit evidence are preserved. The original package's `review/README.md` is the authoritative portable replay entry point if a separate new execution is actually needed.

The parent canonical command is reproduced in `PUBLICATION_HANDOFF.md`; its recorded original flags remain separate from the explicit-trust-zero independent run. Historical author generators, preflight/sealing scripts and incremental build helpers have different side effects and reuse old dependency objects. They are retained for provenance and must not be substituted for the documented clean verification entry points. Their source inspection is in the full package report.

Unchanged source and registry identities allow reuse of the existing verified execution. A new run is warranted only for a concrete affected obligation or an independently requested replay, not simply because a delivery owner changes.

## Actual integration remains separate

The prospective Git trees establish a conditional content result on the recorded main. They do not merge prerequisites or PR167, retarget the PR, acquire main ownership, update cumulative publication indexes or certify unknown platform checks. Follow `DELIVERY_PACKET.md` for the exact owner actions and actual target/ordered-parent/tree/postcheck readback that complete delivery.
