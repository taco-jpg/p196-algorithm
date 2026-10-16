# Agent #5 repair-adoption: independent semantic review

**Date:** 2026-10-16. **Reviewer:** Agent #5's independent semantic reviewer, a supporting reviewer rather than a separately numbered repository worker.

**Verdict:** PASS for the exact repaired source and the scope stated below. No blocking mathematical defect, changed theorem contract, circular assumption, or inappropriate proof shortcut was found. The repaired sources establish finite overflow and moment absorption for the specified abstract exterior iteration. They do not establish a statement about all-time concrete integer reverse-and-add orbits.

This review supports the repair-adoption task claimed at coordination commit `b95eca7444656d69f01f85720e2d748b045d93b0`, task path `proofs/coordination/tasks/agent5-even-base-repair-adoption-20261016.json`. Repository `AGENTS.md` was read. The review was conducted in a separate local directory; the canonical checkout and other agents' lanes were not edited. Remote coordination and publication remain with the parent Agent #5.

## 1. Exact reviewed materials and evidence

The three imported dependencies were read from the checkout based at `4b4edf976b2c7a9ba1dad80636c0e21c66350325`. Their contents match the original package's dependency pins. The original two contribution files were recovered from `agent5-recovery/original/agent5_assumption_discharge`. The Agent #11 patch was applied independently in this review directory, then the resulting bytes were compared with the runtime reviewer's repaired tree.

| Material | SHA-256 |
|---|---|
| Original `InitialValidity.lean` | `5193c15275794f3d6f1415df8a6b7b180de3d0ce538fdd71925d706905335abb` |
| Repaired `InitialValidity.lean` | `7b398ebb1f48bf42f754979ab02093b0c6a16323aff5e90d772c8fb061b5f986` |
| Original `FiniteOverflow.lean` | `68a0a20cd6426ff51a05faa6405f4761ec2c77fe3e0bdbb4a78b9fb844aca031` |
| Repaired `FiniteOverflow.lean` | `4384f88ac757a22324eb53cba106b952930b61f32f04772c446705150fae130e` |
| Agent #11 repair patch | `646b2efd1126d9c88b08b5624e31dc80031760d814bc0570aa0a463b9a7a85f9` |
| `ExteriorClock__b2b9d37012d53747.lean` | `7158c8c7d07fab80c4212ba4c6c4b0a318ca22faee988c8d22eca45edfd439c5` |
| `GeneralCarryMass__ad1a2561147adc83.lean` | `688355dd1209dff4230d5fc7d9c3ce63efb3e2d3ec0037d53c8ec26a662f2138` |
| `GeneralMomentAbsorption__d6c541c17a8aa76f.lean` | `b62006f6ce106ac973865f24185a8391278286c1ddf23fdd5827acda0d3205ca` |

The repaired Git blobs are `adfcc154d43683fa8c07a6a9306f1aa734649f3b` for `InitialValidity` and `308e479acdce02c5c15117f88395bba1f8f392ef` for `FiniteOverflow`, matching the patch's destination identities. `contract-comparison.json` records the source identities, every declaration's contract hash, and the complete declaration comparison. `compare_contracts.py` reproduces this source comparison; it is explicitly not a Lean build.

The runtime specialist executed the package verifier, while this reviewer independently inspected the resulting sources, receipt, logs, axiom coverage, and hashes. Evidence is at `agent5-recovery/build-repaired-core-01`; `runtime-inspection.json` records this inspection. All five source modules match the independently reviewed source identities. The three dependency modules, two repaired modules, and generated axiom-audit module returned exit code zero under official Lean 4.19.0, commit `6caaee842e94`. All 47 contribution theorems have complete transitive axiom reports; every report is contained in `{propext, Classical.choice, Quot.sound}`. There is no `sorryAx`, custom axiom, or native decision oracle in those reports.

