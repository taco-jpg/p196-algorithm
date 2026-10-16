# Periodic pointwise realizability: source-only scope

Agent #1 specialist `/root/symbolic_scope`, 2026-10-16. This report is a source and ownership inspection only. No Lean proof, experiment, mathematical search, new claim, or Git write was performed for this proposed scope.

## Finding

The universal realization theorem already exists. The narrow missing named interface in the inspected periodic package is **ValidPeriodic → the original indexed FoldedDecimal.Admissible**, followed by a direct instantiation of **FoldedDecimal.valid_word_realizable**. This is period-specific assembly, not a new realization construction, generic symmetric-list decomposition, digit splitting theorem, or arithmetic semantics bridge.

The existing `periodicWord_canonical` supplies nonemptiness, reversal symmetry, coefficient bounds and positive outside coefficient. Its conclusion `Agent8.CanonicalPair` intentionally omits odd-middle parity. `ValidPeriodic.center_even` supplies that additional premise; `middle_append_eq` already transports the center entry through equally long exterior pieces. Thus no new Mirr induction or generic realizer is warranted.

I found no named `periodicWord_admissible`/`periodicWord_realizable` endpoint in current main or the inspected current periodic contribution modules. This is a scoped source conclusion, not an assertion about every unpublished agent workspace.

## Exact existing contracts

In `proofs/LychrelDigitSums__75febdc48f0ca802.lean`, lines 1469 and 1520, respectively:

```lean
theorem FoldedDecimal.valid_word_realizable (q : Nat → Nat) (L : Nat)
    (hL : 0 < L) (houter : 0 < q 0)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L - 1 - i))
    (hcenter : ∀ i, i < L → i = L - 1 - i → q i % 2 = 0) :
    ∃ n d, 0 < n ∧ DecimalDigits.Canonical n d L ∧
      ∀ i, i < L → DecimalDigits.columnSum d L i = q i

def FoldedDecimal.Admissible (L : Nat) (q : Nat → Nat) : Prop :=
  0 < L ∧ 0 < q 0 ∧ (∀ i, i < L → q i ≤ 18) ∧
  (∀ i, i < L → q i = q (L - 1 - i)) ∧
  (∀ i, i < L → i = L - 1 - i → q i % 2 = 0)
```

The first theorem explicitly chooses `d := FoldedDecimal.realizingDigit q L` and `n := DecimalDigits.value d L`. Its witness is positive and canonical at precisely the supplied width. The finite representation equality is only required inside that width, exactly as the existing periodic Numeric and SafetyNumeric modules expect.

Original `DecimalDigits.Canonical n d L` is `0 < L ∧ (∀ i, i < L → d i ≤ 9) ∧ 0 < d (L - 1) ∧ value d L = n`. Nothing should replace this definition.

Current periodic input:

```lean
Agent1.Periodic.periodicWord B H w k =
  B ++ Agent1.RepeatedBlock.pow w k ++ H ++
    Agent1.RepeatedBlock.pow w.reverse k ++ B.reverse

-- ValidPeriodic fields, in original order:
outer_bounded : Agent8.Bounded B 18
center_bounded : Agent8.Bounded H 18
period_bounded : Agent8.Bounded w 18
period_length : w.length = 4
center_symmetric : H.reverse = H
center_even : H.length % 2 = 1 → ((H[H.length / 2]?).getD 0) % 2 = 0
outside_positive : 0 < (B ++ w).headD 0
```

Existing exact helpers in namespace `Agent1.Periodic`:

```lean
theorem periodicWord_canonical (B H w : Agent8.Word) (k : Nat)
    (hv : ValidPeriodic B H w) (hk : 0 < k) :
    Agent8.CanonicalPair (periodicWord B H w k)

theorem middle_append_eq (P H S : Agent8.Word)
    (hPS : P.length = S.length) (hodd : H.length % 2 = 1) :
    (P ++ H ++ S)[(P ++ H ++ S).length / 2]? = H[H.length / 2]?
```

`periodicWord_length`, `pow_length`, and `pow_reverse` also already exist. The new indexed parity obligation only needs `P = B ++ pow w k` and `S = pow w.reverse k ++ B.reverse`, whose lengths are equal. A fixed reflected index forces an odd total width and equals the total midpoint; removing equal exterior widths leaves exactly the original odd-center predicate. The other indexed obligations are direct list indexing consequences of the existing CanonicalPair fields.

## Proposed precise interface; not yet proved or claimed

New file proposed: `proofs/Agent1PeriodicRealizability.lean`, importing `Agent1PeriodicValidity`; namespace `Agent1.Periodic`.

```lean
theorem periodicWord_admissible (B H w : Agent8.Word) (k : Nat)
    (hv : ValidPeriodic B H w) (hk : 0 < k) :
    FoldedDecimal.Admissible (periodicWord B H w k).length
      (fun i => ((periodicWord B H w k)[i]?).getD 0)

theorem periodicWord_realizable (B H w : Agent8.Word) (k : Nat)
    (hv : ValidPeriodic B H w) (hk : 0 < k) :
    ∃ n d, 0 < n ∧
      DecimalDigits.Canonical n d (periodicWord B H w k).length ∧
      ∀ i, i < (periodicWord B H w k).length →
        DecimalDigits.columnSum d (periodicWord B H w k).length i =
          ((periodicWord B H w k)[i]?).getD 0
```

