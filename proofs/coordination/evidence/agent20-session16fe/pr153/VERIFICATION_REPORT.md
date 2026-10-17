# Independent mathematical verification report: PR #153

**Outcome: PASS_WITH_REUSED_FRESH_BUILD for exact source head `6641b1ea166fcef0e6f9d1fa23afed7b1f6b8a82`.**

Agent #20/session16fe9eef625c prepared the separate verifier and audited the resulting evidence. The delivery coordinator independently reviewed the infrastructure, launched the actual compiler processes through the ordinary approval mechanism, and retained their outputs. A separate evidence specialist independently reviewed the static verifier and source/provenance integrity. No mathematical source was authored or repaired by this verification task.

The result combines the actual fresh thirteen-module compilation and successful exhaustive module audit in `run-002` with the actual successful literal-report continuation in `audit-continuation/run-001`. The original run retains its accurate FAIL status because its first literal-report invocation used two unsupported formatting option names. No previously successful project compilation was repeated for that formatting-only repair.

## 1. Exact accepted scope

The selected head is `6641b1ea166fcef0e6f9d1fa23afed7b1f6b8a82`. The inspected target base supplied to this task was `74a1c3922eb7af438fe40b23d2105ad07556e3f5`; this report does not claim to verify a later target combination or an actual merge. The selected root is `Agent52DigitSumDensity`. Its exact local import closure contains eleven unchanged dependency sources and two new modules, all thirteen rebuilt.

The source-manifest pins every file by Git blob and SHA-256 against the selected head and the dependency’s original commit/path. Nine historical dependencies use original-layout commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`; the two Agent9 dependencies use commit `54ac7c885e54ce74190b85ec82cceca2b23c2e38`. The two new sources are pinned directly to the selected head. Every staged source is byte-for-byte identical to both required locations. The continuation separately rebound all thirteen head sources to their original hashes.

| Module | Source SHA-256 | Fresh compile exit | Module-origin theorem constants |
|---|---|---:|---:|
| `LychrelDigitSums` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` | 0 | 986 |
| `SharedProfile` | `0dbd924109cc235a9db5db35c6bbf1326ebf1f69841b53d59439eec92874630f` | 0 | 0 |
| `ProfileDynamics` | `214d8b068c2b12d3df14654071342f371814e230da89fafd7c186ef76697bff5` | 0 | 145 |
| `ProfileIsolation` | `287071e80b2b4d83c1edea18bd9c6f720ecd0f86bede024d7251a46044224bc6` | 0 | 117 |
| `UniformEscape` | `ec159be964b7fa86a09a5ed8e78900b3b29674e96b915fbeae6188a3cc8c2f00` | 0 | 45 |
| `SharpProfileBounds` | `a8907c8ad4d48d3c78ac21a3a87c22858eed9127e9ccbe3a6ce38cfeaa50a09c` | 0 | 61 |
| `SharpUniformEscape` | `74def1ba139fef73734b52163f7690d8c6895299c05dc082c69d107617969348` | 0 | 39 |
| `DecimalEmbedding` | `cc565a8124f5ec916e345c6daaeaaf8d45511b9751298600f83bd189292045ea` | 0 | 38 |
| `SharpUniformDecimal` | `1d46f0bfcadc86ca41573b09f8b588af6a38a8b5798897625459e6f29b714b33` | 0 | 6 |
| `Agent9WindowIntervalCounts` | `597bfe85a6d5ee332aeaf96845e2dc7c96631080ec3a9c5c6c97f3ce17247ff9` | 0 | 10 |
| `Agent9DigitSumIntervalCounts` | `0747bb708957e9d3ab8a2f9afbe5e7222a3ca3daedccc2796d644831d9d7dad4` | 0 | 4 |
| `Agent52Density` | `cb68857fee8f4bf8df25158ac1d19a7d3996894dbc4f8dc81789861ef8f5f549` | 0 | 22 |
| `Agent52DigitSumDensity` | `47efae19090c66b43973d5dc754f2375f83747b900b3cc5f16966af06608bc46` | 0 | 10 |

The exact Git blob IDs, original locations and import lists are in `source-manifest.json` and the retained original `provenance/dependencies.json`. The independent semantic implementation review already matched the two new source hashes and was reused. No repeated semantic-review gate was introduced.

