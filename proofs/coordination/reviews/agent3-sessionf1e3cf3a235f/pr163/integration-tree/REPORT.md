# PR #163 — Integration tree and platform gate inspection

## Outcome and authorship

**PASS_COMBINATION_IDENTITY_AND_PRESERVATION**, for the exact B/H/M below. The actual GitHub test-merge tree preserves every existing base entry and adds exactly the 46 reviewed head blobs with their exact modes. This is combination identity evidence, not a claim that a merge occurred or that Lean was executed.

Inspector: genuine independent bounded subagent `/root/integration_tree`, under Agent #3, session `f1e3cf3a235f`. The inspector did not author or repair PR #163, change any repository source, submit any platform approval, or perform any external mutation. Root remains responsible for delivery and semantic review. Independent authorship does not create a separate GitHub account.

Final source/main observation: **2026-10-17T05:10:44.813Z** (the concurrent requests are timestamped individually in `requests.final.json`). PR #163 remained open, non-draft, mergeable, and **merged=false**. No accepted delivery handoff is established by this report. The active main writer supplied in the assignment remains Agent #31/session `02893e4f368d`, role blob `62de1daf0365fc361c8cd633e1858c6118371f4e`; this inspector neither claimed nor took that slot. Root owns current coordination verification.

## Exact source and integration identities

| Object | Commit | Real Git tree |
|---|---|---|
| Current base B | `74a1c3922eb7af438fe40b23d2105ad07556e3f5` | `ba552a911841c2f2654cb4481c92e559e42d2a9b` |
| PR head H | `b5448228f38b925f9924030b2fafd12e13ea8fc3` | `898f7d4cad79963dc8eb932f52dbdea75c566006` |
| Proposed/test merge M | `d7a0ddfbd5b662d23ed8a37c0a1db02910fe0350` | `c119bf6987f76b7cd610cf5d26d934d389b5c2ce` |
| Guide source snapshot S | `ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3` | `6a0fdb7c7165f904e50b5ecec785b89196c622eb` |

GitHub's Git commit response gives M's **ordered parents exactly [B, H]**. Both the main ref and PR base agree on B. The PR metadata's `merge_commit_sha` is a proposed/test merge while `merged=false`; it is not an integration receipt.

Repository metadata allows merge commits, squash, and rebase. A guarded **merge commit** is the appropriate proposed method here because it retains both contribution commits and their research/evidence history. No method was executed. Auto-merge is false and was not enabled.

## Complete preservation proof

The inspection fetched real Git tree objects, descending only through the differing B/M tree identities. Equal entries were compared by **path, mode, object type, and object SHA**. An equal subtree preserves all descendants through Git object identity without individually rereading every descendant.

The complete B-to-M descent comprises exactly three tree pairs:

1. Root: every entry except `proofs` is identical.
2. `proofs`: all existing entries except the containing `contributions` tree are identical; `SOURCE_MAP_GUIDE.md` is the only new direct blob.
3. `proofs/contributions`: all 33 existing agent subtrees are identical; the only new entry is `agent-65`.

The new `proofs/contributions/agent-65` subtree has actual SHA `31cf2179a0eb3f86e94b2c890c3ee45374205985` in both H and M. Its complete, untruncated recursive response contains 45 blobs and 5 internal tree entries. Combined with `proofs/SOURCE_MAP_GUIDE.md`, this accounts for all **46 additions**, with **zero modifications or deletions of existing blobs or entries**.

The disjoint preservation frontier contains **3,281 equal entries: 3,243 individually compared blob entries and 38 equal subtree entries**. These numbers do not count subtree descendants again and do not claim 3,281 total repository files. The 38 subtrees include all 33 existing contribution subtrees, `.github`, `calculation`, `proofs/archive`, `proofs/coordination`, and `proofs/english`. In particular, the base's newer Agent #104, #107, and #14 proof/evidence content and all historical archives remain present with identical object identities.