The original runtime log at `build-original-core-01/InitialValidity.log` reproduces failure of `split` beneath unreduced `let` bindings and failure to synthesize the concrete counterexample's `Decidable` instance. That run stops at `InitialValidity`; it should not be described as a successful original build or as a compiler run of original `FiniteOverflow`.

The source comments and original package reports retain their historical `BUILD_NOT_RUN` status. This new report supplies separate later evidence; those original historical statements should not be silently reclassified. The parent's canonical repository-verifier replay and coordination review are separate integration steps and were not executed by this semantic reviewer.

## 2. The repair preserves the exact mathematical contract

All **47 theorem statements** and **11 non-theorem declarations** are unchanged. The latter consist of ten definitions and the `State` structure. Imports, namespaces, the abstract transition functions, and the imported dependencies are unchanged. Exactly eight proof bodies change:

| Declaration | Proof-only repair |
|---|---|
| `rawExterior_bounded` | Reduce the existing `let` bindings before splitting the existing conditional. |
| `raw_head_cons_no_overflow` | Unfold the raw update, reduce its `let` bindings, explicitly select the existing zero-overflow branch, then simplify. |
| `raw_head_cons_overflow` | Explicitly select the existing nonzero-overflow branch before simplification. |
| `head_positive_step` | Expose the existing empty-word goal as `0 < c - m` before arithmetic automation. |
| `odd_base_phase_counterexample` | Simplify the existing phase and transition definitions in the concrete proposition. |
| `sharpStart_valid` | Simplify the existing concrete validity and positive-head proposition. |
| `sharpAbsorptionStart_valid` | Simplify the existing concrete validity and positive-head proposition. |
| `zeroHeadStart_valid` | Simplify the existing concrete validity proposition. |

No hypothesis was added, removed, weakened, or moved into a definition. No result was changed to assume the desired conclusion. A source scan of both repaired modules and all three dependencies found no `sorry`, `admit`, `native_decide`, `sorryAx`, `axiom`, or `unsafe` token outside comments. Existing finite `by decide` proofs remain ordinary Lean proofs, and the transitive axiom audit is the stronger evidence for the exported theorems.

## 3. Exact state space and hypotheses

All contribution declarations are in namespace `P196.Agent5.General.InitialValidity`. The base is `b = m + 1`, with `m : Int`. A state has fields `c : Int` and `B : List Int`. The transition is exactly

`step m (c,B) = (General.nextPhase m c, General.nextExterior m c B)`.

`orbit m s n` is structural iteration of that transition from `s`. It is not defined through a natural-number digit encoding or concrete integer orbit.

The initial validity predicate is precisely

\[
\operatorname{Valid}_m(c,B)\iff
0<c<2m,\quad c\ne m,\quad \forall x\in B,\;0\le x\le2m.
\]

The head is `B.headD c`: it is the first coefficient for a nonempty word and the phase for an empty word. Finite-overflow and uniform-absorption endpoints additionally require this integer head to be positive. Validity alone allows a nonempty word beginning with zero, so positive head is a substantive additional premise.

The general orbit endpoints explicitly require `1 ≤ m` and `∃ r : Int, m = 2*r + 1`. These express positive odd `m`, hence an even base. **Base two (`m = 1`) has no valid phase:** the only positive integer below two is one, which is excluded by `c ≠ m`. The results are therefore vacuous there; the nonempty stated domain begins at base four. They are not generally vacuous: decimal states such as `(2,[1,0])` satisfy the hypotheses, with compiled witness proofs.

Initial phase parity is unrestricted. In decimal the domain has the integer phases `1,…,17` except `9`; the eight usual even phases are a subset. The word may be empty, arbitrarily long, or contain a phase-valued suffix. No trimmedness hypothesis is required. There is no unit-phase, multiplicative-inverse, coprimality, periodicity, or closed-orbit assumption in the moment-absorption endpoints.

## 4. Exported endpoint interpretations

The table uses `s_n = orbit m s n`, `g_n = exteriorOverflow m s_n.c s_n.B`, `a_n = head s_n`, and

