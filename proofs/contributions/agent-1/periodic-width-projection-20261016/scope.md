# Period-four width, actual clock, and finite-return scout

Status: source-only investigation by Agent #1 specialist `/root/symbolic_scope`, 2026-10-16. No new Lean proof, experiment, claim, Git write, or external message was performed. The parent owns publication and coordination. All interfaces below marked proposed are unproved proposals.

## Finding and recommended next scope

The exact local signed width balance is already proved for the actual maximally stripped period-four quotient. The actual ordinary reverse-and-add decimal-width theorem is also already proved. In the inspected sources there is no period-four finite-return telescope or exact head/phase/width-residue projection theorem.

The consequential missing assembly is the projection of the actual quotient to the preserved necessary-condition graph. The complementary head scout supplies the actual head/phase edge. This scope can supply the width residue `r = (2*B.length + H.length) % 8`, its exact update by the actual `rawGamma`, and the resulting finite-return clock divisibility. A standalone generic telescoping lemma would be routine packaging of established accounting, so it should be a consequence or supporting lemma of that projection, not the advertised research target.

Do not claim that the temporal period is divisible by eight. The sum of actual overflow bits is divisible by eight when the finite interface returns. The sum of signed exponent increments is that overflow count divided by eight. Neither a positive overflow count nor a realizable graph cycle follows from width accounting alone.

## Exact current source and dependency pins

Inspected current Agent1 publication: commit `e2ce8e1cd121b78ce839c120d0d475990f561b8f`, branch `research/agent-1/periodic-phase-catalog-20261016T2247Z`, Draft PR143. Parent's issue61 source checkpoint is comment `6226153210`; its fresh combined review was still running at that checkpoint. This report makes no new build claim.

Paths below are in that commit unless another commit is supplied.

| Path | Git blob | Relevant source |
| --- | --- | --- |
| `proofs/Agent1PeriodicQuotient.lean` | `63bd5f4319f6a79924b7292db3eb82e0d027b26c` | `periodicWord_length`, `exponentDelta`, `quotient_width_balance`, `quotient_exponent_accounting` |
| `proofs/Agent1PeriodicNumeric.lean` | `710e899d559514f48e409569268929803dde3ce9` | `periodic_actual_step_decimalLength`, canonical-width and actual-carry bridges |
| `proofs/Agent1PeriodicPhase.lean` | `ecb0816aa6411068956b9c746c61d267dcd11feb` | actual non-nine phase image |
| `proofs/Agent1PeriodicPhaseCatalog.lean` | `a9414bc8c9be783f5dfc48778db7161c481a96fc` | actual `rawPeriod_catalog_edge`, preserving all-nine carry labels |
| `proofs/Agent1PeriodicValidity.lean` | `3c5673981d4c9a73a0ade71552f5867d8f73dd69` | original `ValidPeriodic` and successor validity |
| `proofs/Agent1PeriodicSafetyAlphabet.lean` | `e5c1480c24770054ff24b7c770e457a5162a7d26` | original periodic word head bridge |
| `proofs/Agent1PeriodicOuterStrip.lean` | `9e35c06bf3dd393f33dfd2af965a1ea2d4305bc7` | stripping preserves the outside head |
| `proofs/CertificateAccounting__ad0d1bd9b0242036.lean` | `79bf1fdfebabcf95dee96698be9aab3747c2599a` | Agent110 scalar-certificate sum and width accounting |
| `proofs/CertificateCharge__46feaa8077e59426.lean` | `8af8e26c4112b5074b6b9e8e39c77cc416054c86` | scalar-certificate mod-nine accounting |
| `proofs/CertificatePhases__e0f11dab45134f94.lean` | `6921374766aadbc38bca86fc79d3a47b7d737400` | scalar-certificate temporal six-divisibility |
| `proofs/ExteriorCharge__52cbb237030a07b3.lean` | `3020c27a4f65aa5c59a76d2facecc6739fc25d00` | original scalar exterior overflow-count mod-nine and conditional full-return arithmetic |
| `proofs/width_phase_filter__890cbbe4ac2ff549.py` | `c320ea36d1d562bc315b097d80177df3668dea2a` | saved necessary width lift |
| `proofs/outer_filter__4b3d159990f5e177.py` | `ca0fe5e4cf9f6df4528d1e1375c9bfc404ad04f6` | saved outer-head graph construction |

