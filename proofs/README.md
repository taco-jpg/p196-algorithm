# Current research entry point

This directory retains the current source selected during the reorganization. A byte-identical historical original is preserved separately for every source version. A historical tree is not the current proof, and a timestamp is not evidence of validity.

[Results directory](RESULTS.md) · [Status](STATUS.md) · [Open problems](OPEN_PROBLEMS.md) · [Source mapping](SOURCE_MAP.json)

Original mainline baseline: `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.

## Verification using the original layout

Existing scripts may depend on the original paths. `replay_original_layout.py` reconstructs that layout in a new temporary directory outside the repository, preferring matching current source from this directory and checking each file's hash without modifying the current working tree.

```sh
python3 proofs/verify_project.py --lean /absolute/path/to/lean --project consolidation-core --output /absolute/new/output/directory
python3 proofs/verify_release.py
```

These commands replay the corresponding checks for the original mainline; they do not claim to cover newly selected source or every historical project. Each other current source must retain its own independent verification commands and dependencies in the migration-check records. The cleanup tool's independent preservation verifier separately checks the entire migrated tree; the old release check is not a substitute.
