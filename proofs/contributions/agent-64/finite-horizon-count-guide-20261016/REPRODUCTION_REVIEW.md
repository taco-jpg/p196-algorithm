# Source-inspected reproduction review

**Specialist:** `/root/reproduction_links`, genuine Agent64 specialist, explicitly configured `gpt-6-astra`, `reasoning_effort=ultra`. This specialist supplied source analysis and proposed reproduction wording; it is not the independent reviewer of the resulting guide.
**Source snapshot:** `ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3`. All package-relative paths below are under `proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/`.

## Concrete prerequisite correction

The package README's direct `controls.py` invocation omits the prerequisite archive recovery supplied in PUBLICATION.md. The complete package directory listing at the pinned commit has no package-level `verification/` directory, and exact requests for that directory and `verification/full-001/summary.json` returned 404. The evidence manifest declares those paths as archive members.

`controls.py` computes its ten parameter rows and then writes `verification/finite-controls.json` without creating the directory. The independent source registry also needs archive-only `review/horizon-safety/frozen-source/` inputs. The guide therefore places the existing archive recovery command before the controls and independent replay. It recommends a disposable checkout because recovery restores original published files and the controls overwrite their own receipt.

## Exact command contracts inspected

| Item | Inspected source conclusion |
| --- | --- |
| Author arguments | `--lean`, `--repo-root`, `--build-dir`, and `--report-dir` are required. |
| Author output paths | Either existing output path is rejected. Use distinct nonexistent directories. |
| Author source checks | Eleven dependency SHA-256 checks, then the frozen five mathematical modules and audit source. |
| Author compiler flags | `--trust=0 -j1 -DElab.async=false` are hard-coded for each module. |
| Author success receipt | New report-directory `summary.json` has `status: LEAN_CHECKED` on success; no new successful run is claimed here. |
| Independent arguments | Explicit repository, package-root and manifest arguments avoid location-dependent defaults. Override `--auditor` with the actual executor identity. |
| Independent output path | The output directory must not exist. |
| Independent provenance | Source SHA-256 and Git blobs, original commit/path identity, exact imports and selected closure are checked. Required old Git objects must exist locally. |
| Independent runtime | Official Lean 4.19.0 release `6caaee842e94`; runtime hashes are recorded and checked for change during the run. Python 3.9 or later is needed for `Path.is_relative_to`. |
| Independent result | Fresh `verification.json` reports `PASS_SELECTED_SOURCE_CLOSURE` on success; `FILES.json` records output files. |
| Resource boundary | Independent commands have a 1,800-second timeout each, not an overall runtime or memory bound. |
| Controls | No alternate-output or reduced-case CLI; the ten parameter rows entail 1,999,008 seed/case visits and overwrite the package receipt. |

Both drivers check the compiler version and record its hashes. Neither hard-codes the historical executable SHA-256 as an acceptance allowlist. The historic executable hash in PUBLICATION.md remains a recorded measurement, not a hash newly verified in this session.

## Actual source identity checks

The specialist fetched all eleven dependency files at the pin and compared each returned Git blob with dependencies.json. The dependency array agrees with AUTHOR_FREEZE.json and the independent registry. Directory-listed blobs for all five mathematical modules agree with the registry; their SHA-256 fields agree across freeze, registry and independent RESULT.json. The 100 export entries are distinct and equal both the concatenated frozen export lists and independent registry endpoints. The seed/case total was derived arithmetically from the parameter rows without enumerating the seeds.

The parent independently read both complete verifier drivers, controls.py, PUBLICATION.md and the evidence manifest. It fetched the historical written argument directly and confirmed blob `6d6d188df78e26eb6ffdde6ebc3bdb6fc749eb9c`. The separate nonauthor guide reviewer checks the concrete command prose; this source specialist's proposed wording is not independent approval of itself.

## Retained archive metadata

