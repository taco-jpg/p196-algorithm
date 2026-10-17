# PR #153 combined-tree and preservation review

## Disposition

**PASS_COMBINED_TREE_SOURCE_REBIND_AND_BASE_PRESERVATION.** An independently executed local Git merge-tree operation produced the expected conflict-free integration tree. Its complete diff against the fixed base consists of exactly the thirteen incoming additions. Every pre-existing base entry is structurally preserved, and all thirteen mathematical module source files are byte-identical across the combined tree, H, their original source revisions, and the actual `run-002` staging directory.

This is integration source/preservation evidence, not a repeated semantic review or a new Lean build. The captured `run-002` record is **FAIL** overall: all thirteen local compilations and the module audit record exit 0, but the later literal types/axioms/definitions command records exit 1. That failure is retained and is not converted into a complete verification pass by this source rebind.

## Exact pins and permitted operation

- Repository: `taco-jpg/p196-algorithm`.
- Base B: `74a1c3922eb7af438fe40b23d2105ad07556e3f5`.
- Source head H: `6641b1ea166fcef0e6f9d1fa23afed7b1f6b8a82`.
- Actual combined tree T: `6cfa3582ce49216a0fc055f42dba84532a608407`.
- Reviewer: Agent #20, session `16fe9eef625c`, specialist `/root/evidence_qualifier`.
- Git version: `git version 2.51.1`.
- Local Git object creation by `merge-tree` was authorized. No ref, index, worktree, remote, or mathematical source was changed. No Lean process was started by this review.

## Actual merge execution and complete base-to-result diff

The following command executed in `/workspace/scratch/16fe9eef625c/repo` with `GIT_NO_LAZY_FETCH=1` and `GIT_OPTIONAL_LOCKS=0`:

```text
git merge-tree --write-tree 74a1c3922eb7af438fe40b23d2105ad07556e3f5 6641b1ea166fcef0e6f9d1fa23afed7b1f6b8a82
```

It returned **exit 0**, empty stderr, and exactly this stdout line:

```text
6cfa3582ce49216a0fc055f42dba84532a608407
```

The actual integration diff was obtained with:

```text
git diff-tree -r --no-renames 74a1c3922eb7af438fe40b23d2105ad07556e3f5 6cfa3582ce49216a0fc055f42dba84532a608407
```

It also returned **exit 0** and empty stderr. Its complete output contains **13 A entries, zero M entries, zero D entries, and no other status**. Every addition is mode `100644`, with an absent old entry and the exact incoming Git blob. No broad H-minus-B history/tree comparison was attempted.

The common path prefix for the following table is `proofs/contributions/agent-52/digit-sum-density-20261016/`. Each combined-tree byte stream was read and compared with both its retained incoming source copy and the original inventory hashes.

| Added file | Bytes | Git blob | SHA256 |
|---|---:|---|---|
| `Agent52Density.lean` | 10068 | `7b2e0b94973a9f76db21e90d635c9660ff357aef` | `cb68857fee8f4bf8df25158ac1d19a7d3996894dbc4f8dc81789861ef8f5f549` |
| `Agent52DigitSumDensity.lean` | 4817 | `045d69bc98c868b47e8b26d83f195acceae8d45b` | `47efae19090c66b43973d5dc754f2375f83747b900b3cc5f16966af06608bc46` |
| `CONTRACT.json` | 4376 | `da4a71ac68eea914f5577509e1ff597a428b6d3e` | `86b6242e6b4331ed56a89d85a944bfd70e18bbbacf3b0eee4b211b3cae0e1d32` |
| `COVERAGE.json` | 989 | `14daad8651ab083cb108e76705cc7a111d51630f` | `899ef42d16caa82c5ccefd90070e4642996aa765f4361ec0b0475375e7cb26ae` |
| `README.md` | 5127 | `5c80bcd7618a0c5e71b63d27fa0942474f680707` | `c752024e16abe23614122a59a19156026a27eb3f1d722d8b84e8f41f8108126b` |
| `dependencies.json` | 4493 | `a4e1745c95c1c13fa48b6644a194f5f26be552b4` | `3debdf14f7c8efc13997e3c4d23555b1fc4a6deaa5df9d3e7f4e439713495030` |
| `evidence/development-20261016.tar.gz` | 12532 | `ac0b3a51994bc1af58a2b7fbdfcb473e951329f9` | `1b0639ca1b28442392cbbcf6b0c4a8d2f861b64873d43e92e6537b38c6b433ca` |
| `evidence/development-manifest.json` | 8956 | `40f54e0da7718f538ad5de52f674d4d4e2e6ddec` | `400b24b39aa56b39ec3e6240d0e44c2771cdaef95a4bb13fbb0ef4283bf3667a` |
| `review/semantic/CENSUS.md` | 16085 | `f2ce61c04aff3ea84dd1fc889ba8cf3d8e377944` | `8d273ae1a7e798e16b9a727bec6668eabfd4077f0e4bbe0cad23e43ea2e16bc4` |
| `review/semantic/CONTRACT_REVIEW.md` | 16010 | `b06c8b95e8f26439b9fc7a81aa74e024e319c83e` | `ec40a2ef8b4abf6c5826765707507f57f62f50985c66d584d690278a9e534989` |
| `review/semantic/IMPLEMENTATION_REVIEW.md` | 15089 | `de32e17b5838fd5154e7e3e3f54c6742b4d87436` | `37a943aef1a9c7345a90fb4406c1705d750adec9cee106a4ce0cfbd03fec9b2a` |
| `source/mathlib-lake-manifest.json` | 2786 | `92a8049abc1f1b43ae2b4a6605616034f0dd2682` | `5c6421b650bc87a2427a892a39e5522dc44543ca4ac1bd6e9f08d536c044a752` |
| `source/strengthening_notes.txt` | 13174 | `7103ee939d82740b970dd23fb91e9db50db4ea54` | `15e07772d87cc4ee469541f4fb39ce1d0dce28ac5f630b16980c8abb02db258f` |

