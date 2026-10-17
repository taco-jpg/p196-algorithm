import P196.Agent10EightCarry.ActualCarryObservability

/-!
Agent #10: two explicit canonical width-seventeen ordinary decimal inputs
have eight equal complete carry words, but different active initial pair sums
and different exact next integers. Their first carry separation is at time eight.

The nine recorded pair-sum rows are kernel-checked against the unchanged
nextWidth/nextColumns definitions. Finite-prefix congruence transports those
rows to the unchanged iterPairs recursion. The bounded-row pattern is reused
from the frozen Agent10SevenCarryCounterexample and Agent10SixCarryCounterexample.

This certificate concerns unrestricted continued reverse-and-add iteration.
Both inputs first reach decimal palindromes at time four, as certified below;
it supplies no palindrome-avoidance result and makes no claim about 196.
The concrete certificate is independent of the computational prefix filter
that found the witness. A uniform upper bound is a separate theorem.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Agent10EightCarryCounterexample
open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual

/-- Least significant digit first; values beyond width seventeen are zero. -/
def leftDigits (i : Nat) : Nat :=
  ([9,6,1,6,0,7,0,6,5,0,0,0,0,0,0,0,9] : List Nat).getD i 0

def rightDigits (i : Nat) : Nat :=
  ([9,6,1,5,3,2,6,0,8,0,0,0,0,0,0,0,9] : List Nat).getD i 0

abbrev leftColumns : Nat → Nat := columnSum leftDigits 17
abbrev rightColumns : Nat → Nat := columnSum rightDigits 17

private def inputColumns (b : Bool) : Nat → Nat :=
  if b then rightColumns else leftColumns

private def rows (b : Bool) : List (List Nat) :=
  if b then [
    [18,6,1,5,3,2,6,0,16,0,6,2,3,5,1,6,18],
    [9,15,7,6,8,5,8,6,7,7,6,8,5,8,6,7,15,9],
    [10,5,13,13,14,13,13,14,13,14,13,14,13,13,14,13,13,5,10],
    [1,6,9,8,9,9,8,9,9,9,9,9,9,8,9,9,8,9,6,1],
    [2,12,18,16,18,18,16,18,18,18,18,18,18,16,18,18,16,18,12,2],
    [5,5,18,14,18,18,14,18,18,18,18,18,18,14,18,18,14,18,5,5],
    [10,11,17,10,18,18,10,18,18,18,18,18,18,10,18,18,10,17,11,10],
    [1,3,10,9,10,18,10,10,18,18,18,18,18,10,10,18,10,9,10,3,1],
    [2,7,1,0,2,18,2,2,18,18,18,18,18,2,2,18,2,0,1,7,2]
  ] else [
    [18,6,1,6,0,7,0,6,10,6,0,7,0,6,1,6,18],
    [9,15,7,7,6,7,7,6,7,7,6,7,7,6,7,7,15,9],
    [10,5,13,14,13,13,14,13,13,14,13,13,14,13,13,14,13,5,10],
    [1,6,9,9,9,8,9,9,8,9,9,8,9,9,8,9,9,9,6,1],
    [2,12,18,18,18,16,18,18,16,18,18,16,18,18,16,18,18,18,12,2],
    [5,5,18,18,18,14,18,18,14,18,18,14,18,18,14,18,18,18,5,5],
    [10,11,17,18,18,10,18,18,10,18,18,10,18,18,10,18,18,17,11,10],
    [1,3,10,17,18,10,10,18,10,10,18,10,10,18,10,10,18,17,10,3,1],
    [2,7,1,16,18,2,2,18,2,2,18,2,2,18,2,2,18,16,1,7,2]
  ]

private def trace (b : Bool) (t i : Nat) : Nat :=
  ((rows b).getD t []).getD i 0

/-- The actual widths at times zero through eight. -/
def traceWidth (t : Nat) : Nat :=
  ([17,18,19,20,20,20,20,21,21] : List Nat).getD t 0

