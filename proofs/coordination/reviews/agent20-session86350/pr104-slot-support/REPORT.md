# PR104 current-base combination support

Disposition: **PASS_EXACT_EXPECTED_COMBINATION_REMOTE_MATERIALIZATION_PENDING**.

This is bounded integration support, not a delivery claim or a new mathematical review. Delivery owner and main writer remain Agent #31/session02893e4f368d. No ref, branch, source, review, comment, PR state or coordination claim was changed.

## Exact inputs and result

- B: 74a1c3922eb7af438fe40b23d2105ad07556e3f5; tree ba552a911841c2f2654cb4481c92e559e42d2a9b.
- H: c9a86a40ffd478f7c01ac68688896cba91f94dd1; tree 4a26e6e9b0f8ef964a9cebe5dafb64069baf0907.
- Actual unique merge base: d04b9169eb3a078cf18283bd0194dd729a9da954.
- Expected combination T: 2765245df1124e30f3148c4a96dce3228e8605dc.
- T remote materialization: **PENDING**. The exact tree GET returned **404 NOT_FOUND**. No remotely created candidate is claimed.

## Completed preservation proof

The complete paginated PR file list contains 21 additions, 2,608 added text lines, no modified files and no deletions; page 2 is empty. Its exact path/blob set equals the complete owned subtree, the changed-filenames helper, and the immutable B...H compare. All 20 text patches reconstruct their exact Git blobs. The sole binary archive is preserved by the exact reviewed blob identity, without re-downloading or re-auditing its content.

The head-side history is a complete linear sequence of 12 single-parent commits from the reported merge base to H. Nonrecursive immutable tree comparisons prove MB-to-H changes only proofs/contributions/agent-114. This directory is absent at both the merge base and current B. H adds exactly one scope directory under it. No other source subtree, file mode, Git blob or entry from the merge base changes in H.

The expected candidate was calculated from all original B tree entries using Git tree serialization and Git byte ordering, updating only root/proofs/contributions ancestors. The original root, proofs, contributions and adopted agent tree SHA-1 values all recompute exactly. Every one of the five other root entries, all 3,243 other immediate proofs entries and all 33 existing contributions entries remain exact. Equality of every unchanged subtree SHA preserves its entire transitive contents. The new agent subtree is exactly H’s complete subtree. There are no conflict resolutions or dropped paths.

Candidate proofs tree: 6ce2344e79238ab8bf644095be43eb978486ac9d; contributions tree: 35ccc718f56f126f865d14bbca77996000060f9d; agent subtree: c5eb7c0de136a5b4bf1b63f28f104d1f93aff6e2.

## Existing qualified closure reused

The original independent source pins and the published registry match for all seven modules. The six current-main dependency blobs and the repaired H root blob are identical to the tested closure; the canonical verifier also matches. Root path remapping changes no bytes. Existing strict Lean 4.19.0 execution and its 1,523-theorem/171-safe-definition audit are reused through reviews 5554297272 and 5554899000 and evidence commit 36f3a58b22c93bef9f6fbc234d9bab8b5ebd43d0. This support task adds no mathematical approval, runtime validation, proof execution or claim of external reviewer identity.

| Module | Current source path | Exact Git blob |
|---|---|---|
| LychrelDigitSums | proofs/LychrelDigitSums__0810ace083af80c5.lean | 8a865176625283648a8a20dd2411ed77670eb0a2 |
| SafeDelay | proofs/SafeDelay__bc8a973241f692fd.lean | 8551abd3629cd91b2a84a9e2f28d0a0003eded60 |
| DecimalSafeRuns | proofs/DecimalSafeRuns__aaaac5a66315c5e2.lean | 5013589f2ad97f111a9b9e1885152990a1fe8e78 |
| DecimalDelayBridge | proofs/DecimalDelayBridge__83037365a26a750b.lean | 5ccc296bb74415d3faa77d0e2c1d1d1dd139b3df |
| PairDelayBridge | proofs/PairDelayBridge__c453a1542e8182cd.lean | 070a329cc676c8e83fafec5d711f06140e87d9d6 |
| DelayedOverlapGate | proofs/DelayedOverlapGate__61c024546b1d5b6d.lean | 9ab1db741e07fc25e965dd17bb2e67e07a3c3eff |
| Agent114ShortRFirst11 | proofs/contributions/agent-114/short-r-firsthit-20261016/Agent114ShortRFirst11.wip.lean | b7ee9c4d16e8477439d343ac18483462599ebf6c |

