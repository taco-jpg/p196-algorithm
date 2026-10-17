# PR155 publication package: selected 64 MiB variant

Status: **PASS — local only, not published.** This is the selected publicable representation because it saves 8,421,868 compressed bytes (49.197%) and reduces transport from 44 to 23 ASCII base64 parts. It preserves the exact same 215 frozen payloads, 113,516,408 original bytes, and nine documented operational exclusions as the original package.

## Exact identities

| Representation | Compressed bytes | SHA-256 | Base64 parts |
|---|---:|---|---:|
| Original 16 MiB dictionary | 17,118,656 | `44f35020ade23d100000ba803d6a36e59f03e3c2e3b1ce1d9b4ac526f20789f1` | 44 |
| Selected 64 MiB dictionary | 8,696,788 | `7074071e389c6f9d70f1ab72cdcb5ca598af48c3e4ffccc58c1484e8e35fb1d7` | 23 |

Both archives decompress to the **identical complete tar byte stream**: 113,694,720 bytes, SHA-256 `2a4bb4330cc0f090f1e066e14f4dc5c957713ebf4240f884c68201139745e35d`. The original 16 MiB serialization is a regenerable operational copy of the same payload. It, its receipts, manifest, parts, and local verification workspace remain preserved. No duplicate remote upload of that older serialization is required to preserve research coverage.

The corresponding positions of the two approximately 46 MB patches are 46,966,784 bytes apart in the tar stream, outside a 16 MiB dictionary and inside a 64 MiB dictionary. The larger window allows the compressor to reuse that earlier content without changing or omitting either patch.

## Memory and execution

Exactly one additional compression variant was run, with one XZ/LZMA2 compressor, CRC64, and a 67,108,864-byte dictionary. The packager had a 1,610,612,736-byte address-space limit (RLIMIT_AS, 1.5 GiB). Its measured peak resident set was 706,240 KiB (689.6875 MiB). The recovered payloads were checked from disk against the originals and the manifest. Both uncompressed tar streams were also compared by byte count and SHA-256.

No Lean execution, mathematical review, source mutation, remote operation, deletion, or ownership action was performed. The source snapshot was required to match the original frozen inventory before compression and remained unchanged afterward. All failed attempts and substantive logs remain retained payloads.

## Programmatic paths

- Archive: `pr155-evidence.tar.xz`
- Complete manifest: `publication-manifest.json`
- Manifest SHA-256: `2a4067d93e2d9720cd2b349b22368c97a87eb55f1f33627cc22a5b5461e8485f`
- Part pattern: `parts/pr155-evidence.tar.xz.b64.part-{index:06d}.txt`, with integer index 1 through 23.
- First part: `parts/pr155-evidence.tar.xz.b64.part-000001.txt`
- Last part: `parts/pr155-evidence.tar.xz.b64.part-000023.txt`
- Maximum part length: 524,288 ASCII characters/bytes; final part: 61,384 bytes.
- Total ASCII base64 bytes: 11,595,720.

For upload, iterate `manifest["base64"]["parts"]` in its recorded order. Every part has its exact path, bytes, SHA-256, decoded bytes, decoded offset, and decoded SHA-256. Every original payload has its path, bytes, SHA-256, permission mode, and tar member name. Exclusions are individually enumerated with reasons. The only exclusions remain six compiled Lean files and three private Git objects.

## Safe recovery

Run from this directory, using a destination that does not exist and whose parent already exists:

```bash
python3 -B recover_evidence.py --manifest publication-manifest.json --from-parts --destination /tmp/pr155-restored-64m
```

For recovery from the archive instead, omit `--from-parts`. Original paths are restored under `<destination>/pr155-evidence/`. The script verifies the compressed identity and every payload, rejects path traversal, links, duplicates and unexpected members, and does not use `extractall`.

## Receipts and file inventory

- `variant-comparison.json`: both compressed identities, exact savings, same-payload proof, identical tar identity, original-package preservation, and memory observations.
- `packaging-success.json`: complete successful recovery from the 23 parts.
- `post-recovery-validation.json`: separate disk verification and exact source/recovered coverage.
- `snapshot.json`: this variant's inventory, checked against the original frozen snapshot.
- `variant-plan.json`: bounded-memory variant plan and baseline identities.
- `publication-files.json`: external deliverable paths, bytes, and SHA-256 hashes.
- `package_evidence.py` and `recover_evidence.py`: implementation and recovery instructions.
- `recovery.stdout` and `recovery.stderr`: actual retained recovery outputs.

`recovered-from-parts/` is a retained local validation copy, not additional research content requiring another upload. The final archive and its complete base64 parts are two transport representations of the same bytes; both are supplied locally.