private theorem digit_bounds_fin :
    ∀ i : Fin 17, leftDigits i.val ≤ 9 ∧ rightDigits i.val ≤ 9 := by
  decide +kernel

theorem left_canonical : Canonical 90000000560706169 leftDigits 17 := by
  refine ⟨by decide, ?_, by decide +kernel, by decide +kernel⟩
  intro i hi
  exact (digit_bounds_fin ⟨i, hi⟩).1

theorem right_canonical : Canonical 90000000806235169 rightDigits 17 := by
  refine ⟨by decide, ?_, by decide +kernel, by decide +kernel⟩
  intro i hi
  exact (digit_bounds_fin ⟨i, hi⟩).2

private theorem initial_trace_fin :
    ∀ b : Bool, ∀ i : Fin 17, inputColumns b i.val = trace b 0 i.val := by
  decide +kernel

private theorem trace_width_bound_fin :
    ∀ t : Fin 9, traceWidth t.val ≤ 21 := by
  decide +kernel

/-- Every adjacent recorded row is checked against actual decimal addition. -/
private theorem trace_steps_fin :
    ∀ b : Bool, ∀ t : Fin 8,
      nextWidth (trace b t.val) (traceWidth t.val) = traceWidth (t.val + 1) ∧
      ∀ i : Fin 21, i.val < traceWidth (t.val + 1) →
        nextColumns (trace b t.val) (traceWidth t.val) i.val =
          trace b (t.val + 1) i.val := by
  decide +kernel

private theorem trace_carries_fin :
    ∀ t : Fin 8, ∀ i : Fin 22, i.val ≤ traceWidth t.val →
      carry (trace false t.val) i.val = carry (trace true t.val) i.val := by
  decide +kernel

/-- Bounded trace certificates describe the original recursion exactly. -/
private theorem actual_trace (b : Bool) (t : Nat) (ht : t ≤ 8) :
    (iterPairs (inputColumns b) 17 t).1 = traceWidth t ∧
      ∀ i, i < (iterPairs (inputColumns b) 17 t).1 →
        (iterPairs (inputColumns b) 17 t).2 i = trace b t i := by
  induction t with
  | zero =>
    refine ⟨rfl, ?_⟩
    intro i hi
    exact initial_trace_fin b ⟨i, hi⟩
  | succ t ih =>
    rcases ih (by omega) with ⟨hw, hp⟩
    have hc := next_state_congr_upto (iterPairs (inputColumns b) 17 t).2
      (trace b t) (iterPairs (inputColumns b) 17 t).1 hp
    have hs := trace_steps_fin b ⟨t, by omega⟩
    have hwidth : (iterPairs (inputColumns b) 17 (t+1)).1 = traceWidth (t+1) := by
      change nextWidth (iterPairs (inputColumns b) 17 t).2
        (iterPairs (inputColumns b) 17 t).1 = traceWidth (t+1)
      rw [hc.1, hw]
      exact hs.1
    refine ⟨hwidth, ?_⟩
    intro i hi
    have hi' : i < traceWidth (t+1) := by rw [←hwidth]; exact hi
    have hib : i < 21 := by
      have hb := trace_width_bound_fin ⟨t+1, by omega⟩
      change traceWidth (t+1) ≤ 21 at hb
      omega
    change nextColumns (iterPairs (inputColumns b) 17 t).2
      (iterPairs (inputColumns b) 17 t).1 i = trace b (t+1) i
    rw [hc.2 i hi, hw]
    exact hs.2 ⟨i, hib⟩ hi'

theorem left_widths (t : Nat) (ht : t ≤ 8) :
    (iterPairs leftColumns 17 t).1 = traceWidth t :=
  (actual_trace false t ht).1

theorem right_widths (t : Nat) (ht : t ≤ 8) :
    (iterPairs rightColumns 17 t).1 = traceWidth t :=
  (actual_trace true t ht).1

