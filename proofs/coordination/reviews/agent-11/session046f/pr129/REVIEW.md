# PR 129 integration review

**Verdict: PASS for the stated finite/conditional results, using independently validated retained exact-source Lean evidence. No substantive mathematical blocker found. Fresh Lean execution by this reviewer: NOT_RUN.**

Reviewer: Agent #11 `/root/review129`, session `046f9285a650`. This reviewer authored no mathematical source and made no Git/main/remote writes. Reviewed head: `c74c9d1ca1fef5463738abac348a5d12eaab4a01`; mathematical source: `c75036b527dc4faa98ec1f1de5d85338749b9c96`.

The normal Lean application launch is unavailable in this session; escalation was already automatically rejected. I neither retried nor bypassed that restriction. Historical execution belongs to Agent #1's `research_status` reviewer and original parent verifier, not to this reviewer. The acceptance basis is source review, independent validation of their complete exact-source commands/logs/exit codes/axiom outputs, and newly executed Python checks.

## Dependency and integration scope

| Stage | Exact head |
| --- | --- |
| PR 87, repeated-block normalization | `0431e0a64da285455421d8a267a92c37dffbfee7` |
| PR 95, raw period-four guard | `95a17ceeaba51b7d2c14645401df5159a3d483d1` |
| PR 111, maximal stripping and quotient | `bf4ff749000a6995e1755e37b59988ef362bae16` |
| PR 122, original validity preservation | `ae4e1f09a0bb75f1fa9a0eebabcefd0c362fc72a` |
| PR 129, safety test and boundaries | `c74c9d1ca1fef5463738abac348a5d12eaab4a01` |

Order: **87 → 95 → 111 → 122 → 129**. Against stipulated main `1ee9123344dbe17e9bda224ff8af5b1cbb2b64e4`, the actual merge base is PR 95's head: the full diff is eight commits and 452 added files. It includes PR 111 and PR 122; it is not exclusively new safety work. Relative to PR 122, PR 129 adds three commits and 166 files, including four mathematical modules and its registry. All changes are additions.

The combined tree must contain the exact 21-module closure pinned in `Agent1PeriodicSafety.registry.json`, with roots `Agent1PeriodicSafetyNumeric` and `Agent1PeriodicSafetyBoundary`. All 17 inherited modules equal PR 122 byte-for-byte. At stipulated main, eleven closure modules already match and ten are absent: the three quotient modules, three validity modules and four safety modules. Reconcile against the current integration tree, retain all prerequisite evidence, and verify every closure pin again after composition. No changed dependency or altered theorem is authorized by this verdict. A fresh combined Lean run remains NOT_RUN here; the reviewed historical build already compiles these exact 21 source files together. Live PR mergeability metadata alone is not the integration verdict.

## Findings and evidence

The 16 new public theorem statements and their proof chains preserve the original semantics. `safePeriodic` is exactly the stored alphabet/head test. Positive repetition and a nonempty period connect it to the complement of original `FoldedDecimal.BadWord`; maximal whole-period stripping preserves that test even with empty residuals. The quotient equality compares the stripped **target** with the raw **target**, never with its predecessor.

The numeric corollary retains original `DecimalDigits.Canonical` and every in-range `columnSum` equality. It classifies `Lychrel196.step n`, supplies no realization witness, and claims nothing about repeated safety or 196. `ValidPeriodic`, `BadWord`, the arithmetic criterion, normalization, and pair operations are unchanged. The prerequisite transition requires `k ≥ 3` and only establishes successor exponent `≥ 1`.

The exact boundary theorems are sound: empty B/H with four tens is valid and safe but its quotient `([1,2,2,2], [2], [2,2,2,2])` is unsafe; B=[1], H=[] and four eighteens is valid and safe while its exponent-zero word is BadWord. The concrete normalization and quotient equations use kernel reduction/ordinary `decide`, without native evaluation shortcuts.

New checks passed: 2,707 retained-evidence/source checks, 38 supplementary checks, and the inspected original Python diagnostic's 48 positive-exponent comparisons, ten stripping controls, and both fixed boundaries. Diagnostic content exactly matches the historical result except Python version. Historical independent execution records contain all 21 module builds plus the audit, explicit `--trust=0 -j1 -DElab.async=false`, and zero exits; all log hashes match. The complete audit covers 1,396 theorem constants and all 94 named Agent1 exports (16 new, 78 prerequisites), with only `propext`, `Classical.choice`, and `Quot.sound`. The logical `safePeriodic` definition is axiom-free. No source-level `sorry`, `admit`, `sorryAx`, custom axiom, `native_decide`, extern/unsafe shortcut or kernel bypass occurs in the pinned closure.

The original canonical verifier separately passed the exact closure; its command record omits explicit `--trust=0`, so it is not mislabeled as the explicit-trust independent run. Its dirty-tree flag is retained, and its registry plus all mathematical source snapshots match published bytes. Existing compiler helper inventories are distinguished from proof dependencies; a new general safe-definition census was not imposed as an acceptance gate.

All 436 entries of the three stacked EVIDENCE inventories, their complete coverage, and 113 parent FILES entries validate. Original failed proof attempts, the overstrict compiler-helper audit, and the original failed inventory classification remain outside the accepted proof chain. This review's first parser incorrectly handled wrapped axiom lists; its failed source/output are retained, and the comma/whitespace correction passes without mathematical edits.

Complete new evidence is in `publish-evidence/`; exact published source/log duplicates have SHA-256, Git blob, byte-count and recovery mappings in `duplicate-recovery.json`. Detailed semantic notes and the publication inventory accompany the review. Root owns publication and any formal PR COMMENT.
