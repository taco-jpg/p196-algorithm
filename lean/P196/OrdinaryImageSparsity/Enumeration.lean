import P196.SymmetricCarryCensus.Enumeration
import P196.Agent101DigitSplit.Agent101NumericFibers
import P196.Drafts.Misc.Agent221FiniteSeedBridge

/-!
# Exact enumeration of ordinary reverse-and-add images below a cutoff

Agent #6: the existing symmetric coefficient words cover every positive
ordinary source. Mapping their numerical values and inserting each value
once removes collisions both within and between source widths. The final
filter imposes the exclusive numerical cutoff.
-/

set_option autoImplicit false

namespace OrdinaryImageSparsity

open DecimalDigits DecimalQuantitativeMass FoldedDecimal Lychrel196 Agent101
open Agent124.PrefixK SevenColumn.ShortBoundary

private theorem mem_insertFold (xs : List Nat) (Y : Nat) :
    Y ∈ xs.foldr (fun x acc => acc.insert x) [] ↔ Y ∈ xs := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
    simp only [List.foldr_cons, List.mem_insert_iff, List.mem_cons, ih]

private theorem insertFold_nodup (xs : List Nat) :
    (xs.foldr (fun x acc => acc.insert x) []).Nodup := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
    simp only [List.foldr_cons]
    by_cases hx : x ∈ xs.foldr (fun y acc => acc.insert y) []
    · simpa only [List.insert_of_mem hx] using ih
    · rw [List.insert_of_not_mem hx]
      exact List.nodup_cons.mpr ⟨hx, ih⟩

private theorem insertFold_length_le (xs : List Nat) :
    (xs.foldr (fun x acc => acc.insert x) []).length ≤ xs.length := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
    simp only [List.foldr_cons, List.length_cons]
    by_cases hx : x ∈ xs.foldr (fun y acc => acc.insert y) []
    · rw [List.insert_of_mem hx]
      omega
    · rw [List.insert_of_not_mem hx, List.length_cons]
      omega

private theorem source_width_below_cutoff (n N L : Nat) (d : Nat → Nat)
    (hn : 0 < n) (hc : Canonical n d L) (hstep : step n < N) :
    L ≤ decimalLength (N - 1) := by
  have hnstep : n ≤ step n := Nat.le_add_right n _
  have hnN : n ≤ N - 1 := by omega
  obtain ⟨e, W, hW⟩ := canonical_exists (N - 1) (by omega)
  rw [decimalLength_of_canonical (N - 1) e W hW]
  have hlo := (canonical_decimalWidth n d L hc).2.1
  have hup := (canonical_decimalWidth (N - 1) e W hW).2.2
  by_cases hLW : L ≤ W
  · exact hLW
  · have hp := Nat.pow_le_pow_right (by decide : 0 < 10)
      (show W ≤ L - 1 by omega)
    omega

private theorem mem_wordValues_iff (Y K : Nat) :
    Y ∈ (shortWordsK K).map natValue ↔
      ∃ n d L, 0 < n ∧ Canonical n d L ∧ L < K ∧ step n = Y := by
  constructor
  · intro hY
    obtain ⟨w, hw, hvalue⟩ := List.mem_map.mp hY
    change w ∈ (List.range K).flatMap symWords at hw
    obtain ⟨L, hL, hw⟩ := List.mem_flatMap.mp hw
    obtain ⟨hlen, ha⟩ := (SymmetricCarryCensus.mem_symWords_iff L w).mp hw
    obtain ⟨n, d, hn, hc, _, hstep⟩ :=
      Agent221FiniteSeedBridge.realizable_step_value (wordFun w) L
        ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2
    refine ⟨n, d, L, hn, hc, List.mem_range.mp hL, ?_⟩
    calc
      step n = value (wordFun w) L := hstep
      _ = natValue w := by rw [← hlen]; rfl
      _ = Y := hvalue
  · rintro ⟨n, d, L, _, hc, hL, hstep⟩
    let q := columnSum d L
    have ha : Admissible L q :=
      NormalizationBridge.canonical_admissible n d L hc
    refine List.mem_map.mpr
      ⟨wordOf q L, wordOf_mem_shortWordsK q L K ha hL, ?_⟩
    calc
      natValue (wordOf q L) = value q L := by
        unfold natValue
        rw [wordOf_length]
        apply value_congr
        intro i hi
        exact wordOf_get q L i hi
      _ = step n := (step_eq_word_value n d q L hc (fun _ _ => rfl)).symm
      _ = Y := hstep

