# Independent Width review evidence

Source commit: `8f9249c855418eaadf9bb68bd645948d15777b5b`. Read `semantic-review.md` for exact hypotheses, scope, attribution and execution history. `audit-summary.json` and `final-review-receipt.json` give final counts and identities.

The fresh 30-module build plus complete origin/public audit passed all 31 Lean commands with explicit `--trust=0`. Its original Python wrapper then failed on `admit` inside a documentation comment. The unchanged original driver is `clean-001/replay.py`; all compiled-source snapshots and logs are retained. `clean-001/postcheck-recovery-001/` preserves the failure record, corrected driver, actually executed recovery script, scanner controls, and successful postcheck receipt. Recovery did not execute Lean. The top-level `replay.py` is the corrected portable driver, not the byte-identical original full-build driver.

For a new full replay, choose unused build and evidence paths:

```sh
python3 proofs/contributions/agent-1/periodic-width-projection-20261016/review/replay.py \
  --source-root /path/to/checkout \
  --build-dir /tmp/width-review-fresh-build \
  --evidence-dir /tmp/width-review-fresh-evidence \
  --lean /path/to/lean-4.19.0-linux/bin/lean \
  --memory-mib 8192 \
  --module-timeout-seconds 600
```

Run from the checkout root. The driver copies only pinned source, verifies the official compiler hash, builds in dependency order with a fresh `LEAN_PATH`, and preserves the audit source, logs, every executed command, and driver bytes. It uses default stack size. The corrected scanner tail was tested by the retained recovery; the corrected whole driver has not been executed as a second fresh build in this package. `recover-postcheck.py` is an exact historical recovery script with fixed original paths and must not be mistaken for a portable new-build entry point.

`FILES.json` covers this review's text evidence and excludes itself. The parent's independent canonical evidence is separately copied under `../verification/parent-clean-001/`, preserving its original 63-entry `FILES.json`; its separate 66-entry `PACKAGE-FILES.json` covers the copy and identity receipt. No project compiled objects are packaged. The parent's canonical command flags differ from this specialist's explicit strict flags and are preserved without alteration.
