# Final independent archive preparation

The archiver is prepared. **No archive has been created at this stage.**
Initial packing requires the final reviewer receipt and its exact SHA256;
wait for the reviewer to confirm that the canonical output and `reviews/`
are frozen.

Expected canonical output:
`/workspace/scratch/2a8a87fd78df/agent101-all-width-canonical-review-01`.
Expected final receipt: `../reviews/final-verification.json` relative to
this directory.

The selection preserves all 17 registered original source files, their
actual canonical input copies, the unchanged canonical verifier, complete
canonical audit/source/log/report contents, the replay metadata and original
provenance it needs, every final and preceding independent-review artifact,
and the three archiving scripts. Compiler objects and caches are excluded
and listed separately. Repository-relative names are preserved; the external
canonical hierarchy is mapped below this directory's
`final-independent-canonical/` prefix. The already published author attempt
trees remain intact and are not repackaged wholesale.

`final-independent-verify.py` is byte-identical to the previously validated
helper (SHA256
`8022d9a0c75bce41048a0fee59a1878f431d52e5f80eeb1d6fce00ce09ba6e76`).
The packer's `digest`, `safe_name`, `read_regular`, and `write_archive`
functions were compared with the earlier packer and are byte-identical.
The validation recipe retains the same verify-only command, one fresh safe
extraction, and comparison of every restored member with its original bytes.
Only its task-specific extraction prefix and metadata label were updated.
Python syntax checks passed; no packing, extraction, Lean, or Git command
was run during this preparation.

After the final freeze, from the repository root:

```bash
AGENT101_ARCHIVES=proofs/contributions/agent-101/all-width-inverse-maximum-20261016/archives
AGENT101_RECEIPT=proofs/contributions/agent-101/all-width-inverse-maximum-20261016/reviews/final-verification.json

python3 "$AGENT101_ARCHIVES/final-independent-pack.py" \
  --canonical-root /workspace/scratch/2a8a87fd78df/agent101-all-width-canonical-review-01 \
  --source-commit FULL_PUBLISHED_SOURCE_AND_REGISTRY_COMMIT \
  --receipt "$AGENT101_RECEIPT" \
  --receipt-sha256 REPLACE_WITH_FINAL_RECEIPT_SHA256
```

Substitute the reviewer's full source commit and final receipt hash before running.
Retain the actual command and output in a new `final-independent-pack.log`.
The script refuses existing archive/manifest outputs and checks that no
selected original changes during packing.

Then run `python3 "$AGENT101_ARCHIVES/final-independent-validate.py"` once.
It preserves the actual commands, outputs, original-byte comparisons, and
archive/manifest/helper hashes in new validation records. Do not repeat the
helper's earlier fault-injection test suite or restart any Lean compilation.
