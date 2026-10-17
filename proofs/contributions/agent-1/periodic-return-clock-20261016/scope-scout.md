# Positive clock and gain for exact period-four returns: source-only scope

Scout: Agent #1 specialist `/root/research_status/cap4_existing_theorems`.
Inspected worktree: `/workspace/p196-agent1-return-20261016`, HEAD
`04f7e37b11412c3053c1e0c29e4699019ee13dd2` at the final source read.
No Lean execution, mathematical search, source changes, Git mutation, external
message, or task claim was performed. This report is the only scout output.

## Conclusion and precise proposed endpoint

Yes: the existing checked exterior potential theorem supplies the missing
positive-clock premise, with stronger rate bounds. Only its adapter to the
already defined exact period-four `QuotientPath` remains to be checked.
No ordinary-number realization, exponent guard, phase catalog, graph rank,
safe-state hypothesis, primitive-period hypothesis, or finite-interface search
is needed.

Write `C = quotientClockSum B H w N : Nat` and
`G = quotientDeltaSum B H w N : Int`. Under

- `hp : QuotientPath B H w N`,
- `hv : ValidPeriodic (B 0) (H 0) (w 0)`,
- `hN : 0 < N`, and
- exact endpoint equalities `B N = B 0`, `H N = H 0`, `w N = w 0`,

the proposed consequence is

```
0 < C, 8 ∣ C, 8 * G = (C : Int),
1 ≤ G, 8 ≤ C, 16 ≤ N,
16 * G ≤ (N : Int), (N : Int) ≤ 32 * G.
```

These are source-derived proposed consequences, not newly compiled theorems.
The core rate adapter needs only return of the physical outside coefficient;
the final factor-eight conclusion additionally needs equality of endpoint
interface widths. Full tuple return implies both weaker conditions. This does
not imply `16 ∣ N`, exclude every positive-gain return, or construct a return.

## Existing exact interfaces and minimal missing adapter

1. `proofs/Agent1PeriodicValidity.lean:51`,
   `Agent1.Periodic.quotient_valid`, preserves the unchanged `ValidPeriodic`
   predicate through `quotientOuter`, `quotientCenter`, and `rawPeriod`, without
   safety or an exponent threshold. Induction on the path using its three
   successor equalities gives validity at every `i ≤ N`.
   The current `Agent1PeriodicQuotientPath.lean:17`
   `quotient_path_valid_catalog` already carries out this induction while also
   requiring catalog membership. There is no need to import that catalog for
   the proposed result: extract a catalog-free validity helper using
   `quotient_valid`, leaving that existing theorem unchanged.

2. `proofs/Agent1PeriodicOuter.lean:24`, `outside_bounds`, gives
   `0 < outside B w ∧ outside B w ≤ 18` from validity. Here
   `outside B w = (B ++ w).headD 0`; empty stored exteriors are covered.
   Its `quotient_outside_step` at line 58 gives, with the **actual** bit
   `e = Agent8.lastInput (periodicWord B H w 3)`,

   ```
   e ≤ 1 ∧ rawGamma B H w = Agent8.overflow (outside B w) e ∧
   outside (quotientOuter B H w) (rawPeriod B H w) =
     Agent8.nextExterior (outside B w) e.
   ```

3. `proofs/PeriodObstructions__70ce034b31b5b218.lean:209`,
   `Agent8.closed_path_bounds`, already proves

   ```
   (N : Int) ≤ 4 * Agent8.total (fun i => (overflow (p i) (e i) : Int)) N ∧
   2 * Agent8.total (fun i => (overflow (p i) (e i) : Int)) N ≤ (N : Int)
   ```

   under exactly `0 < p i`, `p i ≤ 18`, `e i ≤ 1`,
   `p (i+1) = nextExterior (p i) (e i)` for `i < N`, and `p N = p 0`.
   Set `p i = outside (B i) (w i)` and use the actual bit above at each state.
   Reuse this theorem; do not reprove its finite table, potentials or telescope.
   Its preceding `path_potential_bounds` also exists if a nonclosed endpoint
   estimate is useful, but is not required for the narrow return claim.

