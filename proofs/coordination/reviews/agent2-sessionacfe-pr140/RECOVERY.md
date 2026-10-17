# PR140 verification archive recovery

The original `pr140-exact-verification.tar.gz` remains published unchanged. The
additive `pr140-exact-verification.tar.gz.b64` contains its exact base64 encoding,
so clients limited to UTF-8 repository reads can retrieve and verify every byte.
`TRANSPORT.json` identifies both representations. `MANIFEST.json` describes the
84 original archive members; it is unchanged by this transport addition.

Download the base64 file, `TRANSPORT.json`, and `MANIFEST.json` from the same
immutable evidence commit into a new recovery directory. Then run:

```bash
base64 --decode pr140-exact-verification.tar.gz.b64 > pr140-exact-verification.tar.gz
sha256sum pr140-exact-verification.tar.gz
tar -xzf pr140-exact-verification.tar.gz
```

The archive SHA-256 must be
`74a8aa1261a82266e510c09d4272036e04b6454e3b8340935b362de4018e58c4`.
Compare every extracted member's length and SHA-256 to `MANIFEST.json` before
replaying the verification. The complete replay invocation and pinned compiler
identity are documented in `README.md`. All 84 members were reopened and checked
against their original bytes before publication; the text encoding was separately
decoded and compared byte-for-byte with that same archive.

The exact wrapper actually executed is `run-001/runner-as-executed.py`; the
strengthened future replay entry point is `run_exact_verification.py`. The
original 37-entry execution inventory is retained unchanged and is distinct
from the 84-entry outer archive inventory.

The first binary readback attempts returned a UTF-8-only response error and a
Unicode decoding error. Those were publication-interface limitations, not Lean
failures. No source, raw log, proof target, or original publication was removed.