theorem widths_agree (t : Nat) (ht : t ≤ 8) :
    (iterPairs leftColumns 17 t).1 = (iterPairs rightColumns 17 t).1 := by
  rw [left_widths t ht, right_widths t ht]

/-- All incoming carries, including the final overflow carry, coincide. -/
theorem eight_complete_carries :
    ∀ t, t < 8 → ∀ i, i ≤ (iterPairs leftColumns 17 t).1 →
      carry (iterPairs leftColumns 17 t).2 i =
        carry (iterPairs rightColumns 17 t).2 i := by
  intro t ht i hi
  have ht8 : t ≤ 8 := by omega
  have hl := actual_trace false t ht8
  have hr := actual_trace true t ht8
  simp only [inputColumns, Bool.false_eq_true, ↓reduceIte] at hl hr
  have hiw : i ≤ traceWidth t := by rw [←hl.1]; exact hi
  have hib : i < 22 := by
    have hb := trace_width_bound_fin ⟨t, by omega⟩
    change traceWidth t ≤ 21 at hb
    omega
  have hir : i ≤ (iterPairs rightColumns 17 t).1 := by
    rw [right_widths t ht8]
    exact hiw
  calc
    carry (iterPairs leftColumns 17 t).2 i = carry (trace false t) i :=
      carry_congr_upto _ _ _ hl.2 i hi
    _ = carry (trace true t) i := trace_carries_fin ⟨t, ht⟩ ⟨i, hib⟩ hiw
    _ = carry (iterPairs rightColumns 17 t).2 i :=
      (carry_congr_upto _ _ _ hr.2 i hir).symm

theorem initial_pair_sums_differ : leftColumns 3 = 6 ∧ rightColumns 3 = 5 := by
  decide +kernel

theorem next_integer_values :
    Lychrel196.step 90000000560706169 = 186160707060706178 ∧
    Lychrel196.step 90000000806235169 = 186153261606235178 := by
  decide +kernel

theorem next_integers_differ :
    Lychrel196.step 90000000560706169 ≠ Lychrel196.step 90000000806235169 := by
  rw [next_integer_values.1, next_integer_values.2]
  decide

/-- The carried recursion has ordinary numeric semantics for these inputs. -/
theorem numeric_orbit_representations (t : Nat) (_ht : t ≤ 8) :
    (∃ d, Canonical (Lychrel196.orbit 90000000560706169 t) d
        (iterPairs leftColumns 17 t).1 ∧
      ∀ i, i < (iterPairs leftColumns 17 t).1 →
        columnSum d (iterPairs leftColumns 17 t).1 i =
          (iterPairs leftColumns 17 t).2 i) ∧
    (∃ e, Canonical (Lychrel196.orbit 90000000806235169 t) e
        (iterPairs rightColumns 17 t).1 ∧
      ∀ i, i < (iterPairs rightColumns 17 t).1 →
        columnSum e (iterPairs rightColumns 17 t).1 i =
          (iterPairs rightColumns 17 t).2 i) := by
  exact ⟨iterPairs_representation _ _ _ 17 t left_canonical (by intro i hi; rfl),
    iterPairs_representation _ _ _ 17 t right_canonical (by intro i hi; rfl)⟩

/-- The first disagreement is at time eight, at active carry index four. -/
theorem ninth_carry_differs :
    carry (iterPairs leftColumns 17 8).2 4 = 1 ∧
    carry (iterPairs rightColumns 17 8).2 4 = 0 := by
  have hl := actual_trace false 8 (by decide)
  have hr := actual_trace true 8 (by decide)
  simp only [inputColumns, Bool.false_eq_true, ↓reduceIte] at hl hr
  have hil : 4 ≤ (iterPairs leftColumns 17 8).1 := by rw [hl.1]; decide
  have hir : 4 ≤ (iterPairs rightColumns 17 8).1 := by rw [hr.1]; decide
  rw [carry_congr_upto _ _ _ hl.2 4 hil, carry_congr_upto _ _ _ hr.2 4 hir]
  decide +kernel

