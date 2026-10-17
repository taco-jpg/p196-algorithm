# Constant-nine full quotient return: source-only scout

Agent #1 specialist `/root/research_status/numeric_bridge_review`, 2026-10-17 UTC. Sources read in `/workspace/p196-agent1-reduced-core-20261017` and the preserved source archive. Only this report was written. No Lean execution, new proof, mathematical experiment, cycle search, new claim, Git mutation, or external message was performed.

## Conclusion and preferred next obligation

The useful bounded next task is a **conditional nine-cycle safety adapter**, before attempting a center obstruction. No equivalent checked period-four endpoint was found in the inspected declarations or adjacent current claims. The exact proposed endpoint is:

```text
quotient_cycle_nines_positive_seed
  (B H w : Nat → Word) (N : Nat)
  (hp : QuotientPath B H w N)
  (hv : ValidPeriodic (B 0) (H 0) (w 0))
  (hw0 : w 0 = [9,9,9,9]) (hN : 0 < N)
  (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) :
  ∃ n, 0 < n ∧ Lychrel196.IsLychrel n
```

There is no supplied safety premise. A useful companion conclusion is `∀ i, i<N → safePeriodic (B i) (H i) (w i)=true`. These are proposed statements, not proved or compiled in this scout. They reuse the already checked conditional same-seed cycle realization. They construct neither a full return nor an unconditional ordinary Lychrel seed and do not enter historical affirmative interface discovery.

The source supports this narrow route: the actual nine phase can go only to zero, nine, or eighteen; zero and eighteen are absorbing phases. A supplied return to nine therefore supplies nine at every finite cycle state. Every canonical realization with a positive nine-band exponent has an odd pair column, so it cannot be a palindrome. Apply that observation to the existing same-seed actual-cycle realization, including time zero. Alternatively, derive each finite state's `safePeriodic=true` from its represented successor and apply the existing safe-cycle theorem unchanged. The latter explicitly discharges the parent's requested Boolean safety premise.

A separate **unproved longer investigation** is whether every positive original-valid full tuple return initially at nine is impossible. No such exclusion or actual full-tuple counterexample was found. The new `quotient_return_reduced_core` deliberately leaves component129 and component8; it supplies no finite-center contradiction. The new conditional seed adapter does not depend on settling that question. If a future no-return result were proved, its catalog corollary would remove129 while retaining explicit initial catalog membership and leaving8 untouched.

## Exact numeric and safety route

`Agent1PeriodicCycleNumeric.lean:22`, `quotient_cycle_actual_orbit`, already takes precisely hp, hv, positive N, and all three endpoint equalities. It supplies one schedule with k0=2*N+3 and k(t)≥3 at every t, then **one positive ordinary seed n before every time index**, and original Canonical/full in-range column representation of `orbit n t` by the tuple at t%N. This is the main existing endpoint to reuse; there is no need to reprove guarded repetition, positive clock gain, generic certificate soundness, or a finite-to-infinite uniformity principle.

`LychrelDigitSums__75febdc48f0ca802.lean:780`, `DecimalDigits.palindrome_value_iff`, states that bounded canonical digits with a nonzero most significant digit give a palindrome exactly when reflected digits agree. At any column whose pair sum is9, such agreement is impossible: it would make twice one natural digit equal9. For `periodicWord B H [9,9,9,9] k` with k>0, index `B.length` lies in the first nine band. The source does not currently export this specific nine-band nonpalindrome wrapper; a small local indexed-list helper can supply it without a new generic arithmetic theorem. It requires the actual original Canonical and all-column representation premises, not an arbitrary symmetric list.

`IntrinsicSeam.numeric_highNine_input_nonpalindrome` (IntrinsicSeam__32ebb990c7babba0.lean:138) illustrates the same original parity argument but requires an adjacent high coefficient followed by9. A nine band alone does not supply that adjacency. Do not import or apply this stronger-premise theorem to a general valid nine tuple; use the existing `palindrome_value_iff` directly.

