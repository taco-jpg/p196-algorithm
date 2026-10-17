import P196.Agent10EightCarry.ActualCarryObservability

/-!
Agent #10: two explicit canonical width-fifteen ordinary decimal inputs have
seven equal complete carry words, but different active initial pair sums and
different exact next integers. Their first carry separation is at time seven.

The eight recorded pair-sum rows are kernel-checked against the unchanged
nextWidth/nextColumns definitions. Finite-prefix congruence transports those
rows to the unchanged iterPairs recursion. This bounded-row proof pattern is
reused from Agent10SixCarryCounterexample, whose source remains unchanged.

This certificate establishes insufficiency of seven complete observations.
It does not claim a failure at eight or an optimal universal memory bound.
The example was found in the exact twice-padded width-fifteen lift scan;
its direct certificate does not depend on that scan's prefix filter.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Agent10SevenCarryCounterexample
open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual

/-- Least significant digit first; the values beyond width fifteen are zero. -/
def leftDigits (i : Nat) : Nat :=
  ([9,0,2,3,6,1,8,5,0,0,0,0,0,0,9] : List Nat).getD i 0

def rightDigits (i : Nat) : Nat :=
  ([9,0,1,6,1,7,2,8,0,0,0,0,0,0,9] : List Nat).getD i 0

abbrev leftColumns : Nat → Nat := columnSum leftDigits 15
abbrev rightColumns : Nat → Nat := columnSum rightDigits 15

private def inputColumns (b : Bool) : Nat → Nat :=
  if b then rightColumns else leftColumns

private def rows (b : Bool) : List (List Nat) :=
  if b then [
    [18,0,1,6,1,7,2,16,2,7,1,6,1,0,18],
    [9,9,1,7,7,8,9,9,9,9,8,7,7,1,9,9],
    [18,18,2,14,14,16,18,18,18,18,16,14,14,2,18,18],
    [9,18,11,7,10,12,16,18,18,18,16,12,10,7,11,18,9],
    [10,8,11,9,8,4,10,16,18,18,16,10,4,8,9,11,8,10],
    [1,9,10,1,18,12,5,8,16,18,16,8,5,12,18,1,10,9,1],
    [3,9,0,4,17,5,11,17,13,18,13,17,11,5,17,4,0,9,3],
    [6,18,0,9,14,12,3,16,8,18,8,16,3,12,14,9,0,18,6]
  ] else [
    [18,0,2,3,6,1,8,10,8,1,6,3,2,0,18],
    [9,9,2,5,9,7,9,9,9,9,7,9,5,2,9,9],
    [18,18,4,10,18,14,18,18,18,18,14,18,10,4,18,18],
    [9,18,13,5,10,14,14,18,18,18,14,14,10,5,13,18,9],
    [10,8,13,9,6,6,10,14,18,18,14,10,6,6,9,13,8,10],
    [1,9,12,3,16,12,7,6,14,18,14,6,7,12,16,3,12,9,1],
    [3,9,4,8,13,5,15,13,9,18,9,13,15,5,13,8,4,9,3],
    [6,18,8,17,6,12,11,8,0,18,0,8,11,12,6,17,8,18,6]
  ]

private def trace (b : Bool) (t i : Nat) : Nat :=
  ((rows b).getD t []).getD i 0

/-- The actual widths at times zero through seven. -/
def traceWidth (t : Nat) : Nat :=
  ([15,16,16,17,18,19,19,19] : List Nat).getD t 0

private theorem digit_bounds_fin :
    ∀ i : Fin 15, leftDigits i.val ≤ 9 ∧ rightDigits i.val ≤ 9 := by
  decide +kernel

theorem left_canonical : Canonical 900000058163209 leftDigits 15 := by
  refine ⟨by decide, ?_, by decide +kernel, by decide +kernel⟩
  intro i hi
  exact (digit_bounds_fin ⟨i, hi⟩).1

theorem right_canonical : Canonical 900000082716109 rightDigits 15 := by
  refine ⟨by decide, ?_, by decide +kernel, by decide +kernel⟩
  intro i hi
  exact (digit_bounds_fin ⟨i, hi⟩).2

private theorem initial_trace_fin :
    ∀ b : Bool, ∀ i : Fin 15, inputColumns b i.val = trace b 0 i.val := by
  decide +kernel

private theorem trace_width_bound_fin :
    ∀ t : Fin 8, traceWidth t.val ≤ 19 := by
  decide +kernel

