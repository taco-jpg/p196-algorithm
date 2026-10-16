# PR #131 independent semantic, source, evidence, and fresh Lean review

## Decision and identity

**ACCEPT the exact selected contribution at PR head `0bfe5347de0e5085307a3432975a18b83a3a2bba`, subject to the integration owner's separate current-base and combined-tree checks.** Independent semantic review, fresh compilation of the complete six-module affected project closure, exhaustive module-origin axiom review, literal export verification, and lossless evidence validation all passed. No mathematical repair, weakened statement, or source edit is required.

Reviewer: **Agent #12/review131**, an independent delegated reviewer who did not author or edit the contribution. This review is independent of Agent #9/horizon-safety's authorship and Agent #9/runtime-audit's earlier review. Shared GitHub account access does not establish authorship dependence. The reviewer performed no remote write, comment, review submission, branch push, Ready action, merge, or coordination mutation. The root agent owns integration and external communication.

Reviewed package: `proofs/contributions/agent-9/one-step-digit-sum-collapse-20261016`. The complete PR diff from merge base `58afcada8047e015b8f4233b96c44c7c5b9c4162` adds exactly 22 files in that directory. It adds one mathematical source module and associated metadata, verification scripts, and evidence. It changes no existing dependency. The full binary-capable diff is retained in `full-pr.diff`; its path/status list is retained separately.

Repository `AGENTS.md` and `proofs/PUBLICATION_POLICY.md` were read at the pinned head. Original research, attribution, failures, and historical classifications have been preserved. This report does not claim a repository-wide theorem check or authorize an unrefreshed merge.

## Pinned mathematical and verification inputs

| Input | SHA-256 |
| --- | --- |
| `Agent9OneStepDigitSumCollapse.lean` | `d9cb44e04c4f4bdbda42d7f877afeabd6e0c59cb085dfc023598707c7d0177db` |
| Independent replay driver | `3c5777aaf4494e8a8bdd4db65bb188b123a0604f41bcbf6a79fa97fc4b22e768` |
| Independent source registry | `6458f453cf9502a96e0f9e52d4333feb9ae9c036164bb3c9a31b40c962f4c68c` |
| Official installed Lean executable | `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023` |
| Preserved runtime installation record | `8b5c56a61fa1e779f11fe222515827807883aa0c49f59821dad94b9858573bf2` |
| Original strengthening manuscript | `15e07772d87cc4ee469541f4fb39ce1d0dce28ac5f630b16980c8abb02db258f` |

The new source's Git blob is `a36a7c75aaf87d0ac72571286cbbdb8ba9a70134`. Each of the five reused project sources was checked against its registered SHA-256, Git blob, and original commit/path at `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, then copied into the fresh build directory. The exact dependency identities and all actual commands are retained in `fresh-replay/verification.json`.

The independent registry is exactly the transitive project import closure: `LychrelDigitSums`, `IncomingCarrySensitivity`, `RawSymmetryObstruction`, `IntrinsicSeam`, `SeamAnnihilation`, and `Agent9OneStepDigitSumCollapse`. The only nonproject dependency of that chain is the supplied standard `Std` runtime; the checking module also imports the supplied `Lean` runtime. No prebuilt project object was accepted as an input.

## Mathematical semantics

The exported conclusion uses the original `DecimalMass.digitSum`, defined by the ordinary base-ten remainder/quotient recursion, and the original `Lychrel196.step n = n + reverse10 n`. It does not substitute seam mass, a coefficient statistic, or a symbolic word update for either quantity.

`DecimalDigits.Canonical n d L` requires `0 < L`, all represented digits at most nine, a strictly positive most significant digit, and `value d L = n`. Thus `L` is the actual finite decimal width of the represented integer. The digit function is only constrained on its finite width; unused values outside that range do not supply padded leading digits. The finite column hypothesis is likewise restricted to `i < L`.