`safePeriodic` (Agent1PeriodicSafety.lean:16) rejects exactly either all coefficients in B++H++w being≤9, or outside11 with the whole alphabet restricted to0/11. Its convenient `safePeriodic_spec` is private. The public `safePeriodic_iff_not_bad` at42 covers every k>0 and nonempty w. The public `safePeriodic_iff_next_not_palindrome` (Agent1PeriodicSafetyNumeric.lean:14) translates the Boolean into **next-output** nonpalindromicity for every supplied Canonical/full-column realization.

Hence an explicit finite-safety proof can use the existing cycle realization at i and i+1: the successor's period is nine by persistence, so its indexed odd pair sum excludes a palindrome; the public numeric safety equivalence then gives `safePeriodic (B i) (H i) (w i)=true` for each i<N. This route automatically handles the final wrap because the existing realization uses residues modulo N and all three full-return equalities. `quotient_cycle_safe_positive_seed` at51 then gives a positive all-time witness. It selects the successor seed because the generic Boolean criterion concerns next outputs. A direct proof from the same realized nine band at every t can instead retain the original positive seed n: `Lychrel196.IsLychrel` at line131 includes time zero. Either route has the requested existential conclusion; the explicit Boolean companion plus reuse of the safe-cycle endpoint makes the safety discharge reviewable.

A source nine band alone excludes palindromicity of the **represented input**, but does not by itself certify its next output. The required extra fact is the returned cycle's nine successor phase. No unconditional forward preservation of safePeriodic is asserted by the existing safety module or proposed here.

First action after a fresh accepted claim: formalize the finite phase-persistence adapter using the three actual nine successors plus zero/eighteen absorption. Its minimal phase hypotheses can be only hp, w0=nines, and wN=nines, yielding `∀i≤N, wi=nines`; positive N, full closure, and initial validity are used later by the existing cycle-realization endpoint. Then add the local indexed odd-column observation and the conditional finite-safety/numeric wrappers. This is a bounded source adapter, with no catalog/SCC decision or interface enumeration.

## Exact existing periodic interfaces

| Declaration | Precise existing content |
| --- | --- |
| `rightEntry_nines`, `Agent1PeriodicNines.lean:26` | Under `Bounded B 18`, `rightEntry B H [9,9,9,9] = terminalCarry H (leftEntry B)`. The center is scanned with its genuine incoming carry. |
| `nines_entry_bits`, same file:34 | Bounds both actual incoming carries by one, using bounds18 on B,H. |
| `rawPeriod_nines`, same file:44 | The raw period is `List.replicate 4 (18 - 9*(leftEntry B + rightEntry B H [9,9,9,9]))`. It preserves the actual whole-word terminal clock internally and introduces no independently selectable bits. |
| `rawPeriod_eq_phaseImage`, `Agent1PeriodicPhase.lean:62` | Away from four nines, the period update equals `phaseImage w (rawGamma B H w)` under coefficient bounds and length four. A constant-eighteen specialization at clock0/1 can support the preliminary persistence reduction; no standalone all-time eighteen phase theorem is needed. |
| `rawPeriod_zero`, `Agent1PeriodicZeroPeriod.lean:50` | The constant-zero phase is preserved for bounded B,H. |
| `QuotientPath`, `Agent1PeriodicWidthPath.lean:17` | All three literal successor equations and used-source bounds/period lengths, not just phase graph edges. |
| `quotient_path_valid`, `Agent1PeriodicReturnClock.lean:25` | Initial original validity propagates along every supplied finite exact path. |
| `quotient_return_clock_gain`, same file:105 | Positive full return forces positive G, actual clock sum8G, signed exponent gainG, and16G≤N≤32G. It does not give a center obstruction or a nine-run ancestry law. |
| `quotient_return_component_constant`, `Agent1PeriodicReturnCore.lean:25` | Full tuple return and explicit initial outerCatalog membership imply constant component label throughout i≤N. |
| `quotient_return_reduced_core`, `Agent1PeriodicReturnReducedCore.lean:18` | Same full-return hypotheses, positive N, original initial validity and catalog membership now leave one constant label in[8,129]. |

