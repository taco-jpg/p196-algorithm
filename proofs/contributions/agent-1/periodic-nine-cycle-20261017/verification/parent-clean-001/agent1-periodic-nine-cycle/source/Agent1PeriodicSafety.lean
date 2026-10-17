import Agent1PeriodicSafetyAlphabet

/-!
The literal finite safety test from periodic_word_quotient.py. Its two rejected
patterns are the original FoldedDecimal.BadWord patterns. Positive repetition
does not change the alphabet or outside coefficient, and maximal whole-period
stripping preserves this test. No forward preservation of safety is asserted.
-/

namespace Agent1.Periodic

open Agent8

/-- Exact Boolean counterpart of the original Python safe(s), without
expanding any repeated word. On valid states the period is nonempty. -/
def safePeriodic (B H w : Word) : Bool :=
  !((B ++ H ++ w).all (fun x => decide (x ≤ 9)) ||
    (decide ((B ++ w).headD 0 = 11) &&
      (B ++ H ++ w).all (fun x => decide (x = 0 ∨ x = 11))))

private theorem safePeriodic_spec (B H w : Word) :
    safePeriodic B H w = true ↔
      ¬ ((∀ x ∈ B ++ H ++ w, x ≤ 9) ∨
        ((B ++ w).headD 0 = 11 ∧ ∀ x ∈ B ++ H ++ w, x = 0 ∨ x = 11)) := by
  unfold safePeriodic
  rw [Bool.not_eq_true', Bool.eq_false_iff]
  apply not_congr
  simp only [Bool.or_eq_true, Bool.and_eq_true, List.all_eq_true, decide_eq_true_eq]

private theorem forall_index_iff_mem (W : Word) (P : Nat → Prop) :
    (∀ i, i < W.length → P ((W[i]?).getD 0)) ↔ ∀ x ∈ W, P x := by
  constructor
  · intro h x hx
    obtain ⟨i, hi, he⟩ := List.mem_iff_getElem.mp hx
    simpa only [List.getElem?_eq_getElem hi, Option.getD_some, he] using h i hi
  · intro h i hi
    rw [List.getElem?_eq_getElem hi, Option.getD_some]
    exact h _ (List.getElem_mem hi)

/-- The finite state test is exactly the complement of the original bad
language at every positive exponent. No bounds or symmetry are assumed. -/
theorem safePeriodic_iff_not_bad (B H w : Word) (k : Nat)
    (hk : 0 < k) (hw : w ≠ []) :
    safePeriodic B H w = true ↔
      ¬ FoldedDecimal.BadWord (periodicWord B H w k).length
        (fun i => ((periodicWord B H w k)[i]?).getD 0) := by
  have hhead : ((periodicWord B H w k)[0]?).getD 0 = (B ++ w).headD 0 := by
    simpa only [List.headD_eq_head?_getD, List.head?_eq_getElem?] using
      periodicWord_head B H w k hk hw
  rw [safePeriodic_spec]
  apply not_congr
  rw [FoldedDecimal.BadWord,
    forall_index_iff_mem (periodicWord B H w k) (fun x => x ≤ 9),
    forall_index_iff_mem (periodicWord B H w k) (fun x => x = 0 ∨ x = 11), hhead]
  simp only [mem_periodicWord_iff B H w k _ hk]

/-- The exact stopped outer/center algorithms preserve the state safety
test, even when either residual block is empty. -/
theorem safePeriodic_strip (B H w : Word) (hw : w ≠ []) :
    safePeriodic (stripPeriodSuffix w B).1 (stripPeriodCenter w H).1 w =
      safePeriodic B H w := by
  apply Bool.eq_iff_iff.mpr
  rw [safePeriodic_spec, safePeriodic_spec, stripPeriodSuffix_outside w B hw]
  simp only [mem_stripped_alphabet_iff]

/-- The quotient safety flag equals the raw image safety flag. It is not
asserted equal to the predecessor flag. -/
theorem safePeriodic_quotient_eq_raw (B H w : Word) (hv : ValidPeriodic B H w) :
    safePeriodic (quotientOuter B H w) (quotientCenter B H w) (rawPeriod B H w) =
      safePeriodic (rawOuter B H w) (rawCenter B H w) (rawPeriod B H w) := by
  have hw : rawPeriod B H w ≠ [] := by
    intro he
    have hl := (raw_block_lengths B H w hv.outer_bounded hv.center_bounded
      hv.period_bounded hv.period_length).2.1
    simp only [he, List.length_nil] at hl
    omega
  exact safePeriodic_strip (rawOuter B H w) (rawCenter B H w) (rawPeriod B H w) hw

end Agent1.Periodic

#print axioms Agent1.Periodic.safePeriodic_iff_not_bad
#print axioms Agent1.Periodic.safePeriodic_strip
#print axioms Agent1.Periodic.safePeriodic_quotient_eq_raw
