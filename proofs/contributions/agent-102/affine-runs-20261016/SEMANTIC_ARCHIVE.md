# Complete independent semantic evidence

`independent-semantic-complete.tar.xz` contains every file in the sealed semantic
review bundle, including the original source/search snapshots and full public
coordination evidence. The archive stores paths beginning `independent-semantic/`.
Every member was read back and its SHA-256 compared with the original bytes.
`SEMANTIC_ARCHIVE.json` records all members, the archive hash and the PASS result.

The principal reports, scripts, result receipts, pins and source snapshots are
also published as ordinary text under `independent-semantic/`. Larger historical
and coordination snapshots remain fully available in the lossless archive.
To reconstruct all relative links and the full original BUNDLE_INDEX, extract
this archive into a fresh directory; it recreates the complete sealed tree.
No compiled cache, runtime binary or private conversation is included.

```sh
mkdir /absolute/new/agent102-semantic-review
 tar -xJf independent-semantic-complete.tar.xz -C /absolute/new/agent102-semantic-review
```
