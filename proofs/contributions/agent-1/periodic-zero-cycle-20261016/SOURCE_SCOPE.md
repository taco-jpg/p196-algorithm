# Source-only next bottleneck: exclude cycles after the period becomes zero

Prepared by the genuine Agent #1 specialist `verification_plan`, 2026-10-16. This is a proposal and dependency/ownership inspection, not a claimed scope or a new proved theorem. No mathematical experiment, Lean execution, proof-source change, Git mutation, or external post was performed for this scout. Parent may relay the attributed findings on issue61.

## Recommendation

Propose **acyclicity of the exact maximal period-four quotient on the zero-period branch**, with no safety assumption:

Let `Z = [0,0,0,0]`, and let

```
zeroNext (B,H) = (quotientOuter B H Z, quotientCenter B H Z).
```

For every original `ValidPeriodic B H Z` and every `P > 0`, prove that the P-fold iterate of this exact executable map is different from `(B,H)`. The map must be the already published maximal strip map, not a newly selected decomposition or a bounded search graph. As the necessary arithmetic prerequisite, prove

```
rawPeriod B H Z = Z
```

under the original bounds/validity. Then zero-period validity propagates by the existing `quotient_valid` theorem. A public final statement can use a small recursive `zeroStateOrbit` if no shared state-iterator interface is already present. The exact proposed negative endpoint is `zeroStateOrbit (B,H) P ≠ (B,H)`, universally in finite B,H and positive P.

This is one obstruction package, not ownership of general quotient cycles, interface searches, affine returns, or the historical finite-interface lift. No `safePeriodic` assumption is needed: the obstruction concerns actual arithmetic even if palindromes are continued.

## Why this changes the search

The retained `periodic_bulk_followup/METHOD_AND_PROOF.md` sections4–5 say:

- The eleven initial states are B=(17), w=(0,9,18,9), and H empty or one even coefficient0..18.
- Every recorded path reaches the constant-nine period at time21 and constant-zero period by time26.
- All paths reach the128-step cap; no cycle was found; all remain UNKNOWN.
- The proposed positive mechanism is a safe normalized-state cycle with nonnegative cumulative guard-domain bookkeeping and positive exponent gain.

The zero-period obstruction would show that **no longer search on these already collapsed zero-bulk paths can ever find the desired normalized-state cycle**. It would not show that any path terminates, reaches a palindrome, or has bounded interfaces. In particular, it must not relabel the eleven UNKNOWN ordinary trajectories as terminating.

This goes beyond observing no repetition in128 samples: it excludes every period, interface size, and zero-band exponent for the exact map. It does not exclude cycles retaining a nonzero bulk, unbounded-interface strategies, or other finite-seed mechanisms.

## Existing mathematics that supplies the obstruction

The essential global arithmetic is already proved, and must be credited/reused:

1. `DecimalUnboundedMass.digitSum_unbounded_after n hn B start` in the accepted original `LychrelDigitSums` proves that every positive ordinary decimal orbit has digit sums exceeding every bound arbitrarily late. There is **no** remaining carry-propagation premise. `not_eventually_bounded_digitSum` is its direct equivalent.
2. `DecimalUnboundedMass.iterPairs_wordSum` identifies actual indexed pair-word mass with twice the ordinary digit sum, with original Canonical and full finite hrep premises.
3. Original `Agent8.mass_append`, `mass_reverse`, and `mass_replicate`, or ordinary finite-list sum identities, supply the zero-period mass formula: mass of `periodicWord B H Z k` is `2*mass B+mass H`, independent of k.
4. Existing `quotient_step_bounded` gives exact actual transitions whenever the current exponent is at least3; `quotient_exponent_accounting` keeps signed deltas explicit; `quotient_width_balance` relates each delta to actual gamma.

Thus the new mathematical content is a precise obstruction in the original quotient, not a second unbounded-digit-sum proof or a new generic cycle sufficiency theorem.

## First concrete step and expected proof work

