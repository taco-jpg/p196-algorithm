# Multipart transport and recovery

The logical archive `pr132-verification-evidence.tar.gz` is stored losslessly as 36 ordered binary files in `archive-parts/`. Each part's path, offset, byte size, SHA-256 and Git blob is listed in MULTIPART.json. The whole archive is 1151309 bytes with SHA-256 `236b1fb05d910109964fa4316f1f970d166568764ea9a4270ee95411db0c0409`.

The whole-blob connector invocation was interrupted after675.8s without a response; the expected blob was absent at subsequent reads. No automatic approval denial was returned. Bounded part creation uses the same ordinary authorized connector and every returned SHA matches the original bytes. This is a transport adaptation, not a mathematical or evidence-content change.

After downloading this directory, run these commands in it with Python3 and an unused restoration destination:

```bash
cat archive-parts/part-*.bin > pr132-verification-evidence.tar.gz
python3 restore_and_verify.py PACKAGE_MANIFEST.json pr132-verification-evidence.tar.gz restored-evidence
```

The exact inspected script interface is manifest, archive, destination. Before extraction the script requires the compressed size and SHA-256 above; it then verifies all289 files,51directories and4653910 original payload bytes against the complete per-file manifest. The part concatenation was independently compared byte-for-byte with the already restored and verified original archive. RECOVERY.md retains the original single-archive instructions and expected identities. REPORT.md is the original completed evidence-validation report, unchanged.

All original research bytes, validation scripts, raw success/failure logs and retrieval records remain in the archive. Packaging metadata, scripts and logs are also published beside it. Fresh Lean remains NOT_RUN in Agent20's delivery. The staged full-archive Git blob is not claimed created; after reconstruction its computed Git identity is77e9f43a5370608f2a0bdaac9fb07175b1b7a24e.