The total component definition literally assigns phase9 to129 (`Agent1PeriodicOuterRank.lean:19`), zero to131, and eighteen to130. Its currently exported converse is only the new label130→eighteen theorem. A label129→nine converse plus initial nine catalog membership could turn existing component constancy into phase persistence, but that route imports the large catalog/rank closure. It is not a center-obstruction theorem and should not become a standalone theorem-count exercise.

## Preliminary phase reduction and the separate center question

The existing local formula has only three possible nine-phase outputs: zero, nine, eighteen. Its nine output corresponds to actual incoming carry sum one. The source phase rules make zero and eighteen absorbing phases. Consequently the natural preliminary obligation for a supplied positive return to nine is:

```text
∀ i≤N, w i = [9,9,9,9],
∀ i<N, leftEntry (B i) + rightEntry (B i) (H i) [9,9,9,9] = 1.
```

This is a proposed small path adapter from existing rules; it was not proved or compiled here. It should retain arbitrary input sequences beyond N and all finite endpoint conditions. It is **conditional on the supplied return**, not unconditional nine persistence. In particular, the historical checked finite probes reach nine at time21 and then zero at22 or26 (`METHOD_AND_PROOF.md:188`). Those retained observations are source evidence against assuming arbitrary nine states persist; they are not full-return counterexamples and were not rerun.

The second displayed condition says the finite center sends its actual entering bit to the opposite bit. `rightEntry_nines` supplies the exact finite-center scan. This identifies a useful constrained center regime but does not show that it cannot recur. A proof must establish a changing quantity or a finite center interface restriction that survives maximal stripping and both actual overflow cases. No such monotone quantity or checked center obstruction was found.

For a separate future obstruction investigation, after its own accepted scope: specialize the existing raw-center zipper under the two mixed-carry orientations and actual clock, retaining the literal normalization of H and the exact stopped stripping result. Try to obtain a finite-center obstruction under those exact premises. Do not start by postulating generic nine-run survival, inventing a free boundary carry, assuming a length decrease, or enumerating an unrestricted interface graph.

## Center and carry APIs available for that action

`Agent1PeriodicDigits.lean:14–25` defines the actual entries and digit blocks. In particular `centerGuardDigits` is `fixedDigits H (leftCarry B w) ++ fixedDigits w.reverse (rightEntry B H w)`.

`Agent1PeriodicGuard.lean:89` defines

```text
zipperCenter U C V g = pair (U ++ C ++ V.take g).
```

The third conclusion of `raw_blocks_eq_zipper` at217 identifies this expression with the literal rawCenter; `raw_block_lengths` in GuardFacts:14 gives length `H.length+8+rawGamma`. The raw center is symmetric and its odd middle is even by the already checked GuardFacts/Parity modules. These formulas include empty H and both parity/overflow branches.

`quotientCenter` is the maximally stripped raw center. `stripPeriodCenter_decomposition` at133, `stripPeriodCenter_maximal` at142, and `stripPeriodCenter_length` at148 preserve the exact number of whole mirrored periods removed. `stripPeriodCenter_length_le` only compares the stripped result with its **raw input**, which already grew by8+gamma; it does not assert `quotientCenter.length < H.length` or any temporal decrease. Odd-center parity and symmetry are available but are not a recurrence obstruction by themselves.

The original `IncomingCarry` supplies carry concatenation, actual-interval correspondence, bit boundedness, `carryIn_ne_iff`, `carryIn_eq_of_nonNine`, and `carryIn_nines` (lines37–117). `CarryTransferNormalForm.carryIn_last_nonNine` at27 and `rightmost_nonNine_transfer` at42 give a finite center's transfer class from its last non-nine coefficient. These are already proved generic facts and must be reused if helpful. They do not assert how that distinguishing center coefficient evolves under the next quotient.

Several tempting shortcuts have mismatched hypotheses:

- `RunAncestry.descendant_step` explicitly requires coefficient0 or18. The new EighteenBand/Track argument does not apply to coefficient9. No generic nine-run ancestry/population theorem should be reproved within this scope.
- `OverflowNormalizationNine.normalized9_low_after_three` concerns the special `normalizedZero` whole-word map with overflow and its **outside** coefficient9. A repeated internal nine band does not supply those premises.
- `Agent107.PartitionMass.partition_collision_mass` is an exact one-step partition identity with actual seam corrections. Its source explicitly disclaims persistence; it does not give a nine-center descent inequality.
- The positive full-return clock gain is a global necessary constraint. It does not force the two mixed-carry orientations or center trims to obey an unproved temporal balance.
- A nine band does not mean the entire word has coefficients≤9. Next-output safety cannot be inferred or refuted from the period alone. The preferred conditional safety target uses the additional proved successor-nine fact; the separate no-return target should not silently add an all-word bound.

## Scope, ownership, and actual source comparison

Fresh coordination snapshot `b977f99f5a61e68679d492040d0c429d44696168` had242 task records, an untruncated recursive tree, and no inspected target matching constant-nine full-return/center obstruction. Task targets were screened and the adjacent records read. The readback advanced to `1dba239473ceb1da69a25727b8f58e652f3b7022`; the sole changed task was Agent105's ceil-half palindromic suffix realization, whose exact target was read and is unrelated. Issue61 page9 was inspected through comment6228131461; page10 was empty. A fresh159-branch listing contained no nine-return branch. This is bounded targeted review, not proof of absence of all unpublished work.

Relevant actual source heads:

- EighteenReturn branch `5e67f08231c1973cb4908c167dbd8e08b3ee50fa` (parent reports PR170/source1c655 and checked evidence). This scout reads/reuses the source without claiming a new execution.
- ReducedCore branch `e84dfed51f9dfd48995ddc4920f5bf2bd6b80f82`; its theorem explicitly preserves129 and8. Parent/independent full verification is separate.
- Agent418 multiblock source checkpoint `b6c98af6f783f82b24707424721c33638f981270`: the actual submission tree and declarations were read, including `Agent418ActualCarrySuppression` blob `1c5de9f361539f14d2780aad75eb8a69dbfca7fa`. Its complete-window theorems assume observed saturated three-column prefixes of one canonical ordinary orbit; they constrain the fourth coefficient and corresponding incoming carry. `Agent418TwoBlockWitnesses` supplies64 finite16-step control witnesses. These are not a constant-nine full center/exterior return theorem.
- Agent12 branch `4ca35f4707cce305c3b08a07411d56f05ba4f93f`: actual `GuardPreservation.lean` blob `01fd4c037cefd05e3a28faae7f3cbf9c39cb292d` was read. It states a WIP seven-step guard-preservation counterexample target and explicitly omits a proof. Its middle `[1,3,16,3,1]` witness is not a nine-period full-return theorem.

Keep Agent418's active multiblock/continuation claims (blobs `cece5c4ce4fb6ea366e97e7934734c75c5639355`, `aa2047b6d9325f9deff3f7372f27efe9ebe36c4c`), Agent8's lower-width potentials (`c8e850bd4d99f6b09dd853eb3b6d5f20de06cd02`), and Agent7's population-renewal scope (`caf4e64b9730b3deb85ed4e831a225747e8516b3`) untouched. Neither cap4 nor verification_plan knew of a separate checked nine-center obstruction; their responses are supporting bounded-census information, not an ownership release.