4. A short prefix induction identifies that `Agent8.total` with `(C : Int)`,
   using the exact `rawGamma = overflow` equality and the two recursive sum
   definitions. This is the second small adapter, not a new carry formula.
   The resulting bounds are `2*C ≤ N ≤ 4*C`; positive `N` forces positive `C`.

5. `proofs/Agent1PeriodicWidthPath.lean:58`,
   `quotient_path_equal_width_clock`, already gives `8*G=(C:Int)`, `8 ∣ C`, and
   `G=((C/8:Nat):Int)` from exact path and equal endpoint interface widths.
   Substitute this into the preceding inequalities; integer arithmetic gives
   `G ≥ 1`, `C ≥ 8`, and `16*G ≤ N ≤ 32*G`, hence `N ≥ 16`.

Direct imports can be only `Agent1PeriodicOuter` and
`Agent1PeriodicWidthPath`. The existing WidthLift registry declares a 20-module
dependency closure for these two roots (excluding `Std`); this is a static
dependency count, not a new build result. No new catalog or numeric dependency
is necessary.

| Existing source | Git blob | SHA-256 |
| --- | --- | --- |
| PeriodObstructions | `a89dda20e9a9b3452f7d0272b4fbd28f7d6ce119` | `83102a949036799a929ba72d74ce9d76bc2a11cb3adf61e0bc06b6013b22991a` |
| Agent1PeriodicOuter | `aa17a6398fb1ef5c5215771cdfb2c2992bfb9472` | `b30b54bce57542a649208c29900d511e9cc4b64429fb4a48f8da2a387d040678` |
| Agent1PeriodicValidity | `3c5673981d4c9a73a0ade71552f5867d8f73dd69` | `4652df468f38ed9696f5b68616f5bfd9225ab6f377a4d449289d8c2ad65b0e52` |
| Agent1PeriodicWidthPath | `ad3cee7e70fddbf0220c66313d8421e99f90678b` | `e97afd670460a3df90e836360fed59797cb60b339ee63e42d51de826c46a2241` |

The current scoped registry explicitly is not a repository-wide accepted
catalogue. Its older combined-review-pending text is not a fresh status claim;
root/reviewer own publication and current clean-build receipts. This scout
rechecked declarations and source identities, not Lean validity.

## Comparison with existing Agent2, Agent110 and Agent6 results

- `Agent2Exterior.full_return_arithmetic`,
  `proofs/ExteriorCharge__52cbb237030a07b3.lean:411`, blob
  `3020c27a4f65aa5c59a76d2facecc6739fc25d00`, **assumes** `0 < H`,
  `H % 9 = 0`, `2*(dg+dh)=H`, `2*H ≤ p`, and `(dg-dh)%9=0`. It concludes
  `18 ∣ H` in remainder form, `H ≥ 18`, `p ≥ 36`, and coordinate mod-nine
  conditions. Its scalar charge and width premises do not follow from an
  arbitrary four-site period. It does not discharge the requested positivity.

- `Agent110.CarryBudget.certificate_carry_budget_of_positive`,
  `proofs/CertificateCarryBudget__5307cef97cfab646.lean:147`, blob
  `08391617ca35f23ad89d9c6a4a98e7cb89a70741`, already proves
  `0 < carryCount cert ∧ 2*carryCount cert ≤ cert.P ∧
  cert.P ≤ 4*carryCount cert` from original scalar `Agent109.Cert.Valid` and
  initial exterior positivity. `Agent110.Consequences.total_carry_budget`,
  `CertificateConsequences__799ad43db1806ce1.lean:56`, blob
  `2df708284873ad036aeebfa14f602a8fc2452314`, expresses the same result for
  integer `totalGam`. These are close prior analogues and must be credited.
  Their original state has scalar `c,B,A,C` and a different `LocalOK` contract;
  there is no existing conversion of arbitrary period-four paths to it.
  Agent8's theorem is already the representation-independent endpoint needed.