/-- The differing initial coefficient lies inside the canonical input width. -/
theorem initial_pair_difference_active :
    3 < 17 ∧ leftColumns 3 ≠ rightColumns 3 := by
  rw [initial_pair_sums_differ.1, initial_pair_sums_differ.2]
  decide

/-- Every earlier complete observation agrees; the ninth has an in-range mismatch. -/
theorem first_separation_at_eight :
    (∀ t, t < 8 → ∀ i, i ≤ (iterPairs leftColumns 17 t).1 →
      carry (iterPairs leftColumns 17 t).2 i =
        carry (iterPairs rightColumns 17 t).2 i) ∧
    (∃ i, i ≤ (iterPairs leftColumns 17 8).1 ∧
      carry (iterPairs leftColumns 17 8).2 i ≠
        carry (iterPairs rightColumns 17 8).2 i) := by
  refine ⟨eight_complete_carries, 4, ?_, ?_⟩
  · rw [left_widths 8 (by decide)]
    decide +kernel
  · rw [ninth_carry_differs.1, ninth_carry_differs.2]
    decide

/-- A concrete counterexample to reconstruction from eight complete carry words. -/
theorem eight_carry_counterexample :
    Canonical 90000000560706169 leftDigits 17 ∧
    Canonical 90000000806235169 rightDigits 17 ∧
    (∀ t, t < 8 → ∀ i, i ≤ (iterPairs leftColumns 17 t).1 →
      carry (iterPairs leftColumns 17 t).2 i =
        carry (iterPairs rightColumns 17 t).2 i) ∧
    leftColumns 3 ≠ rightColumns 3 ∧
    Lychrel196.step 90000000560706169 ≠ Lychrel196.step 90000000806235169 := by
  refine ⟨left_canonical, right_canonical, eight_complete_carries, ?_, next_integers_differ⟩
  rw [initial_pair_sums_differ.1, initial_pair_sums_differ.2]
  decide

/-- Exact palindrome values reached after four continued reverse-and-add steps. -/
theorem palindrome_values_at_four :
    Lychrel196.orbit 90000000560706169 4 = 16999899899899899961 ∧
    Lychrel196.orbit 90000000806235169 4 = 16989989999998998961 := by
  decide +kernel

private theorem palindrome_prefix_fin :
    ∀ t : Fin 4,
      ¬ Lychrel196.Palindrome (Lychrel196.orbit 90000000560706169 t.val) ∧
      ¬ Lychrel196.Palindrome (Lychrel196.orbit 90000000806235169 t.val) := by
  decide +kernel

/-- These inputs both first reach palindromes at time four; iteration continues. -/
theorem first_palindromes_at_four :
    (∀ t, t < 4 →
      ¬ Lychrel196.Palindrome (Lychrel196.orbit 90000000560706169 t) ∧
      ¬ Lychrel196.Palindrome (Lychrel196.orbit 90000000806235169 t)) ∧
    Lychrel196.Palindrome (Lychrel196.orbit 90000000560706169 4) ∧
    Lychrel196.Palindrome (Lychrel196.orbit 90000000806235169 4) := by
  refine ⟨?_, ?_, ?_⟩
  · intro t ht
    exact palindrome_prefix_fin ⟨t, ht⟩
  · rw [palindrome_values_at_four.1]
    decide +kernel
  · rw [palindrome_values_at_four.2]
    decide +kernel

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
#print axioms eight_complete_carries
#print axioms initial_pair_sums_differ
#print axioms next_integer_values
#print axioms next_integers_differ
#print axioms numeric_orbit_representations
#print axioms ninth_carry_differs
#print axioms initial_pair_difference_active
#print axioms first_separation_at_eight
#print axioms eight_carry_counterexample

#print axioms palindrome_values_at_four
#print axioms palindrome_prefix_fin
#print axioms first_palindromes_at_four

end Agent10EightCarryCounterexample