First prove zero-period stability **from the current stable-digit and zipper formulas**. For bounded B,H, incoming carries are bits; the four-zero block resets either bit to zero. Hence both stable digit periods in `Agent1PeriodicDigits` are four zeros. Apply `raw_blocks_eq_zipper` and the existing zipper formula, treating gamma0 and gamma1. The guard absorbs the shifted reflection, so an unguarded boundary-value assertion must not be substituted here. This requires no finite family scan and should be a small arithmetic/list proof.

The rest is finite cycle realization and mass bookkeeping:

- A hypothetical exact cycle has nonnegative total signed exponent increment by summing the already checked width balances; the interface lengths telescope and every gamma is nonnegative. Strict positivity is available from the existing exterior return bounds but is not needed for the negative argument.
- Choose an initial exponent large enough for all transitions in one cycle; the per-edge lower bound delta>=-2 gives a simple sufficient choice depending on P. Nonnegative total gain then keeps repeated traversals in the guard domain. Do not apply the next guard merely from the existing output exponent>=1.
- Reuse the separately proposed `ValidPeriodic -> Admissible -> valid_word_realizable` assembly for one positive ordinary initial realization. That pointwise theorem is symbolic_scope's scope, not this proposal's.
- Transfer the repeated exact list transitions to the original numeric orbit, and bound pair mass by the maximum of the finitely many interface masses in the cycle.
- Apply the original unconditional mass-escape theorem. A finite version using `DecimalQuantitativeMass.digitSum_escape_of_canonical` also suffices; no separate all-time safety theorem is necessary.

Expected effort is moderate: zero-period arithmetic and mass identity are small; the main work is exact finite-cycle/exponent bookkeeping and preserving the list/index/numeric bridge. A first compiled arithmetic checkpoint should be possible before the full cycle argument. Estimate roughly one substantial proof session (a few hours), subject to the actual bridge APIs. This estimate is not an execution result.

One bridge detail remains to select before implementation: current pointwise realizability returns original `Canonical n d L` plus finite hrep, whereas `Agent109.Compat.pairWord_orbit` uses the literal list `Agent109.pairWord n`. Prefer staying entirely in the original `FoldedDecimal.iterPairs_representation` / `DecimalUnboundedMass.iterPairs_wordSum` interface and proving only the required finite-list/index compatibility. Do not invent an unchecked equivalence or silently identify the weaker `CanonicalPair` with realizability.

The genuine independent realization scout subsequently confirmed that no direct Canonical/hrep-to-`Agent109.pairWord` endpoint was found in the current periodic closure. The alternative `Agent101.NumericFibers.canonical_to_list` plus `digitFn_digitPairSums` exists in a separate `Lychrel196Research` closure; do not pull that second foundation root in merely for this bridge. Original `FoldedDecimal.valid_word_realizable` already returns exactly the indexed Canonical/hrep input accepted by `iterPairs_wordSum`. The pointwise realization scout retains its own narrow scope and made no additional bridge claim.

## What is already proved or owned nearby

### Agent105 uniform return

Actual branch `research/agent-105/8f1107db019a-affine-dynamics` was read at `b312815ba86b086fa195768d685a2a0f355801be`; mathematical source is frozen at `87130870e6d17de1d9d2cd709395fbe664645c9b`. Current coordination at `2b3e165cb5cb46b5a610841307c72996ac345206` records REVIEWED, PR105 Ready. Exact declarations read:

- `Agent105.UniformReturn.uniform_return_wordAt`;
- `uniform_safe_return_wordAt`;
- `uniform_bounded_return` and `uniform_bounded_safe_return`;
- the documented final `uniform_integer_return` / `uniform_integer_safe_return` interpretation.

These derive one common positive return time1<=t<=4*A*s from a substantive **eventual return-existence hypothesis**. They do not exhibit any such return family. All closure/stability/head/width obligations are already discharged; proposing those again would duplicate completed work. The new zero-period negative endpoint neither reproves their theorem nor assumes the existence hypothesis it intends to exclude.

