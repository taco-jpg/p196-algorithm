# Reproduce the scoped PR104 checks

This registry covers seven exact source modules and six public endpoints. The logical root `Agent114ShortRFirst11` maps to the original author path `proofs/contributions/agent-114/short-r-firsthit-20261016/Agent114ShortRFirst11.wip.lean`. The file keeps its historical name and comments; its adopted repaired bytes have SHA-256 `e2557923cdbe694ab4a21463ab765bd0d609623f98e77e5c3aac593ed101bd81` and Git blob `b7ee9c4d16e8477439d343ac18483462599ebf6c`.

## Exact source and scope

The repair was published on the author branch at `945fb3337513d52c52df09cc6b11bde62841a7eb`. Its six dependency pins match inspected main `80b749b314be2588c44be2607862a76eac8ea7e0` and the immutable independent review publication `36f3a58b22c93bef9f6fbc234d9bab8b5ebd43d0`. Every module has its repository path, SHA-256, Git blob and ordered imports in `BUILD_REGISTRY.json`; the logical names are staging names used by the existing verifier.

Under the original canonical digit and finite pair-coefficient hypotheses, the six endpoints give the common first reverse-add value, nonpalindromicity at time zero for `r=1,2,3,4`, and nonpalindromicity at every positive time from 1 through 11 for each of these four parameters. They do not establish the first later palindrome time, a universal 3,000-step Lean theorem, infinite avoidance, or the 196 conjecture. Original finite experiments and earlier WIP/failure labels retain their historical meanings.

## Structural source and import check

Run from an actual Git checkout containing this registry and its pinned files. Use an existing official Lean 4.19.0 release, commit `6caaee842e94`, and a new output directory for every attempt:

```sh
python3 proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/contributions/agent-114/short-r-firsthit-20261016/integration/BUILD_REGISTRY.json \
  --project agent114-short-r-first-eleven \
  --check-only \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/path/to/new-pr104-source-check
```

A successful structural run reports `SOURCE_AND_IMPORT_CHECK_ONLY`, `mathematical_proof_check=false`, and `repository_wide_pass=false`. It verifies exact bytes, imports, the selected root closure and the source-token policy. It queries compiler identity and standard-library availability but does not compile these seven Lean sources or execute a theorem audit. Inspect the retained `verification.json` and `FILES.json`; a zero exit status is not a new Lean proof result.

The unchanged verifier reads the checkout's real `git rev-parse HEAD`. A locally initialized source fixture therefore reports its local synthetic commit, not a remote source or merge commit. The preparation check uses such an explicitly identified fixture; its receipt separately records the real source and base commits above and every staged file hash. That local fixture is not a full main checkout or a combined-tree acceptance result.

## Optional fresh scoped build

To request a new canonical compilation and module-origin theorem audit, use the same command with `--check-only` omitted and another new output directory. The unmodified verifier compiles the selected seven sources with `-j1 -DElab.async=false`, then runs its generated theorem audit. It does **not** add `--trust=0`, does not read an arbitrary registry `compiler_arguments` setting, and does not reproduce the independent reviewer's additional safe-definition audit. Its axiom allowlist is exactly `propext`, `Classical.choice`, `Quot.sound`.

No such new proof build is claimed by this registry or its preparation check. Existing independent evidence already provides a fresh seven-module build with explicit `--trust=0`, a complete 1,523-theorem and 171-safe-definition audit, and literal types/axioms for all six public endpoints.

## Retained independent evidence

The independent reviewer did not author Agent #1's isolated repair. The report is an attributed same-session technical review relayed through a shared account, not a separate platform-account approval.

- Formal review: https://github.com/taco-jpg/p196-algorithm/pull/104#pullrequestreview-5554297272
- Immutable evidence commit: `36f3a58b22c93bef9f6fbc234d9bab8b5ebd43d0`
- Package: `proofs/contributions/agent-1/pr104-review-20261016/`
- Exact pins: `repair-review/source-pins.json`
- Review: `repair-review/REVIEW.md`
- Commands and outcome: `repair-review/clean-001/report.json`
- Literal six types and axiom sets: `repair-review/public-types-and-axioms.txt`
- Preserved original failure: `REVIEW.md` and `clean-001/`

Retain all original failures, statements, sources and manifests. Reconcile any later source change with these exact pins and rerun only the verification obligations that the change actually affects.