## Structural preservation of existing base content

The complete recursive B-to-T diff establishes that no existing file was modified or removed. A second, direct check compared tree entries at each changed ancestor. At each ancestor, exactly one child changed; all other existing children retained their exact mode, type, and object ID. Equal subtree object IDs preserve all descendants without requiring traversal into unrelated historical trees.

| Ancestor | Only changed child | Existing sibling entries preserved exactly |
|---|---|---:|
| `<root>` | `proofs` | 5 |
| `proofs` | `contributions` | 3243 |
| `proofs/contributions` | `agent-52` | 33 |

At `proofs/contributions`, `agent-52` did not exist in B and is the single added child in T. Therefore **all 33 existing contribution entries** retain their object identities. At `proofs`, **3,243 existing sibling entries** remain identical; at the repository root, **5 existing sibling entries** remain identical. These are direct-entry counts, not a claimed recursive file census.

The changed subtree identities are:

| Child tree | B object | T object |
|---|---|---|
| `proofs` | `29f9c383f132740ba33ed6dd8356eece96a481eb` | `873e31794ee68b813326522e0807fd7a6c0ebb4e` |
| `proofs/contributions` | `d4b88b21e5e61647dcacaaf0bd73c7fd4139e7f6` | `c45c662685928bdac67e2fe0dd5373d8ae0b886c` |
| `proofs/contributions/agent-52` | Absent | `1247a08e4189b8861ec9c1713dd7a7ad132f87c3` |

The machine-readable report retains every unchanged sibling identity. This preserves existing proofs, historical evidence, configuration, and other base content structurally; it does not claim that all those unrelated files were read or rebuilt.

## Rebinding the actual compilation source closure

The thirteen entries in `source-manifest.snapshot.json` exactly equal the manifest embedded in the captured actual `run-002` report. For each module, the review read `T:path`, `H:path`, and the manifest's original source commit/path, compared all three byte streams with `pr153-verifier/run-002/source/<module>.lean`, and independently recomputed both SHA256 and Git blob SHA1. All comparisons passed.

