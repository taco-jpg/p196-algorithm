Independent PR #99 integration review — Agent #11 session046f9285a650 /root/review99

Verdict: PASS for independent source, semantics, provenance, and retained-evidence validation. Fresh Lean execution in this review is NOT_RUN: the candidate runtime failed ordinary `--version` preflight with exit 1, `error: failed to locate application`. No escalation or alternate execution bypass was attempted. This review does not claim a newly executed Lean kernel check.

Merge recommendation: approve the exact head using the explicitly reused, fully pinned independent trust-zero evidence, subject to the integration writer's final base freshness and compatibility gate. No mathematical source correction or substantive evidence blocker was found. If policy requires another newly executed Lean build rather than the authorized reuse, that additional execution remains blocked and must not be reported as passed.

| Identity | Exact value |
|---|---|
| PR head H | `d81784d62b399775982084a54313b6df1695b2c4` |
| Initial integration base B | `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5` |
| Merge base | `4b4edf976b2c7a9ba1dad80636c0e21c66350325` |
| Root-provided clean combined tree | `fe65cf5b1219fdd9bdd1f77d1c43c0cb53adc019` |
| Reviewed PR diff | All 20 added files; 2305 text insertions; one 122200-byte evidence archive |
| Review independence | New independent reviewer agent; existing GitHub login does not imply a separate human or external peer review |

I read AGENTS.md and proofs/PUBLICATION_POLICY.md, the complete new mathematical and audit sources, all changed readable documentation and checkers, source registries, and required arithmetic definitions and bridge proofs. Machine inspection covered every archive manifest entry and every retained theorem/definition audit row. The direct B..H comparison includes unrelated main changes; the reviewed contribution is merge-base..H, with combined-tree checks reported separately.

The theorem states, for every natural n with `0<n` and every natural B,s,N, that at least `N/(sharpDigitSumEscapeBound B+1)` distinct times in `[s,s+N)` have `B < digitSum(orbit n t)`. Division is natural division. The generic predicate is explicitly decidable; the complete-block proof uses exact adjacent interval additivity, one witness per disjoint block, induction, and monotonicity for the final remainder. `List.range'` has step one, so the filtered length counts distinct times. The existing escape witness is inclusive at `a+F(B)`; length `F(B)+1` converts it to the correct strict right endpoint. No ceiling-count claim is made for a short remainder.

All quantifiers and boundary cases are correct. At B=0, F(0)=0, so the denominator is 1 and every iterate of a positive seed has positive digit sum. N=0 yields zero on both sides; s=0 is included. Positivity is necessary: n=0 remains zero and falsifies the proposed premise-free bound already at B=0,s=0,N=1. The 196 corollary discharges positivity with ordinary kernel `decide`.

The imported arithmetic is the original ordinary decimal reverse-and-add: `step n = n + reverse10 n`, `orbit n 0 = n`, successor iteration never stops at palindromes, and digitSum uses the decimal mod/div recursion. `canonical_exists`, `canonical_admissible`, padded profile validity, exact profile iteration, and `mass_numeric_iter = 2*digitSum(orbit n t)` instantiate the numerical bridge without an unsupplied actual-orbit premise. `orbit_positive` and `orbit_add` justify shifting to every start s. The original manuscript section 6 and its exact tree/blob provenance support the finite block argument.

The safe interpretation is a uniform finite lower count of excursions above each fixed threshold. The contribution has no real density-limit endpoint, pointwise divergence claim, eventual permanent threshold avoidance, palindrome-avoidance conclusion, infinite safe seed, or proof of the 196 conjecture. Audit declaration counts are metadata, not independent major-result counts.

The independent Python audit executed here validates all 142 archive members byte-for-byte, archive size and compressed/uncompressed SHA-256, the author manifest's 43 entries, the complete review manifest's 95 entries, and the full-closure manifest's 84 entries. Eleven selected source modules are exactly the registered transitive closure, including all nine unchanged original dependencies. Each registered source agrees with its retained build snapshot, SHA-256, Git blob and historical source. All 20 changed files and the selected dependencies/checker/registry match the combined tree; the nine dependency blobs also match B. The original manuscript blob was absent from the partial object cache; its commit/path tree identity was read and matched to the recomputed blob hash of the preserved manuscript. That initially failed direct blob read is retained separately.

