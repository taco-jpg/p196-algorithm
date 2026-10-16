import ActualCarryObservability

/-!
Agent #10: two explicit ordinary decimal inputs have six equal complete carry
words, but different initial pair sums and different next integers.

The seven recorded pair-sum rows below are certificates checked by the kernel
against the unchanged nextWidth/nextColumns definitions. Finite-prefix
congruence transports them to the unchanged iterPairs recursion. The initial
digit functions are proved Canonical for the two displayed integers.

The seventh observation already differs. This establishes insufficiency of
six complete carry observations, with no claim about seven or eight.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Agent10SixCarryCounterexample
open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual

/-- Least significant digit first; the values beyond width eleven are zero. -/
def leftDigits (i : Nat) : Nat :=
  ([9,3,5,1,7,5,0,0,0,0,8] : List Nat).getD i 0

def rightDigits (i : Nat) : Nat :=
  ([9,6,0,7,1,8,0,0,0,0,7] : List Nat).getD i 0

abbrev leftColumns : Nat → Nat := columnSum leftDigits 11
abbrev rightColumns : Nat → Nat := columnSum rightDigits 11

private def inputColumns (b : Bool) : Nat → Nat :=
  if b then rightColumns else leftColumns

private def rows (b : Bool) : List (List Nat) :=
  if b then [
    [16,6,0,7,1,16,1,7,0,6,16],
    [7,13,6,7,8,8,8,8,7,6,13,7],
    [15,6,13,14,16,16,16,16,14,13,6,15],
    [6,12,10,9,12,14,14,14,12,9,10,12,6],
    [13,5,2,0,6,10,10,10,6,0,2,5,13],
    [4,9,7,2,6,7,2,2,7,6,2,7,9,4],
    [8,18,14,4,12,14,4,4,14,12,4,14,18,8]
  ] else [
    [17,3,5,1,7,10,7,1,5,3,17],
    [8,11,8,6,8,8,8,8,6,8,11,8],
    [17,2,17,12,16,16,16,16,12,17,2,17],
    [8,10,10,11,10,14,14,14,10,11,10,10,8],
    [17,1,2,4,2,10,10,10,2,4,2,1,17],
    [8,9,3,6,6,3,2,2,3,6,6,3,9,8],
    [16,18,6,12,12,6,4,4,6,12,12,6,18,16]
  ]

private def trace (b : Bool) (t i : Nat) : Nat :=
  ((rows b).getD t []).getD i 0

/-- The actual widths at times zero through six. -/
def traceWidth (t : Nat) : Nat :=
  ([11,12,12,13,13,14,14] : List Nat).getD t 0

private theorem digit_bounds_fin :
    ∀ i : Fin 11, leftDigits i.val ≤ 9 ∧ rightDigits i.val ≤ 9 := by
  decide +kernel

theorem left_canonical : Canonical 80000571539 leftDigits 11 := by
  refine ⟨by decide, ?_, by decide +kernel, by decide +kernel⟩
  intro i hi
  exact (digit_bounds_fin ⟨i, hi⟩).1

theorem right_canonical : Canonical 70000817069 rightDigits 11 := by
  refine ⟨by decide, ?_, by decide +kernel, by decide +kernel⟩
  intro i hi
  exact (digit_bounds_fin ⟨i, hi⟩).2

private theorem initial_trace_fin :
    ∀ b : Bool, ∀ i : Fin 11, inputColumns b i.val = trace b 0 i.val := by
  decide +kernel

private theorem trace_width_bound_fin :
    ∀ t : Fin 7, traceWidth t.val ≤ 14 := by
  decide +kernel

/-- Every adjacent recorded row is checked against actual decimal addition. -/
private theorem trace_steps_fin :
    ∀ b : Bool, ∀ t : Fin 6,
      nextWidth (trace b t.val) (traceWidth t.val) = traceWidth (t.val + 1) ∧
      ∀ i : Fin 14, i.val < traceWidth (t.val + 1) →
        nextColumns (trace b t.val) (traceWidth t.val) i.val =
          trace b (t.val + 1) i.val := by
  decide +kernel

private theorem trace_carries_fin :
    ∀ t : Fin 6, ∀ i : Fin 15, i.val ≤ traceWidth t.val →
      carry (trace false t.val) i.val = carry (trace true t.val) i.val := by
  decide +kernel

/-- Bounded trace certificates describe the original recursion exactly. -/
private theorem actual_trace (b : Bool) (t : Nat) (ht : t ≤ 6) :
    (iterPairs (inputColumns b) 11 t).1 = traceWidth t ∧
      ∀ i, i < (iterPairs (inputColumns b) 11 t).1 →
        (iterPairs (inputColumns b) 11 t).2 i = trace b t i := by
  induction t with
  | zero =>
    refine ⟨rfl, ?_⟩
    intro i hi
    exact initial_trace_fin b ⟨i, hi⟩
  | succ t ih =>
    rcases ih (by omega) with ⟨hw, hp⟩
    have hc := next_state_congr_upto (iterPairs (inputColumns b) 11 t).2
      (trace b t) (iterPairs (inputColumns b) 11 t).1 hp
    have hs := trace_steps_fin b ⟨t, by omega⟩
    have hwidth : (iterPairs (inputColumns b) 11 (t+1)).1 = traceWidth (t+1) := by
      change nextWidth (iterPairs (inputColumns b) 11 t).2
        (iterPairs (inputColumns b) 11 t).1 = traceWidth (t+1)
      rw [hc.1, hw]
      exact hs.1
    refine ⟨hwidth, ?_⟩
    intro i hi
    have hi' : i < traceWidth (t+1) := by rw [←hwidth]; exact hi
    have hib : i < 14 := by
      have hb := trace_width_bound_fin ⟨t+1, by omega⟩
      change traceWidth (t+1) ≤ 14 at hb
      omega
    change nextColumns (iterPairs (inputColumns b) 11 t).2
      (iterPairs (inputColumns b) 11 t).1 i = trace b (t+1) i
    rw [hc.2 i hi, hw]
    exact hs.2 ⟨i, hib⟩ hi'

