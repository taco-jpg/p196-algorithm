# Recover and verify the independent review evidence

This package contains the completed Agent #6 runtime specialist's independent review of the exact normalized-carry/accounting source published at `affa037ad537f3ae66a97008991850ce397f613a`. It is a lossless archive of evidence file bytes. The Lean runtime and compiled project objects are excluded; no new Lean execution occurred during packaging.

## Verify the stored package

Keep `portable-evidence.tar.gz`, `PORTABLE_MANIFEST.json`, `verify_package.py`, and the readable report copies in the same directory. Compare the archive and manifest hashes to the separately supplied publication handoff, then run:

```sh
python3 verify_package.py
```

This reads every archive member and checks its complete byte count, SHA256, and Git blob SHA1 against the manifest. It also checks the complete member inventory and the byte-identical readable copies. It neither extracts files nor runs Lean.

## Recover the original file bytes

From a directory containing the archive:

```sh
tar -xzf portable-evidence.tar.gz
```

All included evidence appears under `normalized-carry-review/`, with original relative paths preserved. To check the extracted bytes as well as the stored archive:

```sh
python3 verify_package.py --check-extracted .
```

The manifest records every original absolute path, relative path, archive member name, original file byte count, SHA256, Git blob SHA1, mode, and modification time. It also records every excluded compiled file's original byte count and hashes. Archive ownership and timestamps are normalized; all included file bytes and modes are preserved. `evidence-package/` itself is omitted from the archive selection to prevent recursive inclusion.

## Entry points and scope

The readable `REVIEW_RESULT.json`, `FORMAL_REVIEW.md`, `verification.json`, `binding.json`, and accepted `SEMANTIC_REVIEW.md` are exact copies of the corresponding archived originals. `binding.json` is the accepted composite binding after the documentation-only scope correction. The original binding, superseded semantic draft, and correction receipt remain under `final/publication/` and `final/semantic-history/`.

The archive retains the 21-module exact source closure, frozen registry and dependency documents, complete compiler and audit logs, full multiline axiom receipts, module-origin records, original and adapted reviewer scripts, their patch, author failures, publication readbacks, inherited provenance, and runtime recovery provenance. All numerical controls stated as established results in the accepted review are among the seven kernel-checked controls. Superseded planning and draft text retain their original unexecuted status.

The historical runtime receipt describes the initial recovery of Lean 4.19.0 and an earlier repository snapshot; the current source identity is established by `final/publication/binding-affa037-final.json`. Original commands retain the absolute paths used in the actual run. The evidence archive does not claim that those unchanged commands can run from a different filesystem layout without restoring or adapting their recorded paths and supplying the pinned runtime. No compiled objects or runtime binaries are needed to inspect and verify the evidence bytes.

The final mathematical review is PASS: all 21 modules were compiled freshly with Lean 4.19.0 and `--trust=0 -j1 -DElab.async=false`; all 16 new public theorem receipts and the full 712-theorem/261-safe-definition audit passed. Counts describe verification coverage. The separate parent canonical replay is attributed to the parent in `REVIEW_RESULT.json`.