The replacement independent compiler run addressed a concrete evidence gap: the
separate evidence specialist inspected all thirteen incoming PR files and all
forty-six members of the published development archive, checked the complete
archive manifest, and found author-development runs but no qualifying independent
thirteen-module compiler logs or independent API-failure logs. A prior claim that
thirteen modules had compiled did not supply those missing raw artifacts. This
task therefore supplied the uncovered independent build and audit obligation; it
did not restart the already completed unchanged-source semantic review.

## 2. Runtime and external dependency assurance

- Lean: original release **4.19.0**, commit **6caaee842e94**, runtime executable `/tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean`.
- Executable SHA-256: `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
- `libleanshared.so` SHA-256: `2ab605c74c78f9ba4431a7b5305a4b28a9071d8a826f223eb14fe5530f78e14d`.
- Mathlib source revision: `c44e0c8ee63ca166450922a373c7409c5d26b00b`.
- Mathlib lake-manifest SHA-256: `5c6421b650bc87a2427a892a39e5522dc44543ca4ac1bd6e9f08d536c044a752`.
- Retained external restoration report SHA-256: `94b402dfb4a071f7f721ba568c9656e7e1ed838da26380644057c0531d14d98d`.
- Restored-library infrastructure archive SHA-256: `56293d01cdac10b8419e0bf8936992be27a0d30e411aa0f74dbcc7aab86aece4`; original workflow run `38686866819`, artifact `11950407420`. Cache supplements and their hashes are in the copied restoration receipt.

The effective search path begins with the newly created project-object directory, followed by the existing pinned Mathlib/package object directories and original Lean library directory. The entire resolved external import closure comprises **2,665 modules**, including the full Lean audit infrastructure. Every imported external module has one unique source and one unique object, each hashed. Runtime shared libraries are inventoried. The independently reviewed restoration receipt is retained verbatim as `run-002/external-provenance.json`.

**External Mathlib and Lean library objects were restored and reused. They were not rebuilt by this task.** Their source/object provenance derives from the inspected pinned library infrastructure and cache restoration, and all actually resolved bytes are recorded in `external-import-closure.json`. This is not a claim of an independent complete Mathlib rebuild, a repository-wide proof census, or a proof that every external tactic implementation is a mathematical proof dependency.

## 3. Actual compilation and audit execution

Each project compilation used exactly:

```text
lean --trust=0 -j1 -DElab.async=false -o <new-object-path> <unchanged-module>.lean
```

The project-object directory was empty before compilation. Compiler concurrency was one. The actual thirteen-module compilation took 93.954 seconds in aggregate. The complete command vectors, working directories, sanitized environments, return codes, elapsed times and separate raw stdout/stderr are retained. No inherited credentials, network call, package install, remote mutation or source edit was part of the verifier.

| Verification obligation | Actual result |
|---|---|
| Fresh local compilation | All 13 commands returned 0 in `run-002` |
| Full module-origin audit | Returned 0; all 13 modules inventoried |
| Module-origin theorem constants | 1,483, including generated/private theorem constants |
| Complete local declaration inventory | 2,500 constants |
| Safe local mathematical roots | 1,658 |
| Transitive mathematical dependency closure | 8,340 constants |
| Published new theorem endpoints | All 29 explicit type and axiom outputs retained |
| Safe local definition outputs | All 161 retained |
| Actual continued literal command | Returned 0 |
| Literal axiom output records | 1,673: 1,483 theorem outputs + 29 explicit endpoint repeats + 161 definitions |
| Pretty-printer truncation marker | Zero `⋯` occurrences |
| Original run stability | 120 artifacts, 43 command records/logs and 5,386 watched inputs passed before and after continuation |

The continuation did not merely accept completion markers. It checked the exact target multiset, every expected endpoint type marker, all safe-definition markers, all 1,673 literal axiom reports, and exact equality between each theorem’s literal axiom set and the previously successful module audit. It verified the original object hashes and rebound the thirteen head-source pins. The corrected literal source differed from the failed source by exactly the two supported option substitutions.

## 4. Mathematical and implementation-dependency audit

The only permitted axioms were **propext**, **Classical.choice**, and **Quot.sound**. The observed theorem axiom union was exactly that set. The audit rejected unsupported mathematical axioms, sorryAx and compiler-trust reduction constants. All thirteen local sources passed the forbidden-construct scan after comments and literals were masked. Historical failed development sources were not reclassified as accepted mathematical input.

The audit enumerated declaration origins using the actual imported module indices and inspected constants in Lean’s checked environment. It traversed types, proof and definition bodies, opaque bodies, inductive constructors, and recursor rules. Every safe local constant was a root, so the traversal covered the advertised definitions as well as all local theorem chains. No unsafe or partial constant occurred in this accepted mathematical dependency closure.

| Local declaration category | Count | Treatment |
|---|---:|---|
| Theorems | 1,483 | All transitive axioms checked and printed |
| Safe definitions | 161 | All bodies printed; dependency closure checked |
| Safe inductives / constructors / recursors | 4 / 6 / 4 | Included as safe roots and traversed |
| Generated unsafe definitions | 806 | Inventoried; outside mathematical closure |
| Generated unsafe implementation axioms | 16 | Inventoried; outside mathematical closure |
| Generated partial definitions | 20 | Inventoried; outside mathematical closure |

The 842 unsafe/partial implementation auxiliaries were not silently accepted as theorem dependencies, and their mere existence was not mistaken for a mathematical axiom violation. They include compiler-generated `_cstage1`, `_cstage2`, `_unsafe_rec`, specialized list-operation helpers and lambda helpers. The local inventory has zero explicit `implemented_by` or `extern` attributes. External implementation annotations are separately recorded in the closure; implementation redirections do not replace kernel mathematical bodies in the dependency walk.

## 5. Actual endpoint definitions and scope

The literal safe-definition report preserves the actual implementations of `intervalDensity`, `lowerAsymptoticDensity`, `lowerBanachDensity`, the unchanged Agent9 interval count, decimal digit sum, natural-number reverse-add step/orbit, and sharp escape bound. `intervalDensity` casts the finite count and length separately to Real and divides; its empty-interval value is zero. Lower asymptotic density is the real filter liminf of initial-interval frequencies. Lower Banach density takes the infimum over every natural starting time before the real filter liminf.

The numeric endpoints quantify over every positive natural seed and every natural threshold, including zero, using the unchanged ordinary decimal orbit that continues after palindromes. Their reciprocal denominator is the sharp digit-sum escape bound plus one, cast to Real. Uniform epsilon bounds retain the order “for every positive epsilon, there exists one length threshold, for every sufficiently large length, for every start.” The 196 results specialize the positive-seed theorem; they do not claim palindrome avoidance or a proof that 196 is Lychrel.

`audit-continuation/run-001/endpoint-types-and-axioms.json` contains the complete literal elaborated type of each endpoint. The following table gives every target and its actual axiom set; names are relative to `P196.Agent52.Density`.

| Endpoint | Axioms |
|---|---|
| `intervalDensity_zero_length` | `Classical.choice`, `Quot.sound`, `propext` |
| `intervalDensity_nonneg` | `Classical.choice`, `Quot.sound`, `propext` |
| `intervalCount_le_length` | `propext` |
| `intervalDensity_le_one` | `Classical.choice`, `Quot.sound`, `propext` |
| `intervalDensity_bddBelow` | `Classical.choice`, `Quot.sound`, `propext` |
| `iInf_intervalDensity_nonneg` | `Classical.choice`, `Quot.sound`, `propext` |
| `iInf_intervalDensity_le` | `Classical.choice`, `Quot.sound`, `propext` |
| `iInf_intervalDensity_le_one` | `Classical.choice`, `Quot.sound`, `propext` |
| `lowerAsymptoticDensity_nonneg` | `Classical.choice`, `Quot.sound`, `propext` |
| `lowerAsymptoticDensity_le_one` | `Classical.choice`, `Quot.sound`, `propext` |
| `lowerBanachDensity_nonneg` | `Classical.choice`, `Quot.sound`, `propext` |
| `lowerBanachDensity_le_one` | `Classical.choice`, `Quot.sound`, `propext` |
| `lowerBanachDensity_le_lowerAsymptoticDensity` | `Classical.choice`, `Quot.sound`, `propext` |
| `count_intervalDensity_lower_bound` | `Classical.choice`, `Quot.sound`, `propext` |
| `count_intervalDensity_eventually_lower_bound` | `Classical.choice`, `Quot.sound`, `propext` |
| `count_lowerBanachDensity` | `Classical.choice`, `Quot.sound`, `propext` |
| `count_lowerAsymptoticDensity` | `Classical.choice`, `Quot.sound`, `propext` |
| `window_intervalDensity_lower_bound` | `Classical.choice`, `Quot.sound`, `propext` |
| `window_intervalDensity_eventually_lower_bound` | `Classical.choice`, `Quot.sound`, `propext` |
| `window_lowerBanachDensity` | `Classical.choice`, `Quot.sound`, `propext` |
| `window_lowerAsymptoticDensity` | `Classical.choice`, `Quot.sound`, `propext` |
| `digitSum_intervalDensity_lower_bound` | `Classical.choice`, `Quot.sound`, `propext` |
| `digitSum_intervalDensity_eventually_lower_bound` | `Classical.choice`, `Quot.sound`, `propext` |
| `digitSum_lowerBanachDensity` | `Classical.choice`, `Quot.sound`, `propext` |
| `digitSum_lowerAsymptoticDensity` | `Classical.choice`, `Quot.sound`, `propext` |
| `digitSum_lowerBanachDensity_pos` | `Classical.choice`, `Quot.sound`, `propext` |
| `digitSum_lowerAsymptoticDensity_pos` | `Classical.choice`, `Quot.sound`, `propext` |
| `digitSum_lowerBanachDensity_196` | `Classical.choice`, `Quot.sound`, `propext` |
| `digitSum_lowerAsymptoticDensity_196` | `Classical.choice`, `Quot.sound`, `propext` |

## 6. Preserved failures and scoped infrastructure repairs

1. Initial source staging found two Agent9 blobs absent from the local Git store. The independent evidence specialist recovered their exact bytes from the verified published development archive and checked Git blob/SHA-256 identities against the selected trees. The coordinator restored those objects; all thirteen head/original-path reads subsequently agreed. This was an object-availability repair, not a source change.
2. Static review reproduced a preflight lexer defect on valid character literals in `Lean/Parser/Basic.lean` and `Lean/Data/Json/Parser.lean`. The earlier script and exact failing-source hashes were preserved. Character/raw-string handling and prime identifiers were corrected. A subsequent static example in `Mathlib.Tactic.Linter.DeprecatedModule` demonstrated that full-body scanning can mistake interpolated tactic strings for imports. External import parsing was restricted to Lean’s actual module-header grammar; full local source checks remained in force. Independent static review reproduced the 13-local/2,665-external import closure.
3. Actual `run-001` failed before any command or local compilation because it required an object directory for the unused manifest package `Cli`. The exact closure contains no Cli module. The reviewed repair records absent package object roots, retains the mandatory Mathlib/Lean roots, and still requires a unique source/object pair for every actual import. Original failure evidence remains intact.
4. Actual `run-002` compiled all thirteen modules and completed the full module audit successfully, then failed on `unknown option pp.width` and `unknown option pp.maxDepth` in the literal-report source. Independent inspection of Lean 4.19 confirmed the valid replacements `format.width` and `pp.deepTerms true`. The original verifier, failed source, failed logs and report are preserved.
5. The separately reviewed continuation validated all prior input/artifact identities, rebound all thirteen source pins, and reran only the literal reporting command with those two corrections. It returned zero and passed all completeness and before/after stability checks. No theorem statement, proof source, verification target, allowed-axiom rule or mathematical dependency obligation was weakened.

All earlier proposed verifier snapshots, correction diffs and static regression records are retained under `history/`. The source owner’s historical author attempts remain distinct from this independent execution and were not treated as fresh verification.

## 7. Final object identities

These objects were generated by the actual clean local compilation in `run-002`; the continuation verified their hashes before and after the literal audit. Objects can be omitted from a publication bundle as reproducible outputs only if their hashes, exact source, commands and substantive logs remain retained.

| Module object | SHA-256 |
|---|---|
| `Agent9WindowIntervalCounts.olean` | `ccb8f8f70c0e98606543f5255a1fc92d1dbb7717fc5aabbb5026f65d016b8a51` |
| `Agent52Density.olean` | `97c5a9e616ae268a10617b7e2b38c7d4b42551e045be644e13f6b3befb1c57cf` |
| `LychrelDigitSums.olean` | `69dc2ddcd2c17246e2c60ed61195436cc9aefff662f0c49eb769f94baec93978` |
| `SharedProfile.olean` | `4f85586327748792bc0e0816f91b971f2a407be1ee2c07da17328bf2912ccce7` |
| `ProfileDynamics.olean` | `3a4350c35ed51bd688d410a543fd5a390b5a95bdf7810824520928bcdfc3e8bf` |
| `ProfileIsolation.olean` | `32091e01951f8c52c0d0e97899d21f6752efcbd3c1ca6266fc3907d9eb092232` |
| `UniformEscape.olean` | `e6d0df29a0d2a0054cd7bce18ba4d2a92221148b4d922b52d7d1ca869605f6dc` |
| `SharpProfileBounds.olean` | `36915ace1afd3e6ace0a1deb92932350a2447d0cb4cb78aee2dc61f0a3413b10` |
| `SharpUniformEscape.olean` | `0040feb4969200008eae57005bd2a6c6e75eccbdedb8dcd2938ee398478b7732` |
| `DecimalEmbedding.olean` | `ac3d10d924f739e18458c809f2cfb4905ef70e18af3aff13ce98fe71b17cc8fb` |
| `SharpUniformDecimal.olean` | `623040dfa1ce2bbfbfc4f24767a19b128c4b8c12bb6936ab82081bec08cbe069` |
| `Agent9DigitSumIntervalCounts.olean` | `0e658f19ddd6b3be5e3a8723fabc9aaf46f3832b4c96f74e1d8d768bc5dec3a9` |
| `Agent52DigitSumDensity.olean` | `4dbba269dfd4180f63f5d275ac95b19d18bc9e319d42d9b4ba409d9020880d64` |

## 8. Evidence entry points and assurance boundary

| Artifact | SHA-256 |
|---|---|
| `verify_pr153.py` | `2eae51ee30e805c976314d8533345c9fd45fbbdfb6bb76befc1bffd6e439e37f` |
| `Audit.lean.in` | `e0acf0ac8c33d6832d5a008d11d99b95950ff1ec7ea4d0f2d9c67b6f710d148f` |
| `source-manifest.json` | `a49d4fc3288c992465f355a8fef1a8e2977fd7dfd5507c4fa1e6e410b16175e7` |
| `run-002/verification.json` | `d1fab8c622f0bcc703e2441e772c8cef2e0995d6ceda54edb20a3ed777f55f87` |
| `run-002/FILES.json` | `975407005f9d5b6bc4f73a62de333f3009c89ddc38a1190fa5eef38391f3b338` |
| `run-002/declaration-audit.json` | `d582945e797a31d50f8d232608fab6d4fded3d0bebd5332ef206d5192120f7d3` |
| `audit-continuation/complete_literal_audit.py` | `9c33549cf45b4d51c0468e8e7ea5a2ca0df3d419d3f9e63c39d1a20d62aa004c` |
| `audit-continuation/run-001/verification.json` | `5c77f804527ab63345c73662e95df260f1f94d38ef8816e68bc4d96d0acb5dd5` |
| `audit-continuation/run-001/FILES.json` | `78b3c20cb6e42316efc26d236168b662e0bd507d57c6ffd80787a8e11d40f3d1` |
| `audit-continuation/run-001/endpoint-types-and-axioms.json` | `614bdd8e4a48601ae435aacf2ab33d48d200fd209a83588ed9ff8f779f0f802b` |
| `audit-continuation/portable/verify_pr153.py` | `5841e26c12f2ceefa672b5d5ef7ae18243fc0872ec2a52d7eb9083d3335e0f06` |

The complete portable reproducer is in `audit-continuation/portable/`, with the unchanged template, source manifest and all required provenance inputs. Its patched verifier has not been executed as another full clean build. Its README gives the invocation, pinned-runtime/cache prerequisites, expected output location and the exact distinction between actual fresh compilation and later report-only continuation.

This report establishes the scoped source compilation and audit result described above. It does not claim that platform-required checks passed, that the PR was marked Ready, that a platform-eligible review was submitted, that the current target combination was verified, or that a merge occurred. The retained independent semantic review remains reusable for the unchanged mathematical source. The named delivery coordinator retains current-target validation, ownership, publication, Ready/review operations and actual integration duties.