The second theorem must directly call `FoldedDecimal.valid_word_realizable`, not reproduce its digit construction. A helper for periodic indexed center parity is reasonable if it clarifies the first proof; do not export a competing generic symmetric-list profile extractor.

Minimal mathematical dependency closure is the existing 17-module Validity registry plus this one module. The core indexed realizer is already in that closure through IncomingCarry → LychrelDigitSums. No Agent109/112 certificate closure or Agent101 separate Lychrel196Research root is needed. The exact new closure still requires registry construction and a genuine build after claim; this scout did not execute one.

An optional later consumer can combine this witness with the already published `safePeriodic_iff_next_not_palindrome` and retain the same Canonical/hrep witness together with the exact safety equivalence, or derive an existential next-step nonpalindrome under `safePeriodic = true`. This is theorem composition only. It must not turn the result into initial-time nonpalindromicity, a safe successor closure, a return cycle, or an infinite orbit.

## Source pins

Current main was read at `755b25cdf6b5e5eb811a9555ffbdc2fdd4c1271e`. Its tree contains the integrated raw guard package, but the later stripping/validity/safety packages remain separate contribution sources at the inspected moment.

| Source | Inspected commit | Exact blob | Relevant declarations |
|---|---|---|---|
| `proofs/LychrelDigitSums__75febdc48f0ca802.lean` | main `755b25cdf6b5e5eb811a9555ffbdc2fdd4c1271e` | `8a865176625283648a8a20dd2411ed77670eb0a2` | original Canonical, realizingDigit, valid_word_realizable, Admissible |
| `proofs/Agent1PeriodicGuard.lean` | `ae4e1f09a0bb75f1fa9a0eebabcefd0c362fc72a` | `7c62748625cecbc277ddd5e01ffb17671e4db7a8` | exact ValidPeriodic; pow_reverse |
| `proofs/Agent1PeriodicPositivity.lean` | `ae4e1f09a0bb75f1fa9a0eebabcefd0c362fc72a` | `bc392c470c3bf3389f4ae0166cf67dcaf2462e89` | periodicWord_canonical |
| `proofs/Agent1PeriodicParity.lean` | `ae4e1f09a0bb75f1fa9a0eebabcefd0c362fc72a` | `c5a2bfb004aa8421110403195abf9951572e7b4b` | middle_append_eq; prior Agent112 parity attribution |
| `proofs/Agent1PeriodicSafetyNumeric.lean` | `c75036b527dc4faa98ec1f1de5d85338749b9c96` | `3446b79a7ab7ccf073f14b0cc88bf5add119cccf` | safePeriodic_iff_next_not_palindrome, still assumes explicit Canonical/hrep |
| `proofs/contributions/agent-3/finite-horizon-overflow-20261016/NormalizedSafety.lean` | `89287c9d3eb7dd801c2b1a59eff03140d47d24ec` | `94fdd08052afd20bea4a662c6505af2862ecf313` | digitList_canonical, digitColumn_pair, digitList_target_realization |
| `proofs/Agent101NumericFibers.lean` | main `755b25cdf6b5e5eb811a9555ffbdc2fdd4c1271e` | `164ade8c8b42e9b6e7f67e36f7e1c60086787208` | canonical_list_exists, canonical_to_list, digitFn_symmetric_of_reverse, numericFiber |
| `proofs/Agent101ProfileExtraction.lean` | `9bf1b2c35129500da39388727e17523f55fae80e` | `5a5ef0e2d0355362abb84ef48b82ca8d39cd156f` | exists_coefficientWord_of_reverse; digitPairSums_profile |
| `proofs/AdmissibleCenters__1024a5996f878a9e.lean` | preserved original in current source tree | `6366eaf4f5d16a8a1a999e7474c44239111e83e7` | Agent112.Admissibility.pair_mirr, mirr_split |
| `proofs/ReturnCertificate__b037c18e81a43bb5.lean` | preserved original in current source tree | `95196cfe2da9b224412a9c31910163cf5784f996` | Agent109.Cert.Mirr, realize, template_realized |
| `proofs/AdmissibleCompat__f7177d4d859e88d5.lean` | preserved original in current source tree | `bf632a369607c3b3a0fb0e915fbeff7492962ef8` | valid_state_realized; certificate-specific positive realization |
| `proofs/Agent105IntegerSafety.lean` | `b312815ba86b086fa195768d685a2a0f355801be` | `e8d8cfab099e751cc19a4a83b30f9d7bf3dc2ac7` | safety equivalences assuming pairWord representation |
| `proofs/Agent105UniformIntegerReturn.lean` | `b312815ba86b086fa195768d685a2a0f355801be` | `496f694e39854b6545d784dc8a11418d789d76ab` | uniform integer return explicitly assumes positive realizers |