- `Agent110.Accounting.totalGam_eq_twice_gains` at line 267 of
  `CertificateAccounting__ad0d1bd9b0242036.lean`, blob
  `79bf1fdfebabcf95dee96698be9aab3747c2599a`, gives
  `totalGam = 2*(totalG+totalH)` for that scalar certificate. It does not replace
  the exact factor-eight identity already checked for the period-four quotient.
  `Agent110.CertificateSaturation.period_at_least_forty_two` and
  `saturated_period_constraints` in `CertificateSaturation__80df3f83acb87b5d.lean`
  (blob `e90960e42b165e7c328935406968ceaff0e409be`) need the scalar SixPhase
  hypothesis, with saturation additionally needed for the period-72 conclusion.

- Agent110's global exterior investigation does **not** supply general
  acyclicity. `Agent110.RadixExterior.witness_observation_return`,
  `witness_not_state_return`, `no_autonomous_radix_factor`, and
  `no_overflow_strict_radix_observable` in
  `RadixExterior__b76295884106f975.lean`, blob
  `ce1942cadb6c3be3928ac847f16e1b9954482bce`, establish limits of a particular
  observable, expressly distinguishing its return from a state return.
  They neither rule out nor prove the proposed positive-clock adapter.

- Agent6's checked `P196.Agent6.no_reversal_invariant_strict_potential` and
  `no_strict_additive_potential` in
  `ExteriorPotentialObstruction__ccf419f4e5eece0c.lean`, blob
  `a257f462a715d2738a9e42927e0f03a473d394b8`, likewise rule out certain
  potentials for the original scalar exterior map; they do not rule out the
  existing carry-budget potentials, whose decreases are charged to overflow.
  Later Agent6 coordinate and certificate accounting remain scalar. The prior
  pinned scout `periodic-width-next-scope.md` identifies published
  `overflowBit_stateOuter`, `rowOverflowSum_eq_totalGam_of_bounded`,
  `checked_weighted_balance_totalGam`, and `checked_weighted_balance_gains`
  at commit `f0e2097b82286128005ba81d8e50f2dca4e2d50b`, source blobs
  `c936414929bc44c775feb49bb05e1e6560903be0` and
  `338432fa1a0ffaee74f30f67d055840c9f4e940d`. Their checker balance ends in
  `18*(totalG+totalH)`. Those newer objects are not in this worktree's object
  database, so their exact-source comparison here is inherited from that
  earlier pinned scout plus the current task record, not a fresh blob read.

## Existing ordinary and symbolic growth alternatives

The numerical route is possible in principle but introduces avoidable bridges.
There is no need to establish a finite guarded exponent lift for this claim.

- `P196.Agent12.FixedTarget.step_strictly_increases` and
  `orbit_ge_seed_add_time`, `FixedTarget__48ad6589a34c7bc6.lean:34,40`, blob
  `da2990f6492dc7fdd49584200dc32bdfde84640b`, already prove strict ordinary
  reverse-and-add growth and `n+t ≤ orbit n t` for every positive seed.
- `Agent112.Admissibility.stepWord_strict` and `no_bounded_width_orbit`,
  `SymbolicGrowth__60274c3f3418dae4.lean:25,43`, blob
  `e6ea91c07f9600df656cd6d8193623ce34c659c1`, provide symbolic evaluation
  growth and a bounded-width obstruction. Their `stepWord` is Agent109's
  implementation. Do not silently substitute Agent8's implementation: a
  compatibility bridge and a finite quotient-to-word orbit lift are required.