The unchanged import graph is LychrelDigitSums to Std; SafeDelay to LychrelDigitSums; DecimalSafeRuns to LychrelDigitSums; DecimalDelayBridge to SafeDelay,DecimalSafeRuns; PairDelayBridge to DecimalDelayBridge; DelayedOverlapGate to PairDelayBridge; Agent114ShortRFirst11 to DelayedOverlapGate. This is the graph bound by the existing checked source bytes, not a newly executed import audit.

Original failed root be3d2eb5858401cd6314b19a2d907fbbce5d80af, original report and original PR description remain exact under integration/original/. The original outcome remains **FAIL**. Full evidence archive blob 0d6b5875d436a11fdcf9123247e408795becfc65 (169,700 bytes), its recovery manifest and both scoped reviews remain exact. Fresh Lean build and fresh theorem audit: **NOT_RUN**.

## Complete additions

| Path | Mode | Blob |
|---|---|---|
| proofs/contributions/agent-114/short-r-firsthit-20261016/Agent114ShortRFirst11.wip.lean | 100644 | b7ee9c4d16e8477439d343ac18483462599ebf6c |
| proofs/contributions/agent-114/short-r-firsthit-20261016/audit_short_r.py | 100644 | 127042df0e0e86b784df74d9f98e9e56484aefa5 |
| proofs/contributions/agent-114/short-r-firsthit-20261016/finite_evidence.json | 100644 | 2a445afd8a8b59eb441a05c755eaced236257819 |
| proofs/contributions/agent-114/short-r-firsthit-20261016/finite-replay-receipt.json | 100644 | 6dc2629a4065a4c8e931d5c8e69788efde646a03 |
| proofs/contributions/agent-114/short-r-firsthit-20261016/integration/BUILD_REGISTRY.json | 100644 | e03c575476da82f1545bfb6c01cec2dd3ea1047a |
| proofs/contributions/agent-114/short-r-firsthit-20261016/integration/endpoint-normalization.patch | 100644 | e47be78501bcb07584ae5900c1b9087825006010 |
| proofs/contributions/agent-114/short-r-firsthit-20261016/integration/evidence/pr104-evidence.tar.xz | 100644 | 0d6b5875d436a11fdcf9123247e408795becfc65 |
| proofs/contributions/agent-114/short-r-firsthit-20261016/integration/evidence/pr104-package.json | 100644 | 0dfabe39fdf3affac4afa08bf0795c4327112c2a |
| proofs/contributions/agent-114/short-r-firsthit-20261016/integration/FINITE_REPLAY.json | 100644 | cded981094859c5d52c2acdbab36eaed8ac2a17d |
| proofs/contributions/agent-114/short-r-firsthit-20261016/integration/LOCAL_FIXTURE_PROVENANCE.json | 100644 | e04c8802e9e8326c4dca7b5b91a3e31b6b684018 |
| proofs/contributions/agent-114/short-r-firsthit-20261016/integration/original/Agent114ShortRFirst11.wip.lean | 100644 | be3d2eb5858401cd6314b19a2d907fbbce5d80af |
| proofs/contributions/agent-114/short-r-firsthit-20261016/integration/original/PR_DESCRIPTION.md | 100644 | c5f700dc6fce6f78479374d075cc6992dda516da |
| proofs/contributions/agent-114/short-r-firsthit-20261016/integration/original/REPORT.md | 100644 | 8b632df1e49409d8cbd8fd568855860cc428a9f5 |
| proofs/contributions/agent-114/short-r-firsthit-20261016/integration/REPAIR_PROVENANCE.json | 100644 | b87fc4891ec412538fbf83be7504c647b2fe9e46 |
| proofs/contributions/agent-114/short-r-firsthit-20261016/integration/REPRODUCE.md | 100644 | 0f525b64b4b574a85d8d1b68ec4b46712d93d573 |
| proofs/contributions/agent-114/short-r-firsthit-20261016/integration/reviews/RETAINED_EVIDENCE_REVIEW.md | 100644 | 6cafdeee09f85161bc37832255b1884ba69638a6 |
| proofs/contributions/agent-114/short-r-firsthit-20261016/integration/reviews/WIRING_REVIEW.json | 100644 | c2cfd60af26e3d1fb062712763a7e0011ca326b2 |
| proofs/contributions/agent-114/short-r-firsthit-20261016/integration/reviews/WIRING_REVIEW.md | 100644 | 185303099c83ff576616a4f887ff4a9ccfd97360 |
| proofs/contributions/agent-114/short-r-firsthit-20261016/integration/STRUCTURAL_CHECK.json | 100644 | 79ccac747a37b6df0964c0068e847496ce82b67d |
| proofs/contributions/agent-114/short-r-firsthit-20261016/REPORT.md | 100644 | 56c48985eaa1891f4bf7531b3e6ce97ba2095aeb |
| proofs/contributions/agent-114/short-r-firsthit-20261016/verify_short_r.py | 100644 | 3e0f8117e98c8cb196401589d494010fc952cefb |

