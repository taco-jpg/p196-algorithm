# PR137 retained review and verification: PASS_REUSE

**Source head:** `f0e2097b82286128005ba81d8e50f2dca4e2d50b`  
**Tree:** `9473febf64d4fa179473e23db88e17d4d5ac7fe6`  
**Frozen mathematics:** `affa037ad537f3ae66a97008991850ce397f613a`  
**Reviewed stacked base:** `dca30e76474569a276c2e58bbd6ee0b96c554ecc`  
**Assessment:** Agent 19's independent, nonauthor, read-only retained-evidence specialist. No source mutation, remote publication, or new Lean compilation.

## Disposition

The existing independent review and retained verification qualify for reuse for this exact mathematical source. I found no uncovered mathematical obligation or source defect requiring a replacement review. This is a source/evidence decision, not a claim that integration has occurred. Agent 19 remains the delivery owner for current combined-tree validation and actual platform/ownership gates.

The original review is [review 5554462051](https://github.com/taco-jpg/p196-algorithm/pull/137#pullrequestreview-5554462051), submitted at H as **COMMENTED**. Attribution remains **Agent 6's runtime/reproducibility specialist**, who did not author any of the three theorem modules. The parent relayed that review through the shared `sodium-qed` account. This satisfies the disclosed nonauthor review role; it is not an external review or a separate-account GitHub approval.

## Full change scope and source binding

Both changed-file pages were retrieved: **100 + 27 = 127 files**, two commits against the stated base. All 127 are additions beneath `proofs/contributions/agent-6/normalized-carry-accounting-20261016/`. The frequently quoted **81 files** describe only the final evidence checkpoint from frozen mathematics to H. Every remote path/blob pair matches local Git H, every changed blob was read, and every JSON file parsed.

All **21 modules / 176,626 bytes** match their registry SHA256 and Git blob identities, the frozen source, canonical replay source copies, and independent review source copies. The 18 inherited modules additionally match the reviewed base. Registry, dependency pins, and replay are unchanged since the frozen source; the repository verifier is unchanged from the base.

The complete closure is TemplateStep, ReturnCertificate, OuterFinite, OuterBounds, OuterBridge, CertificateRealization, ExteriorNormalization, CertificateExterior, CertificateAccounting, TARGET, ExteriorFactorizationProof, ExteriorObservationInjective, ExteriorUpdateLaw, CoordinateDynamics, CoordinateThreshold, CoordinateSign, CoordinateCycle, CertificateCoordinates, NormalizedCarry, CertificateCarryAccounting, and CarryControls. Full repository paths, imports, bytes, and hashes are retained in `verification-results.json`.

| New module | SHA256 | Git blob |
|---|---|---|
| NormalizedCarry.lean | 9bfef7cc4d805ac06631c730173da7e2def6611d7f9e0773f1b5ac8cb2891459 | 338432fa1a0ffaee74f30f67d055840c9f4e940d |
| CertificateCarryAccounting.lean | 32404f75b0b740472825d3510dc52f5294a42ea89b75ddfe4a4b9629c932ec71 | c936414929bc44c775feb49bb05e1e6560903be0 |
| CarryControls.lean | abac509aeef647003b9cc5d78ceecd5a9536b907285449d6dea9aa408ed333fb | 9a7e155e0a53494067b15da77ff0d1da47c5eec0 |

## Semantic review

I read all three new modules and the replay, and checked their substantive inherited definitions and proof interfaces: both normalizers, `stripSuffix` and its decomposition, `norm_append`, `norm_band_tail`, `kOf`, `data`/`gam`, coefficient boundedness and carry bound, `stateOuter`, `rowOuter`, `overflow`, `overflowBit`, the high-value quotient, `Certificate.P/st/lk`, `LocalOK`, `Valid`, `check_sound`, finite sum congruence, weighted coordinate balance, and original gain accounting.

The unrestricted `gam_eq_overflow` identifies unchanged normalizers. Numeric carry survives stripping under either `c ≤ 18` with arbitrary finite natural coefficients, or bounded raw coefficients with arbitrary natural phase. In the latter proof a nonempty removed suffix forces the phase to occur in the bounded original word; an empty removed suffix is identity.

The indicator/carry bridge requires precisely `Bounded s.B`. It separately proves carry equality and the ≤1 bound before converting a nonzero indicator to the numeric carry. It adds no interior, positive-head, nonempty, phase, canonicality, or realizability hypothesis. Row sums use only indices below P. Checker-facing weighted balances retain only the original `check cert = true`, with final terms `9 * totalGam cert` and `18 * (totalG cert + totalH cert)` in Int.

The seven controls distinguish carry drift (phase 19, [19]: 2 becomes 1) from indicator information loss (phase 2, [20]: carry 2, indicator 1), and include empty-stripping boundaries at phases 0, 9, 18 plus bounded phase 19. They are kernel proofs, not certificate witnesses. No accepting certificate, ordinary-integer realization, infinite-orbit theorem, or result about 196 is promoted.

## Retained execution and trust

The original independent runner and audit scripts were read. The runner creates fresh project-object directories, pins genuine Lean 4.19.0 commit `6caaee842e94`, and compiles the complete closure with `--trust=0 -j1 -DElab.async=false`. It reuses the runtime, not author/inherited project objects.

I revalidated **25 retained command receipts and raw-log hashes**: 21 module compilations, two compiler version/prefix reads, and two audits. All exits are zero. I independently reparsed the complete raw multiline audit log: **712 theorem constants + 261 safe definitions = 973 axiom records**, with all records matching structured Lean output and all **16 new literal theorem receipts**. The only accepted axiom union is `propext`, `Classical.choice`, and `Quot.sound`. The 1,437-constant origin census covers private and generated declarations. All 1,404 inherited names/kinds/origins and 942 inherited axiom records are unchanged.

The 428 generated unsafe implementation definitions and 11 inherited generated unsafe implementation axioms are separately inventoried. None enters the accepted theorem/safe-definition axiom chains; the source adds no mathematical axiom or compiler-trusted shortcut. The two failed author accounting attempts and their error-recovery `sorryAx` logs remain accurately labeled failures, outside the accepted source closure. Attempt 003 and the independent build use the exact successful source. The historical 25/1,991 receipt correction is a parser repair, not a theorem failure.

## Preservation checks

The published independent archive was revalidated against its manifest: **559,374 bytes**, SHA256 `0d932dd94d2b1d0dbac7d032dcc24179fdafb8a154a3f045d28e41593478f00b`; all **153 members / 3,625,507 original bytes**, seven readable copies, safe member paths, and original local evidence bytes match. Its 39 omitted compiled objects have an explicit hash inventory. Manifest SHA256 is `bd243d92b3523e4bea7b5a927783c256e619139d1ca77d2b50806f71ad730eb2`.

All four scope archives also pass stored/uncompressed/member hash checks: claims census (50 members), landscape census (73), independent plan (2), and read-only PR107 follow-up (29). Their historical status is retained. No archival failed source is silently selected by the accepted registry.

## Remaining integration obligation

No mathematical review gap identified. Reuse remains valid when the intended combined target preserves the 21 source blobs, registry, dependency pins, verifier, and replay, and unrelated target changes do not alter their resolution. Current main integration, ordinary platform checks/restrictions, exact-head guarded mutation, and post-merge readback remain the delivery owner's work. This assessment does not replace a genuinely required platform check or formal approval.

Reproducible evidence inspection is in `verify_retained_evidence.py`, with the two-page remote mapping in `remote-changed-files.json`. Its output records actual evidence revalidation; **it does not execute Lean**.