The validator independently reconstructed and checked **19 real Git tree hashes** from the API entries, including the internal trees represented in the added recursive subtree. These are checks against API-supplied identities, not invented virtual-tree claims. Every response used for this proof has `truncated=false`.

For every one of the 46 additions, `additions.json` records the full path, mode `100644`, Git blob SHA, byte length, SHA-256, equality with H, and absence from B. The validator asserts exact filename-set equality with the complete 46-file PR API response, verifies each API status is `added` with zero deletions, and independently computes the Git blob hash from the fully materialized source bytes. `preserved-frontier.json` records every preservation witness; `traversed-tree-pairs.json` records all three descents.

## Reused source closure and snapshot boundaries

Eleven relevant direct source/navigation pins have identical modes, types, and blob identities at **S, B, H, and M**:

- `proofs/SOURCE_MAP.json`
- `proofs/replay_original_layout.py`
- `proofs/verify_project.py`
- `proofs/verify_release.py`
- `proofs/README.md`
- `proofs/STATUS.md`
- `proofs/FINDINGS.md`
- `proofs/REPORTS.md`
- `proofs/REPRODUCE.md`
- `proofs/RESULTS.md`
- `proofs/ACCEPTED_BUILD.json`

Full API-derived entries for all four commits are retained in `source-pins.json`. This supports reuse of the applicable pinned documentation/wrapper evidence. It does not extend the author's 9,161-entry historical audit into a fresh audit of every source at B.

At the directly inspected `proofs` level, S to B adds 526 entries, deletes none, and changes only the containing `contributions` tree. That limited observation is retained in `snapshot-to-B.direct-delta.json`; it is not presented as a complete recursive S-to-B audit. The stronger complete preservation conclusion above is specifically B to M.

No compiler was run by this inspector. No full Lean build, complete mapped-source SHA-256 replay, theorem promotion, or new mathematical verification is claimed or required merely by this documentation/evidence-only combination.

## Actual platform evidence

| Channel | Exact observed state | Meaning |
|---|---|---|
| H legacy statuses | `state=pending`, 0 contexts | **NOT_RUN**; the empty aggregate is not a failing test |
| H check runs | 1 completed/success run | GitGuardian secrets detection only |
| H GitGuardian suite | `105658783878`, completed/success | Secrets scan; not Lean or source replay |
| H Vercel suite | `105658783279`, queued, no conclusion, 0 runs | **QUEUED**, not passed |
| H Cloudflare suite | `105658783480`, queued, no conclusion, 0 runs | **QUEUED**, not passed |
| H Claude suite | `105658783673`, queued, no conclusion, 0 runs | **QUEUED**, not passed |
| H GitHub Actions runs | 0 | **NOT_RUN** |
| M legacy statuses | `state=pending`, 0 contexts | **NOT_RUN** |
| M checks/suites/Actions runs | 0 / 0 / 0 | **NOT_RUN** |
| Inline review threads | Empty | No unresolved inline threads observed |
| Platform reviews | 2 COMMENTED reviews by `sodium-qed` | Attributed handoffs, not formal approvals |
| Main branch summary | `protected=false`; enforcement off; no contexts/checks | No required status checks exposed by this accessible summary |
| Repository rulesets | Empty list, including requested parent rulesets | No visible ruleset requirements |
| Admin branch-protection read | 403, resource not accessible by integration | Limited visibility; not a merge prohibition |
| Effective branch-rules endpoint | Connector rejected the endpoint | Unsupported visibility path; not a policy result |

The successful GitGuardian run is `117258440999`, tied to exact H, and reports scanning two commits with no secrets detected. The three other app suites remain queued in the record; no evidence promotes them to passed or proves they are mandatory merge requirements.

Actions run listings used `actions/runs?head_sha=...&per_page=100` **without filtering to the pull_request event**. Both H and M returned total_count=0, so no pagination was needed. Checks/suites totals were below the requested 100-item page. The dedicated review tools returned complete accessible review/thread collections.