Exact blobs: `Agent105UniformReturn.lean`=`56af3389e169bf50592de52fc4f9246651efbfcd`; `Agent105UniformReturnPlain.lean`=`05db00e40e247715efb46b9efdc2ba089ad5ddab`; `Agent105UniformIntegerReturn.lean`=`496f694e39854b6545d784dc8a11418d789d76ab`; README=`a1b746c62794c35910aa893ac01c57528ea1772f`. Issue61 comments6225564304 and6225738576 supply the final attributed status. The newly proposed Agent105 help in6225709228 is a specific phase6 exterior source-to-boundary bridge for Agent110, unrelated to period-zero whole-word cycles.

### Agent102 static decisions

PR93 source `cba5dc441289bbed383972aa522a45c473879396`, reviewed branch head `69392ee406cd346f5a377056f18d7f1be74e760a`, already has eventual word/palindrome equality and exact tail Bool specifications. PR124 mathematical source `15d2e9cc9a6ed0ad68096b2c547c72f140087fb6`, reviewed head `9361e8a8d13c731a4004b08957f4cd543b3ae38f`, adds arbitrary-k compressed equality plus complete forall/exists static parameter decisions. These do not assert orbit time behavior. The new interval-union proposal6225680857 replaces prefix enumeration in static decisions; it is not the zero-period obstruction. No Agent102 code is needed for the recommended direct quotient proof.

### Agent4 separated zero gaps

Current exact tasks read: `agent4-separated-block-exhaustion-20261016`, blob `3306465a0c7b8ed936f594fbd012f4e247219719`, and `agent4-zero-gap-auxiliary-departure-20261016`, blob `6070945f7cb2f8019f40c14369c0757302325a1f` at snapshot5f67d283.

The former uses **separately CanonicalPair B,H**, an exact isolated-block decomposition, first zero-gap exhaustion and an ordinary bridge. The latter gives the exact criterion at gap0 and first disagreement with that auxiliary orbit within five further steps. Source publication was reported blocked; those theorem sources are not remotely importable merely from their status metadata. Latest issue6225700179 reports additional local checks but does not release ownership.

The proposed quotient result permits the original arbitrary bounded exterior B, uses exact maximal stripping, and excludes all periods of state cycles. It must not recreate Agent4's isolated-block recurrence, exhaustion time, postcollision disagreement, or reset classification. Notify Agent4 of this explicit distinction in the scope proposal; no claim of generic zero-gap dynamics ownership is justified.

### Existing repeatability obstructions

`Agent8.no_two_step_canonical_template_return` and `no_repeatable_six_step_canonical_template_return` in `ActualWordBridge`, the all-phase refinement, and `Agent109.Endpoints.no_repeatable_six_step_actual_template_return` concern the distinct complementary two-gap template. `PeriodObstructions` also has the exact modulo9 mass and lower/upper exterior-potential constraints. These are existing results, not missing work.

Original `ZeroExterior.fixed_outer_return_time_zero` rules out a fixed positive head followed by three zeros; it does not cover arbitrary period-zero interfaces B. `NeutralWidthBound.no_infinite_compensated_return` has its explicit special emission/tag hypotheses and is not an unconditional quotient theorem.

## Historical ownership: not known to be released

Original periodic METHOD ends: “The sibling `../periodic_interface_followup/` owns the subsequent finite exterior/center lift attempt and is outside this bundle.” STATUS repeats that assignment; OUTCOMES records `next_lift_owner`.

No implementation, matching source-map path, named current owner, current task, or available-history commit under that sibling directory was recovered. The existing Agent1 ownership-source-scout records the same negative result. This scout repeated the source-map/retained-ledger searches and `git log --all -- '**/periodic_interface_followup/**'`, which returned no entries. **That establishes neither that the historical task is currently active nor that it has been released.** Its status remains unresolved.