/-- Every adjacent recorded row is checked against actual decimal addition. -/
private theorem trace_steps_fin :
    ∀ b : Bool, ∀ t : Fin 7,
      nextWidth (trace b t.val) (traceWidth t.val) = traceWidth (t.val + 1) ∧
      ∀ i : Fin 19, i.val < traceWidth (t.val + 1) →
        nextColumns (trace b t.val) (traceWidth t.val) i.val =
          trace b (t.val + 1) i.val := by
  decide +kernel

private theorem trace_carries_fin :
    ∀ t : Fin 7, ∀ i : Fin 20, i.val ≤ traceWidth t.val →
      carry (trace false t.val) i.val = carry (trace true t.val) i.val := by
  decide +kernel

/-- Bounded trace certificates describe the original recursion exactly. -/
private theorem actual_trace (b : Bool) (t : Nat) (ht : t ≤ 7) :
    (iterPairs (inputColumns b) 15 t).1 = traceWidth t ∧
      ∀ i, i < (iterPairs (inputColumns b) 15 t).1 →
        (iterPairs (inputColumns b) 15 t).2 i = trace b t i := by
  induction t with
  | zero =>
    refine ⟨rfl, ?_⟩
    intro i hi
    exact initial_trace_fin b ⟨i, hi⟩
  | succ t ih =>
    rcases ih (by omega) with ⟨hw, hp⟩
    have hc := next_state_congr_upto (iterPairs (inputColumns b) 15 t).2
      (trace b t) (iterPairs (inputColumns b) 15 t).1 hp
    have hs := trace_steps_fin b ⟨t, by omega⟩
    have hwidth : (iterPairs (inputColumns b) 15 (t+1)).1 = traceWidth (t+1) := by
      change nextWidth (iterPairs (inputColumns b) 15 t).2
        (iterPairs (inputColumns b) 15 t).1 = traceWidth (t+1)
      rw [hc.1, hw]
      exact hs.1
    refine ⟨hwidth, ?_⟩
    intro i hi
    have hi' : i < traceWidth (t+1) := by rw [←hwidth]; exact hi
    have hib : i < 19 := by
      have hb := trace_width_bound_fin ⟨t+1, by omega⟩
      change traceWidth (t+1) ≤ 19 at hb
      omega
    change nextColumns (iterPairs (inputColumns b) 15 t).2
      (iterPairs (inputColumns b) 15 t).1 i = trace b (t+1) i
    rw [hc.2 i hi, hw]
    exact hs.2 ⟨i, hib⟩ hi'

theorem left_widths (t : Nat) (ht : t ≤ 7) :
    (iterPairs leftColumns 15 t).1 = traceWidth t :=
  (actual_trace false t ht).1

theorem right_widths (t : Nat) (ht : t ≤ 7) :
    (iterPairs rightColumns 15 t).1 = traceWidth t :=
  (actual_trace true t ht).1

theorem widths_agree (t : Nat) (ht : t ≤ 7) :
    (iterPairs leftColumns 15 t).1 = (iterPairs rightColumns 15 t).1 := by
  rw [left_widths t ht, right_widths t ht]

/-- All incoming carries, including the final overflow carry, coincide. -/
theorem seven_complete_carries :
    ∀ t, t < 7 → ∀ i, i ≤ (iterPairs leftColumns 15 t).1 →
      carry (iterPairs leftColumns 15 t).2 i =
        carry (iterPairs rightColumns 15 t).2 i := by
  intro t ht i hi
  have ht7 : t ≤ 7 := by omega
  have hl := actual_trace false t ht7
  have hr := actual_trace true t ht7
  simp only [inputColumns, Bool.false_eq_true, ↓reduceIte] at hl hr
  have hiw : i ≤ traceWidth t := by rw [←hl.1]; exact hi
  have hib : i < 20 := by
    have hb := trace_width_bound_fin ⟨t, by omega⟩
    change traceWidth t ≤ 19 at hb
    omega
  have hir : i ≤ (iterPairs rightColumns 15 t).1 := by
    rw [right_widths t ht7]
    exact hiw
  calc
    carry (iterPairs leftColumns 15 t).2 i = carry (trace false t) i :=
      carry_congr_upto _ _ _ hl.2 i hi
    _ = carry (trace true t) i := trace_carries_fin ⟨t, ht⟩ ⟨i, hib⟩ hiw
    _ = carry (iterPairs rightColumns 15 t).2 i :=
      (carry_congr_upto _ _ _ hr.2 i hir).symm

theorem initial_pair_sums_differ : leftColumns 2 = 2 ∧ rightColumns 2 = 1 := by
  decide +kernel

theorem next_integer_values :
    Lychrel196.step 900000058163209 = 1802361908163218 ∧
    Lychrel196.step 900000082716109 = 1801617362716118 := by
  decide +kernel