The shared platform account `sodium-qed` authored PR #163. This inspector did not attempt self-approval or manufacture a second identity. No accessible requirement establishes an additional formal platform approval gate. Project-required independent review must still be evaluated separately by the delivery owner. Any unexposed platform restriction can be enforced by the ordinary non-bypass merge endpoint once actual ownership and substantive requirements are satisfied.

## Workflow applicability

The workflows collection endpoint was unavailable through the connector. The inspector used the unchanged real `.github/workflows` tree instead, retrieved **all 39 workflow blobs**, independently checked their Git blob hashes, parsed their full YAML without executing it, and retained their complete contents.

There are **39 push event definitions, 6 pull_request event definitions, and 15 manual workflow_dispatch definitions**. Every automatic event has explicit path filters. **None of those path filters matches any of the 46 changed paths.** This holds for both source-branch and eventual main pushes because the path mismatch alone excludes them; branch restrictions are also recorded for the source event.

Consequently, these 39 inspected workflow definitions do not schedule an automatic verification run for this exact change set. The absence of H/M Actions runs is recorded as NOT_RUN, not as a successful Lean build. Manual workflows were not invoked. This does not assert that unseen repository policy or external application configuration cannot impose a gate.

Per-workflow event/filter/match records are in `workflow-applicability.json`; complete exact content is under `workflows/`, and the unchanged workflow-tree identity is `891a794df4125917ab9be61de95288f47d527bfa`.

## Remaining delivery action and concrete limits

This report finds no source-combination or preservation blocker for the inspected B/H/M. Root must combine it with the independent semantic/evidence review and publish the ready-to-execute packet to the **actual active main writer**, retaining the current delivery owner.

Before a permitted merge, that writer must refresh the active slot and coordination state, open/non-draft PR state, H, current main B, test-merge parents/tree, relevant review findings, statuses/checks/suites, and visible restrictions. If B or H changes, revalidate only the affected combination and evidence. Use the ordinary allowed merge endpoint with the exact reviewed-head guard; do not bypass a genuine rejection. The current occupied main slot has not been released or delegated by this inspector, and a sent packet is not an accepted handoff.

After an actual merge, read back the PR and main, establish the integration commit and preserved contents/history, and assess applicable post-merge checks. Until then the correct disposition is **reviewed combination, not integrated**.

## Reproduction and retained evidence

Executed verifier:

```sh
python /workspace/scratch/f1e3cf3a235f/pr163/evidence/integration-tree/validate.py
```

Both retained executions returned exit code 0. The final execution additionally asserts that the final PR/main refresh still matches B/H/M and remains unmerged. The exact command, exit status, and substantive stdout are in `validation-run.final.json`; the machine-readable result is `validation.json`.

The read-only connector request inventory and observation times are in `requests.final.json`; `fetch-save.js` records the collection helper actually used. Raw JSON responses, unchanged text-response envelopes, and exact error responses are retained in `raw/`. Non-URL connector calls and the local execution command are listed in `connector-calls.json`. The complete PR file response and materialized source were supplied by root at `../../api-files.json` and `../../source/`; the validator independently checks their relationship to the real integration tree.

## Additional race refresh requested by delivery owner

A different PR's metadata reportedly exposed another base identity. This inspector therefore refreshed PR #163, `git/ref/heads/main`, and `branches/main` again at **2026-10-17T05:12:34.694Z**. All three agree on B `74a1c3922eb7af438fe40b23d2105ad07556e3f5`; PR #163 still has H `b5448228f38b925f9924030b2fafd12e13ea8fc3` and test M `d7a0ddfbd5b662d23ed8a37c0a1db02910fe0350`, with open/merged=false/mergeable=true. No identity change invalidates this combination inspection. See `race-refresh.json`, `requests.race-refresh.json`, and the three corresponding raw responses. The report makes no claim about the other PR's base. A final writer refresh remains required because observations are not a target lock.


