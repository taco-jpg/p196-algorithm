# PR #101 — independent build and identifier-repair supplement

## Qualified verdict

**REVIEW_STATUS: PASS_EXACT_CANDIDATE_AND_IDENTIFIER_REPAIR.** The build and axiom obligations left pending in `FINDINGS.md` are now discharged for the exact 17-module historical dependency closure, 86 original generated certificate modules, and the exact repaired WIP definitions identified here. The independent semantic findings in `FINDINGS.md` continue to apply because those 103 proof-chain sources are unchanged. I separately inspected the only source repair: quoting four uses of the reserved identifier `prefix` as `«prefix»` in the WIP definitions.

This is a qualified independent acceptance of the local candidate and that exact repair. It is not a claim that the original unmodified WIP file compiles, that the current remote PR contains the generated certificate, that the source owner has adopted the repair, that the current target combination has been verified, or that PR #101 has merged. Those delivery actions remain with Agent #10 under the existing source and target ownership protocol.

Reviewer: `/root/pr101_semantics`, independent of the original contribution and the execution agent's repair. I performed no Lean, generator, or graph-verifier execution. I inspected the actual retained commands, logs, sources, objects, origins, and axiom records. I wrote only new review artifacts in this directory. The sealed checkpoint files `FINDINGS.md` and `STATIC_AUDIT.json` were not modified.

## 1. Exact accepted source scope

The unchanged source pins remain:

- Original PR head: `361de9f7ee5190c8f486c2e5b91ba563cbb95cac`.
- Historical dependency commit: `a4d803f489c3104455555ec6e5d9156d61c3aa05`.
- Original adapter Git blob: `2e3b2380ec3ab7e987f7925dbe2689121315f6e8`.
- Original rank-table Git blob: `5c4406ff4ff41699dccc7490cd897794e331e0d0`.
- Complete original-source manifest: `../source-closure/SOURCE_PINS.json`.
- Complete generated-source identities: `../execution/generator-original-001/receipt.json`, corroborated by the sealed `STATIC_AUDIT.json`.
- Generated final module SHA-256: `5d0f6a62db628923e126a37b484afce49c3b9bf2ed5a7ddc829f797315504c40`.

The complete 17-module table in `FINDINGS.md` remains applicable. No mathematical source, generated data, rank, checker guard, completeness theorem, short-word obligation, initial predicate, or final endpoint was changed to achieve the successful build.

## 2. Strict build evidence and justified reuse

The retained runtime reports:

```text
Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)
```

Every qualified module command used the explicit flags:

```text
--trust=0 -j1 -DElab.async=false
```

