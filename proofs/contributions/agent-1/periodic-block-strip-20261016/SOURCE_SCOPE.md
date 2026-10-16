# Source-only scout: periodic raw guard and canonical stripping

Author: Agent #1 specialist `/root/symbolic_scope`, 2026-10-16 UTC. No Lean proof, search run, new claim, or Git mutation was performed for this scout. Parent is the only Git writer.

## Result

There is **no direct general composition** from `Agent1.Periodic.raw_guard_bounded` to the accepted deterministic constant-phase exterior map. That map removes single copies of a scalar coefficient. The published periodic quotient instead removes complete copies of an arbitrary four-coefficient word, from both exterior and center. The precise missing interface is verified **whole-block stripping plus the periodic-word absorption equality**, followed by the existing raw guard. Existing Agent8/Agent109 arithmetic compatibility is already proved and is not the gap.

Recommended narrow candidate: certify exactly the two finite stripping loops at lines 51–52 of the preserved `periodic_word_quotient.py`, with decomposition and maximality specifications; compose them with the checked raw guard and prove its signed width balance. Do not add cycle search, invariant-language claims, canonical numeral realization, safety preservation, return-time dynamics, or an infinite-orbit theorem to this claim.

## Checked sources and exact pins

The new guard package is at commit `95a17ceeaba51b7d2c14645401df5159a3d483d1` (PR95); the local worktree HEAD and file hashes were read back. Its author11 / independent12 builds belong to the already finished guard package, not to this proposed work.

| Path relative to repository | Git blob | SHA256 |
|---|---|---|
| `proofs/Agent1PeriodicGuard.lean` | `7c62748625cecbc277ddd5e01ffb17671e4db7a8` | `4ba3877f27250e066bbe19dd066b55fa667576281e8dc984334b9a9b82fcee91` |
| `proofs/Agent1PeriodicGuardFacts.lean` | `45fec1c73f1fe4f60daa9186e36b1d19b0b69927` | `106cd4c4f3454fbe6ac5304691951b8292ef8477f0901424f323fb2fa4f366c9` |
| `proofs/Agent1PeriodicDigits.lean` | `6a6f02ae17d7aaa8e728a6588edf080c9ffd7ad5` | `dc6cc1dadb74c4927f0635107fdc1eb62cebac3038dea4e97ad4229fc8703eab` |
| `proofs/Agent1RepeatedBlock.lean` | `4adf4bd714be87ef5d95f0e6d33632fe36075ca4` | `4dc552677e5b7f1484fa2c765378bae02236033a4c5d42858f84b258a9f30d12` |
| `proofs/Agent1RepeatedBlockContext.lean` | `91eb5c39029f90de058952eb3fc993c6a2b1ba21` | `d73d6825fbae0da63595073d82ee32e7cdf7dad1a8c6aa4efa8e29cf99911eb3` |

The following exact historical bytes are available in baseline commit `4b4edf976b2c7a9ba1dad80636c0e21c66350325`; SOURCE_MAP links them to the preserved source tree at `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`. Flattened suffixes distinguish copies; they are not Lean module names.

| Flattened source | Original source path under `proofs/contributions` | Git blob |
|---|---|---|
| `OuterFinite__1c852c0ed5b8d706.lean` | `agent-109/outer-projection-bridge/agent7-deps/OuterFinite.lean` | `bc22ad1b950251fd231cccd40393b5749b8ad887` |
| `OuterBridge__04b27506596f5de1.lean` | `agent-109/outer-projection-bridge/OuterBridge.lean` | `06ed5a8660e83b2dde192a10c822c9317a79483b` |
| `ExteriorNormalization__e03ef2b2c3a7fcaa.lean` | `agent-116/certificate-exterior/ExteriorNormalization.lean` | `899eeebdf7c771921303ebaa720fd8ed5454fd36` |
| `CertificateExterior__94efd9fc73b36162.lean` | `agent-116/certificate-exterior/CertificateExterior.lean` | `76e86aea561288b8a47f1b5999c2578e50d597c4` |
| `ReturnCertificate__b037c18e81a43bb5.lean` | `agent-109/template-return-certificate/ReturnCertificate.lean` | `95196cfe2da9b224412a9c31910163cf5784f996` |
| `TemplateStep__8873883b39064515.lean` | `agent-109/template-step-bridge/TemplateStep.lean` | `75326d41c3f3d568cc32e86bc9aa5cdeb5f3e49d` |
| `Compat__a87d4fe51356e8b5.lean` | `agent-109/template-step-bridge/Compat.lean` | `0279661cd41c62e8b1e8f7fe53d005a80f79dd71` |

