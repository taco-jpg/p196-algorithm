import P196.OrdinaryImageCensus.Widths
import P196.CrossWidthTargetRecurrence.Evaluator

/-!
# Exact balance of ordinary output counts

The complete list at an output width is the union of the same-width
carry-zero values and the preceding-width carry-one values. Partitioning
both lists by membership in the first family identifies their common
part with the existing adjacent-width target census.
-/

set_option autoImplicit false

namespace OrdinaryImageCensus

open DecimalDigits Agent124.PrefixK SevenColumn.ShortBoundary

/-- The distinct output count, the adjacent-width overlap, and the
same-width overflow count exactly balance all same-width profiles and
the overflow profiles from the preceding source width. -/
theorem count_balance (W : Nat) (hW : 0 < W) :
    (widthTargets W).length + CrossWidthTargetRecurrence.targetCount (W - 1) +
      (symWords W).countP (fun w => carry (wordFun w) W == 1) =
    SymmetricCarryCensus.wordCount W +
      (symWords (W - 1)).countP (fun w => carry (wordFun w) (W - 1) == 1) := by
  have hin :
      ((widthTargets W).filter
        (fun Y => decide (Y ∈ carryValues W 0))).Perm (carryValues W 0) := by
    apply SymmetricCarryCensus.perm_of_nodup_mem_iff _ _
      ((widthTargets_nodup W).filter _) (carryValues_nodup W 0)
    intro Y
    simp only [List.mem_filter, decide_eq_true_eq]
    constructor
    · exact fun h => h.2
    · intro h
      exact ⟨(mem_widthTargets_iff_carryValues W Y hW).mpr (Or.inl h), h⟩
  have hout :
      ((widthTargets W).filter
        (fun Y => !decide (Y ∈ carryValues W 0))).Perm
      ((carryValues (W - 1) 1).filter
        (fun Y => !decide (Y ∈ carryValues W 0))) := by
    apply SymmetricCarryCensus.perm_of_nodup_mem_iff _ _
      ((widthTargets_nodup W).filter _)
      ((carryValues_nodup (W - 1) 1).filter _)
    intro Y
    simp only [List.mem_filter, not_decide_eq_true]
    constructor
    · rintro ⟨hY, hnot⟩
      rcases (mem_widthTargets_iff_carryValues W Y hW).mp hY with hY | hY
      · exact False.elim (hnot hY)
      · exact ⟨hY, hnot⟩
    · rintro ⟨hY, hnot⟩
      exact ⟨(mem_widthTargets_iff_carryValues W Y hW).mpr (Or.inr hY), hnot⟩
  have hoverlap :
      ((carryValues (W - 1) 1).filter
        (fun Y => decide (Y ∈ carryValues W 0))).Perm
      (CrossWidthTargetCensus.targets (W - 1)) := by
    apply SymmetricCarryCensus.perm_of_nodup_mem_iff _ _
      ((carryValues_nodup (W - 1) 1).filter _)
      (CrossWidthTargetCensus.targets_nodup (W - 1))
    intro Y
    simp only [List.mem_filter, decide_eq_true_eq, CrossWidthTargetCensus.mem_targets]
    constructor
    · rintro ⟨hshort, hlong⟩
      exact (mem_overlap_iff W Y hW).mp ⟨hlong, hshort⟩
    · intro hY
      obtain ⟨hlong, hshort⟩ := (mem_overlap_iff W Y hW).mpr hY
      exact ⟨hshort, hlong⟩
  have hwidth := List.length_eq_countP_add_countP
    (fun Y => decide (Y ∈ carryValues W 0)) (l := widthTargets W)
  have hshort := List.length_eq_countP_add_countP
    (fun Y => decide (Y ∈ carryValues W 0)) (l := carryValues (W - 1) 1)
  simp only [List.countP_eq_length_filter, decide_not, Bool.decide_coe] at hwidth hshort
  have h_in := hin.length_eq
  have h_out := hout.length_eq
  have h_overlap := hoverlap.length_eq
  have hpartition := carryValues_partition W
  have hlong_count := carryValues_length W 1
  have hshort_count := carryValues_length (W - 1) 1
  have hcommon_count := CrossWidthTargetRecurrence.targetCount_eq_length (W - 1)
  omega

end OrdinaryImageCensus

#print axioms OrdinaryImageCensus.count_balance