/-- Every distinct positive ordinary reverse-and-add target below the
exclusive cutoff, enumerated through the existing finite coefficient words. -/
def allBelow (N : Nat) : List Nat :=
  (((shortWordsK (decimalLength (N - 1) + 1)).map natValue).foldr
    (fun Y acc => acc.insert Y) []).filter (fun Y => decide (Y < N))

/-- Numerical collisions between coefficient words do not create duplicates. -/
theorem allBelow_nodup (N : Nat) : (allBelow N).Nodup := by
  exact List.Pairwise.filter _ (insertFold_nodup _)

/-- Exact unconditional membership in the ordinary reverse-and-add image.
The predecessor is an ordinary positive integer and need not have a
specified width or coefficient representation. -/
theorem mem_allBelow (Y N : Nat) :
    Y ∈ allBelow N ↔ Y < N ∧ ∃ n : Nat, 0 < n ∧ step n = Y := by
  rw [allBelow, List.mem_filter, mem_insertFold, mem_wordValues_iff]
  simp only [decide_eq_true_eq]
  constructor
  · rintro ⟨⟨n, _, _, hn, _, _, hstep⟩, hY⟩
    exact ⟨hY, n, hn, hstep⟩
  · rintro ⟨hY, n, hn, hstep⟩
    obtain ⟨d, L, hc⟩ := canonical_exists n hn
    have hL := source_width_below_cutoff n N L d hn hc
      (by simpa only [hstep] using hY)
    exact ⟨⟨n, d, L, hn, hc, by omega, hstep⟩, hY⟩

/-- Every listed target is positive and strictly below its cutoff. -/
theorem allBelow_bounds (N Y : Nat) (hY : Y ∈ allBelow N) :
    0 < Y ∧ Y < N := by
  obtain ⟨hN, n, hn, hstep⟩ := (mem_allBelow Y N).mp hY
  refine ⟨?_, hN⟩
  rw [← hstep]
  exact Nat.lt_of_lt_of_le hn (Nat.le_add_right n _)

/-- The exclusive cutoffs zero and one contain no positive targets. -/
theorem allBelow_eq_nil_small (N : Nat) (hN : N ≤ 1) : allBelow N = [] := by
  apply List.eq_nil_iff_forall_not_mem.mpr
  intro Y hY
  obtain ⟨hpos, hlt⟩ := allBelow_bounds N Y hY
  omega

/-- Distinct numerical targets cannot outnumber the original coefficient
words in the sufficient source-width range. -/
theorem allBelow_length_le (N : Nat) :
    (allBelow N).length ≤
      (shortWordsK (decimalLength (N - 1) + 1)).length := by
  have h := insertFold_length_le
    ((shortWordsK (decimalLength (N - 1) + 1)).map natValue)
  simp only [List.length_map] at h
  exact Nat.le_trans (List.length_filter_le _ _) h

end OrdinaryImageSparsity

#print axioms OrdinaryImageSparsity.allBelow
#print axioms OrdinaryImageSparsity.allBelow_nodup
#print axioms OrdinaryImageSparsity.mem_allBelow
#print axioms OrdinaryImageSparsity.allBelow_bounds
#print axioms OrdinaryImageSparsity.allBelow_eq_nil_small
#print axioms OrdinaryImageSparsity.allBelow_length_le