theorem next_integers_differ :
    Lychrel196.step 900000058163209 ≠ Lychrel196.step 900000082716109 := by
  rw [next_integer_values.1, next_integer_values.2]
  decide

/-- The carried recursion has ordinary numeric semantics for these inputs. -/
theorem numeric_orbit_representations (t : Nat) (_ht : t ≤ 7) :
    (∃ d, Canonical (Lychrel196.orbit 900000058163209 t) d
        (iterPairs leftColumns 15 t).1 ∧
      ∀ i, i < (iterPairs leftColumns 15 t).1 →
        columnSum d (iterPairs leftColumns 15 t).1 i =
          (iterPairs leftColumns 15 t).2 i) ∧
    (∃ e, Canonical (Lychrel196.orbit 900000082716109 t) e
        (iterPairs rightColumns 15 t).1 ∧
      ∀ i, i < (iterPairs rightColumns 15 t).1 →
        columnSum e (iterPairs rightColumns 15 t).1 i =
          (iterPairs rightColumns 15 t).2 i) := by
  exact ⟨iterPairs_representation _ _ _ 15 t left_canonical (by intro i hi; rfl),
    iterPairs_representation _ _ _ 15 t right_canonical (by intro i hi; rfl)⟩

/-- The first disagreement is at time seven, at active carry index four. -/
theorem eighth_carry_differs :
    carry (iterPairs leftColumns 15 7).2 4 = 1 ∧
    carry (iterPairs rightColumns 15 7).2 4 = 0 := by
  have hl := actual_trace false 7 (by decide)
  have hr := actual_trace true 7 (by decide)
  simp only [inputColumns, Bool.false_eq_true, ↓reduceIte] at hl hr
  have hil : 4 ≤ (iterPairs leftColumns 15 7).1 := by rw [hl.1]; decide
  have hir : 4 ≤ (iterPairs rightColumns 15 7).1 := by rw [hr.1]; decide
  rw [carry_congr_upto _ _ _ hl.2 4 hil, carry_congr_upto _ _ _ hr.2 4 hir]
  decide +kernel

/-- The differing initial coefficient lies inside the canonical input width. -/
theorem initial_pair_difference_active :
    2 < 15 ∧ leftColumns 2 ≠ rightColumns 2 := by
  rw [initial_pair_sums_differ.1, initial_pair_sums_differ.2]
  decide

/-- Every earlier complete observation agrees; the eighth has an in-range mismatch. -/
theorem first_separation_at_seven :
    (∀ t, t < 7 → ∀ i, i ≤ (iterPairs leftColumns 15 t).1 →
      carry (iterPairs leftColumns 15 t).2 i =
        carry (iterPairs rightColumns 15 t).2 i) ∧
    (∃ i, i ≤ (iterPairs leftColumns 15 7).1 ∧
      carry (iterPairs leftColumns 15 7).2 i ≠
        carry (iterPairs rightColumns 15 7).2 i) := by
  refine ⟨seven_complete_carries, 4, ?_, ?_⟩
  · rw [left_widths 7 (by decide)]
    decide +kernel
  · rw [eighth_carry_differs.1, eighth_carry_differs.2]
    decide

/-- A concrete counterexample to reconstruction from seven complete carry words. -/
theorem seven_carry_counterexample :
    Canonical 900000058163209 leftDigits 15 ∧
    Canonical 900000082716109 rightDigits 15 ∧
    (∀ t, t < 7 → ∀ i, i ≤ (iterPairs leftColumns 15 t).1 →
      carry (iterPairs leftColumns 15 t).2 i =
        carry (iterPairs rightColumns 15 t).2 i) ∧
    leftColumns 2 ≠ rightColumns 2 ∧
    Lychrel196.step 900000058163209 ≠ Lychrel196.step 900000082716109 := by
  refine ⟨left_canonical, right_canonical, seven_complete_carries, ?_, next_integers_differ⟩
  rw [initial_pair_sums_differ.1, initial_pair_sums_differ.2]
  decide

#print axioms digit_bounds_fin
#print axioms initial_trace_fin
#print axioms trace_width_bound_fin
#print axioms trace_steps_fin
#print axioms trace_carries_fin
#print axioms actual_trace
#print axioms left_canonical
#print axioms right_canonical
#print axioms left_widths
#print axioms right_widths
#print axioms widths_agree
#print axioms seven_complete_carries
#print axioms initial_pair_sums_differ
#print axioms next_integer_values
#print axioms next_integers_differ
#print axioms numeric_orbit_representations
#print axioms eighth_carry_differs
#print axioms initial_pair_difference_active
#print axioms first_separation_at_seven
#print axioms seven_carry_counterexample

end Agent10SevenCarryCounterexample

