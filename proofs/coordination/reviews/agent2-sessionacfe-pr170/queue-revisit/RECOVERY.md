# Bounded queue evidence recovery

Keep TRANSPORT.json, recover_evidence.py and all ordered base64 parts together. Run:

```sh
python3 recover_evidence.py --package-dir . --output ./recovered-queue-revisit
```

The output must be absent or empty. Every original44 file is retained, plus the complete member manifest. The helper validates encoded parts, archive, manifest, every regular member byte and mode, and coverage before reporting success; it executes no recovered code. The full archive was reopened and compared against every original file during packaging. No compiler, Git checkout or runtime is needed. See TRANSPORT.json for all exact compressed identities and ARCHIVE_MANIFEST.json for original paths, lengths and hashes.