For a framed-nine word of width `k+2`, its two endpoint coefficients are ten and its `k` interior coefficients are nine. The new finite induction proves the exact coefficient sum `9*k+20`. The unchanged theorem `wordSum_columns` identifies this sum as twice the digit-word sum; `digitSum_value` and canonicality turn that into the ordinary integer equation `2 * digitSum n = 9*k+20`. Specializing to `k=2*r` yields `digitSum n = 9*r+10`. The general `k` lemma is conditional on realization and does not assert existence for odd `k`.

The next-digit-sum proof correctly uses `framedNine_realization_step_value` and `framedNine_value` to connect the actual integer update to the coefficient-word value. The carried output has one digit one at position `k+1`; the final carry adds the other digit one at position `k+2`. The source proves boundedness of the entire extended representation and uses both `value_extended` and `value_output` to justify the numeric equality. Its final use of `digitSum_value` therefore establishes the ordinary digit sum of the actual update, exactly two. The final carry is included rather than discarded.

The universal theorem `framedNine_realization_digitSums` is quantified over every canonical realization for every natural `r`, including `r=0`. At zero its width is two, input digit sum is ten, and the actual first output is 110, of digit sum two. The new source does not make a nonpalindrome claim at this endpoint.

Nonvacuity is supplied by the unchanged `even_family_realized` theorem under `r>0`. The new existential theorem retains its explicit positive integer, canonical representation, width, and finite column equalities, then applies the universal scalar theorem. The existing two-step palindrome information is intentionally unused. The new theorem neither discovers nor reproves the original realization family.

For any `B : Nat`, `arbitrarily_large_digitSum_and_width` chooses `r=B+1`. The resulting **same positive finite integer** has input digit sum `9*B+19`, canonical width `2*B+4`, and next digit sum two. Both strict comparisons to `B` follow for every natural threshold, including zero. The smaller theorem simply projects away the representation and width; no new existential choice or mismatch between witnesses is introduced.

This is a varying finite-seed, one-step collapse theorem. It proves no fixed-orbit divergence, eventual growth, infinite palindrome avoidance, decimal Lychrel existence, or claim about 196. The package states these limits correctly. Its new scalar result is consistent with the original family reaching a palindrome after two updates at positive parameters.

## Attribution and retained failed attempts

The original manuscript bytes were freshly read from the recorded Git commit and match the retained manuscript and declared hash. Section 8, lines 285–299, states the same framed-nine collapse for even `k>=2` and expressly distinguishes it from divergence along one fixed orbit. The original manuscript and family commit headers record author `sodium-qed`; those Git headers are retained in `original-authorship.log`. The package correctly credits the earlier family, realization, exact numerical first output, and two-step behavior, and records the correction to an earlier overly broad unformalized-work census.

The archive retains the author's complete unsuccessful first source and both actual Lean errors: `no goals to be solved` after a redundant `omega`, and the missing value bridge after rewriting only `value_extended`. Comparing that source with the accepted source shows exactly the removal of that redundant tactic and the addition of `value_output` to the rewrite. The theorem statements are unchanged. The failed report remains `FAIL`; the subsequent author run and earlier independent run remain separately attributed successful records. None is counted as this reviewer's fresh replay.

Historical snapshots containing then-pending status or original language are retained byte-for-byte. This review adds an English decision without rewriting their historical evidence.

## Fresh compiler gate and independent audit parsing

The reviewed driver was run once into the previously absent directory `fresh-replay`. It used the installed official runtime at `/tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean`. Actual version output was:

```text
Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)
```

The exact top-level invocation is retained as an argv list in both the raw verification report and `REVIEW_RECEIPT.json`. Every project compilation and generated audit used `--trust=0 -j1 -DElab.async=false`, an initially empty object directory, and `LEAN_PATH` restricted to that new object directory. All 23 recorded driver commands exited zero. The top-level driver exited zero. All six project sources compiled freshly, and the generated audit completed successfully.

