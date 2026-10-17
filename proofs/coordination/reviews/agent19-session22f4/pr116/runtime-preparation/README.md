# PR 116 exact-source runtime preparation record

Prepared for additive publication under `proofs/coordination/reviews/agent19-session22f4/pr116/`. The directory name does not imply independent review.

**Classification:** runtime/source preparation for a new formal bridge. **No independent mathematical review, full all-width theorem, or missing-bridge acceptance is claimed.**

The package preserves exact compiler inputs, original GitHub Actions evidence, new import-object preparation commands and raw logs, source/object fingerprints, existing endpoint axiom outputs, and runtime provenance. The compiler inputs in `inputs/` are unmodified copies fetched at head `51f8f8d523eb8434b6a80ad7dc1e30fe63ab8378`; ExteriorCore, ExteriorCapTwo, and ExteriorCoverage are staged under their import names. The hash/path mapping is recorded in `source-pins.json` and `PREPARATION-RESULT.json`. The retained RESEARCH.md is historical source context, with its original status language preserved.

`baseline-build.json` and `closure-build.json` give the actual local argv, cwd, LEAN_PATH, source hash, exit code, object hash, and raw output filenames for every invocation. Seven invocations succeeded; none failed. Every invocation used `--trust=0 -j1 -DmaxHeartbeats=0 -DmaxRecDepth=100000`; `-o` generated the required import object. The newly prepared object bytes are retained locally rather than published in this text evidence package; their fingerprints remain in the records.

The original CI job `117215969204` in run `38973106121` used the five commands retained in `CI-SOURCE-BINDING.json`; these did not include `-DElab.async=false`. Its source hashes match the fetched five inputs. The original CI produced only ExteriorCore.olean; the fresh helper-object compilation was needed for new bridge elaboration.

The selected toolchain is a previously downloaded pruned checker runtime. Its actual binary, key imported objects, and shared library were SHA256-compared to an existing authenticated official Lean 4.19.0 release runtime. These provenance categories remain separate in `runtime-receipt.json` and the two retained origin receipts. This preparation task downloaded no toolchain, rebuilt no Std, and modified no shared runtime or original repository source.

The 20 printed existing endpoints use only the permitted standard axioms propext, Classical.choice, Quot.sound, or no axioms. This says nothing by itself about the new all-width source-to-boundary bridge, which requires its own endpoint check and separate independent review.

`PACKAGE-MANIFEST.json` lists every packaged file with SHA256 and byte length, excluding the manifest itself. `REPORT.md` contains the fuller preparation report and internal execution paths.
