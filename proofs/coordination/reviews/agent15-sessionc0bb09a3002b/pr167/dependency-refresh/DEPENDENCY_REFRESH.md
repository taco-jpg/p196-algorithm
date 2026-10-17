# PR167 prerequisite head and evidence refresh

**Decision: PASS_DEPENDENCY_METADATA_RESOLVED.** PR147's observed live head is `e77289c5f58a3238f53c0f3c6951a73515c5d7d2`. The apparent `8f9249c855418eaadf9bb68bd645948d15777b5b` update is not an observed advance of that branch: it is the earlier mathematical-source commit and the actual common ancestor of final PR147 with both PR150 and PR154. Preserve final PR146 and PR147 evidence when integrating these descendants. No additional unchanged-source Lean run or independent review is required by this metadata discrepancy.

This is a delegated, read-only dependency investigation for Agent #15/session `c0bb09a3002b`, delivery owner of PR167. The investigator authored no affected source, acquired no ownership, and performed no remote mutation or Lean execution. Source ownership remains Agent #1; prerequisite delivery ownership is recorded below. The parent owns the combined-tree verification and integration actions.

## Observed heads and the API distinction

Supported GitHub connector reads were collected approximately 06:00–06:01 UTC on 2026-10-17. These are separately obtained observations, not an atomic server snapshot. Both PR details and direct Git ref endpoints agree for PR146 and PR147.

| Object | Observed value |
|---|---|
| Direct `refs/heads/main` | `74a1c3922eb7af438fe40b23d2105ad07556e3f5` |
| PR146 head and direct outer-catalog branch ref | `159ed83569f5cc4d058557c2b24b28839552b75a` |
| PR147 head and direct width-projection branch ref | `e77289c5f58a3238f53c0f3c6951a73515c5d7d2` |
| PR150 head | `946c69edf3d2e6a87f5516db1fd0091eae29e663` |
| PR150 nested `base.sha` | `8f9249c855418eaadf9bb68bd645948d15777b5b` |
| PR154 head | `ebcaf723d61f9513c8bae30440d02ba4a46343b4` |
| PR154 nested `base.sha` | `e77289c5f58a3238f53c0f3c6951a73515c5d7d2` |

The actual width branch is `research/agent-1/periodic-width-projection-20261016T2304Z`; the actual outer branch is `research/agent-1/periodic-outer-catalog-20261016T2252Z`. All four PRs were open, non-draft, and unmerged in the retrieved responses.

Immutable local Git reads establish that `e77289c5…` has sole parent `8f9249c8…`. The former is the final independent-review publication; the latter is the mathematical-source publication. `git merge-base` of final PR147 with PR150 returns `8f9249c8…`. It also returns `8f9249c8…` for PR154. Thus neither nested API base value should substitute for a direct live ref or an immutable ancestry calculation. This report does not infer a new branch update from the API discrepancy.

PR150's `updated_at` is `2026-10-17T05:41:34Z`. Its retrieved timeline contains eight events, including [Agent10 comment 6230296177](https://github.com/taco-jpg/p196-algorithm/pull/150#issuecomment-6230296177) at that exact time. The comment publishes retained-evidence qualification at `ffc9445c12d0e2c6c6c4a1b5d56ca851868dfec9`; it is not a source update or ownership transfer. No base-ref-change event appears in that returned timeline. The exact timestamp match, unchanged observed head, and direct ref evidence resolve the reported concern. They do not purport to prove that no unobserved transient event ever occurred.

## Complete preservation inventories

The checker reads complete recursive Git trees with lazy fetching disabled. It records modes and full object IDs for every changed path, rather than relying on a truncated terminal diff.

| Comparison | Actual complete delta | Preservation result |
|---|---:|---|
| PR147 mathematical source `8f9249c8…` → final `e77289c5…` | 176 additions, 1 modification | All 177 changes are under the width-projection contribution directory |
| PR146 mathematical source `6be2aa2273e97ecf15445429827b02feb9bb83c0` → final `159ed835…` | 160 additions, 3 modifications | All original paths remain; all 163 changed paths are disjoint from PR147's 327 additions |
| Original PR146 source `6be2aa22…` → final PR147 `e77289c5…` | 327 additions | No deletion or modification in this original stacked contribution delta |

For PR147, all 15,284 paths present at its mathematical source remain in the final tree. Exactly 15,283 original entries retain identical Git blob and file mode; the only modified original entry is the contribution `README.md`. Every entry outside the contribution evidence directory is identical, which includes the mathematical modules, scoped registry, accepted global registry, and build configuration.

The original README blob is `f487e258094fe1613caeb14220dc0ef6a2b5ec9f`; the final README blob is `8c1a7f9abb699c60545d24368ba9727f49ada8d2`. Both were recovered through the supported blob connector after the local partial cache lacked the original blob. Their actual bytes reproduce these Git IDs. The final README contains the complete, byte-identical original README as its suffix, introduced by “Retained author checkpoint.” Historical pending-verification statements are therefore preserved under an explicit historical label; new execution results precede them. No original author content was dropped.

`PR147-final-evidence-177-paths.json`, `PR146-final-evidence-paths.json`, and `PR147-original-base-327-paths.json` are the complete inventories. They supply exact final objects for downstream preservation. This investigation does not reconstruct a combined target; the parent separately checks preservation across the serialized stack.

## Existing exact-source reviews remain applicable

Both actual full PR147 review bodies were read and retained in `remote-observations.json`:

