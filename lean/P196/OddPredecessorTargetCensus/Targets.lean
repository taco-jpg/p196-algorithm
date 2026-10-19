import P196.OddPredecessorTargetCensus.ProfileMeaning
import P196.OddPredecessorTargetCensus.NumericBridge

/-!
# Complete enumeration of targets with odd predecessor cardinality

Agent #6: generate accepted coefficient profiles at the two possible source
widths, then evaluate them as ordinary integers. The exact carry partition
gives the target width, and the complete parity theorem gives membership.
-/

set_option autoImplicit false

namespace OddPredecessorTargetCensus

open DecimalDigits FoldedDecimal Agent101 CompleteFiberParity
open Agent105WordFiber9df76b Agent105NumericDecoder9df76b
open Agent105Predecessors9df76b

/-- All positive targets of decimal width `W` with an odd complete
predecessor count, generated from coefficient choices instead of a search
through all integers below the decimal bound. -/
def targets (W : Nat) : List Nat :=
  if W = 0 then [] else
    (noOverflowWords W ++ overflowWords (W - 1)).map natValue

private theorem source_words_accepted (W : Nat) (qs : List Nat)
    (hq : qs ∈ noOverflowWords W ++ overflowWords (W - 1)) :
    Admissible qs.length (digitFn qs) ∧
      oddProfile (half qs) (center qs) = true := by
  rcases List.mem_append.mp hq with hq | hq
  · obtain ⟨hlen, ha, ho, _⟩ := (mem_noOverflowWords W qs).mp hq
    exact ⟨by simpa only [hlen] using ha, ho⟩
  · obtain ⟨hlen, ha, ho, _⟩ := (mem_overflowWords (W - 1) qs).mp hq
    exact ⟨by simpa only [hlen] using ha, ho⟩

/-- The census lists each numerical target exactly once. This includes
disjointness between the two possible source widths. -/
theorem targets_nodup (W : Nat) : (targets W).Nodup := by
  by_cases hW : W = 0
  · simp only [targets, hW, if_true, List.nodup_nil]
  · have hwords : (noOverflowWords W ++ overflowWords (W - 1)).Nodup := by
      apply List.pairwise_append.mpr
      refine ⟨noOverflowWords_nodup W, overflowWords_nodup (W - 1), ?_⟩
      intro qs hq rs hr heq
      have hl := ((mem_noOverflowWords W qs).mp hq).1
      have hk := ((mem_overflowWords (W - 1) rs).mp hr).1
      have heqlen := congrArg List.length heq
      omega
    rw [targets, if_neg hW]
    change ((noOverflowWords W ++ overflowWords (W - 1)).map natValue).Pairwise
      (fun a b => a ≠ b)
    rw [List.pairwise_map]
    apply List.Pairwise.imp_of_mem (p := hwords)
    intro qs rs hq hr hne hv
    obtain ⟨ha, ho⟩ := source_words_accepted W qs hq
    obtain ⟨hb, hp⟩ := source_words_accepted W rs hr
    exact hne (odd_admissible_natValue_injective qs rs ha hb ho hp hv)

/-- Every enumerated integer is positive and has exactly the requested
ordinary decimal width. -/
theorem targets_have_width (W Y : Nat) (hY : Y ∈ targets W) :
    decimalWidth Y W := by
  by_cases hW : W = 0
  · simp only [targets, hW, if_true, List.not_mem_nil] at hY
  · rw [targets, if_neg hW] at hY
    obtain ⟨qs, hq, rfl⟩ := List.mem_map.mp hY
    rcases List.mem_append.mp hq with hq | hq
    · obtain ⟨hlen, ha, _, hc⟩ := (mem_noOverflowWords W qs).mp hq
      obtain ⟨e, he⟩ := admissible_natValue_canonical qs (by simpa only [hlen] using ha)
      have he' : Canonical (natValue qs) e W := by
        simpa only [hlen, hc, Nat.add_zero] using he
      exact canonical_decimalWidth _ _ _ he'
    · obtain ⟨hlen, ha, _, hc⟩ := (mem_overflowWords (W - 1) qs).mp hq
      obtain ⟨e, he⟩ := admissible_natValue_canonical qs (by simpa only [hlen] using ha)
      have hw : W - 1 + 1 = W := by omega
      have he' : Canonical (natValue qs) e W := by
        simpa only [hlen, hc, hw] using he
      exact canonical_decimalWidth _ _ _ he'

/-- Census membership is exactly odd cardinality of the complete positive
ordinary reverse-and-add predecessor list for any canonical target. -/
theorem mem_targets (Y : Nat) (e : Nat → Nat) (W : Nat)
    (hY : Canonical Y e W) :
    Y ∈ targets W ↔ (predecessors e W).length % 2 = 1 := by
  have hW : W ≠ 0 := by have hw := hY.1; omega
  rw [complete_predecessor_odd_iff Y e W hY]
  constructor
  · intro hm
    rw [targets, if_neg hW] at hm
    obtain ⟨qs, hq, hv⟩ := List.mem_map.mp hm
    rcases List.mem_append.mp hq with hq | hq
    · obtain ⟨hlen, ha, ho, _⟩ := (mem_noOverflowWords W qs).mp hq
      have hd := admissible_natValue_decode Y e W W qs hY hlen ha hv
      exact Or.inl (by simpa only [oddDecoded, hd] using ho)
    · obtain ⟨hlen, ha, ho, _⟩ := (mem_overflowWords (W - 1) qs).mp hq
      have hd := admissible_natValue_decode Y e W (W - 1) qs hY hlen ha hv
      exact Or.inr (by simpa only [oddDecoded, hd] using ho)
  · intro ho
    rw [targets, if_neg hW]
    rcases ho with ho | ho
    · cases hd : decodeNumerical e W W with
      | none => simp only [oddDecoded, hd, Bool.false_eq_true] at ho
      | some qs =>
        obtain ⟨hlen, ha, hv, hw⟩ := decode_admissible_carry Y e W W qs hY hd
        have hp : oddProfile (half qs) (center qs) = true := by
          simpa only [oddDecoded, hd] using ho
        have hc : carry (digitFn qs) W = 0 := by omega
        exact List.mem_map.mpr ⟨qs, List.mem_append.mpr (Or.inl
          ((mem_noOverflowWords W qs).mpr ⟨hlen, ha, hp, hc⟩)), hv⟩
    · cases hd : decodeNumerical e W (W - 1) with
      | none => simp only [oddDecoded, hd, Bool.false_eq_true] at ho
      | some qs =>
        obtain ⟨hlen, ha, hv, hw⟩ := decode_admissible_carry Y e W (W - 1) qs hY hd
        have hp : oddProfile (half qs) (center qs) = true := by
          simpa only [oddDecoded, hd] using ho
        have hc : carry (digitFn qs) (W - 1) = 1 := by omega
        exact List.mem_map.mpr ⟨qs, List.mem_append.mpr (Or.inr
          ((mem_overflowWords (W - 1) qs).mpr ⟨hlen, ha, hp, hc⟩)), hv⟩

end OddPredecessorTargetCensus

#print axioms OddPredecessorTargetCensus.targets
#print axioms OddPredecessorTargetCensus.targets_nodup
#print axioms OddPredecessorTargetCensus.targets_have_width
#print axioms OddPredecessorTargetCensus.mem_targets
