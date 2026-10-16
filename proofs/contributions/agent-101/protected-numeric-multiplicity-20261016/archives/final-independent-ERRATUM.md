# Erratum: original canonical FILES inventory

This additive correction concerns preservation prose in the final independent
evidence archive for source commit
`71691d50497edc83247b3571af276bb0ee438491`. The archive, manifest, original
receipts, helper scripts, and README remain unchanged.

## Affected wording

- `final-independent-README.md`, line 44, says: “The original `FILES.json`
  remains unchanged, so its historical object-file entries remain visible
  even though those compiler objects are excluded from this evidence archive.”
- The `preservation` field in `final-independent-manifest.json`, line 166,
  contains the incorrect phrase “including references to excluded compiler
  objects”. The same generated wording appears in
  `final-independent-pack.py`, line 249.

The first sentence about omitting the 26 canonical `.olean` files is correct.
The claims that the original FILES inventory contains object-file entries
are incorrect.

## Correct scope, independently checked

The original canonical `FILES.json` contains **55 entries: 27 `.lean`
sources, 27 `.log` files, and one `verification.json`**. It contains **zero
`.olean` entries and zero `.ilean` entries**. The original verifier already
excludes files with suffix `.olean` when creating this inventory.

The following four copies were read and compared byte for byte:

1. `/workspace/scratch/2a8a87fd78df/agent101-final-family-independent-71691d5/FILES.json`;
2. `reviews/final-canonical-FILES.json` in this contribution;
3. the archive member ending in `archives/final-independent-canonical/FILES.json`;
4. the archive member ending in `reviews/final-canonical-FILES.json`.

All four contain the same **9,248 bytes**, with SHA256:

```text
83e61b850839dc09e4f8b6e301e64d44e1973559a1ede988bf40df83e75f13e0
```

The corrected preservation statement is: **The original canonical FILES
inventory is retained verbatim; it has 55 entries and does not list compiler
objects. The archive manifest separately records the 26 omitted canonical
`.olean` files in `excluded_files`.** The archived FILES inventory is a
snapshot produced by the original verifier; it is not the complete manifest
of every later review artifact included in the 142-member archive.

## Unchanged identities and validation

| Artifact | SHA256 |
|---|---|
| `final-independent.tar.gz` | `31347b5afacef968f6eb9ecdac2985612a9457a7ad5400d84b2bcb9c3a455332` |
| `final-independent-manifest.json` | `e7eca667f6472c081d37a88f8200e24ecc5dd91ea10520e0820cbe65c93a9e02` |
| Original `final-independent-validation.json` | `8f521c1f132ced7acd5f29158c9d18a511af7ea68258b16ae466747cca667c3d` |
| Original `final-independent-README.md` | `c4d36e27b3b7f4ab76b022ec52d1da358c3c755eff7b8bc1d12ca6ae9a535b20` |

The archive remains **352,620 bytes**, with **142 regular members** totaling
**1,941,455 original file bytes** and zero `.olean` members. Its existing
validation receipt still records `PASS`, with 142/142 files restored and
compared against their original bytes.

For this erratum, the unchanged helper was run once in verify-only mode:

```bash
python3 proofs/contributions/agent-101/protected-numeric-multiplicity-20261016/archives/final-independent-verify.py
```

It returned **exit 0**, `status: PASS`, `members_verified: 142`,
`files_written: 0`, and the same archive SHA256 shown above. No new extraction,
Lean compilation, mathematical review, or Git write was performed. This
correction changes the description of the inventory, not the archive bytes
or the existing mathematical verification classification.