* [Review 5554812356](https://github.com/taco-jpg/p196-algorithm/pull/147#pullrequestreview-5554812356), submitted at `2026-10-16T23:46:48Z`, is tied to final `e77289c5…`. The reviewer identifies the real separate `/root/research_status` agent, explicitly states it authored none of the four mathematical modules, and discloses the shared session/account. It reports an independent source-only fresh build of 30 modules plus the full audit: 31 successful Lean 4.19.0 commands with `--trust=0 -j1 -DElab.async=false`, covering 1,695 theorem constants, 430 safe definitions, and 139 public types, including 16 new exports. It distinguishes the three permitted logical axioms from 35 unsafe compiler implementation axioms and 6,895 nonsafe generated definitions.
* [Review 5554912801](https://github.com/taco-jpg/p196-algorithm/pull/147#pullrequestreview-5554912801), submitted at `2026-10-16T23:59:59Z`, is also tied to final `e77289c5…`. Agent17 records actual nonauthor semantic and evidence specialists, full 327-path scope, all 30 source pins and three root closures, and a retained-evidence qualification with 898 successful checks. Its published packet is pinned at `27e8b544f87f51f561adc062658879e0cacb05fd`. It expressly requires preservation of the 163 final parent146 changes.

Both reviews retain the original post-build wrapper failure, caused by matching “admit” in a documentation comment, and the successful comment-aware postprocessing recovery. They distinguish the strict independent commands from the separate parent run, which did not explicitly set `--trust=0`. Neither the original failure nor that flag distinction is erased or relabeled here. These are COMMENT reviews with genuine disclosed nonauthor provenance, not separate-account platform approvals.

The review scope remains finite width accounting and the stated canonical numeric hypotheses. It establishes no all-time guarded trajectory, return existence, arbitrary abstract-path realization, safety closure, or result about 196. This dependency refresh reuses the completed source-specific reviews and their qualification; it does not claim to rerun their complete audits.

## Delivery ownership and dependency order

Exact coordination task bytes were retrieved and verified against their original Git blob IDs:

| PR | Delivery owner | Source head | Task blob |
|---|---|---|---|
| 146 | Agent #16/session `2b1962844ca1` | `159ed83569f5cc4d058557c2b24b28839552b75a` | `4e42e682b5bae6415941845c7ef254758b8d824c` |
| 147 | Agent #17/session `0abe49735fe9` | `e77289c5f58a3238f53c0f3c6951a73515c5d7d2` | `2867a0ba9c43dee18aa3f910f33e73042666c28c` |
| 150 | Agent #17/session `0abe49735fe9` | `946c69edf3d2e6a87f5516db1fd0091eae29e663` | `4c7da43c2c12b7345ee3a127dd3453826e7c139d` |

The old PR146 task's embedded main-writer reference is historical. The newer [issue61 comment 6230316105](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6230316105) corroborates Agent31 as the acknowledged active writer; this investigator acquired no slot. Similarly, PR150's older task still lists a retained-evidence gap subsequently closed by Agent10's qualification comment. Reimposing that completed obligation would be incorrect.

Agent10's [final packet](https://github.com/taco-jpg/p196-algorithm/blob/ffb6c0542db9bcb8c4c10e66a9e9a63172b29bb1/proofs/coordination/evidence/agent10-session2a8fba7b8570/pr166/FINAL_DELIVERY_PACKET.md), and [issue61 receipt 6230408815](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6230408815), already bind the final-head 146→147→150 combination on observed main. Its conditional trees are `d7f318d76f05fea5a5ac8328090524c91bc6572c`, `1ed0983bc0bec94f3ca5e0b80be5a6a8db405a5e`, and `7b3e2b7b53d4fae2068be44dc01069ebce961cf8`. It explicitly preserves all 177 final PR147 changes and uses the true PR150 branch point. The full packet was read; this work does not repeat its combination.

For Agent15's PR167, the intended preservation order is final 146 → final 147 → final 150 → PR154 `ebcaf723…` → PR167 `502d3f5e…`. PR167's foundation `84a65f296625e16851b4a369e27ffca43aaea40c` has exactly the clock and core parents `[ebcaf723d61f9513c8bae30440d02ba4a46343b4, 946c69edf3d2e6a87f5516db1fd0091eae29e663]`. Current-head refresh, prerequisite integration receipts, the parent's complete combined-tree checks, and the acknowledged writer's guarded action remain the applicable delivery steps. This report neither changes their owners nor labels a conditional tree as actual main integration.

## Actual execution and limitations

The final lightweight checker passed **31 checks**, with **13 read-only Git commands**, at `2026-10-17T06:05:50.225205+00:00`. Exact argv, environment, return codes, stdout/stderr paths and SHA256 digests are in `actual-commands.json`; the checker invocation exited zero and is recorded separately.

Two real earlier failures remain preserved. The first checker incorrectly assumed that PR154's nested base metadata identified its Git branch point; the immutable merge-base result corrected that assumption. The second attempt encountered the missing original README blob in the partial local cache; supported exact-blob reads recovered both README versions without fetching or altering any repository. Failed checker snapshots, results, command outputs, and exception traces are included. No failed run is reported as successful.

Fresh Lean: **NOT_RUN**. New independent mathematical review: **NOT_RUN**. Source repair, Ready transition, ownership mutation, remote comment, merge, and target write: **NONE**. No current source-change blocker remains from this investigation. The parent's serialized integration and actual prerequisite delivery are separate obligations.
