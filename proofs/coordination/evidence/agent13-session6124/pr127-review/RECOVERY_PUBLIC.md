# Public packet recovery

Use only the new review127-public-evidence.tar.xz or its base64 form, with the SHA-256 in PUBLIC_ARCHIVE_RECEIPT.json. The earlier private archive was withheld before publication and is not a publication candidate.

The public archive root is review127-public/. PUBLIC_ARCHIVE_MANIFEST.json lists every substantive member with its exact length and SHA-256; the outer receipt binds that manifest and the complete xz bytes, including a Git blob SHA-1 calculated from the standard blob header and archive bytes.

Verify without extraction:

```text
python recover_public_packet.py review127-public-evidence.tar.xz --expected-sha256 SHA_FROM_PUBLIC_RECEIPT
```

Extract only into a new directory:

```text
python recover_public_packet.py review127-public-evidence.tar.xz --expected-sha256 SHA_FROM_PUBLIC_RECEIPT --extract-to recovered-public-review127
```

The verifier decompresses every member, rejects duplicate/unsafe/non-file entries, requires exact manifest coverage, checks every byte count and hash, and rejects excluded archive members. Extraction uses exclusive file creation and executes no archive content. The manifest itself is bound by the outer receipt rather than recursively hashing itself.

For base64 transport, decode the complete text to a new file with a standard base64 decoder, then apply the same archive hash verification. The packaging receipt records an actual byte-for-byte base64 decode round trip.

The existing mathematical reproduction material is unchanged: the thirteen .lean sources, original command/environment records, pinned Lean executable identity, full direct execution logs, accepted audit source, and excluded .olean identities are included. Any future Lean reproduction is a new execution and must be identified as such. This publication correction does not run Lean.

PUBLIC_EXCLUSIONS.json distinguishes private/nonresearch administrative and mixed transport omissions from the thirteen reproducible compiler objects. Omitted administrative bodies were not reopened or read to prepare this packet. The original files and original archive remain local and unchanged. The public packet excludes previous delivery containers to prevent recursive self-inclusion.
