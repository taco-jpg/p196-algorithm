import P196.EightCarryWidthBound.Reconstruction

/-!
Agent #10: the exact complete-carry observation threshold at initial widths
at most fourteen is eight. A direct canonical width-thirteen pair supplies
the lower bound: seven complete observations agree, while initial pair sums
and the next ordinary integers differ. The eighth observation separates them.

The finite rows below are checked against the original decimal transition.
Existing prefix congruence and numeric representation theorems provide the
semantic bridge. Both inputs first reach palindromes at time two; continued
iteration is used, without a palindrome-avoidance hypothesis. The result does
not assert that fourteen is the largest width admitting reconstruction from
eight observations.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace EightCarryWidthBound
open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual

/-- A finite list of certified active rows represents the original recursion.
Irrelevant function tails are handled by the existing prefix congruence lemma. -/
private theorem certified_rows_sound
    (q : Nat → Nat) (L K : Nat) (w : Nat → Nat) (r : Nat → Nat → Nat)
    (hwidth : w 0 = L)
    (hinitial : ∀ i, i < L → q i = r 0 i)
    (hsteps : ∀ t, t < K →
      nextWidth (r t) (w t) = w (t + 1) ∧
      ∀ i, i < w (t + 1) → nextColumns (r t) (w t) i = r (t + 1) i) :
    ∀ t, t ≤ K → (iterPairs q L t).1 = w t ∧
      ∀ i, i < (iterPairs q L t).1 → (iterPairs q L t).2 i = r t i := by
  intro t ht
  induction t with
  | zero => exact ⟨hwidth.symm, hinitial⟩
  | succ t ih =>
    rcases ih (by omega) with ⟨hw, hp⟩
    have hn := next_state_congr_upto (iterPairs q L t).2 (r t)
      (iterPairs q L t).1 hp
    have hs := hsteps t (by omega)
    have hw' : (iterPairs q L (t + 1)).1 = w (t + 1) := by
      change nextWidth (iterPairs q L t).2 (iterPairs q L t).1 = _
      rw [hn.1, hw]
      exact hs.1
    refine ⟨hw', ?_⟩
    intro i hi
    have hir : i < w (t + 1) := by rw [← hw']; exact hi
    change nextColumns (iterPairs q L t).2 (iterPairs q L t).1 i = _
    rw [hn.2 i hi, hw]
    exact hs.2 i hir

namespace WidthThirteenWitness

/-- The two ordinary positive decimal inputs. -/
def seed (b : Bool) : Nat :=
  if b then 9000001716109 else 9000004163209

/-- Canonical decimal digits, least significant first. -/
def digits (b : Bool) (i : Nat) : Nat :=
  ((if b then [9,0,1,6,1,7,1,0,0,0,0,0,9] else [9,0,2,3,6,1,4,0,0,0,0,0,9]) : List Nat).getD i 0

abbrev columns (b : Bool) : Nat → Nat := columnSum (digits b) 13

private def rows (b : Bool) : List (List Nat) :=
  if b then [
    [18,0,1,6,1,7,2,7,1,6,1,0,18],
    [9,9,1,7,7,8,9,9,8,7,7,1,9,9],
    [18,18,2,14,14,16,18,18,16,14,14,2,18,18],
    [9,18,11,7,10,12,16,18,16,12,10,7,11,18,9],
    [10,8,11,9,8,4,10,16,16,10,4,8,9,11,8,10],
    [1,9,10,1,18,12,5,8,14,8,5,12,18,1,10,9,1],
    [3,9,0,4,17,5,11,17,8,17,11,5,17,4,0,9,3],
    [6,18,0,9,14,12,3,15,18,15,3,12,14,9,0,18,6]
  ] else [
    [18,0,2,3,6,1,8,1,6,3,2,0,18],
    [9,9,2,5,9,7,9,9,7,9,5,2,9,9],
    [18,18,4,10,18,14,18,18,14,18,10,4,18,18],
    [9,18,13,5,10,14,14,18,14,14,10,5,13,18,9],
    [10,8,13,9,6,6,10,14,14,10,6,6,9,13,8,10],
    [1,9,12,3,16,12,7,6,10,6,7,12,16,3,12,9,1],
    [3,9,4,8,13,5,15,13,0,13,15,5,13,8,4,9,3],
    [6,18,8,17,6,12,11,7,2,7,11,12,6,17,8,18,6]
  ]

private def row (b : Bool) (t i : Nat) : Nat :=
  ((rows b).getD t []).getD i 0

/-- Exact active widths at times zero through seven. -/
def traceWidth (t : Nat) : Nat :=
  ([13,14,14,15,16,17,17,17] : List Nat).getD t 0

private theorem digit_bounds_fin :
    ∀ b : Bool, ∀ i : Fin 13, digits b i.val ≤ 9 := by
  decide +kernel

theorem canonical (b : Bool) : Canonical (seed b) (digits b) 13 := by
  refine ⟨by decide, ?_, ?_, ?_⟩
  · intro i hi
    exact digit_bounds_fin b ⟨i, hi⟩
  · cases b <;> decide +kernel
  · cases b <;> decide +kernel

theorem admissible (b : Bool) : Admissible 13 (columns b) :=
  NormalizationBridge.canonical_admissible (seed b) (digits b) 13 (canonical b)

private theorem initial_rows_fin :
    ∀ b : Bool, ∀ i : Fin 13, columns b i.val = row b 0 i.val := by
  decide +kernel

private theorem width_bound_fin : ∀ t : Fin 8, traceWidth t.val ≤ 17 := by
  decide +kernel

/-- Every recorded transition is checked against ordinary decimal addition. -/
private theorem steps_fin :
    ∀ b : Bool, ∀ t : Fin 7,
      nextWidth (row b t.val) (traceWidth t.val) = traceWidth (t.val + 1) ∧
      ∀ i : Fin 17, i.val < traceWidth (t.val + 1) →
        nextColumns (row b t.val) (traceWidth t.val) i.val = row b (t.val + 1) i.val := by
  decide +kernel

/-- The finite check includes incoming index zero and the terminal carry. -/
private theorem carries_fin :
    ∀ t : Fin 7, ∀ i : Fin 18, i.val ≤ traceWidth t.val →
      carry (row false t.val) i.val = carry (row true t.val) i.val := by
  decide +kernel

private theorem actual_rows (b : Bool) (t : Nat) (ht : t ≤ 7) :
    (iterPairs (columns b) 13 t).1 = traceWidth t ∧
      ∀ i, i < (iterPairs (columns b) 13 t).1 →
        (iterPairs (columns b) 13 t).2 i = row b t i := by
  apply certified_rows_sound (columns b) 13 7 traceWidth (row b)
    (by decide) (fun i hi => initial_rows_fin b ⟨i, hi⟩) ?_ t ht
  intro k hk
  have hs := steps_fin b ⟨k, hk⟩
  refine ⟨hs.1, ?_⟩
  intro i hi
  have hb := width_bound_fin ⟨k + 1, by omega⟩
  have hib : i < 17 := by
    change traceWidth (k + 1) ≤ 17 at hb
    omega
  exact hs.2 ⟨i, hib⟩ hi

theorem widths (b : Bool) (t : Nat) (ht : t ≤ 7) :
    (iterPairs (columns b) 13 t).1 = traceWidth t :=
  (actual_rows b t ht).1

/-- Seven complete carry observations agree at a shared initial width thirteen. -/
theorem seven_complete_carries :
    ∀ t, t < 7 → ∀ i, i ≤ (iterPairs (columns false) 13 t).1 →
      carry (iterPairs (columns false) 13 t).2 i =
        carry (iterPairs (columns true) 13 t).2 i := by
  intro t ht i hi
  have hl := actual_rows false t (by omega)
  have hr := actual_rows true t (by omega)
  have hiw : i ≤ traceWidth t := by rw [← hl.1]; exact hi
  have hib : i < 18 := by
    have hb := width_bound_fin ⟨t, by omega⟩
    change traceWidth t ≤ 17 at hb
    omega
  have hir : i ≤ (iterPairs (columns true) 13 t).1 := by rw [hr.1]; exact hiw
  calc
    carry (iterPairs (columns false) 13 t).2 i = carry (row false t) i :=
      carry_congr_upto _ _ _ hl.2 i hi
    _ = carry (row true t) i := carries_fin ⟨t, ht⟩ ⟨i, hib⟩ hiw
    _ = carry (iterPairs (columns true) 13 t).2 i :=
      (carry_congr_upto _ _ _ hr.2 i hir).symm

/-- The differing coefficient is active and equals two versus one. -/
theorem initial_pair_difference :
    2 < 13 ∧ columns false 2 = 2 ∧ columns true 2 = 1 := by
  decide +kernel

theorem next_values :
    Lychrel196.step (seed false) = 18023618163218 ∧
    Lychrel196.step (seed true) = 18016172716118 := by
  decide +kernel

theorem next_integers_differ : Lychrel196.step (seed false) ≠ Lychrel196.step (seed true) := by
  rw [next_values.1, next_values.2]
  decide

/-- The original numeric orbit realizes the certified pair evolution. -/
theorem numeric_orbit_representation (b : Bool) (t : Nat) :
    ∃ d, Canonical (Lychrel196.orbit (seed b) t) d (iterPairs (columns b) 13 t).1 ∧
      ∀ i, i < (iterPairs (columns b) 13 t).1 →
        columnSum d (iterPairs (columns b) 13 t).1 i = (iterPairs (columns b) 13 t).2 i :=
  iterPairs_representation (seed b) (digits b) (columns b) 13 t (canonical b)
    (by intro i hi; rfl)

/-- The eighth observation separates the inputs at active incoming index four. -/
theorem eighth_observation_differs :
    4 ≤ (iterPairs (columns false) 13 7).1 ∧
    carry (iterPairs (columns false) 13 7).2 4 = 1 ∧
    carry (iterPairs (columns true) 13 7).2 4 = 0 := by
  have hl := actual_rows false 7 (by decide)
  have hr := actual_rows true 7 (by decide)
  have hil : 4 ≤ (iterPairs (columns false) 13 7).1 := by rw [hl.1]; decide
  have hir : 4 ≤ (iterPairs (columns true) 13 7).1 := by rw [hr.1]; decide
  refine ⟨hil, ?_⟩
  rw [carry_congr_upto _ _ _ hl.2 4 hil, carry_congr_upto _ _ _ hr.2 4 hir]
  decide +kernel

/-- Direct ordinary-integer witness against seven-observation reconstruction. -/
theorem seven_carry_counterexample :
    Canonical 9000004163209 (digits false) 13 ∧
    Canonical 9000001716109 (digits true) 13 ∧
    Admissible 13 (columns false) ∧ Admissible 13 (columns true) ∧
    (∀ t, t < 7 → ∀ i, i ≤ (iterPairs (columns false) 13 t).1 →
      carry (iterPairs (columns false) 13 t).2 i =
        carry (iterPairs (columns true) 13 t).2 i) ∧
    columns false 2 ≠ columns true 2 ∧
    Lychrel196.step 9000004163209 ≠ Lychrel196.step 9000001716109 := by
  refine ⟨canonical false, canonical true, admissible false, admissible true,
    seven_complete_carries, ?_, next_integers_differ⟩
  have h := initial_pair_difference
  omega

/-- Both inputs first reach palindromes at time two; the carry history continues. -/
theorem first_palindromes_at_two :
    (∀ b : Bool, ∀ t, t < 2 → ¬ Lychrel196.Palindrome (Lychrel196.orbit (seed b) t)) ∧
    (∀ b : Bool, Lychrel196.Palindrome (Lychrel196.orbit (seed b) 2)) := by
  have hsmall : ∀ b : Bool, ∀ t : Fin 2,
      ¬ Lychrel196.Palindrome (Lychrel196.orbit (seed b) t.val) := by decide +kernel
  refine ⟨fun b t ht => hsmall b ⟨t, ht⟩, ?_⟩
  decide +kernel

end WidthThirteenWitness

/-- Uniform active-pair reconstruction at shared initial widths at most fourteen. -/
def PairReconstructionUpToFourteen (K : Nat) : Prop :=
  ∀ (q r : Nat → Nat) (L : Nat), Admissible L q → Admissible L r → L ≤ 14 →
    (∀ t, t < K → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) →
    ∀ i, i < L → q i = r i

/-- Uniform next-integer reconstruction at shared canonical initial widths at most
fourteen. There is no bound on later widths and iteration continues at palindromes. -/
def NextIntegerReconstructionUpToFourteen (K : Nat) : Prop :=
  ∀ (n m : Nat) (d e : Nat → Nat) (L : Nat),
    Canonical n d L → Canonical m e L → L ≤ 14 →
    (∀ t, t < K → ∀ i, i ≤ (iterPairs (columnSum d L) L t).1 →
      carry (iterPairs (columnSum d L) L t).2 i =
        carry (iterPairs (columnSum e L) L t).2 i) →
    Lychrel196.step n = Lychrel196.step m

theorem pair_reconstruction_up_to_fourteen_iff (K : Nat) :
    PairReconstructionUpToFourteen K ↔ 8 ≤ K := by
  constructor
  · intro h
    by_cases hK : 8 ≤ K
    · exact hK
    · have he := h (WidthThirteenWitness.columns false) (WidthThirteenWitness.columns true) 13
        (WidthThirteenWitness.admissible false) (WidthThirteenWitness.admissible true)
        (by decide) (fun t ht i hi => WidthThirteenWitness.seven_complete_carries t (by omega) i hi)
      have hdiff := WidthThirteenWitness.initial_pair_difference
      have he2 := he 2 (by decide)
      omega
  · intro hK q r L hq hr hL hc
    exact eight_carry_words_determine_pair_sums_of_width_le_fourteen q r L hq hr hL
      (fun t ht i hi => hc t (by omega) i hi)

theorem next_integer_reconstruction_up_to_fourteen_iff (K : Nat) :
    NextIntegerReconstructionUpToFourteen K ↔ 8 ≤ K := by
  constructor
  · intro h
    by_cases hK : 8 ≤ K
    · exact hK
    · exfalso
      apply WidthThirteenWitness.next_integers_differ
      exact h (WidthThirteenWitness.seed false) (WidthThirteenWitness.seed true)
        (WidthThirteenWitness.digits false) (WidthThirteenWitness.digits true) 13
        (WidthThirteenWitness.canonical false) (WidthThirteenWitness.canonical true)
        (by decide) (fun t ht i hi => WidthThirteenWitness.seven_complete_carries t (by omega) i hi)
  · intro hK n m d e L hn hm hL hc
    exact eight_carry_words_determine_next_integer_of_width_le_fourteen n m d e L hn hm hL
      (fun t ht i hi => hc t (by omega) i hi)

/-- Eight is the exact uniform observation threshold for both bounded-width tasks. -/
theorem eight_is_exact_threshold_through_fourteen :
    (∀ K, PairReconstructionUpToFourteen K ↔ 8 ≤ K) ∧
    (∀ K, NextIntegerReconstructionUpToFourteen K ↔ 8 ≤ K) :=
  ⟨pair_reconstruction_up_to_fourteen_iff, next_integer_reconstruction_up_to_fourteen_iff⟩

#print axioms certified_rows_sound
#print axioms WidthThirteenWitness.canonical
#print axioms WidthThirteenWitness.admissible
#print axioms WidthThirteenWitness.seven_complete_carries
#print axioms WidthThirteenWitness.numeric_orbit_representation
#print axioms WidthThirteenWitness.eighth_observation_differs
#print axioms WidthThirteenWitness.seven_carry_counterexample
#print axioms WidthThirteenWitness.first_palindromes_at_two
#print axioms pair_reconstruction_up_to_fourteen_iff
#print axioms next_integer_reconstruction_up_to_fourteen_iff
#print axioms eight_is_exact_threshold_through_fourteen

end EightCarryWidthBound