The recommendation is therefore an exact proposed obstruction with no equivalent current claim found, not a declaration that the entire future-lift lane is unowned. Parent should publish the narrow target, preserve the historical attribution, ask for any exact equivalent theorem/active helper, and obtain a fresh guarded claim before proof. No affirmative cycle search or finite exterior/center lift is included.

## Pins and dependency choice

Current source worktree inspected at `c74c9d1ca1fef5463738abac348a5d12eaab4a01`. The first import should be `Agent1PeriodicValidity`; add the separately checked periodic realization module only after it actually exists. If using the list numeric bridge, reuse original `Compat` unchanged. The unbounded-mass theorem is already inside the pinned `LychrelDigitSums`, not a new optional oracle.

| Source | Git blob | SHA256 when recorded |
|---|---|---|
| `Agent1PeriodicDigits.lean` | `6a6f02ae17d7aaa8e728a6588edf080c9ffd7ad5` | `dc6cc1dadb74c4927f0635107fdc1eb62cebac3038dea4e97ad4229fc8703eab` |
| `Agent1PeriodicGuard.lean` | `7c62748625cecbc277ddd5e01ffb17671e4db7a8` | `4ba3877f27250e066bbe19dd066b55fa667576281e8dc984334b9a9b82fcee91` |
| `Agent1PeriodicQuotient.lean` | `63bd5f4319f6a79924b7292db3eb82e0d027b26c` | `562ad271c282a8a246de344b5fa9ea7e96bd64f74098c3799c839853e792a9a4` |
| `Agent1PeriodicValidity.lean` | `3c5673981d4c9a73a0ade71552f5867d8f73dd69` | `4652df468f38ed9696f5b68616f5bfd9225ab6f377a4d449289d8c2ad65b0e52` |
| `LychrelDigitSums__75febdc48f0ca802.lean` | `8a865176625283648a8a20dd2411ed77670eb0a2` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` |
| `ActualWordBridge__7f032d27940694a8.lean` | `d3f49353f9970c610d818d8f5da78ad5c739e7df` | original byte-pinned source |
| `Compat__a87d4fe51356e8b5.lean` | `0279661cd41c62e8b1e8f7fe53d005a80f79dd71` | `73dca78232b0c2c048da4d1d182f84b31c0e95bab283fad603fd342bf38616e6` |
| Original periodic METHOD | `5c5f94c66d6c3adb0288b610f748fcbed32b115c` | `45c34243ff0eef9fb30ef91e2d43ae933a77e4ca4d0b4bd307e9f0c259781559` |
| Original periodic Python | `c7b87ad87287a7fafb6849c2e6cf9c4cd4ebe72a` | `122fcd390283f956f97d21327ec6cb9d4ae193e9bd3ab1b155bb65e1e61c2425` |

Relevant original theorem locations in `LychrelDigitSums`: `iterPairs_wordSum` around5142, unconditional unboundedness5226, tail version5255, explicit finite escape5403/5421. The original periodic METHOD is under `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/main_existence_attempt/continuation_pass/periodic_bulk_followup/`.

## Inspection scope and remaining prerequisites

Programmatically scanned the target/status fields of141 current task records available on the refreshed local coordination ref; read the targeted relevant complete claims and the remote delta through5f67d283, then the latest Agent105/102 records at `2b3e165cb5cb46b5a610841307c72996ac345206`. Read relevant issue61 content through comment6225746264, including Agent105's exact final uniform-return scope and new assistance proposal, Agent102's static interval proposal, and Agent4's current checkpoint. The absence of a duplicate is scoped to those inspected records and sources, not every unpublished local workspace.

Before execution: fresh claim/overlap check; finalized periodic realization API; exact list/index/numeric transfer selection; pin the final combined import closure. After execution: preserve all attempts, use official Lean4.19.0 `--trust=0`, print every new public theorem's axioms, audit complete theorem origins, and obtain independent fresh reconstruction. No claimed proof or computational outcome is attached to this report.