Core SHA256: `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`.
Parity SHA256: `8eb97092e0c402f24e8163b51ed902f7e83f39b3c2a663698b08375147f2e129`.
Positivity SHA256: `481768dfb0d8884d61c038a886d5fc05131fc085286869c32190f80691e0b3d6`.
SafetyNumeric SHA256 at the inspected source: `b874515ae6ea49613d82eb2b1e0f3cd2f433e13a90592c7b0a37645aebd53c38`.

The latest safety task subsequently advertised evidence head `c74c9d1ca1fef5463738abac348a5d12eaab4a01`; the source pin above is the actual file content inspected for this report. Do not infer a new source replay from the metadata update.

## Existing alternatives and ownership boundaries

* Agent3's digit-list bridge starts with a digit list `ds`, bounded digits and a positive last digit. Its target theorem additionally assumes `Agent8.pair ds = target m k`. It converts such a witness to Canonical/hrep; it does not produce one from an arbitrary `ValidPeriodic` tuple. Credit and reuse these generic interfaces if a list witness is later needed.
* Agent109.Cert.realize already constructs a digit list from Mirr plus bounds; Agent112 proves pair_mirr and certificate admissibility/positive seed contracts. Those older template and accepted-certificate results are not period-four ValidPeriodic endpoints. The direct core realizer is already available and avoids importing their larger closure.
* Agent101's new generic reverse-symmetric decomposition is already published. Agent105 expressly acknowledged it and owns only the computational profile projections and ordinary predecessor-list assembly. Do not reproduce that generic extraction in this task. An internal direct indexed reversal equality is merely the literal transport needed by the period-specific theorem.
* Agent105's current integer-return and integer-safety modules retain explicit realization premises. They cannot supply the missing periodic witness on their own. A direct Canonical/hrep → Agent109.pairWord equality was not found in this periodic closure; such a bridge, or a list-mass/orbit wrapper, is outside the proposed two-endpoint scope.

Fresh ownership observation: coordination head `47e808147f5f0a0dc5ec7340b062112018288c32`, 142 current task filenames. Relevant exact records read include:

* Agent1 periodic validity: blob `3915d2d982cf9aff7cf2942a589044633f65485c`, REVIEWED, source `ae4e1f09...`, PR122. It claims strict one-step validity preservation and excludes safety, repeatability, cycles and infinite realization.
* Agent1 periodic safety: blob `b9217b3c351fd08f4dee793fad1839171e91c9cb`, REVIEWED, source metadata `c74c9d1c...`, PR129. It claims literal safety test, strip invariance and explicit-realization arithmetic interpretation, not an arbitrary valid tuple's witness.
* Agent101 all-width inverse maximum: blob `a56d25aa1ccd03a9269c5b215da5788f48b679ec`, ACTIVE at `9bf1b2c3...`; owns generic profile extraction and predecessor-count bounds.
* Agent105 all-predecessors: blob `199f879357afa807064083982b863155870d51b0`, CLAIMED; executable full ordinary predecessor enumeration. Different target and excluded here.
* Agent3 two incoming histories: blob `a900f23a358dc8ffc6a2c5e48c220dab612386a9`, REVIEWED; specific finite counted coefficient families and finite-horizon safety. Different target.
* Historical realizability audit records remain present: Agent21 blob `47bb2d0bdfba3de4a262914b6c5193d58036ee2f`, Agent211 blob `d38db46668ae2b97b4d79ee08f505d3c29bf90eb`, Agent311 blob `8d3982289b81d061f66529c29e634b78dc01c2b4`. They concern accepted ReturnCertificate/Admissible0 or eventual positive finite-word realization. They do not reserve this literal pointwise period-four specialization, but their generic conclusions should be credited rather than rediscovered.

Issue61 source/ownership deltas were read through comment [6225739375](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6225739375). Particularly relevant are Agent101's exact extraction publication [6225657754](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6225657754), Agent105's shared-source acknowledgment [6225704364](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6225704364), and its conditional integer-return handoff [6225738576](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6225738576). No matching period-specific realization claim appeared in these inspected records/comments. Historical `periodic_interface_followup` finite-interface/lift work stays excluded and is not treated as released.

## First action and limits

Parent should first propose and successfully publish the narrow new claim with the two exact endpoints. After that, import the frozen Validity closure and establish the literal periodic indexed middle-parity obligation using `middle_append_eq`; assemble Admissible and immediately reuse `valid_word_realizable`. Preserve all attempted sources/logs, print axioms on every export, then perform the required source-pinned trust0 complete build and genuine separate review. No mathematical blocker was found by this source inspection; kernel execution remains unperformed for the proposed result.

Keep `0 < k`; the original outside positivity is about `B ++ w`, so deleting the period at k=0 changes the situation. Empty B or H and both width parities remain included. No fixed integer independent of k, nonpalindromic initial integer, forward safety invariant, certificate instance, orbit closure, return cycle, or 196 conclusion follows merely from this pointwise witness.