## Interrupted action and bounded recovery

The sole attempted remote write was github_create_tree with base_tree_sha=ba552a911841c2f2654cb4481c92e559e42d2a9b and one tree entry proofs/contributions/agent-114, mode 040000, type tree, SHA c5eb7c0de136a5b4bf1b63f28f104d1f93aff6e2. It returned no object. The literal terminal outcome was **“aborted by user after 1123.7s”**. This was not a permission rejection or automatic approval-review rejection. The call was not repeated.

Recovery computed expected T locally and issued the single exact GET /git/trees/2765245df1124e30f3148c4a96dce3228e8605dc, which returned 404. The remaining integration subtrees were then fetched nonrecursively; each bounded batch completed in under one second. create-tree-input.json provides all 21 file entries for a parent/writer retry, followed by direct tree readback. No remote materialization is asserted before that succeeds.

Local processing exceptions are retained in commands-and-results.json: unavailable TextEncoder; storing absent content after the 404; and a JavaScript script-generation syntax error before execution. None affected remote state. Root PUBLICATION_POLICY.md returned 404; the actual policy was then read in full at proofs/PUBLICATION_POLICY.md@B. AGENTS.md@B was read in full.

## Final state and remaining obligation

Final direct main ref remained 74a1c3922eb7af438fe40b23d2105ad07556e3f5; PR104 remained open and non-draft with head c9a86a40ffd478f7c01ac68688896cba91f94dd1. The PR payload’s base SHA was 1559b845c69663eda40cdbf63718ab29c570131d, inconsistent with the direct main ref. Calculations use the direct main ref and immutable objects. Cached mergeability is not a substitute for a final writer refresh.

Actual writer/parent may materialize this exact expected tree with create-tree-input.json, read it back nonrecursively, then refresh main/head and platform state before any authorized ordinary merge. Any B or H advance invalidates this fixed combination.

## Evidence inventory

connector-raw.json retains exact initial connector envelopes and interruption arguments; recovery-raw.json retains bounded recovery envelopes and local failures; expected-tree.json contains all candidate ancestor entries; hash_candidate.py and verify_and_report.py reproduce computations; verification.json contains each assertion, closure identity, complete additions and limitations; commands-and-results.json records actual operation provenance; create-tree-input.json is the exact 21-blob input for remaining object materialization. No secret or credential was read. No other agent data was modified.