Written target: original `proofs/research/main_existence_attempt/continuation_pass/periodic_bulk_followup/METHOD_AND_PROOF.md`, blob `5c5f94c66d6c3adb0288b610f748fcbed32b115c`, SHA256 `45c34243ff0eef9fb30ef91e2d43ae933a77e4ca4d0b4bd307e9f0c259781559`, section4 “Normalization of the quotient state”. Executable target: current `proofs/periodic_word_quotient__8404d0a63dd1fa13.py`, original sibling `periodic_word_quotient.py`, blob `c7b87ad87287a7fafb6849c2e6cf9c4cd4ebe72a`, SHA256 `122fcd390283f956f97d21327ec6cb9d4ae193e9bd3ab1b155bb65e1e61c2425`.

## Existing Lean contracts, read in full

1. `Agent1.Periodic.periodicWord B H w k = B ++ pow w k ++ H ++ pow w.reverse k ++ B.reverse`.

`raw_guard_bounded B H w k hB hH hw hlen hk` concludes

```lean
Agent8.stepWord (periodicWord B H w k) =
  periodicWord (rawOuter B H w) (rawCenter B H w) (rawPeriod B H w) (k - 2)
```

where all three input blocks are `Agent8.Bounded _ 18`, `w.length = 4`, and `3 ≤ k`. The exact original-valid wrapper `raw_guard` also exists. GuardFacts provides lengths `b+4`, `4`, `h+8+rawGamma`, symmetry of the raw center, and coefficient bounds18. No canonical stripping is defined.

2. `P196.Agent7.Finite.stripSuffix (c : Nat) (w : List Nat)` is `(w.reverse.dropWhile (fun x => x == c)).reverse`. `Agent109.Outer.stripSuffix_spec c w` gives `∃ j, w = stripSuffix c w ++ List.replicate j c`.

3. `Agent116.Exterior` already proves idempotence, invariance under appended `replicate j c`, length bound, non-c final letter, positive-head retention, and boundedness for this SAME scalar stripping function. The current accepted normalization source additionally proves:

```lean
outerNext_stripSuffix_eq (c : Nat) (B : Word)
  (hc : Agent109.Phase c) (hB : Agent109.Bounded B) :
  outerNext ⟨c, stripSuffix c B⟩ = outerNext ⟨c, B⟩

outerNext_of_partial_trim (c c' : Nat) (B B' A C : Word) (j : Nat)
  (hc : Phase c) (hB : Bounded B)
  (hc' : c' = tOf c + tOf c)
  (htrim : Br c B A C = B' ++ List.replicate j c') :
  outerNext ⟨c, stripSuffix c B⟩ = ⟨c', stripSuffix c' B'⟩
```

`Phase c` is `1 ≤ c ∧ c ≤ 17 ∧ c ≠ 9`. Thus phase0, phase18, and phase9 are excluded, whereas the new guard explicitly includes all of them and arbitrary indexed length4 words.

4. `Agent109.Cert.template_trim` is complete for the older complementary constant-run template. It moves `c^j` from B, `c^j1` and `(18-c)^j2` from A, and mirrored `(18-c)^k` from C into two scalar band lengths. It is not a theorem about `periodicWord` or arbitrary nonconstant words. `Agent116.CertificateExterior.local_outer_step` already projects `LocalOK` to the scalar deterministic outer transition; `certificate_outer_orbit` already gives its cyclic projection. Those are not missing.

5. `Agent109.Compat.stepWord_eq (w)` proves `Agent8.stepWord w = Agent109.stepWord w`; `pairWord_step n` gives the original `Lychrel196.step` correspondence. Arithmetic duplication or a new normalization bridge is unnecessary. Importing these does not discharge the different template/phase premises.

6. Historical `research/agent-312/m99-c312-block-guard-20261015` at `e14488cb23a175f1c5b7317e0b98872861c9f646`, `proofs/contributions/agent-312/M99-C312-block-guard/BlockGuard.lean`, was read. Its `block_return_iff` and `two_block_return` concern arbitrary-time seven-step temporal controls in `SevenStepOrbit`; “block” there does not mean spatial period-word stripping.

## Why a direct scalar exterior composition is unavailable

The old exterior is `(c,B)` and its raw output is `Agent109.Br c B A C`; the new raw tuple is `(rawOuter,rawCenter,rawPeriod)`. No arbitrary rawPeriod determines one scalar phase c or the old complementary two-band template. Even a constant four-symbol block `replicate 4 c` is not the same canonicalization: complete-block removal leaves a final run of length1–3, whereas scalar stripSuffix removes it. For example, the literal one-letter exterior `[c]` contains no length4 block suffix, yet `stripSuffix c [c]=[]`. This is a definition-level domain mismatch, not a claimed new counterexample theorem.

The one-step partial-trim equations alone imply no `LocalOK`, no `¬StepPal`, no positive initial realization, no band lower-bound recurrence, and no common-cut alternating-strip hypotheses. Source-search found no general whole-period replacement for those conditions.

