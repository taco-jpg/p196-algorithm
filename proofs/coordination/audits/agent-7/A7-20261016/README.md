# Agent #7 — integrated PR79 scope correction

This revision applies the reviewed affine-width reporting correction to `proofs/contributions/agent-318/candidate-10k-minus26/REPORT.md`. The first mismatches 15/8/5 belong to explicitly sampled widths; no width-independent nonlinearity or eventual-affinity conclusion follows. Agent #452 identified the correction; Agents #431 和 #11 independently corroborated it. Agent #7 retained that attribution, rebased the exact patch, 和 performed the user-requested integration.

The full original report is retained at `proofs/archive/integration-repairs/agent-7/pr79-09271f108816-REPORT.md`, Git blob `0370c44913a8864e0f6b2dcfeb60b40d4f59b9b2`. The applied proposal has SHA-256 `e2dbfe48037bbbedbc0f5d8cb212ac7e6fba4ed45729375f7c83a8a7fd83931a`; a final note distinguishes its historical proposal status from this revision. Executable research sources, numerical coefficients, finite-search bounds, 和 proof classifications are unchanged.

## Complete retained evidence

The four binary parts reconstruct one 32,648-byte xz-compressed tar with 39 regular-file members. `original-audit/` preserves all 31 original bundle files byte-for-byte, including the complete report, scripts, logs, failed-patch record, exact rebased patch, source inventory, evidence ledger, CI receipts, local audit patch, 和 original manifest. `integration-replay/` contains seven fresh numerical result/log/receipt files. `EVIDENCE_CONTENTS.json` records lengths 和 SHA-256 hashes for those 38 members. No original log was overwritten or silently upgraded.

`INTEGRATION.json` records source identities, per-part checksums, the ownership sequence, actual local checks, 和 limitations. Agent #6’s prior STATUS.md integration is retained as parent `28358aef8fdfa145c5da3232cee891d08dbe51a6`. The rejected initial ownership update caused no write; Agent #7 acquired the explicitly released slot before integration.

## Recovery 和 replay

Run from this directory, extracting outside the repository:

```sh
set -eu
work=$(mktemp -d)
cat evidence.tar.xz.001 evidence.tar.xz.002 evidence.tar.xz.003 evidence.tar.xz.004 > "$work/evidence.tar.xz"
printf '%s  %s\n' 7c6a34db5050400f93e9dc1cbef794cd2a5894b9fccaa70c10c14a13bd6d6df1 "$work/evidence.tar.xz" | sha256sum --check
mkdir "$work/decoded"
tar -xJf "$work/evidence.tar.xz" -C "$work/decoded"
cd "$work/decoded/original-audit"
sha256sum --check MANIFEST.sha256
python3 run_all_checks.py
```

The disposable replay may write new local outputs. The numerical programs passed again at 17:53:58–17:54:10 UTC on 16 October 2026. Their optional cache-dependent patch checks are explicitly marked skipped; separate exact patch application, reversal, restoration, archival identity, 和 final whitespace checks passed. No fresh Lean build or repository-wide verification is claimed. Historical `original-audit/REPORT.md` statements that integration was pending describe the earlier checkpoint; this entry point records the subsequent correction.

Agent #7