\[
M(c,B)=2\sum_{i=0}^{|B|-1}(-1)^iB_i+(-1)^{|B|}c,
\qquad q=2(m+2).
\]

Here `powTwo H` is the imported integer-valued recursion `powTwo 0 = 1`, `powTwo (H+1) = 2*powTwo H`. General orbit rows below have the explicit `m ≥ 1`, odd-`m`, and initial-`Valid` hypotheses unless stated otherwise.

| Export | Exact interpretation |
|---|---|
| `valid_step`, `valid_orbit` | Initial validity is preserved for every natural-number iterate. No validity or coefficient-bound premise is supplied for later times. |
| `overflow_bit_orbit` | Every computed `g_n` is either zero or one, from initial validity. |
| `residue_zero_orbit` | If initial `M(s) % q = 0`, then `M(s_n) % q = 0` for every `n`. Positive head is unnecessary here. |
| `residue_zero_after_overflow` | A supplied `g_j = 1` implies residue zero at every state `j+1+n`. Positive head is unnecessary here. |
| `decimal_valid_orbit`, `decimal_residue_after_overflow` | The preceding corresponding contracts specialized to `m = 9`, with modulus 22. |
| `head_no_overflow` | For one valid state and `m ≥ 1`, `g = 0` implies `head s ≤ m` and `2*head s ≤ head (step m s)`. Oddness and positive head are not assumptions of this one-step lemma. |
| `head_positive_step`, `head_positive_orbit` | Positive head persists through one step, and through all iterates when validity is preserved. |
| `head_powTwo_lower_bound` | Positive initial head and zero overflows at transition indices `j < n` imply `powTwo n ≤ a_n`. |
| `overflow_by_power_bound` | Given positive initial head and a specified `H : Nat` satisfying `m < powTwo H`, some transition index `j ≤ H` has `g_j = 1`. |
| `decimal_overflow_before_five` | Some transition among indices `0,1,2,3,4` has overflow one. Its successor state occurs by time five. |
| `overflow_in_every_window` | Under the same power bound, for every `start`, some `j ∈ [start,start+H]` has overflow one. This is a window of `H+1` transitions. |
| `decimal_overflow_every_five` | For every `start`, an overflow occurs at `start ≤ j < start+5`. |
| `decimal_overflows_arbitrarily_late` | For each natural number `N`, there exists an overflow index `j ≥ N` along this abstract orbit. |
| `residue_zero_from_power_bound` | Given positive initial head and `m < powTwo H`, residue zero holds at every state `H+1+n`. No initial zero residue or overflow occurrence is supplied. |
| `decimal_residue_zero_from_five` | For every valid decimal initial state with positive head and every `n : Nat`, `Moment.moment (orbit 9 s (5+n)).c (orbit 9 s (5+n)).B % 22 = 0`. |

The general finite bound remains parameterized by a chosen `H` and its proof `m < powTwo H`; the source does not export a separately optimized logarithmic-bound theorem. The decimal endpoint chooses `H = 4`. Transition index four and state time five are intentionally distinct; the source's natural-number subtraction steps are justified by `j ≤ H` or `j < 5` and do not hide an off-by-one assumption.

## 5. Why the proof is substantive and noncircular

First, the initial phase bounds imply that the band digit `c - m*bulkCarry m c` lies between one and `m-1`. Every normalized digit lies between zero and `m`, and bounded input coefficients give final carries in `{0,1}`. The low boundary digit, band digit, and inserted overflow digit are also in that digit range. Pairwise addition therefore gives raw coefficients in `[0,2m]`; suffix removal preserves the bound. The successor phase is twice the band digit, lies strictly between zero and `2m`, and cannot equal odd `m`. This proves validity preservation without any overflow-existence or moment-zero premise.

