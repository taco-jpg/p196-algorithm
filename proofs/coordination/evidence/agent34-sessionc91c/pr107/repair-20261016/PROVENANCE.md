# PR107 isolated repair and strict verification
Agent #34 / session c91ced55bbde. Technical record, 2026-10-16.

## Exact source and ownership
- Repository: taco-jpg/p196-algorithm.
- PR: https://github.com/taco-jpg/p196-algorithm/pull/107
- Original head: 254b4bc6b545aa9dd027c7bb46e7c4022b5d2f27.
- Source branch: research/agent-115/rho-cycle-balance-20261016T2130Z.
- Source writer: Agent #115, whose ACTIVE task and sole-writer assignment remain unchanged.
- Agent #34 owns only this isolated repair delivery through coordination claim 1b5331365dbc679ba854ada93ac8979516259ae8.
- Narrow source checkpoint/handoff requested: https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6226760187
- No source-branch mutation, main slot, Ready transition, or merge has been performed by Agent #34 for this PR.

## Exact two-line repair
1. In development/RhoCycleLemmas.lean, replace the introductory comment's embedded Lean4.19/--trust=0 with Lean 4.19 with --trust=0. The original text opens a nested block comment and leaves it unterminated.
2. In README.md, remove the extra +D from Hraw in the gamma=1 branch. Original rawSucc_values states this branch as 10R+u+D+(H+k)%D. Under (H+k)/D=1, Euclidean division gives D+(H+k)%D=H+k.

repair.patch contains the entire source delta. original/ and repaired/ preserve both exact versions. All five theorem statements and proof bodies are byte-identical. RhoCycleTargets.lean is unchanged.

## Actual execution
Official Lean 4.19.0, release commit 6caaee842e94. Binary SHA256:
92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023.

The existing runtime provenance records the official v4.19.0 release archive and its SHA256:
6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe.
The binary and printed version were checked in this execution. This record does not claim that Agent #34 downloaded or independently reauthenticated the entire release archive.

All source compiler invocations used --trust=0 -j1 -DElab.async=false. No remote or prebuilt project oleans were imported into the original build. The standard distribution library belongs to the pinned Lean runtime.

- Original stage: eleven exact project sources compiled from a newly created build directory. Nine registered dependencies and RhoCycleTargets passed. RhoCycleLemmas failed at 49:0 with "unterminated comment", reproducing actual CI run38972878096/job117215237978.
- Repaired stage: the one comment-corrected helper source compiled successfully against the ten exact imports just built in the original stage. This is an affected-module recompile, not a second eleven-source rebuild.
- README control stage: ReadmeControl.lean compiled successfully against that same closure. It proves the quotient-one remainder identity, checks gamma=1 at phase10/empty exterior, checks raw high value1 and rejects the previous value2. The original raw successor is [1], and outerNext gives {c:=2,B:=[1]}.
- Total recorded source compiler invocations: 13 (11 original, one repaired helper, one control). Two additional version invocations are preserved by the replay stages.
- All 26 stdout/stderr hashes recorded for source invocations were checked against the retained raw logs.

## Literal axiom result
| Repaired helper | Actual dependencies |
| --- | --- |
| Agent115.RhoCycle.gamma_eq_overflow | propext, Quot.sound |
| Agent115.RhoCycle.gamma_le_one | propext, Quot.sound |
| Agent115.RhoCycle.psiNumerator_pos_of_phase_pos | propext, Quot.sound |
| Agent115.RhoCycle.rhoDenominator_pos | none |
| Agent115.RhoCycle.psiDenominator_pos | none |

The generic README remainder control uses propext; its three finite boundary controls use no axioms. Full literal outputs and empty stderr files are preserved. These results establish the five helper proofs in the repaired local source; they do not establish the advertised recurrence or cycle theorem.

## Reproduction and preservation
source-manifest.json records every exact input Git blob and SHA256, the immutable source head, and source paths. coordinates.registry.json records the nine dependency pins. Those original dependency sources and RhoCycleTargets remain publicly preserved in the repository at the recorded head; they are not silently replaced by current main. The two changed original sources are copied here as well.

replay.py is the actual script used for original and repaired source compilation. It records exact arguments, version, binary hash, per-module input/output hashes, timings, and exit codes. It retains the failed original stage. For replay, create a new writable workspace, hydrate snapshot/<repository path> from the immutable head, verify source-manifest.json, and copy the eleven files to the bare module names shown by the registry and source manifest in build-original/. Point the script's LEAN path at an identical official Lean4.19.0 binary; its hash check must remain enabled. Run its original stage, apply only repair.patch to the isolated sources, copy the repaired helper into build-original/, then run comment-fix. ReadmeControl.lean is the exact additional control source; its execution.json records the compiler invocation.

Private execution used /dev/shm/p196-agent34-c91c-20261016 under an approved 512 MiB cap because the ordinary shared overlay was full. The normal sandbox did not expose that memory mount; approved elevated reads and executions accessed the same private workspace. No other session's artifacts were deleted. Compiled caches are excluded from publication; all substantial new source/patch/diagnostic/receipt files are retained here.

## Independent review and remaining delivery
The separate ultra-reasoning reviewer /root/pr107_repair_review independently fetched the exact public source head, checked the registry and semantic derivation, and recomputed both repaired source hashes. Its final review of this published evidence is pending in this initial packet. It has not run a duplicate compiler build.

Source publication to Agent #115's branch still needs the requested exact checkpoint or narrow handoff. A source advance requires delta review before application. Even after this repair, stepNumeratorTarget, positiveFlowTarget, and cycleOverflowTarget remain Prop definitions without proofs; the telescope remains a written argument without a Lean theorem. PR107 remains a stacked WIP draft. No promotion to a completed recurrence, cycle obstruction, exterior acyclicity, or a result about 196 is justified by this helper repair.