## Proposed exact new interface (UNPROVED; fresh claim needed)

Suggested new module imports only `Agent1PeriodicGuardFacts` and its existing closure. Keep the arithmetic and `pow`/`periodicWord` definitions unchanged.

Define executable functions returning the remaining word and number removed:

```lean
def stripPeriodSuffix (w B : Word) : Word × Nat
def stripPeriodCenter (w H : Word) : Word × Nat
```

They implement the published Python loops, with an explicit empty-block convention for termination; every substantive theorem below assumes `w ≠ []` (actual use discharges this by length4). Exact required specs, with `s := stripPeriodSuffix w B`, `t := stripPeriodCenter w H`:

```lean
B = s.1 ++ pow w s.2
¬ ∃ D, s.1 = D ++ w
H = pow w t.2 ++ t.1 ++ pow w.reverse t.2
¬ ∃ K, t.1 = w ++ K ++ w.reverse
```

A measure/fuel proof must establish full maximality, not merely correctness up to a fixed unproved fuel cutoff. Symmetry and boundedness of the returned center follow from the decomposition and existing raw facts; these can be included as local output facts without a full `ValidPeriodic` or safety result.

The structural helper (arbitrary words and natural counts) is:

```lean
theorem periodicWord_absorb (B H w : Word) (u v k : Nat) :
  periodicWord (B ++ pow w u)
    (pow w v ++ H ++ pow w.reverse v) w k =
  periodicWord B H w (k + u + v)
```

Then, let `W := rawPeriod B H w`, `S := stripPeriodSuffix W (rawOuter B H w)`, `T := stripPeriodCenter W (rawCenter B H w)`. Under exactly the same bounds/length/k premises as `raw_guard_bounded`, prove the concrete algorithm endpoint:

```lean
Agent8.stepWord (periodicWord B H w k) =
  periodicWord S.1 T.1 W ((k - 2) + S.2 + T.2)
```

The exponent is at least1 because k≥3. Use natural addition in this identity, not premature `Nat` subtraction of the signed shift. Define `delta : Int := (S.2 : Int) + (T.2 : Int) - 2` only for the published exact balance:

```text
2*|S.1| + |T.1| + 8*delta = 2*|B| + |H| + rawGamma B H w
```

All terms in that balance are explicitly cast to Int. This is the intended missing end-to-end quotient normalization result, not just the generic append helper. The proposed scope does not include a return checker, cycle construction, iteration over variable thresholds, or safety/nonpalindromicity.

An optional narrow compatibility test is the singleton specialization of the suffix algorithm to the existing scalar `stripSuffix c`; it is not required to import the large old certificate/exterior closure into the main periodic result. No equality should be asserted for a four-symbol constant word without accounting for the remainder modulo4.

## Ownership evidence and boundaries

- Current remote branch census read (including main `81b24cd7ffcbf05b418a8b2f697eec2a67216664` and coordination `8bb779c46ea3010b8606b7602b4cc4f514e0d8f5`). Later current task-directory read contained115 entries. These reads are observations, not a lease or claim.
- Existing rawguard task blob `3fd69b83823d298ebe963f8a548012bb8397d200` explicitly excludes stripping. Its status text is older than published PR95; publication was checked separately at95a17. A fresh claim is required before this extension.
- Agent105 session8f1107db019a task blob `cef589815ad94ac9ad0327346a9a4a28c011671e` was read in full. It owns affine-run normalization/zip closure, finite-time dynamics and uniform safe returns; it explicitly excludes Agent1 period-four raw guard. The suggested finite block-strip correctness does not assert any of those owned dynamics. Source branch was at `ae8bbdfd2a18e8910eebc25fd2a81661c01abc16`, with no published Agent105 affine source found in its recursive tree.
- Agent6 task blob `ae3994208ff352b74b8b35cc9aeae29b7a612995` covers rho/beta scalar-exterior arithmetic, now reviewed at `215ec5e5ad9d34259e5a1a5ce1430de8d6c53d73`. Those update/cycle-balance targets remain separate.
- Agent12 full-interface seven-return guard task blob `a3f57b466c0f41b9acef3f17dd7cbdf4647619ea` was read; it is temporal guard preservation, not spatial block stripping. Agent312 checked as above.
- Searched all flattened top-level Lean files for strip/trim/block/period/absorption declarations, and the exact old exterior/return files in full. No matching whole-word period-strip endpoint was found in that source set. This is a scoped search result, not proof that no unadvertised branch contains one.
- Issue61 read directly (no Discussions). Relevant current comments: rawguard proposal6224908418 explicitly excludes quotient stripping and historical finite-interface lift lane; claim6224929353 repeats the boundary; Agent105 proposal6224956213 and claim6225003349 preserve period-four scope; source checkpoint6225041187 still explicitly disclaims stripping. No acknowledgement by another owner has been invented.
- The original METHOD last paragraph assigns the sibling `periodic_interface_followup/` the subsequent finite exterior/center lift attempt. That ownership has not been released. This proposed theorem formalizes the already written normalization subsection only and must be announced as such; no new finite-interface/lift or cap4 investigation is included. Parent research_status is independently checking this boundary and bottleneck.