The runner used an isolated object directory and an explicit `LEAN_PATH`; its source preflight checked the original Git blob/SHA-256 pins and all generated output identities. The build source and runtime manifests match before and after execution. The runtime manifest contains 1,503 runtime files; the executable SHA-256 is `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.

Attempt 001 successfully compiled six modules, then failed compiling `LychrelDigitSums` with the actual stderr `INTERNAL PANIC: out of memory`. Its 2 GiB address-space cap was the identified resource constraint. The failure is retained and is not relabelled as a successful full build.

Attempt 002 raised that cap to 3 GiB and left all mathematical sources unchanged. It compiled the remaining 97 modules successfully in the recorded 558.716-second attempt. The six earlier successes were reused only after checking the same source bytes, runtime manifest, and compiled-object hashes:

- `PrefixCertificate`
- `PrefixInverse`
- `LongRowsBase`
- `FastInverse`
- `FastRowsBase`
- `Agent124FastPred`

Thus 103 modules have qualifying strict compilation evidence: 17 historical dependencies plus 86 generated modules. This is 97 fresh commands in attempt 002 plus six qualifying earlier commands, not 103 fresh compilations in the second attempt. The initially empty second object directory was populated with precisely those six verified objects before the remaining commands ran.

I independently checked all 103 successful command records for exit 0 and the strict flags, verified both retained log hashes for each command, checked that their module order equals the recorded complete build order, checked the source-manifest before/after equality and current source bytes, and checked current compiled-object bytes against the object manifest. The six reused objects and corresponding sources match their earlier counterparts. These checks are retained in `BUILD_EVIDENCE_CHECK.json`.

I did not redundantly hash every runtime file a second time. I inspected the identical runtime manifests across both attempts and the successful supplement preflight that rechecked those files; my own new hash checks cover the nonruntime sources, objects, logs, and review evidence described in the JSON records.

## 3. Exact WIP failure and repair

The original WIP file has SHA-256:

```text
408f14252ab599c39723b0deca031099ba32d7f081a4b7ca23b6c2b62d880c9b
```

Its explicit strict compile in supplement 001 exited 1. The first meaningful error is:

```text
Agent1172641Targets.lean:17:3: error: unexpected token 'prefix'; expected identifier
```

The later errors at lines 23, 28, and 32 are consistent with the same reserved identifier being used as a term. This is a real parser defect in the original additional module; the successful 103-module endpoint build does not conceal or repair it.

The exact isolated patch is `../execution/strict-build/repair/reserved-identifier.patch`, SHA-256 `bea81183087a5270cc870e636685a5eb49dde723184b0a2cf7f0c9caec16de60`. It changes only:

```diff
-def prefix : List Nat := [2, 6, 4, 1]
+def «prefix» : List Nat := [2, 6, 4, 1]
-  entryOK 7 (R tree) (prefix, 5) = true
+  entryOK 7 (R tree) («prefix», 5) = true
-    PalStartsL prefix P → orbit A t = P → t ≤ 6
+    PalStartsL «prefix» P → orbit A t = P → t ≤ 6
-  ∀ t, ¬ PalStartsL prefix (orbit 196 t)
+  ∀ t, ¬ PalStartsL «prefix» (orbit 196 t)
```

The repaired source is 1,140 bytes, SHA-256 `961bd5aa6a6462443434b40b53da032236201d8e7a543c92d73841283881dd15`. I checked that replacing its four `«prefix»` occurrences by `prefix` recovers the original bytes exactly. Quoting preserves the intended Lean identifier; the actual origin audit records the resulting name as `Agent117.C2641.prefix`.

The repaired file was strictly compiled in supplement 002 with exit 0. Its resulting object SHA-256 is `d1a9582deb782bce4085956c70cdb4de885f4271ab074e4a616e10c8a0aae075`. The propositions, quantifier order, positivity premise, four-digit target, and bound are unchanged. The file continues to define propositions rather than asserting new theorems. I independently approve this exact syntactic repair. No approval is extended to additional unseen changes.

## 4. Complete origin and transitive axiom audit

The execution agent's actual supplement 002 audit completed with exit 0 in 95.440 seconds and empty stderr. Its final receipt is `PASSED`, with all recorded inputs unchanged. The audit source imports the completed final certificate and repaired WIP module, selects exactly the 104 relevant module names, obtains declaration provenance from the Lean environment, rejects safe custom axioms, and invokes both `Lean.collectAxioms` and actual `#print axioms` for every theorem, safe definition, and safe opaque declaration originating in those modules.

The actual coverage is:

| Category | Count |
|---|---:|
| Selected modules covered | 104 |
| Total declarations with selected module origins | 29,808 |
| Theorems audited transitively | 2,188 |
| Safe definitions audited transitively | 472 |
| Safe opaque declarations | 0 |
| Total audited declarations | 2,660 |
| Actual matching `#print axioms` results | 2,660 |

I parsed the complete raw audit log independently and checked it against both `audit-declarations.json` and `module-origins.json`. The set of audited declarations equals all theorem/safe-definition/safe-opaque origins; all 104 module names are covered exactly once. Every raw `#print axioms` set agrees with the corresponding raw `collectAxioms` set. Every such set is a subset of `propext`, `Classical.choice`, and `Quot.sound`. No `sorryAx`, compiler reduction oracle, or unsupported mathematical axiom occurs in those transitive proof dependencies.

The retained environment also contains compiler implementation declarations. The inventory explicitly records 26,990 unsafe definitions, 70 unsafe implementation axioms, and 38 partial definitions. Of these 27,098 entries, 26,654 names end in `._cstage2`; the remaining names are `._cstage1`, specialization/closure names, or `._unsafe_rec` implementations. I inspected the full names of all 70 unsafe implementation axioms and 38 partial definitions. They correspond to the compiled implementations of list operations, recursors, and source functions, and are not newly asserted mathematical premises. They are kept visible in the origin inventory rather than described as safe theorems. Crucially, none appears in the transitive axiom sets of the 2,660 audited mathematical declarations. The source screen also rejects explicit unsafe declarations and the prohibited proof shortcuts in the accepted sources.

These audit qualifications are important: “no unsafe declarations exist anywhere in the compiled environment” would be false, while “all audited proof dependencies use only the three permitted foundational axioms” is directly supported by the actual evidence.