Original archive directory:
`proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/main_existence_attempt/continuation_pass/periodic_bulk_followup/`.

Within it, `METHOD_AND_PROOF.md` is blob `5c5f94c66d6c3adb0288b610f748fcbed32b115c`; `width_phase_results.json` is blob `7e480b160969965abd880f922ef211347eecc6c1`.

## What is already proved exactly

In namespace `Agent1.Periodic`, the original definitions are retained:

```lean
def exponentDelta (B H w : Word) : Int :=
  (outerPeriods B H w : Int) + (centerPeriods B H w : Int) - 2

theorem periodicWord_length (B H w : Word) (k : Nat) :
  (periodicWord B H w k).length =
    2 * B.length + H.length + 2 * (k * w.length)

theorem quotient_width_balance (B H w : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hlen : w.length = 4) :
    2 * ((quotientOuter B H w).length : Int) +
      ((quotientCenter B H w).length : Int) + 8 * exponentDelta B H w =
      2 * (B.length : Int) + (H.length : Int) + (rawGamma B H w : Int)
```

This local width equality needs no safety premise, no positive outer coefficient, and no exponent guard. It is already derived from literal raw block lengths and the original maximal stripping decompositions. It includes constant and nonprimitive period words.

The existing `quotient_exponent_accounting B H w k (hk : 3 <= k)` proves both successor exponent at least one and

```lean
(((k - 2) + outerPeriods B H w + centerPeriods B H w : Nat) : Int) =
  (k : Int) + exponentDelta B H w
```

It does not imply that the successor exponent is at least three or that all later guards hold.

The existing `periodic_actual_step_decimalLength` takes `0 < k`, bounded B/H/w, an original `DecimalDigits.Canonical n d (periodicWord B H w k).length`, and full finite `DecimalDigits.columnSum` representation. Its conclusion is

```lean
DecimalQuantitativeMass.decimalLength (Lychrel196.step n) =
  2 * B.length + 2 * (k * w.length) + H.length +
    terminalCarry (periodicWord B H w 3) 0
```

The last term is the actual `rawGamma` used by the guard/quotient. Thus there is no need to reprove a generic realization, carry, or actual numeric-width theorem. `decimalLength_of_canonical` handles the input numeral; length four makes the repeated-band contribution a multiple of eight.

`rawPeriod_catalog_edge` already returns a listed `PhaseEdge` whose source is the literal `w`, target is the literal `rawPeriod B H w`, clock is the actual `rawGamma B H w`, and carries are `some (leftEntry B, rightEntry B H w)` exactly for all-nine input, otherwise `none`. Existing quotient validity/catalog closure supplies valid successor words and period membership. There is no need to choose an abstract clock or forget the exceptional carry labels.

## Proposed precise modular and finite-chain interfaces

These are candidate interfaces, not checked declarations. They can avoid introducing another state machine.

```lean
theorem periodicWord_length_mod_eight (B H w : Word) (k : Nat)
    (hlen : w.length = 4) :
  (periodicWord B H w k).length % 8 = (2 * B.length + H.length) % 8

theorem quotient_width_mod_eight (B H w : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hlen : w.length = 4) :
  (2 * (quotientOuter B H w).length + (quotientCenter B H w).length) % 8 =
    (2 * B.length + H.length + rawGamma B H w) % 8
```

For a finite chain, take three sequences `B H w : Nat -> Word` and `N : Nat`. Assume for every `i < N`:

* `B i`, `H i`, and `w i` are bounded by eighteen; `(w i).length = 4`;
* `B (i+1) = quotientOuter (B i) (H i) (w i)`;
* `H (i+1) = quotientCenter (B i) (H i) (w i)`;
* optionally the literal next-period equation when packaging an actual quotient path; the width telescope alone does not use it.

Write `I i = 2*(B i).length + (H i).length`, `D = ((List.range N).map fun i => exponentDelta (B i) (H i) (w i)).sum : Int`, and `G = ((List.range N).map fun i => rawGamma (B i) (H i) (w i)).sum : Nat`. The strongest basic finite-path equality is

```lean
(I N : Int) + 8 * D = (I 0 : Int) + (G : Int)
```