| Mathematical module | Git blob | SHA256 | Recorded run-002 compilation |
|---|---|---|
| `LychrelDigitSums` | `8a865176625283648a8a20dd2411ed77670eb0a2` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` | PASS, exit 0 |
| `SharedProfile` | `522f234c3cbaf3751812d6069204a66013c8d537` | `0dbd924109cc235a9db5db35c6bbf1326ebf1f69841b53d59439eec92874630f` | PASS, exit 0 |
| `ProfileDynamics` | `9609854eae0920786d6bccdb2a9c344267367af5` | `214d8b068c2b12d3df14654071342f371814e230da89fafd7c186ef76697bff5` | PASS, exit 0 |
| `ProfileIsolation` | `e25a74b7c2e3243831668215fb11f9995c644972` | `287071e80b2b4d83c1edea18bd9c6f720ecd0f86bede024d7251a46044224bc6` | PASS, exit 0 |
| `UniformEscape` | `5e14ad4d9696d1ab0f42286b2ca36e6492d252b9` | `ec159be964b7fa86a09a5ed8e78900b3b29674e96b915fbeae6188a3cc8c2f00` | PASS, exit 0 |
| `SharpProfileBounds` | `f093a9bac7d1381b1bb0fa4ba0da2ff48e83ba18` | `a8907c8ad4d48d3c78ac21a3a87c22858eed9127e9ccbe3a6ce38cfeaa50a09c` | PASS, exit 0 |
| `SharpUniformEscape` | `d011a7d1a24004c20cef80394e670f36fb4aaf17` | `74def1ba139fef73734b52163f7690d8c6895299c05dc082c69d107617969348` | PASS, exit 0 |
| `DecimalEmbedding` | `af92fbce730cec0300ccce5ad7754f8d5aef060f` | `cc565a8124f5ec916e345c6daaeaaf8d45511b9751298600f83bd189292045ea` | PASS, exit 0 |
| `SharpUniformDecimal` | `7492314811162dfcba6d9016a9f98f8a971aea46` | `1d46f0bfcadc86ca41573b09f8b588af6a38a8b5798897625459e6f29b714b33` | PASS, exit 0 |
| `Agent9WindowIntervalCounts` | `efe4e98e937918b505edfe99e4f6d501be8019f4` | `597bfe85a6d5ee332aeaf96845e2dc7c96631080ec3a9c5c6c97f3ce17247ff9` | PASS, exit 0 |
| `Agent9DigitSumIntervalCounts` | `035e6ab3fea49810ccb3f50e5f8ebf426a847c15` | `0747bb708957e9d3ab8a2f9afbe5e7222a3ca3daedccc2796d644831d9d7dad4` | PASS, exit 0 |
| `Agent52Density` | `7b2e0b94973a9f76db21e90d635c9660ff357aef` | `cb68857fee8f4bf8df25158ac1d19a7d3996894dbc4f8dc81789861ef8f5f549` | PASS, exit 0 |
| `Agent52DigitSumDensity` | `045d69bc98c868b47e8b26d83f195acceae8d45b` | `47efae19090c66b43973d5dc754f2375f83747b900b3cc5f16966af06608bc46` | PASS, exit 0 |

The eleven existing dependency modules are also preserved from B because their entries are outside the thirteen additions and the complete B-to-T diff contains no modifications or deletions. The two new modules are the exact reviewed incoming source files. This is the source-byte basis for applying the actual closure compilation evidence to T.

### Actual run evidence and its failure boundary

- Captured run report: `run-002-verification.snapshot.json`, SHA256 `d1fab8c622f0bcc703e2441e772c8cef2e0995d6ceda54edb20a3ed777f55f87`.
- Captured overall status: `FAIL`; `local_compile_count=13`.
- All thirteen `compile-<module>` commands record exit 0.
- `module-audit` records exit 0.
- `literal-types-axioms-definitions` records exit 1; recorded error: `Command failed: literal-types-axioms-definitions; raw stdout/stderr retained`.
- The existing stdout and stderr files for those fifteen commands were read and hashed: **all 30 stream hashes match the captured run metadata**. Their exact paths, arguments, statuses, exits, sizes, and hashes are preserved in `run-002-log-binding.json`.

The original failing literal outputs remain in `pr153-verifier/run-002/logs/0043-literal-types-axioms-definitions.stdout` and `.stderr`. This review neither removes that failed attempt nor labels it a successful complete audit. A later repaired audit or completed verification must be reported under its own actual evidence.

## Command evidence and boundaries

`command-journal.json` retains **61 actual Git commands**, each with exact argv, working directory, controlled Git environment flags, timestamp, elapsed time, exit code, and SHA256-linked raw stdout/stderr. **All 61 returned exit 0.** No failed Git command was discarded. `capture_combined_tree.py` preserves the capture and verification procedure.

This report establishes the exact conflict-free tree, additive incoming-file preservation, unchanged base identities, and byte-level rebinding of the actual compilation source closure. It does **not** establish a separate Lean rebuild in a combined-tree worktree, successful completion of the failed literal audit, whole-repository compilation, platform-required checks, remote Ready state, merge permission, a main-write claim, or actual integration into main.

The tree result is tied to the exact B and H above. If either changes, the coordinator must refresh the affected integration evidence. The source owner, active independent auditor, and serialized main writer retain their respective responsibilities. No semantic proof acceptance was restarted or weakened by this task.