The manifest declares 317 files, 2,817,227 original payload bytes, and 215,004 compressed bytes. Recorded archive SHA-256: `f6311264b4335c320e5763a868f61059d27bee26c7d81ddc1d682f255a39c562`. The archive bytes were not downloaded, extracted or rehashed for this documentation update.

| Retained file | Manifest-declared historical SHA-256 |
| --- | --- |
| `verification/full-001/summary.json` | `202594b31a435413cbb3aac342048dbc13d4b1c4b8999fea6369976190d558de` |
| `review/horizon-safety/runs/full-001/verification.json` | `aeb25ad45cb9992469112640e8e7421c54265cade5c700835656a086a88a76e1` |
| `review/horizon-safety/verification/postcheck.json` | `eae4f868318cfdf1edf11698159c3c559943afc016f8acfee243e6b0cf8ac8ec` |
| `verification/finite-controls.json` | `34fcdfc4db21896fb6c455b6a7a1629e7aeb6d0c0859ab778ae1d9d63bfd82ac` |
| `verification/finite-controls-status.json` | `dc71ebfb7894205dc99c9cec1df4cecdcd5948bd916e47250ee743838aed4815` |

These are prior receipts. The freeze-time `gates_pending` field does not override the later author and independent results. Packaging-only parser and Git-object lookup failures remain in the original contribution history.

## Actual input ledger

| File inspected at the pin | Git blob |
| --- | --- |
| [README.md](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/README.md) | `f2be0d790644ff7b903dac1535454c1889ecd804` |
| [PUBLICATION.md](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/PUBLICATION.md) | `3aaf9ca795efb4d69d1766149032a39b2592b49c` |
| [verify.py](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/verify.py) | `b343f79bf329f97fc655b7c8842a0a8a134b11ac` |
| [dependencies.json](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/dependencies.json) | `afcdb7862035da53ff1a25702df7c3b7e617ad66` |
| [AUTHOR_FREEZE.json](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/AUTHOR_FREEZE.json) | `d41c1fb58c1221f07b71183084260888030b159a` |
| [AUTHOR_RESULT.json](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/AUTHOR_RESULT.json) | `58deb7335d9bb0417a4e0aee37b29c902397f641` |
| [controls.py](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/controls.py) | `b66b65f7a49fb397b449414264680138e76999d0` |
| [controls_parameters.json](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/controls_parameters.json) | `a385c64fc94b4d4e9455fe3ea741c2d39fc3f985` |
| [exports.json](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/exports.json) | `8dfe0647fd8d6f83b5fb3b5cbf2e60720658ed73` |
| [evidence/README.md](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/evidence/README.md) | `4e4eadbc6b18a57d18a860a74b236ac17f732953` |
| [evidence/MANIFEST.json](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/evidence/MANIFEST.json) | `aaa028c058832cc87d9b48e292cae64dad594661` |
| [review/horizon-safety/README.md](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/review/horizon-safety/README.md) | `75077617fdd0cdafa7ae4913c0bda958a1a9ded0` |
| [review/horizon-safety/verify.py](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/review/horizon-safety/verify.py) | `d1924dc354efcb055af8ffb56116395d4ec703ee` |
| [review/horizon-safety/RESULT.json](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/review/horizon-safety/RESULT.json) | `14f1a7ae33411092c2fd13cdf67d6a624f9b9c2e` |
| [review/horizon-safety/verification/source-registry.json](https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/review/horizon-safety/verification/source-registry.json) | `a2a5443ba606c3459493e05a3b51b6ecac1d33e9` |

The eleven dependency paths and hashes remain in the pinned dependency ledger. They include seven unchanged flattened original modules and four preserved Agent101 interfaces. None of those sources was edited.

## Execution classification

- `COMMAND_INSPECTED`: yes, for the recovery, author verifier, controls and independent verifier commands.
- `COMMAND_EXECUTED`: no project command executed.
- `EXPECTED_OUTPUT_CONFIRMED`: no fresh execution output confirmed.
- Archive extraction, archive hash replay, certificate replay and Lean compilation: not performed.
- Repository mutation by this specialist: none.