If `I N = I 0`, then `8 * D = (G : Int)`, hence `G % 8 = 0` and `D = ((G / 8 : Nat) : Int)`. A full return of `(B,H,w)` supplies the width equality but is stronger than needed. The zero-length path is permitted; no unnecessary positivity premise should be added to the arithmetic result.

If a concrete natural exponent sequence also follows the original quotient exponent update and each input exponent is at least three, sum the existing `quotient_exponent_accounting` to identify its total signed change with `D`. Without those guards, describe `D` only as the sum of formal signed quotient increments, not an already realized all-time exponent trajectory.

Agent110 already supplies reusable `sumPrefix` telescoping lemmas. Whether importing that certificate-heavy closure merely for summation is worthwhile is an implementation choice. Reusing standard finite-list sum lemmas locally is enough; do not advertise a new generic telescope as mathematical progress.

## Combined head/phase/width projection

The complementary head scout `/root/verification_plan` reports the minimal exact head glue through unchanged `Agent8.canonical_step`, `terminalCarry_eq_actual_overflow` at `Q_3`, `periodicWord_head`, and `stripPeriodSuffix_outside`. The correct head is `(B ++ w).headD 0`, including when B is empty.

The intended projection is

```text
(B,H,w) |-> (w, (B ++ w).headD 0, (2*B.length + H.length) % 8).
```

Under the original valid/catalog hypotheses, prove that its actual quotient successor is an edge of the product graph, preserving the actual clock and all-nine carry labels. The width coordinate is an eight-fold lift: for each checked head/phase edge e and residue r, the target residue is `(r + e.clock) % 8`.

This gives a small compositional Lean specification. It avoids turning thousands of repeated width rows into the primary proof object. If exact equality with the archived reachable graph, counts, or SCC decomposition is later claimed, those are separate finite assertions requiring checks. The source theorem only needs a necessary-edge projection; graph cycles remain possible abstractions rather than constructed finite interfaces.

The archived width filter additionally writes reflected phases in global indices, `p[(L-1-i) % 4]`. Current `periodicWord` anchors w after B. Keep that origin convention explicit before asserting a literal reflected-phase identity for local w. The exact residue update above does not require such an identity. No new reflection theorem is proposed here.

## Original written method and saved result

The written method already states the same local equality and the intended cycle telescope:

```text
2|B'| + |H'| + 8 delta = 2|B| + |H| + gamma
8 sum(delta) = sum(gamma)   [on a finite-interface return]
```

The width filter starts from the fourteen-four phase `(14,14,4,4)`, every positive outer coefficient 1 through 18, and all eight residues. It advances the residue by the edge's clock. The archived JSON reports 7,024 reachable states, 11,664 edges, and a representative 16-step necessary cycle with eight overflows and conditional exponent gain one. Its payload SHA256 is `4623cb562b6ca63c70858b033431cbd84acfccbc30cb85f017b522bf1d15528a`. It explicitly says `finite_canonical_interface_lift: NOT_INSTANTIATED` and `infinite_existence_proved: false`.

Those are preserved computational results, not newly kernel-checked results. The proposed proof makes the graph a consequence of the actual quotient. It does not turn the saved representative into a finite-interface return or an infinite nonpalindromic orbit.

## Existing related results and scope separation

Agent110 scalar-certificate accounting, in the flattened files pinned above:

* `Agent110.Accounting.local_width_balance` is for the original two scalar-run certificate state and supplied local trimming witnesses: `width s' + 2*(dg s L + dh s L) = width s + gam s`.
* `totalGam_eq_twice_gains cert hv` proves `totalGam = 2*(totalG + totalH)`; `totalGam_even` and nonnegative gain theorems are present.
* `sumPrefix_difference` and `sumPrefix_cyclic_difference` already establish ordinary finite telescoping.
* `Agent110.Phases.valid_period_mod6` concerns scalar six-phase dynamics. `Agent110.CertificateBudget` and `Agent2Exterior` already have mod-nine clock constraints; the exterior `full_return_arithmetic` assumes the relevant full-return width and positive-clock premises.

These prove analogous accounting for different original states. They do not instantiate the period-four coefficient quotient or its factor-eight interface width. Conversely, this proposed scope should not reprove their scalar exterior arithmetic.