theorem left_widths (t : Nat) (ht : t ≤ 6) :
    (iterPairs leftColumns 11 t).1 = traceWidth t :=
  (actual_trace false t ht).1

theorem right_widths (t : Nat) (ht : t ≤ 6) :
    (iterPairs rightColumns 11 t).1 = traceWidth t :=
  (actual_trace true t ht).1

theorem widths_agree (t : Nat) (ht : t ≤ 6) :
    (iterPairs leftColumns 11 t).1 = (iterPairs rightColumns 11 t).1 := by
  rw [left_widths t ht, right_widths t ht]

/-- All incoming carries, including the final overflow carry, coincide. -/
theorem six_complete_carries :
    ∀ t, t < 6 → ∀ i, i ≤ (iterPairs leftColumns 11 t).1 →
      carry (iterPairs leftColumns 11 t).2 i =
        carry (iterPairs rightColumns 11 t).2 i := by
  intro t ht i hi
  have ht6 : t ≤ 6 := by omega
  have hl := actual_trace false t ht6
  have hr := actual_trace true t ht6
  simp only [inputColumns, Bool.false_eq_true, ↓reduceIte] at hl hr
  have hiw : i ≤ traceWidth t := by rw [←hl.1]; exact hi
  have hib : i < 15 := by
    have hb := trace_width_bound_fin ⟨t, by omega⟩
    change traceWidth t ≤ 14 at hb
    omega
  have hir : i ≤ (iterPairs rightColumns 11 t).1 := by
    rw [right_widths t ht6]
    exact hiw
  calc
    carry (iterPairs leftColumns 11 t).2 i = carry (trace false t) i :=
      carry_congr_upto _ _ _ hl.2 i hi
    _ = carry (trace true t) i := trace_carries_fin ⟨t, ht⟩ ⟨i, hib⟩ hiw
    _ = carry (iterPairs rightColumns 11 t).2 i :=
      (carry_congr_upto _ _ _ hr.2 i hir).symm

theorem initial_pair_sums_differ : leftColumns 0 = 17 ∧ rightColumns 0 = 16 := by
  decide +kernel

theorem next_integer_values :
    Lychrel196.step 80000571539 = 173518071547 ∧
    Lychrel196.step 70000817069 = 166072617076 := by
  decide +kernel

theorem next_integers_differ :
    Lychrel196.step 80000571539 ≠ Lychrel196.step 70000817069 := by
  rw [next_integer_values.1, next_integer_values.2]
  decide

/-- The carried recursion has ordinary numeric semantics for these inputs. -/
theorem numeric_orbit_representations (t : Nat) (_ht : t ≤ 6) :
    (∃ d, Canonical (Lychrel196.orbit 80000571539 t) d
        (iterPairs leftColumns 11 t).1 ∧
      ∀ i, i < (iterPairs leftColumns 11 t).1 →
        columnSum d (iterPairs leftColumns 11 t).1 i =
          (iterPairs leftColumns 11 t).2 i) ∧
    (∃ e, Canonical (Lychrel196.orbit 70000817069 t) e
        (iterPairs rightColumns 11 t).1 ∧
      ∀ i, i < (iterPairs rightColumns 11 t).1 →
        columnSum e (iterPairs rightColumns 11 t).1 i =
          (iterPairs rightColumns 11 t).2 i) := by
  exact ⟨iterPairs_representation _ _ _ 11 t left_canonical (by intro i hi; rfl),
    iterPairs_representation _ _ _ 11 t right_canonical (by intro i hi; rfl)⟩

/-- This pair ceases to agree at the seventh complete observation. -/
theorem seventh_carry_differs :
    carry (iterPairs leftColumns 11 6).2 1 = 1 ∧
    carry (iterPairs rightColumns 11 6).2 1 = 0 := by
  have hl := actual_trace false 6 (by decide)
  have hr := actual_trace true 6 (by decide)
  simp only [inputColumns, Bool.false_eq_true, ↓reduceIte] at hl hr
  have hil : 1 ≤ (iterPairs leftColumns 11 6).1 := by rw [hl.1]; decide
  have hir : 1 ≤ (iterPairs rightColumns 11 6).1 := by rw [hr.1]; decide
  rw [carry_congr_upto _ _ _ hl.2 1 hil, carry_congr_upto _ _ _ hr.2 1 hir]
  decide +kernel

/-- A concrete counterexample to reconstruction from six complete carry words. -/
theorem six_carry_counterexample :
    Canonical 80000571539 leftDigits 11 ∧
    Canonical 70000817069 rightDigits 11 ∧
    (∀ t, t < 6 → ∀ i, i ≤ (iterPairs leftColumns 11 t).1 →
      carry (iterPairs leftColumns 11 t).2 i =
        carry (iterPairs rightColumns 11 t).2 i) ∧
    leftColumns 0 ≠ rightColumns 0 ∧
    Lychrel196.step 80000571539 ≠ Lychrel196.step 70000817069 := by
  refine ⟨left_canonical, right_canonical, six_complete_carries, ?_, next_integers_differ⟩
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
#print axioms six_complete_carries
#print axioms initial_pair_sums_differ
#print axioms next_integer_values
#print axioms next_integers_differ
#print axioms numeric_orbit_representations
#print axioms seventh_carry_differs
#print axioms six_carry_counterexample

end Agent10SixCarryCounterexample
