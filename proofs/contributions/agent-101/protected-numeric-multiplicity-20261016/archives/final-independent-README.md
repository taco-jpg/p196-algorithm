# Final independent evidence archive

`final-independent.tar.gz` preserves the final independent verification of source commit `71691d50497edc83247b3571af276bb0ee438491`. It contains **142 regular files**, totaling **1,941,455 original file bytes**, in a **352,620-byte** archive. Original local files remain present and unchanged.

Archive SHA256:

```text
31347b5afacef968f6eb9ecdac2985612a9457a7ad5400d84b2bcb9c3a455332
```

Manifest SHA256:

```text
e7eca667f6472c081d37a88f8200e24ecc5dd91ea10520e0820cbe65c93a9e02
```

## Contents and paths

| Group | Files | Preserved contents |
| --- | ---: | --- |
| Published source inputs | 26 | Original source bytes at the registered repository-relative paths |
| Published replay inputs | 2 | The exact registry and unchanged canonical verifier |
| Actual canonical source directory | 28 | 26 actual module inputs, generated ProjectAudit, and the separate FinalPublicAudit |
| Canonical logs | 27 | Every original module-build log and the original ProjectAudit log, including empty logs |
| Canonical reports | 2 | Original `verification.json` and `FILES.json` |
| Final independent reviews | 43 | Existing `reviews/final-*` receipts, audit sources, complete audit output, semantic review, scripts, and retained build-log copies |
| Nonpalindromic counting review | 14 | Six `counts-nonpalindromic-*` records, the two reviewed source snapshots and compile logs, and the preceding count/palindrome receipts and semantic reports |
| **Total** | **142** | All member contents preserved byte for byte |

Every repository file retains its original repository-relative name. The canonical build originally lived outside the repository at:

```text
/workspace/scratch/2a8a87fd78df/agent101-final-family-independent-71691d5
```

That directory's relative hierarchy is preserved below this repository-relative archive prefix:

```text
proofs/contributions/agent-101/protected-numeric-multiplicity-20261016/archives/final-independent-canonical/
```

`final-independent-manifest.json` records each member's path, byte count, SHA256, group, and original location. It explicitly records the canonical path mapping. The complete original published `Lychrel196Research` source and the different generated canonical facade are both retained under their respective paths. No receipt or historical absolute path was rewritten.

The archive omits all 26 canonical `.olean` files and includes no `.ilean`, Python bytecode, or cache contents. The original `FILES.json` remains unchanged, so its historical object-file entries remain visible even though those compiler objects are excluded from this evidence archive.

The previously archived `runtime-development` and `generic-verification` member paths were compared with the new member set; the intersection is empty. Their archives are not embedded here, and their old development/evaluation trees are not repackaged. To preserve this final complete closure, its current source snapshots and original published inputs remain present even where dependency bytes also occur in an older snapshot. The two prior archive identities and manifest hashes are recorded in the new manifest.

## Default verification

Run from any working directory:

```bash
python3 /path/to/archives/final-independent-verify.py
```

With no options, the helper only verifies `final-independent.tar.gz` against `final-independent-manifest.json` beside the script. It checks the entire archive hash and size, the complete member set, and every member's size and SHA256. It does not write extracted files.

Alternate archive and manifest paths are supported explicitly:

```bash
python3 /path/to/archives/final-independent-verify.py \
  --archive /path/to/final-independent.tar.gz \
  --manifest /path/to/final-independent-manifest.json
```

## Safe restoration

To restore into an empty directory or an existing repository root:

```bash
python3 /path/to/archives/final-independent-verify.py \
  --extract-to /path/to/restore-root
```

The helper validates the whole archive before writing, rejects duplicate or unexpected member names, path traversal, links, non-regular members, and symlink ancestors. It checks every destination first, skips byte-identical existing files, and refuses different existing files. New files use exclusive creation; existing files cannot be overwritten. No Lean or Git command is invoked.

The helper is copied from the already reviewed `verify-runtime-development.py`. **Only two default filename literals changed**, to this archive and manifest. The verification and extraction logic is otherwise byte-identical. The packaging script checks this exact relationship. The original helper SHA256 is `685156a3d48ba59d01153d3a5a145ac018048c8fe1e1d356fb072d7e6353e1e6`; this adapted helper SHA256 is `8022d9a0c75bce41048a0fee59a1878f431d52e5f80eeb1d6fce00ce09ba6e76`.

## Packaging and reproduction

`final-independent-pack.py` is the exact packaging recipe. Initial packaging reads the frozen repository inputs and original canonical output. It refuses to overwrite an existing archive or manifest and checks source identities and original-file preservation.

Tar members are sorted. Every member is a regular file with mode `0644`, zero uid/gid/mtime, and blank owner/group names. The gzip filename is empty, its mtime is zero, and compression level is nine. These rules remove host file metadata from the archive bytes while preserving every file's content and logical path.

After restoration, the recipe can reproduce the exact recorded archive from the extracted member set without needing the original absolute source locations:

```bash
python3 /path/to/archives/final-independent-pack.py \
  --repack-from-root /path/to/restore-root \
  --manifest /path/to/archives/final-independent-manifest.json \
  --output-dir /path/to/new-output-directory
```

The output directory must not already contain `final-independent.tar.gz`. Repacking uses the manifest's fixed member list, checks every restored input, and checks the resulting archive SHA256 against the original. Bit-for-bit recompression uses the same Python/gzip compression behavior; any mismatch is reported and its output retained. No additional repack test was run during this archival task: validation was limited to the requested member verification and one safe extraction.

## Actual validation

`final-independent-validate.py` ran the default verify-only command, then one fresh safe extraction. Every restored member was independently compared with its original file bytes and manifest hash. The extracted file set matched the 142 manifest members exactly. The originals and both sidecar helper hashes remained unchanged.

Results: **PASS**, with **142/142 members verified and restored byte-identically**. The fresh extraction directory was `/tmp/agent101-final-independent-restore-_5542lpp`. The exact commands, complete outputs, and each comparison are retained in `final-independent-validation.json` and `final-independent-validation.log`. The initial packaging output is retained in `final-independent-pack.log`.

No Lean compilation, Git write, or new mathematical proof was performed. The previously reviewed helper's nine test cases were not repeated. This archive preserves the existing mathematical verification classification: one fresh canonical 26-module build whose original verifier commands did not explicitly pass `--trust=0`, followed by explicit-trust-zero audits of all 1,783 module-origin theorems and all 94 selected new public declarations. The independent semantic review's authorship disclosures and finite-horizon/completeness limits remain unchanged.