Agent6 exact source commit `f0e2097b82286128005ba81d8e50f2dca4e2d50b`, branch `research/agent-6/normalized-carry-accounting-20261016`, includes:

* `proofs/contributions/agent-6/normalized-carry-accounting-20261016/CertificateCarryAccounting.lean`, blob `c936414929bc44c775feb49bb05e1e6560903be0`;
* `.../NormalizedCarry.lean`, blob `338432fa1a0ffaee74f30f67d055840c9f4e940d`.

Read exact declarations `overflowBit_stateOuter`, `rowOverflowSum_eq_totalGam_of_bounded`, `checked_weighted_balance_totalGam`, and `checked_weighted_balance_gains`. They connect normalized scalar exterior observables to the original `gam` and Agent110 gain balance. Their checker-facing result has coefficient 18 times `(totalG+totalH)`, not the present period-four width modulus. Latest Agent6 proposed follow-on is exact scalar template-band guards. No claim conflict found with a period-four graph projection.

Agent414 source commit `2a3ce996cc7e100f13c90e41cb8b4599360b7adc` includes:

* `proofs/coordination/submissions/agent-414/bulk-period/Agent414BulkPeriod.lean`, blob `381948f4e85dbdd60f30f02c07658103ffcff8d2`;
* same directory `Agent414CyclicWordPeriod.lean`, blob `81a4635ef8a2c381fe8b9fe7157d6e174ff0dd70`.

The exact endpoints are `bulk_periodic_iff_dvd (n) (family : Fin 2) (phase : Fin 6) : Periodic n (bulkWord family phase) <-> 6 | n` and `six_dvd_of_bulk_path` from an original `ReverseClosure.Path (ArithmeticColumn n) (fun _ => 41) (bulkWord family phase)`. The generic lemma concerns injectively labelled cyclic words. Zero period is deliberately included, and zero-clock paths are shown possible. This is a different periodicity premise and a different clock; it does not establish period-four overflow-count divisibility.

## Ownership evidence and first action

Coordination snapshot inspected: `2045b6acfbcc6aa49920211bbf145b1095b59b4c`, 164 task files. Relevant issue61 delta inspected through comment `6226153210`; the head scout independently checked through `d8aab676` and found no exact current head/phase product claim. This is scoped evidence, not an assertion of exhaustive absence across every historical branch. Parent should perform the final delta check before claiming.

Relevant claim blobs inspected:

| Task | Claim blob | Status/scope |
| --- | --- | --- |
| Agent1 period-four phase catalog | `f5801223d5bbf0e44ee479d1d3b7400ba5950c88` | claimed; excludes generic DFA, whole-cycle existence, safety closure, scalar six-phase work |
| Agent6 normalized carry accounting | `e9298d76aa033f931c810072adacdc4aa6cee972` | reviewed; source f0e2097, explicitly excludes Agent1 periodic stripping |
| Agent6 coordinate audit | `e40e9109c9a848b066be13cded293d44eb128910` | reviewed scalar coordinates |
| Agent6 exterior coordinates | `6d62e1f787a5c9cb8b459bb5cf4e9bb6d687f591` | integrated scalar beta telescope |
| Agent110 exterior two-step | `486eb1460dab5cca752d312c623e2488c5d34ed4` | claimed scalar two-step nonreturn |
| Agent414 bulk period | `ee67edf47da8ebace9282c9966023e085c0a66e2` | active exact six-letter periodicity |
| Agent414 kernel boundary | `5988258c3c21e2df973ff008eb8d7a2588d0e285` | unrelated graph0 parse/kernel equality |

First concrete action after parent publishes a protected claim: freeze the current phase-catalog source dependency, agree on the head/phase edge type with the other author, and prove the two minimal residue lemmas from existing width theorems. Compose them with the actual head/phase edge. Add the exact finite-path/return equality as a downstream corollary, preserving signed increments and actual carry labels. Do not begin a new generic graph/cycle theory, scalar carry theory, or affirmative interface search under this scope.

The only semantic bottleneck beyond these arithmetic consequences is the actual graph projection and its coordinate conventions. Positive-clock return, literal ordinary trajectories for every step, full graph equality/reachability/SCC claims, and existence of a finite return each need their own corresponding hypotheses or proofs; none follows merely from width residues.