Reused Lean evidence is attributed to Agent #9/horizon-safety, independently of the coverage-census proof author. Its recorded run used Lean 4.19.0, commit 6caaee842e94, an initially new output tree with zero project objects, LEAN_PATH restricted to that new build directory, and `--trust=0 -j1 -DElab.async=false` for all eleven project modules and the generated audit. All recorded command exit codes are zero, and all substantive command log hashes match. The current verifier and registry exactly match the recorded hashes; regenerating its audit source produces exactly the retained audit bytes. This is evidence reuse, not execution by this reviewer.

The retained audit enumerates constants by actual originating module, including private/generated theorems, and traverses transitive axioms for all theorem and safe definition/opaque declarations. It rejects safe custom axioms even if unused. I validated 1451 unique theorem rows and 178 unique safe-definition rows, including all eight new public declarations (seven user-written theorems and intervalCount). Their total axiom union is exactly `propext`, `Classical.choice`, `Quot.sound`. The new generic theorem family uses propext/Quot.sound; numerical corollaries additionally use Classical.choice. The log separately exposes 16 unsafe implementation axiom constants and 806 unsafe implementation definitions, none appearing in accepted theorem/safe-definition axiom sets. The accepted closure's source scan found no sorry/admit/sorryAx/custom axiom/native_decide/ofReduceBool/skipKernelTC or user-written unsafe/partial/compiler-trusted replacement.

The rejected numeric boundary review attempt remains a failure: exit 1, an unsolved zero-seed goal, and sorryAx in that failed review-only declaration. It is excluded from accepted chains. The subsequent exact corrected boundary source has exit 0 and only the permitted standard axioms. Both source/log/result identities are verified and retained at H.

Runtime identity is limited precisely: the candidate executable's SHA-256 equals the earlier build's `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. All eight recorded runtime files match the prior hashes: executable, Init/Std/Lean root oleans, and four top-level shared libraries. The standard library was not rebuilt and neither the old record nor this check authenticates every transitive standard-library object. The fresh preflight failed despite byte identity.

| Important evidence | SHA-256 |
|---|---|
| Generic module | `597bfe85a6d5ee332aeaf96845e2dc7c96631080ec3a9c5c6c97f3ce17247ff9` |
| Numeric module | `0747bb708957e9d3ab8a2f9afbe5e7222a3ca3daedccc2796d644831d9d7dad4` |
| Public audit module | `37b98536e7ae0ea520ce20df9ad47a42727625710c72e132180d14b818f011cd` |
| Closure verifier | `7a2ecc9c3e40a99091a61919caf0be5bb71b2423b1cb820d944420786e63674c` |
| Closure registry | `4a14ae70d84ad0c4452073c0fe15360a7fa5a2645adfd6373d0d5ee7606dce6e` |
| Retained closure verification.json | `cdcebfbe79ac1b9e0447a58ab8e9c52c02f3c83770b20b168445e0e64f325cbb` |
| Retained exhaustive audit log | `8b04ae2ea0eba0f0f6696bbfc625cabcf850b0b1ed77372e96b03e6c69782be4` |
| Original evidence archive at H | `dff13c841c7fc263a483a3422ed1755fabfc1c031a939ff109894b2f859fe806` |

Actual local commands include `python3 -B validate_retained_evidence.py` (exit 0), `git rev-parse <commit>:<path>` and read-only Git source comparisons, archive decompression/hash validation, and the failed absolute `lean --version` command preserved in runtime-preflight/receipt.json. Exact historical Lean command arrays and LEAN_PATH are preserved in retained-evidence-validation.json, with their original executor attribution. No new project oleans were imported or produced here. No source proof edits, remote writes, merges, or nested delegation were performed.

Publishable new evidence is in publish-evidence/. The existing 142-file original archive is referenced immutably at H rather than duplicated in that package. Newly produced scripts, Python validation outputs, actual runtime failure logs, source/combined-tree identity receipt, archive validation, and failed manuscript-read record are included. Root owns publication, latest-base reconciliation, and merging; no source/main integration slot is held by this reviewer.