The original METHOD blob `5c5f94c66d6c3adb0288b610f748fcbed32b115c` already states the exceptional nine carry rule at44–46, distinguishes mixed-carry persistence from exits to zero/eighteen at56, and reserves affirmative finite exterior/center lift discovery to `periodic_interface_followup` at212. No release was recovered. The preferred fresh task should own only the conditional phase-persistence/automatic-safety adapter above, exclude discovery/solver work and component8, and invite equivalent source/ownership pointers through the parent relay. A center obstruction would be a separate investigation. The already completed CycleAdapter scope expressly requires supplied finite safety; replacing that hypothesis for the returned-nine case is the narrow remaining adapter, rather than another generic soundness criterion. Historical METHOD lines168–176 already state the positive-gain safe-cycle criterion and remain the correct attribution. The inspected Agent17/Agent217 uniformity work and Agent105 finite-return endpoints do not supply this nine-phase conditional safety specialization; no fixed-seed quantifier is moved outside a finite-horizon family here.

## Dependencies and exact pins

For the preferred conditional adapter, static DFS of CycleNumeric+Nines+Phase gives exactly32 inherited modules: the existing CycleNumeric30 plus Nines and Phase. All32 actual source SHA-256 values match the inspected scoped pins. ZeroPeriod, full canonical representation, positive realization, ReturnClock, and the public Boolean/numeric safety interfaces are already in that union. One new combined module would make33; splitting phase and numeric adapters into two new modules would make34. No OuterCatalog, OuterRank, ReturnCore, ReducedCore, IntrinsicSeam, or RunAncestry import is needed. This is source-derived dependency accounting, not a compiler result.

For the separate preliminary/center route, static DFS from the current scoped registries gives21 inherited modules for the preliminary local phase/path reduction using Nines+Phase+ZeroPeriod+WidthPath; adding the already available ReturnClock/validity route gives23. CarryTransferNormalForm would add one small module if its optional last-non-nine interface is needed; IncomingCarry is already present. The existing full ReducedCore closure is48 and is unnecessary for a catalog-free constant-nine obstruction. Exact final dependencies cannot be settled before the missing center argument is known. These counts are source-derived, not compiler results.

| Source | SHA-256 |
| --- | --- |
| `Agent1PeriodicCycleNumeric.lean` | `4cbf4ee50c819e71ee09d108ab62fd703af1287507b969988a09e61b3fe2c527` |
| `Agent1PeriodicSafety.lean` | `d779d12e1ab558bd9135840cbe562ef8a778938e7260a70c3ec1032158b2b979` |
| `Agent1PeriodicSafetyNumeric.lean` | `b874515ae6ea49613d82eb2b1e0f3cd2f433e13a90592c7b0a37645aebd53c38` |
| `LychrelDigitSums__75febdc48f0ca802.lean` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` |
| `Agent1PeriodicNines.lean` | `b8aae1033e8e90c78f48888ea698e5d345c21e6b99970842dc5a9f3341cd193c` |
| `Agent1PeriodicPhase.lean` | `705c139614ffd4f9f20a305f7c4bff20059da0c7fa127ca180ff8a88397a51ce` |
| `Agent1PeriodicZeroPeriod.lean` | `3761744f62cabdf25cf69f8e2990ce81eec9ac75cfb2273a5e80974304795a8a` |
| `Agent1PeriodicCenterStrip.lean` | `566c7c5eac1fa54b98a9150a21f7ac61c403d8b0391b7aa92c1dbdea51c300c3` |
| `Agent1PeriodicReturnReducedCore.lean` | `2b08587ecb897310fbc83ecb9e0b6b0b219f671f3490d3b39f8e74ca2f5eb952` |
| `CarryTransferNormalForm__676dbc9ce8fd47d4.lean` | `1aedb44d61369b9e1819c53e63b0acbb898e1990245e219d86c848fa309f38aa` |
| `IncomingCarry__13645dd30c0ce73b.lean` | `d8a7cfa955204d03f454fcd1234ca66c2d15f361f9fbc036420dc91ac7579849` |

The preferred adapter has identified existing arithmetic and realization endpoints; its new finite phase/index composition still requires a fresh claim and checked proof. The separate center-obstruction uncertainty remains specific: **what finite center property prevents an exact closed sequence of mixed-carry nine transitions after maximal whole-period stripping?** None of the inspected existing declarations answers it. The phase-persistence reduction is preparatory, not the missing contradiction.
