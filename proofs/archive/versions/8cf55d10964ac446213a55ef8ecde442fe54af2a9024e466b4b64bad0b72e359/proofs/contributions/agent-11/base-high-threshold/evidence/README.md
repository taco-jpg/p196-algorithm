# Retained development and verification evidence

This directory preserves all 15 locally recorded proof-development snapshots and their complete logs, plus 24 baseline, local clean-build and CI audit files: 54 original research files. No substantive saved attempt or recorded audit within the five-module checkpoint is omitted. Compiler distributions, compiled objects, copied source build directories and transport helpers are reproducible infrastructure and are not included.

The exact accepted five-module source checkpoint is `42a165aac1028d261dd4b1bd245c2e169748ff39`. The original research source snapshot is `74df59c5ecb6cb30fb3c88b1d5b26fdb9526d6c4`. Historical attempts are lossless line deltas against those exact accepted source bytes, each checked by its original SHA-256. Logs and audit outputs are retained as exact UTF-8 text, not summaries. This compression is not an additional mathematical certificate.

Run from the contribution directory:

```sh
python3 restore_evidence.py
python3 restore_evidence.py --out /new/restored-evidence-directory
```

The optional output directory must not already exist. Restoration verifies both archive hashes, the immutable source bases, every development source hash, every audit-file hash, safe unique relative paths and expected file counts. It emits an index of original paths, byte counts and SHA-256 digests. Agent 11 restored all 54 files and compared every restored byte with the original saved files successfully before publication.

Archive SHA-256:

- `development-records.json.xz`: `160a71416aa089e2a013ad08c36cebe8d0cf5d41337348c662dedb65b179376e` (4200 bytes).
- `audit-records.json.xz`: `76fa57c48f71738a91d9eb64c5e4ebebdc3157d2a14951963d60b8d9ad04b2f2` (7016 bytes).

The audit archive retains the actual downloaded CI reports for run `38687784317`, artifact `11949824177`, at source commit `42a165aac1028d261dd4b1bd245c2e169748ff39`. The original CI ZIP SHA-256 is `7e7c3fa19e70745bc4b3f3d0f045a844cdb87c8330d5d834dca33f1664e40fdd`; both fresh CI builds reported PASS for all 122 theorems and 32 definitions, including unchanged prerequisite declarations. The two earlier four-module local audits are labeled separately from the later five-module audits. They are not evidence for the subsequently added first-hit theorem.

Replaying `restore_evidence.py` verifies historical preservation only. Replaying `check.py` performs a new Lean build. Neither a direct self-review nor a CI build is represented as independent semantic review. Independent review and default-branch integration remain separate gates. Across these modules three original source targets are covered; 40 newly compiled supporting theorem declarations are not counted as 40 independent source results.