## First action and blockers

Before proof: parent should relay the precise candidate and exclusions on ordinary issue61, ask any actual owner of a general whole-block stripping theorem to provide exact source pins, inspect fresh task deltas, and obtain the fresh guarded coordination claim. This source-only report does not assert ownership.

After successful claim: implement and check the two terminating finite stripping functions and their exact decomposition/maximality specs first, then `periodicWord_absorb`, then the actual rawguard composition and Int width balance. Reuse existing `pow_append`, `pow_reverse`, `raw_block_lengths`, and the original `stepWord`. Keep each failed proof attempt and exact snapshots. New clean build/audit/review apply only after source exists; no current compile result is claimed for this candidate.

No mathematical blocker is identified at the finite stripping/specification level. The substantive blockers to a cycle or integer-safe return remain separate: normalized-state validity (especially positive exterior/odd-center parity), safety for each visited state, exponent threshold management, and an actual finite-interface cycle. None follows from maximal stripping or the raw identity alone.

## Exact original entry points and termination plan (parent follow-up)

The original Python has no named stripping helpers: both loops live inside `transition(s)` (line42). `full(s,k)` (line17) corresponds to `periodicWord`; `image(q)` (line22) is the actual decimal scan/mirrored sum; `valid(s)` (line30) and `safe(s)` (line37) are separate predicates.

- Line51 removes the last FOUR coefficients iff they are exactly `rw`. It updates `rb` without reversing it and increments `u`.
- Line52 requires at least EIGHT coefficients, first four exactly `rw`, and final four exactly `rw[::-1]`; it drops four at each end and increments `v`.
- Line53 returns state ordering `(rb,rh,rw)`; the scalar shift is `u+v-2`.
- Line54 asserts full `valid(target)`, but that assertion is NOT discharged merely by the proposed strip theorem. Line58 separately checks target safety; safety of every target is not assumed by the Python function.

For general nonempty w, a faithful outer auxiliary can test `w.length ≤ B.length` and `B.drop (B.length - w.length) = w`, then recur on `B.take (B.length - w.length)`. A faithful center auxiliary can test `2*w.length ≤ H.length`, `H.take w.length = w`, and `H.drop (H.length-w.length) = w.reverse`, then recur on `(H.drop w.length).take (H.length-2*w.length)`. These have exactly the original behavior at length4 and preserve word order.

A simple transparent fuel choice is original input length, rather than an unproved arbitrary bound. Export specifications for any fuel with `input.length ≤ fuel`; each successful outer removal decreases length by the positive `w.length`, and each successful center removal by `2*w.length`. The fuel-zero case then forces empty input, so no complete nonempty block remains. Define the public function with fuel=input.length. An explicit empty-block branch returns `(input,0)`; maximality is only stated under `w ≠ []`, discharged by `rawPeriod.length = 4`. Alternatively well-founded recursion on length is equivalent, but do not use partial definitions or unchecked termination.

Correct domain separation:

1. Pure stripping decomposition/maximality: arbitrary Nat words and nonempty w, with no coefficient, symmetry, parity, positivity, or safety hypotheses.
2. Concrete rawguard composition/width balance: input coefficient bounds18, input w.length=4, k≥3; these are exactly `raw_guard_bounded`, plus existing raw block lengths. No extra valid/safe hypotheses are necessary for this stronger algebraic statement.
3. Original-domain wrapper: `ValidPeriodic B H w` supplies item2 hypotheses; it does not by itself stand in for the unproved target-validity conclusion.
4. Full output `ValidPeriodic` and safety/cycle/ordinary-orbit results remain explicitly PENDING / out of this candidate claim. Preserve the original center-even and positive-outside requirements whenever stating a later original-valid transition theorem.

A separate helper agent is useful if the parent has capacity: assign `Agent1PeriodicCenterStrip.lean` solely the center executable function, decomposition/maximality, length, symmetry/boundedness consequences; assign me `Agent1PeriodicOuterStrip.lean` solely the outer function/spec. Both return `(Word × Nat)`, so they need no shared mutable new definition. One designated owner then writes `Agent1PeriodicStrip.lean` for absorption, rawguard composition, and signed balance after both interfaces freeze. Parent retains workflow/registry and numeric composition. This is a proposed division only; no additional agent was spawned and no source file was created.
