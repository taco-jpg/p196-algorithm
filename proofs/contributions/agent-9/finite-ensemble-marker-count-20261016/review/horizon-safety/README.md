# Independent ensemble review

**PASS: semantic review and one fresh complete Lean kernel gate.**

Agent #9/horizon-safety reviewed the five frozen modules authored by Agent #9/coverage_census. All 16 project modules and the generated audit compiled with official Lean 4.19.0 at --trust=0 -j1 -DElab.async=false. The audit checked 100 literal exports, 1,505 theorem constants, and 239 safe definitions. The exact permitted axiom union is propext, Classical.choice, and Quot.sound. No mathematical source change was made.

The result covers every canonical width-L integer with no selected mirrored all-nine block, including trailing zero digits, and yields the finite palindrome-hit count upper bound at positive times 1 through R+1. The semantic review explains the exact formula, full numeric completeness, all requested boundaries, and original-result attribution.

## Evidence

- SEMANTIC_REVIEW.md: complete independent semantic assessment.
- RESULT.json: exact final outcome, counts, source hashes, runtime, attribution, and scope.
- frozen-source/: unchanged snapshots of the five mathematical modules.
- author-snapshot/: author freeze, source statement, pins, audit, and separately attributed author gate metadata.
- verification/source-registry.json and verify.py: independent source registry and replay driver.
- verification/postcheck.json: exact public-export and origin-audit validation.
- runs/full-001/: unchanged raw gate reports, all logs, generated audit, and explicit retention inventory.
- preparation-001/: preserved failed checkpoint lookup before the commit was locally available.
- preparation-002/: successful checkpoint and original-source provenance verification after parent fetched it.
- subreview/: attributed product/word review and the single-example arithmetic command; not a full enumeration.
- packaging-history/: preserved unexecuted draft and the actual packaging-parser failure on a multiline axiom list; no failed Lean gate or mathematical source change.
- REVIEW_FILES.json and SHA256SUMS: inventory of this delivered review packet.

## Compiled origin counts

| Module | Theorems | Safe definitions | Literal new exports |
| --- | ---: | ---: | ---: |
| Agent9FiniteProducts | 29 | 9 | 15 |
| Agent101DigitPairs | 27 | 6 | 0 |
| Agent101MultiplicityBounds | 28 | 8 | 0 |
| Agent101SplitEnumeration | 58 | 14 | 0 |
| Agent9MarkerWords | 45 | 9 | 25 |
| Agent9MarkerEnumeration | 35 | 4 | 21 |
| LychrelDigitSums | 986 | 148 | 0 |
| Lychrel196Research | 0 | 0 | 0 |
| Agent101NumericFibers | 56 | 4 | 0 |
| Agent9NumericMarkerCount | 43 | 7 | 26 |
| SafeDelay | 24 | 12 | 0 |
| DecimalSafeRuns | 42 | 3 | 0 |
| DecimalDelayBridge | 41 | 7 | 0 |
| OverflowSafeRuns | 52 | 3 | 0 |
| FiniteHorizonBlocks | 8 | 2 | 0 |
| Agent9FiniteHorizonCount | 31 | 3 | 13 |

Lychrel196Research is the exact original import-only adapter; it was freshly compiled and is the only origin with no declarations. Generated/private declarations are included in the theorem and safe-definition totals. Unsafe compiler implementation declarations are separately logged and are not mathematical proof axioms.

## Replay

Use a new output directory; the driver intentionally refuses to reuse an existing build tree. Set the repository and review paths to their local locations, then run:

```bash
python3 -B "$REVIEW_PATH"/verify.py \
  --repo "$REPOSITORY_PATH" \
  --package-root "$REVIEW_PATH" \
  --manifest "$REVIEW_PATH"/verification/source-registry.json \
  --lean /tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean \
  --output /workspace/scratch/8dcaf4a67fa4/agent9-ensemble-review/replay-NEW \
  --auditor 'Actual replay reviewer identity'
```

The actual executed command, environment, per-command exit status, elapsed time, and log hash are in runs/full-001/verification.json. The standard Lean runtime is hashed rather than rebuilt from source. This PASS is for the selected project closure, not the entire repository.
