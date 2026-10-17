# Independent ReturnCore review

Frozen mathematical source: `a0ae20330cbc1da2a98dc5721228d6590f8ba6da`. The exact 38-module import closure and source/blob identities are in `final-source-identity.json`; the independent reconstruction and comment-aware source scan are in `preflight.json`. Read `semantic-review.md` for the precise mathematical contracts, affiliation and execution status.

The fresh build driver is `replay.py`. Its exact executed bytes, all 38 compiled source snapshots, the generated complete-origin audit source, command records, compiler identity and full logs are retained under `clean-001/`. Project compiled objects are not evidence-package contents. The initial run is independent of the authors' pinned-object increments and the parent's separate canonical fresh run.

For a new full replay from the checkout root, choose unused output directories:

```sh
python3 proofs/contributions/agent-1/periodic-return-core-20261016/review/replay.py \
  --source-root /path/to/checkout \
  --build-dir /tmp/return-core-fresh-build \
  --evidence-dir /tmp/return-core-fresh-evidence \
  --lean /path/to/lean-4.19.0-linux/bin/lean \
  --memory-mib 8192 \
  --module-timeout-seconds 600
```

Every command uses explicit `--trust=0 -j1 -DElab.async=false`, default stack, the stated address-space limit and timeout, and a fresh project-only `LEAN_PATH`. The compiler executable hash is checked. The source scanner masks comments/strings before rejecting forbidden code tokens; this run uses the corrected scanner from the outset. The full logical audit checks actual module origins, all theorem and safe-definition dependencies, and all 163 named Agent1 public theorem types (14 new + 149 prior). Nonsafe compiler implementations are inventoried separately and never accepted as theorem dependencies.

The completed first fresh run passed all 39 Lean commands and wrapper checks: 1,942 actual-origin theorem constants, 566 safe definitions/opaques, and 163 named public theorem interfaces. `audit-summary.json` records exact per-module counts and the separate compiler implementation inventory. `final-review-receipt.json` pins the result and report. There were no failed attempts in this independent run; the separate author attempt histories remain in their original directories.

`FILES.json` covers the completed review text evidence, excluding itself. The parent's separate canonical evidence is preserved under `../verification/parent-clean-001/`, with its original 79-entry `FILES.json` and a separate 82-entry `PACKAGE-FILES.json`. The parent executed that run; the specialist copied and checked its identities. Its original metadata and command flags are preserved, including actual `source_tree_clean: true` and the absence of an explicit `--trust=0` argument in its canonical commands.
