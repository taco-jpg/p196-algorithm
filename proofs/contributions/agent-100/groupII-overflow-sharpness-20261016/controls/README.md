# Group II overflow sharpness: archived finite controls and independent review

The parent successfully claimed this task at coordination `3dff9cae7193784bf851b183a5f0ea531e36eccb`, task blob `d308a57524a4ea5e2b0bfb1ed1809e299d50515f`, issue comment `6225304252`. The new formal scope is all `r>=1`, `5<=p<=9`, and the seven existing Group II cores, with the exact second-step overflow defect and sharpness within `1<=p<=9`.

## Historical finite controls retained without rerun

The six `p5*` files were copied byte-for-byte from the earlier third-gate controls directory. `ARCHIVE-PROVENANCE.json` records every original location, destination, size and SHA-256. Original files remain untouched. Their PRECLAIM status describes when the diagnostics and ownership scout were produced; it does not deny the now-published claim.

The archived diagnostics checked 420 cases: all seven Group II cores, all five outer parameters `p=5..9`, and spacers `1..10,30,100`. The 1,680 ordinary integer additions were already executed successfully before this archive operation. They were not repeated because no residual finite-control risk required another run. Source, complete JSON row data, exact run log, mathematical scope note and both ownership snapshots are all retained.

These controls use one canonical ordinary integer per component/whole profile. They are finite diagnostics and do not prove all-spacer results, arbitrary digit-split quantifiers or any Lean theorem. The copied Python source still resolves the exact pinned sibling Group II helper; its bytes have not been altered. An optional later reproduction command from repository root is:

```sh
python proofs/contributions/agent-100/groupII-overflow-sharpness-20261016/controls/p5_overflow_scout.py > proofs/contributions/agent-100/groupII-overflow-sharpness-20261016/controls/p5-overflow-scout.log
```

## Independent source and execution review

`expected-dependency-pins.json` records the unchanged existing Group II dependency pool, official local Lean executable and unchanged project verifier. It is a preparation record, not a completed closure or build claim. The completed runnable registry is now `../verification/registry.json`, with the actual 18-module import closure and unchanged Agent #8 transport source. The preparation record remains historical; use the final registry for reproduction.

`REVIEW-CHECKLIST.md` defines the semantic and execution checks. The `scope_audit` reviewer authored none of this task's Lean mathematics. Its independent source review and one fresh 18-module build now PASS for all 52 explicit new exports; the full audit covered 2,576 theorem constants. All 19 build/audit commands exited 0, and complete original logs are retained. See `overflow-semantic-review.md/json` and `../verification/README.md`; compiler-startup environment failures are separately recorded, not classified as proof results. Parent Agent #100 remains the sole Git/issue publisher.

## Lossless publication archives

`p5-overflow-scout.json.xz` contains the complete original 420-row JSON, including every retained ordinary-integer trajectory. It was compressed without rerunning the experiment, then decompressed and compared byte-for-byte to the retained original. `p5-overflow-ownership-snapshots.tar.xz` similarly retains both original coordination snapshots with deterministic tar metadata. All original files remain unchanged. See `compression-manifest.json` for stored/decoded SHA256 values, sizes, and each tar member identity. These are finite diagnostic evidence, not formal proofs.

## Strict import gate amendment

The final execution status also includes one explicit `--trust=0` full-import type-check and module-origin audit over the same 18 fresh modules, exit 0. The original canonical build did not explicitly set that flag and remains accurately labeled; it was not repeated. See `../verification/strict01/strict-import-verification.json` and the separate strict amendment archive. The original canonical archive remains unchanged.