For the single eager-lambda auxiliary, I also inspected the installed runtime source `src/lean/Lean/Compiler/Old.lean`: `mkEagerLambdaLiftingName` constructs names with the suffix `_elambda_` plus an index, and `mkUnsafeRecName` explicitly documents the auxiliary unsafe definitions generated for ordinary recursive definitions. The recorded `OverflowCarryNormalization.iterPairs._elambda_1` matches that compiler mechanism. The original `iterPairs` is an ordinary recursive safe definition in `LychrelDigitSums.lean`, and its actual transitive axiom set is empty. More precisely, the unsafe-definition inventory consists of 26,654 `._cstage2` and 336 `._cstage1` names; all 38 partial entries end in `._unsafe_rec`; the 70 implementation axioms comprise 69 specialized names and this one eager-lambda auxiliary.

## 5. Public endpoints and concrete certificate results

The audit's actual `#check` output is:

```lean
Agent124.Cert117P2641K7.ancestry_2641 (A P t : Nat) :
  0 < A → Agent124.PrefixL.PalStartsL [2, 6, 4, 1] P →
  Lychrel196.orbit A t = P → t ≤ 6

Agent124.Cert117P2641K7.no_196_2641 (t : Nat) :
  ¬ Agent124.PrefixL.PalStartsL [2, 6, 4, 1] (Lychrel196.orbit 196 t)
```

The exact source statements inspected previously therefore survived actual elaboration. The supporting results are present with the following transitive axiom sets; order within each set is immaterial:

| Declaration | Actual axiom set |
|---|---|
| `Agent124.Cert117P2641K7.allRowsAll` | `propext`, `Quot.sound` |
| `Agent124.Cert117P2641K7.allRows` | `propext`, `Classical.choice`, `Quot.sound` |
| `Agent124.Cert117P2641K7.short` | `propext`, `Quot.sound` |
| `Agent124.Cert117P2641K7.init_2641` | Empty |
| `Agent124.Cert117P2641K7.ancestry_2641` | `propext`, `Classical.choice`, `Quot.sound` |
| `Agent124.Cert117P2641K7.no_196_2641` | `propext`, `Classical.choice`, `Quot.sound` |
| `Lychrel196.finite_check_196` | Empty |
| `Lychrel196.no_palindrome_through_100` | `propext`, `Quot.sound` |
| All four repaired `Agent117.C2641` definitions | Empty |

The concrete row checks, complete short-word checks, four-digit initial check, arithmetic ancestry theorem, and family-exclusion theorem are now kernel-checked in this isolated exact-source build. The finite check for times 0 through 100 is likewise backed by the successful historical-module build and actual axiom audit. This closes the specific pending proof obligations in the earlier report.

The mathematical claim remains the exclusion of palindromes starting with 2641 from the ordinary orbit of 196, and the uniform six-step ancestry bound for that family. It does not exclude all palindrome prefixes and does not prove that 196 is a Lychrel number. The abstract rank-five witness does not become an ordinary integer trajectory merely because the upper-bound certificate now compiles.

## 6. Evidence identities and remaining delivery boundary

The independent evidence cross-check is `AXIOM_EVIDENCE_CHECK.json`. It records identities for all key artifacts and the exact public/supporting declarations. Principal final evidence pins are:

| Artifact | SHA-256 |
|---|---|
| Attempt 002 receipt | `2965c47a51a973e70614cb216bf818bf7bdd0b332f9cf502dff78662340946ef` |
| Supplement 002 receipt | `c097e948f26aca17bf4c535004d5a2226066964b85db358b49edbb4b104db691` |
| Full raw audit stdout | `bbbef1d3b8107a10ef58a324647bb7144727cabdedc2800436e6acbea9e713b8` |
| Audited-declaration JSON | `3eb9b905424c15ddaa12e1917f6719e8e2cba64e830c919f1f2b51cbbd741de9` |
| Module-origin JSON | `47c05e31243d0e54c11873ee8bb301997a640511614e43654cbc945d24f81965` |
| Actual audit Lean source | `139a6e3d54702fa44777755281988806603087819bb35802c36a4aaff57be52c` |

`BUILD_EVIDENCE_CHECK.json` was written while the full axiom audit was still running and accurately retains `full_axiom_audit: PENDING` for that earlier evidence checkpoint. `AXIOM_EVIDENCE_CHECK.json` and this supplement record the completed audit; the earlier record was not overwritten to disguise its chronology.

The original PR head still includes the original WIP parser defect unless the source owner adopts the exact repair. The proof acceptance above applies to the reviewed generated candidate and repaired WIP bytes, not automatically to a future remote head with additional content. Publication/adoption, preservation of the research record, exact combined-target verification, and the actual guarded merge remain delivery obligations. No further semantic repair or repeated unchanged proof build is requested by this reviewer on the present evidence.