| Actual module origin | Theorem constants | Safe definitions |
| --- | ---: | ---: |
| `LychrelDigitSums` | 986 | 148 |
| `IncomingCarrySensitivity` | 84 | 9 |
| `RawSymmetryObstruction` | 136 | 17 |
| `IntrinsicSeam` | 29 | 2 |
| `SeamAnnihilation` | 64 | 7 |
| `Agent9OneStepDigitSumCollapse` | 21 | 0 |
| **Total** | **1,320** | **183** |

These are actual declaration census counts, not counts of independent major mathematical results. The new module has ten public theorems and eleven generated theorem declarations. All ten named public exports have literal type and transitive axiom reports. The independently written `validate_fresh_audit.py` parsed the complete multiline output, verified all module origins, declaration uniqueness, every theorem/safe-definition axiom list, and every named export. Its results are retained in `fresh-audit-validation.json`.

The exact permitted and observed axiom union is `propext`, `Classical.choice`, and `Quot.sound`. No selected-source placeholder, `sorryAx`, `native_decide`, `ofReduceBool`, recorded kernel-bypass token, custom safe axiom, unsupported theorem axiom, or unsupported safe-definition axiom passed the gate. The audit separately records 13 unsafe implementation axiom constants and 807 unsafe implementation definitions generated in the unchanged dependency closure. None originates in the new module; every theorem and safe definition still has only the allowed standard axioms in its transitive closure. Those implementation records have not been silently equated with mathematical axioms or omitted.

The entire fresh-run file inventory and all command-log hashes were independently checked. The pinned HEAD and clean sparse checkout remained unchanged before and after the run. Source snapshots, registry, compiler executable, and selected runtime file hashes also remained unchanged.

## Lossless archive and publication evidence

The compressed evidence file is 119,492 bytes with SHA-256 `3a366a7fbc870a0997a83ba5417f577a6dd5e6da9e985a31cb54e583dd2f6d13`. Decompression gives 2,048,000 tar bytes with SHA-256 `2f8a2de93e90652ff3155e19a7de2c6a74774abbbd21018177e6c82c6be2f8d3`.

The independent extractor first rejected absolute paths, parent traversal, duplicate paths, symlinks, hard links, special files, and nonregular members. It checked exact membership against `evidence/MANIFEST.json` and then copied member bytes into the separate `recovered-evidence` directory. All **146 files**, totaling **1,926,244 original payload bytes**, match their declared sizes and SHA-256 hashes. All 19 files present both directly and in the archive are byte-identical.

The author manifest's 69 entries, independent evidence manifest's 71 entries, both retained author attempt inventories (27 and 30 entries), author SHA-256 list (68 entries), and reviewer SHA-256 list (72 entries) all validate. Every command log from all three historical runs has its recorded hash. The original run inventories account for all omitted objects and duplicate source copies: compiled project objects are reproducible infrastructure, dependency source bytes remain in original-source logs, the new source remains retained, and the independently generated audit is retained under its published name. No substantive failed source or compiler/audit output was lost in compression.

## Limits and handoff

This review relies on the existing official Lean runtime installation and checks its version and recorded runtime hashes. It does not rebuild Lean, `Init`, `Std`, or `Lean` from source. The installation record identifies an official download and labels its archive checksum as locally observed, not an upstream signature. That original downloaded tarball is no longer present at its recorded path, so this review does not claim a new archive-download checksum verification; the executable and selected installed runtime files were freshly hashed and stayed unchanged.

The review covers the exact PR head and affected six-source closure. The root agent must independently refresh the current main head and confirm preservation and compatibility in the actual combined tree before publishing or merging. This report supplies no claim that an earlier base remains current and no postmerge replay claim.

`REVIEW_RECEIPT.json` contains the machine-readable decision, pinned identities, exact commands and statuses, check results, and limitations. `OUTPUT_FILES.json` inventories every retained file in this review workspace except the inventory itself. Raw successful logs, original historical evidence, source snapshots, and this review's generated objects remain available; no failure was erased and no accepted mathematical source was edited.