- Original `DecimalWidthGrowth.width_lower_bound` and `numeric_width_bounds`
  in `LychrelDigitSums__75febdc48f0ca802.lean` give all-time canonical width
  growth. Blob `8a865176625283648a8a20dd2411ed77670eb0a2` also contains
  `FoldedDecimal.step_eq_word_value` at 1557 and
  `ReverseAddInverse.same_width_step_eq_iff_pair_sums` at 3833.
  Equal column-sum words determine the **next** integer, not the input integer;
  the latter theorem explicitly records 196 and 295 as different inputs with
  the same pair word and the same next value 887.
- `periodicWord_realizable` supplies a positive canonical realization at every
  positive exponent, and the existing `actual_step_representation` in
  `Agent1PeriodicZeroNumeric.lean:102` supplies the full arbitrary-word step
  representation. Neither alone gives the guarded finite quotient path lift.
  They should be reused if such a separately scoped lift is later needed.

## Prior written result and ownership

The original period-four `periodic_bulk_followup/METHOD_AND_PROOF.md` section 4
already proves positive overflow and positive exponent gain for a returned
normalized state: if every overflow is zero, the positive outside coefficient
strictly increases by `a' = 2*a+b`. Its blob is
`5c5f94c66d6c3adb0288b610f748fcbed32b115c`, SHA
`45c34243ff0eef9fb30ef91e2d43ae933a77e4ca4d0b4bd307e9f0c259781559`.
The argument appears inside the safe-cycle discussion, but its overflow
positivity step does not use safety. The proposed Lean result formalizes and
quantitatively strengthens this prior argument using the existing rate bound;
it is not a new discovery of positive gain.

That same document ends: “The sibling `../periodic_interface_followup/` owns
the subsequent finite exterior/center lift attempt and is outside this bundle.”
STATUS and OUTCOMES repeat that reservation. Earlier bounded ownership scouts
found no recovered implementation or release; absence of a directory is not a
release. This proposal excludes affirmative finite-interface lifting/search,
safe cycle existence, and arbitrary abstract graph realization.

Current local coordination records were read at exact commit
`d1e135d56d36cdb61fdd81069ff907a6640e989f`:

- Agent6 coordinate dynamics: INTEGRATED; certificate coordinate audit and
  normalized carry accounting: REVIEWED. Their explicit exclusions preserve
  Agent1 periodic stripping and Agent115 rho-cycle/overflow work.
- Agent110 phase-six two-step exact exterior return: CLAIMED, no published
  Lean result in the record. Preserve this all-width scalar return task.
- Agent2 first-hit-eleven: CLAIMED; overflow fibers: ACTIVE. Both are distinct.
- **Agent115 rho-cycle balance: ACTIVE**, published checkpoint
  `5cacefb3c26e8c0ca7516cb49655485e35beea46`. Its target is a rational
  high-observation recurrence for original scalar
  `P196.Agent7.Finite.outerNext` on permitted nonneutral even phases, followed
  by a cycle telescope and necessary high-side overflow. The record explicitly
  classifies its source as WRITTEN-DERIVATION + FINITE-TESTED, with Lean target
  Prop definitions only, not Lean-checked or accepted. Do not reprove or claim
  that recurrence/telescope. The proposed exact period-four `QuotientPath`
  adapter to already-checked Agent8 bounds has a different original state,
  broader period words, and a distinct factor-eight gain endpoint.
- Agent1 return-core: current claimed path/catalog/component restriction;
  its listed target does not include the catalog-free positive-clock bound.

No equivalent exported period-four adapter was found in these inspected
sources. This is a scoped source/status comparison, not an exhaustive theorem
equivalence or current remote ownership certificate. Root reported a later
coordination delta check through `d63029eff5cbcf16af04bd615604ccd329bb9433`
and the posted clock-scope proposal `issue61#6226742622`; this scout makes no
claim of independently reading that later delta or obtaining a claim receipt.
Proceed only under root's new claim, then compile and independently audit the
small adapter and its exact existing dependency closure.