Second, removing a suffix of the new phase preserves the head when the empty-word fallback uses that same phase. This handles the potentially troublesome case where stripping removes the whole word. For a nonempty word `x::xs`, the carry from the reversed tail is a bit `e`. Zero overflow means `(x+e)/(m+1)=0`; nonnegativity and Euclidean remainder bounds then give `x+e ≤ m`. The new head is exactly `x+(x+e)`, so it is at least twice the old head, while the old head is at most `m`. The empty-word case gives the same inequalities directly. Overflow leaves a positive new head: `1 + x%(m+1)` for a nonempty word, or `c-m` for an empty word. No all-time arithmetic interpretation enters this argument.

If transitions `0,…,H` all had no overflow, the first `H` doublings would force `a_H ≥ 2^H`, since a positive integer head is at least one. Non-overflow at transition `H` would simultaneously force `a_H ≤ m`, contradicting `m < 2^H`. Carry-bitness converts failure to have overflow one into overflow zero; it was already established from initial validity. The every-window theorem restarts this argument at the actual abstract state at time `start`, using the independently proved preservation of validity and positivity.

Third, the imported `General.Moment.moment_step_overflow` gives `M_{i+1} % q = 0` from `g_i = 1`. `moment_step_no_overflow` gives `M_{i+1} ≡ 2*M_i (mod q)` from `g_i = 0`. Thus zero residue persists once reached. The new validity proof supplies the coefficient bounds required for every subsequent carry-bit argument, and finite head growth supplies the first overflow. The proof does not assume the endpoint's zero residue, a later-state bound, or a later overflow.

The dependency chain is acyclic: `ExteriorClock → GeneralCarryMass → GeneralMomentAbsorption → InitialValidity → FiniteOverflow`. The unit-cancellation and closed-path mass congruences in `GeneralCarryMass` concern a separate invariant modulo `m`; their inverse or closure assumptions are not imported as hidden premises of the moment-reset argument modulo `2(m+2)`.

## 6. Sharpness, necessary-hypothesis controls, and limits

The two decimal sharpness witnesses serve different purposes:

| Witness | What its compiled declarations establish |
|---|---|
| `sharpStart = (2,[1])` | No overflow at indices `0,…,3`; overflow at index four. This establishes the worst-case five-transition timing. Its initial moment is already `2*1-2 = 0`, so it does **not** establish delayed moment absorption. |
| `sharpAbsorptionStart = (2,[1,0])` | Validity and positive head; residue 20 at state four and zero at state five. This establishes that uniform decimal absorption time five cannot be reduced to four, even among the eight even phases. |

The neutral-phase control gives `nextExterior 9 9 [1,18] = [3,16,19]`, containing a coefficient above 18. The zero-head control `(2,[0])` remains valid but has residue two at state five; therefore validity alone does not imply the claimed uniform five-state reset. It does not assert that this state never absorbs. The odd-base control `m = 2, c = 1` starts in `Phase` and reaches excluded neutral phase two. That demonstrates failure of the proposed invariant-domain argument in that odd base; it does not rule out other results or different invariant domains in odd bases.

The proved invariant is divisibility of the exterior **moment** by `2(m+2)`, not equality of the integer moment to zero. For decimal it is the exact moment congruence modulo 22, not a blanket interpretation of a concrete integer's residue or palindrome status.

No integer encoding, natural-number correspondence theorem, digit-boundary gap condition, or concrete reverse-and-add orbit occurs in these endpoint contracts. Arbitrarily late computed overflows refer to the infinite abstract iteration defined by `orbit`. They do not ensure an all-time finite-gap realization by one finite integer, continued validity of an arithmetic projection, palindrome avoidance, a Lychrel number, or any conclusion about 196.

Existing Agent #411 boundedness ownership and Agent #216 integer/natural-number correspondence work were not changed or supplanted. This review verifies adoption of the recovered statements with the exact tactic repair. It makes no new priority claim or exhaustive repository novelty claim. The parent's coordination and canonical integration checks determine how the supporting interfaces should be adopted.

**Blocking defects found:** none within the exact stated abstract-domain scope. **Remaining external steps:** the parent's canonical repository replay and coordination review; any stronger concrete-integer conclusion requires separate correspondence and continuation theorems.
