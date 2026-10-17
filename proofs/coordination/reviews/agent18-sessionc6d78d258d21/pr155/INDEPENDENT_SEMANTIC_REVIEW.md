# PR #155 — independent final-source semantic review

## Verdict, independence, and execution boundary

**PASS — exact-source implementation semantics and scoped registry coverage.** No mathematical defect was found in the reviewed contribution. This is a final-source review, not a fresh Lean execution result or an authorization to merge.

- Repository: `taco-jpg/p196-algorithm`, PR #155.
- Reviewed head H: `4c0382b16f0600a3dd07ff36c40793e710b92c96`.
- Stacked base B: `7360b12a0a5889761c845a56a4b8d8a1df5f39b5` (PR #148).
- Reviewer: genuine independent subagent `/root/pr155_semantic_review`, under Agent #18/session `c6d78d258d21`.
- The reviewer authored none of the mathematical contribution and changed no source, registry, branch, ownership record, GitHub review, or target. Only review evidence under the assigned `evidence/pr155/semantic/` directory was written.
- New Lean execution by this reviewer: **NOT_RUN**. Clean compilation and the actual exhaustive axiom audit remain a separate execution obligation; no hypothetical PASS is recorded here.
- The parent reports that delivery belongs to Agent #4/session `87258c67b0f5`, and that Agent #18 has retained only independent-review support. This report is handed to that delivery owner through the parent, not published independently. Source ownership remains with Agent #51/session `3551b32d054b`; this review claims no main-write slot.

The complete 13-file additive diff from B to H was inspected. All final mathematical sources in the selected three-module closure were read, together with the entire existing verifier, registry, README, task/claim records, contract review, both author source attempts, both result records, and both full compiler logs. `complete-diff.patch` retains the exact diff. `source-manifest.json` records hashes for every changed file, the dependency closure, and the verifier. The inspected checkout was at H and had no tracked modifications.

## Exact source identities

| Source | SHA-256 | Git blob |
| --- | --- | --- |
| `OverflowDigits.lean` | `65adeb3ae7bea93e390a95fc5f8b58ec43f0f64f01ed9db3f51392657ba89a41` | `6ad7ea581c1ed9e6f8c4907dcb5ad73558423b97` |
| `ResidueSums.lean` | `1333e156e2da6f02a18ff67f83e8ce36955e93c00e425cf67aff713f916140d4` | `f1e3c1c5e7cd780b28f6752d980158bd9b9c98b6` |
| `ReciprocalMoment.lean` | `76bad5a81d0fd7ddbd8c3a9a6a1fee433573b1276f4ba84b9b90b11967afc11a` | `484cb6f022b2c2397b98e262caa9bcd46076eb08` |
| Original `astra_spectral_carry_quotient.md` | `d39212c9ab98f4c5b0fccb733d3b662e41a09804878178c82b8762684e97fb09` | `eac5b8f61385a615d9cc3e7796a4d698c66b716b` |

The two dependency modules are byte-identical at B and H, as independently checked against their tree blob IDs and working-file hashes. Their full paths and all other reviewed-file hashes are in the manifest. The new module has exactly the bytes of retained author attempt `002`.

The original document resides at `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/astra_spectral_carry_quotient.md`. The reviewer inspected lines 70–140, including the precise assertion at 103–108 and its surrounding physical-coefficient interpretation at 109–118. A local Git read initially failed because the sparse/promisor checkout did not contain that blob and the shell could not reach the remote. The parent then retrieved the content through its connector.

The parent's first materialized transport copy had one extra final LF: 9,530 bytes, SHA-256 `f828477b331173092cb4e078ab2720b7733983693b1ea18fd17d5eaad9b1f017`, Git blob `0cd9455ee7067c6a447e11df4b702c00b03d5c25`. Removing exactly that final byte produces the 9,529-byte source matching **both** pinned identities above. The parent confirmed that its text materialization introduced the extra LF. The transport copy was left untouched; `exact-original-source.md` retains the exact recovered source. This restores transport fidelity and does not revise research content.

## Existing contract review is reusable

The retained `review/CONTRACT_REVIEW.md` has SHA-256 `4a6004fcd0690fbc43f73500e1bc3b4265248e0efbfa80cb8c27fb531ac87165`, matching the task record. It explicitly identifies itself as a genuine nonauthor, preimplementation contract review without a new build. Its mathematical reasoning, original-source identity, frozen `ResidueSums` identity, intended generalization, and boundary analysis remain applicable to H.

It should therefore be reused for that already reviewed contract. It should not be reclassified as a final implementation or execution review. The precise newly covered obligation here is to inspect the **actual final proof definitions, hypotheses, implementation, exported theorem names, dependency bytes, and scoped build registration** and establish that they implement the previously reviewed contract without hidden restriction or semantic substitution. This is the additional final-source work the contract review itself requested. No second review of the unchanged contract is made a new mandatory gate.

## First-moment identity and all-width boundary behavior

The statement in `ReciprocalMoment.lean:50–77` quantifies over arbitrary `q : Nat → Int` and `L : Nat`, with only the bounded premise `∀ i < L, q i = q (L - 1 - i)`. It proves

```text
2 * finiteSum (fun i => (i : Int) * q i) L
  = ((L : Int) - 1) * finiteSum q L.
```

The sums have the same width. Coefficients outside that width are not constrained or read. There are no hidden positivity, decimal-digit, nonzero mass, even-width, or nonzero endpoint assumptions. The statement uses integer subtraction in its multiplier, not truncated natural subtraction.

The implementation is the expected finite reindexing proof. `finiteSum_reflected` at lines 34–47 proves invariance under reversal by induction, using bounded congruence for the shorter prefix, a shifted induction hypothesis, and `finiteSum_shift`. For an in-range index, the arithmetic identity `i + (L - 1 - i) = L - 1` is justified before casting it into the coefficient equation. The main proof replaces coefficients by their reflected counterparts using the supplied symmetry, identifies the reflected moment by that helper, adds the two moment sums using `finiteSum_add_values`, and factors the constant multiplier with the unchanged `finiteSum_mul_left`. It does not assume the desired moment equation or divide by a possibly zero quantity.

At L = 0 both sums are empty, the symmetry premise is vacuous, and the integer factor is -1; the equation is 0 = 0. No out-of-range subtraction identity is required, because `finiteSum_congr` supplies an in-range hypothesis and has no instances at empty width. At L = 1 the weighted sum and the multiplier vanish for every coefficient. Signed coefficients, zero mass, all-zero words, zero endpoints, and an unrestricted central coefficient at odd width are included. The reflection lemma itself also covers empty width.

`reciprocal_first_moment_literal` at lines 80–84 uses the unchanged `finiteSum_eq_range` bridge to expose the exact finite `List.range L` sum, with explicit natural index binders. This prevents an unexplained alternative summation semantics.

The source speaks of a reciprocal polynomial of degree L−1. The implementation deliberately proves the stronger fixed-window coefficient statement. If endpoints vanish, the represented polynomial may have smaller actual degree or be zero. The README and contract correctly distinguish reflection width from actual degree; the theorem does not assert a degree it has not established. A polynomial reciprocal at another degree does not automatically satisfy the specified width premise.

## Formal derivative and modulo-nine semantics

`formalDerivativeValue` at lines 86–89 is the literal coefficientwise formal derivative evaluation

```text
sum (i in List.range L), (i : Int) * q i * x^(i - 1).
```

Its natural subtraction at i = 0 is sound: the exponent becomes zero but the prefactor is zero, so the complete term vanishes for every integer x, including x = 0. For each positive i the exponent is the usual i−1. This is an explicit finite-polynomial differentiation formula, not an analytic derivative API and not a derivative defined by the identity under proof. The accepted contract explicitly permits this representation.

`derivativeAtOne` is independently defined as the literal weighted coefficient sum. `derivativeAtOne_eq_finiteSum` and `formalDerivativeValue_one` at lines 95–103 establish the two required bridges. `reciprocal_derivative_at_one` then applies the first-moment theorem at lines 106–110. It preserves the exact formal coefficient interpretation of Q′(1).

At lines 113–119, `reciprocal_derivative_mod_nine` derives

```text
derivativeAtOne q L % 9
  = (5 * (((L : Int) - 1) * finiteSum q L)) % 9.
```

The factor 5 correctly inverts 2 modulo 9 because 2·5 ≡ 1. No integer division of an arbitrary residue is used. The consequence is valid for negative coefficients and mass because the modulus is the positive integer 9 and the exact first-moment equality is an integer equality. The `omega` step uses this fixed-modulus consequence, not a finite enumeration of widths.

`reciprocal_derivative_mod_nine_determined` at lines 123–135 quantifies over two functions q and r at one common L. Both receive their own bounded symmetry premise. The remaining hypothesis is equality of masses modulo 9, rather than unnecessary exact mass equality. Targeted `Int.mul_emod` rewrites preserve multiplication by the same width factor and then by 5. The quantifier order and hypotheses establish exactly the advertised redundancy at fixed width. They do not claim equal derivatives for arbitrary unrelated widths or arbitrary nonsymmetric words.

## Natural polynomial-value bridge and attribution

In the frozen `ResidueSums.lean`, `finiteSum` is the ordinary recursive integer sum over indices below its natural length (lines 12–14); `finiteSum_eq_range` identifies it with the literal list sum (lines 23–28). `polynomialValue` is the literal evaluation of natural coefficients cast to integers against x^i (lines 31–32), and `polynomialValue_eq_finiteSum` exposes the same sum (lines 34–36). These definitions were not changed by PR #155.

`natural_mass_eq_polynomialValue` at `ReciprocalMoment.lean:138–143` proves that the cast natural mass is exactly this existing `polynomialValue q L 1`. `natural_reciprocal_derivative` at lines 146–154 transfers the bounded natural symmetry by casting and proves the source-facing equation with the existing `polynomialValue` on the right. It introduces neither a replacement mass semantics nor a new digit or canonicality premise.

The original document's lines 103–108 contain the reciprocal moment identity and the derivative-coordinate redundancy modulo 9. The new source and README attribute that mathematics to the original report, identify the original Git blob, and acknowledge the related `DecimalMass.wordSum_reflected` argument as a supporting generalization. This review verifies those attribution statements and their bounded relevance; it does not independently reconstruct the full history of the earlier helper. No mathematical-discovery claim is made.

## Registry closure, build inclusion, and axiom evidence

The selected project in `proofs/Agent51ReciprocalMoment.registry.json` has root `ReciprocalMoment` and the complete local closure

```text
Std → OverflowDigits → ResidueSums → ReciprocalMoment
```

The inspected imports and all module hashes/blob IDs match the registry. The public endpoint list has exactly 50 unique declarations and is exactly the set of source-level public definitions/theorems in these modules: 8 from `OverflowDigits`, 28 from `ResidueSums`, and 14 from `ReciprocalMoment`. All six advertised final endpoints are included. The private `ResidueSums.int_sum_append` helper is also present in the inspected dependency source; an exhaustive module-origin theorem audit must include private and generated theorem declarations, rather than treating 50 public names as the full transitive proof census.

The unchanged `proofs/verify_project__214bf7673efe116b.py` was read in full. For the explicit `--project agent51-reciprocal-moment` command, it checks exact source identities and declared imports, requires the registered modules to equal the root closure, copies fresh sources into a new directory, compiles them in dependency order, checks the named endpoints, and constructs a module-origin theorem axiom audit using `Lean.collectAxioms`. It also rejects custom mathematical axiom declarations and source tokens prohibited by its policy. The build includes this otherwise standalone contribution through the explicit registry/root. There is no need to invent a repository-wide default-build obligation for this scoped claim. `catalogue_complete: false` explicitly prevents a global-census interpretation.

**Execution qualification:** the existing verifier's Lean command lines use `-j1 -DElab.async=false` but do not explicitly include `--trust=0`. The task's acceptance record explicitly requires that strict flag. Therefore the README command alone must not be described as a strict-trust replay. The delivery/execution owner must retain actual strict commands, or a transparently inspected strict wrapper, together with their results. This reviewer neither changed nor executed the verifier and records no full-module audit result.

Manual inspection found no admitted proof, `sorry`, `admit`, new mathematical axiom, `native_decide`, or unsupported external oracle in the accepted three-module source. Ordinary `decide` in unchanged finite arithmetic lemmas is not `native_decide`. Source inspection is not substituted for the separate transitive axiom audit.

Author attempt `002` reports Lean 4.19.0 with `--trust=0 -j1 -DElab.async=false`, exit code 0, and retained `#print axioms` output for all 14 public declarations. Those logs show only `propext` and `Quot.sound` where axioms are present; the two derivative definitions are axiom-free. Its source hash matches the accepted source. The attempt explicitly reused earlier dependency objects and is labeled author development, not an independent clean closure build. That distinction is accurate and must be preserved.

Attempt `001` reports exit code 1. Its full log preserves natural-index elaboration errors, the resulting `sorryAx` artifacts from failed elaboration, and a recursive simplification failure. The final repair adds explicit natural binders and replaces the looping modular simplification with targeted rewrites; the advertised theorem contracts remain unchanged. Both failed and corrected source/log versions are preserved. The failed source is outside the registered closure and is not being accepted as a proved module. Its `sorryAx` output is historical failure evidence, not something to omit or mislabel as PASS.

The task JSON's preimplementation status text remains a historical claim snapshot; the later README and author receipt expressly state the implementation/execution checkpoint. This is not a mathematical contradiction and does not turn unfinished independent execution into a completed result.

## Scoped disposition and remaining delivery action

This review closes the final-source semantic obligation at H. The existing contract review is reusable, and no substantive source repair is requested by this reviewer. The final-source and registry checks were actually performed; Lean execution was not.

The exact remaining acceptance evidence is a qualifying strict clean build of the registered three-module closure and the actual endpoint/module-origin transitive axiom results, whether newly executed by the responsible owner or legitimately reused from matching exact-source evidence. The parent is handing this report to the existing delivery owner to coordinate that evidence without duplicate heavy work. Any changed mathematical source or changed dependency bytes require evaluation of the affected review scope. Integration with the actual target remains a separate delivery check, especially because PR #148 is the stacked prerequisite.

No claim is made here about full Laurent quotient classification, its cardinality, every physical residue realization, carry dynamics, overflow saturation, orbit persistence, or an all-time ordinary-integer conclusion for 196. No Ready transition, merge, or target verification was performed by this reviewer.

### Retained review evidence

- `INDEPENDENT_SEMANTIC_REVIEW.md`: this report.
- `source-manifest.json`: exact source/file hashes, import/declaration census, unchanged-base dependency checks, and original-source transport restoration.
- `complete-diff.patch`: complete additive B-to-H diff.
- `exact-original-source.md`: exact original source with both original identities verified.

