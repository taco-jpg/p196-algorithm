# Remote transport and verification

The repository publishes the exact wrapped UTF-8 `evidence.tar.xz.b64` file.
The binary archive is a lossless transport duplicate and is reconstructed locally;
it is not a separate remote file. No evidence member is omitted.

Before following README.md, download all files from this directory and run:

```sh
base64 --decode evidence.tar.xz.b64 > evidence.tar.xz
python pack_evidence.py --verify-only --output .
```

The decoded archive must be 2,062,492 bytes with SHA256
`d0e22133ad5836356c1696c2f177fc27cfffe89b8cf99ef7e4f319e5171dfc64`.
The verifier checks all 733 archive members and the Base64 round trip.

PUBLICATION_MANIFEST.json identifies the initial remote textual files by exact
byte length, SHA256 and Git blob SHA1. It excludes itself from its own digest
list. Later DELIVERY_STATUS.json and delivery readbacks record actual review,
readiness, writer coordination and integration outcomes separately; those
outcomes are never inferred from successful packing.
