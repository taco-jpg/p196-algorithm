# PR153 delivery evidence recovery

This separate package preserves the requested delivery records following the primary evidence publication at commit `bc956c407be75566fe815beced3b7d1d14985f62` in `taco-jpg/p196-algorithm`. It is packaging evidence, not a new proof review, Lean execution, merge receipt, or main-writer claim.

## Contents and preservation

The archive contains all 20 files in `pr153-delivery-watch/` (19 raw readbacks and their manifest), the exact `DELIVERY_ACTIONS.json`, `FORMAL_REVIEW.md`, and `verify_remote_publication.py` from `pr153-publication/`, and the primary remote-publication readback report plus both verifier output streams from `pr153-remote-readback/`. Every member is regular and retained byte for byte, including the empty stderr stream. The delivery actions snapshot records its own timestamp; later status/task/comment receipts belong to separate records.

`PAYLOAD_MANIFEST.json` lists every archive member with size, SHA-256 and Git blob SHA-1. `EXCLUSIONS.json` lists every excluded remote-readback duplicate with the same identities and a recovery operation at the immutable primary publication. Those 14 published files and one decoded archive are the only exclusions within the scoped remote-readback directory. No source file was deleted or modified. The initial seven primary packaging files, root documents, coordination status and task were not changed by this packaging work.

`CONTENT_SCREENING.json` records the credential/private-prompt pattern and URL checks. Public GitHub pagination/reference parameters, avatar versions, GitGuardian marketing attribution parameters and GitHub URI templates are retained. No credential pattern or signed transient download URL was found. These specific checks do not imply universal secret detection.

## Verify and recover without network access

Keep the package files together. Python 3 with its standard `lzma` library is sufficient; no Lean, repository checkout, external dependency, credential or network request is used by the recovery verifier.

```bash
python3 verify_delivery.py --package .
python3 verify_delivery.py --package . --extract recovered-delivery
```

The optional extraction target must not already exist. The verifier first checks every inventoried packaging artifact, decodes the wrapped Base64 strictly, compares its archive identity, and checks all member names/order/regular type/metadata/size/SHA-256/Git blob IDs against the complete manifest. It then creates only verified regular files under the fresh destination and reads each back. If the raw `delivery-evidence.tar.xz` is absent, its exact bytes are recovered in memory from the Base64 and verified; the raw archive need not be published twice. The verifier never executes scripts or other payload content.

`ARCHIVE_MANIFEST.json` inventories every other packaging artifact, including the packer and standalone verifier. Its own identity is deliberately excluded to avoid self-reference and must be pinned externally at publication. The primary publication prefix is `proofs/coordination/evidence/agent20-session16fe/pr153/`; recovery of an excluded duplicate uses the exact commit and path in `EXCLUSIONS.json`.

## Deterministic production and boundaries

`pack_delivery.py --root /path/to/original/workspace --output /path/to/new-package` recreates the package from the scoped source paths. Place this packer and `verify_delivery.py` in the otherwise empty new package directory first. It verifies the original 19-file delivery-watch manifest, validates all duplicate exclusion identities against the retained primary readback, and checks that included/excluded sources are unchanged after packing.

The archive uses sorted canonical relative names, USTAR regular entries only, mode 0644, uid/gid/mtime zero and empty owner names. XZ uses LZMA2 preset 6, an 8 MiB dictionary and CRC64. The process address-space ceiling is 256 MiB. Base64 is canonical 76-column ASCII with LF and final LF. Two independent archive constructions must produce identical bytes. The packer verifies the raw and Base64-decoded member inventories before freezing only its ten own packaging artifacts at mode 0444. No archive directories, symlinks, hardlinks or device entries are stored. Original input file modes are unchanged.

`PACKING_VERIFICATION.json` records the completed packaging checks. All source evidence retains its original historical meaning: preserving a successful review/Ready receipt does not manufacture a merge result or authorize this packer to perform a remote action.
