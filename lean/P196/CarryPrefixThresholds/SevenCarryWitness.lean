import P196.Agent10EightCarry.ActualCarryObservability
import P196.Agent104P620Witness.PalindromeBridge

/-!
Two canonical width-nine inputs have seven equal complete carry words while
their initial pair coefficients at index one differ. The next integers differ,
and the eighth carry observation separates the inputs at incoming index two.

The finite certificates evaluate ordinary numeric iterates and their decimal
digits. The imported numeric representation and canonical uniqueness theorems
identify these digits with the original pair recursion; no separate transition
recursion is introduced. Iteration is the ordinary continued reverse-and-add
map, with no palindrome-avoidance hypothesis or claim about 196.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace CarryPrefixThresholds.SevenCarryWitness

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual

/-- The two ordinary positive decimal inputs. -/
def seed (b : Bool) : Nat := if b then 480047399 else 490039199

/-- Canonical decimal digits, least significant first. -/
def digits (b : Bool) (i : Nat) : Nat := seed b / 10 ^ i % 10

abbrev leftDigits : Nat → Nat := digits false
abbrev rightDigits : Nat → Nat := digits true
abbrev columns (b : Bool) : Nat → Nat := columnSum (digits b) 9
abbrev leftColumns : Nat → Nat := columns false
abbrev rightColumns : Nat → Nat := columns true

private def traceValue (b : Bool) (t : Nat) : Nat :=
  ((if b then
    [480047399,1473787483,5321661224,9543322459,19085555918,101041114009,
      1001452254110,1115974795111]
  else
    [490039199,1481969293,5411661134,9723322279,19445555558,105001110049,
      1045012210550,1595134315951]) : List Nat).getD t 0

private def orbitDigits (b : Bool) (t i : Nat) : Nat :=
  traceValue b t / 10 ^ i % 10

/-- Exact common widths at times zero through seven. -/
def traceWidth (t : Nat) : Nat :=
  ([9,10,10,10,11,12,13,13] : List Nat).getD t 0

private abbrev orbitColumns (b : Bool) (t : Nat) : Nat → Nat :=
  columnSum (orbitDigits b t) (traceWidth t)

/-- Each adjacent pair of literal integers is checked by ordinary reverse-and-add. -/
private theorem steps_fin :
    ∀ b : Bool, ∀ t : Fin 7,
      Lychrel196.step (traceValue b t.val) = traceValue b (t.val + 1) := by
  decide +kernel

#print axioms steps_fin

private theorem orbit_values (b : Bool) (t : Nat) (ht : t ≤ 7) :
    Lychrel196.orbit (seed b) t = traceValue b t := by
  induction t with
  | zero => cases b <;> rfl
  | succ t ih =>
    rw [Lychrel196.orbit, ih (by omega)]
    exact steps_fin b ⟨t, by omega⟩

/-- Only the eight recorded ordinary iterates are evaluated here. -/
private theorem canonical_data_fin :
    ∀ b : Bool, ∀ t : Fin 8,
      0 < traceWidth t.val ∧
      0 < orbitDigits b t.val (traceWidth t.val - 1) ∧
      value (orbitDigits b t.val) (traceWidth t.val) =
        traceValue b t.val := by
  decide +kernel

#print axioms canonical_data_fin

private theorem orbit_canonical (b : Bool) (t : Nat) (ht : t ≤ 7) :
    Canonical (Lychrel196.orbit (seed b) t) (orbitDigits b t) (traceWidth t) := by
  rw [orbit_values b t ht]
  have h := canonical_data_fin b ⟨t, by omega⟩
  refine ⟨h.1, ?_, h.2.1, h.2.2⟩
  intro i _
  have hm := Nat.mod_lt (traceValue b t / 10 ^ i)
    (by decide : 0 < 10)
  change traceValue b t / 10 ^ i % 10 ≤ 9
  omega

theorem canonical (b : Bool) : Canonical (seed b) (digits b) 9 := by
  cases b <;> exact orbit_canonical _ 0 (by decide)

theorem left_canonical : Canonical 490039199 leftDigits 9 := canonical false

theorem right_canonical : Canonical 480047399 rightDigits 9 := canonical true

theorem admissible (b : Bool) : Admissible 9 (columns b) :=
  NormalizationBridge.canonical_admissible (seed b) (digits b) 9 (canonical b)

theorem left_admissible : Admissible 9 leftColumns := admissible false

theorem right_admissible : Admissible 9 rightColumns := admissible true

private theorem width_bound_fin : ∀ t : Fin 8, traceWidth t.val ≤ 13 := by
  decide +kernel

/-- Complete words include incoming index zero and the terminal overflow carry. -/
private theorem carries_fin :
    ∀ t : Fin 7, ∀ i : Fin 14, i.val ≤ traceWidth t.val →
      carry (orbitColumns false t.val) i.val =
        carry (orbitColumns true t.val) i.val := by
  decide +kernel

/-- Imported numeric semantics identify the actual pair recursion uniquely. -/
private theorem actual_columns (b : Bool) (t : Nat) (ht : t ≤ 7) :
    (iterPairs (columns b) 9 t).1 = traceWidth t ∧
      ∀ i, i < (iterPairs (columns b) 9 t).1 →
        (iterPairs (columns b) 9 t).2 i = orbitColumns b t i := by
  obtain ⟨e, he, hp⟩ := iterPairs_representation (seed b) (digits b) (columns b)
    9 t (canonical b) (by intro i hi; rfl)
  obtain ⟨hw, hd⟩ := SevenColumnKernel.PalindromeBridge.canonical_unique he
    (orbit_canonical b t ht)
  refine ⟨hw, ?_⟩
  intro i hi
  rw [← hp i hi]
  change e i + e ((iterPairs (columns b) 9 t).1 - 1 - i) =
    orbitDigits b t i + orbitDigits b t (traceWidth t - 1 - i)
  rw [hd i hi, hd ((iterPairs (columns b) 9 t).1 - 1 - i) (by omega), hw]

theorem widths (b : Bool) (t : Nat) (ht : t ≤ 7) :
    (iterPairs (columns b) 9 t).1 = traceWidth t :=
  (actual_columns b t ht).1

/-- Seven complete carry observations agree at the common initial width nine. -/
theorem seven_complete_carries :
    ∀ t, t < 7 → ∀ i, i ≤ (iterPairs leftColumns 9 t).1 →
      carry (iterPairs leftColumns 9 t).2 i =
        carry (iterPairs rightColumns 9 t).2 i := by
  intro t ht i hi
  have hl := actual_columns false t (by omega)
  have hr := actual_columns true t (by omega)
  have hiw : i ≤ traceWidth t := by rw [← hl.1]; exact hi
  have hib : i < 14 := by
    have hb := width_bound_fin ⟨t, by omega⟩
    change traceWidth t ≤ 13 at hb
    omega
  have hir : i ≤ (iterPairs rightColumns 9 t).1 := by rw [hr.1]; exact hiw
  calc
    carry (iterPairs leftColumns 9 t).2 i = carry (orbitColumns false t) i :=
      carry_congr_upto _ _ _ hl.2 i hi
    _ = carry (orbitColumns true t) i := carries_fin ⟨t, ht⟩ ⟨i, hib⟩ hiw
    _ = carry (iterPairs rightColumns 9 t).2 i :=
      (carry_congr_upto _ _ _ hr.2 i hir).symm

/-- The second initial pair coefficients equal eighteen and seventeen. -/
theorem initial_pair_values : leftColumns 1 = 18 ∧ rightColumns 1 = 17 := by
  decide +kernel

/-- The differing second pair coefficient is inside the initial active width. -/
theorem initial_pair_difference_active :
    1 < 9 ∧ leftColumns 1 ≠ rightColumns 1 := by
  refine ⟨by decide, ?_⟩
  rw [initial_pair_values.1, initial_pair_values.2]
  decide

theorem next_integer_values :
    Lychrel196.step 490039199 = 1481969293 ∧
    Lychrel196.step 480047399 = 1473787483 := by
  decide +kernel

theorem next_integers_differ :
    Lychrel196.step 490039199 ≠ Lychrel196.step 480047399 := by
  rw [next_integer_values.1, next_integer_values.2]
  decide

/-- The original ordinary numeric orbit realizes the pair recursion at every time. -/
theorem numeric_orbit_representation (b : Bool) (t : Nat) :
    ∃ d, Canonical (Lychrel196.orbit (seed b) t) d (iterPairs (columns b) 9 t).1 ∧
      ∀ i, i < (iterPairs (columns b) 9 t).1 →
        columnSum d (iterPairs (columns b) 9 t).1 i = (iterPairs (columns b) 9 t).2 i :=
  iterPairs_representation (seed b) (digits b) (columns b) 9 t (canonical b)
    (by intro i hi; rfl)

/-- The eighth observation separates the inputs at active incoming index two. -/
theorem eighth_carry_differs :
    2 ≤ (iterPairs leftColumns 9 7).1 ∧
    2 ≤ (iterPairs rightColumns 9 7).1 ∧
    carry (iterPairs leftColumns 9 7).2 2 = 1 ∧
    carry (iterPairs rightColumns 9 7).2 2 = 0 := by
  have hl := actual_columns false 7 (by decide)
  have hr := actual_columns true 7 (by decide)
  have hil : 2 ≤ (iterPairs leftColumns 9 7).1 := by rw [hl.1]; decide
  have hir : 2 ≤ (iterPairs rightColumns 9 7).1 := by rw [hr.1]; decide
  refine ⟨hil, hir, ?_⟩
  rw [carry_congr_upto _ _ _ hl.2 2 hil, carry_congr_upto _ _ _ hr.2 2 hir]
  decide +kernel

/-- Ordinary canonical inputs refute recovery of the second pair from seven observations. -/
theorem seven_carry_counterexample :
    Canonical 490039199 leftDigits 9 ∧ Canonical 480047399 rightDigits 9 ∧
    Admissible 9 leftColumns ∧ Admissible 9 rightColumns ∧
    (∀ t, t < 7 → ∀ i, i ≤ (iterPairs leftColumns 9 t).1 →
      carry (iterPairs leftColumns 9 t).2 i =
        carry (iterPairs rightColumns 9 t).2 i) ∧
    (1 < 9 ∧ leftColumns 1 ≠ rightColumns 1) ∧
    Lychrel196.step 490039199 ≠ Lychrel196.step 480047399 := by
  refine ⟨left_canonical, right_canonical, left_admissible, right_admissible,
    seven_complete_carries, initial_pair_difference_active, next_integers_differ⟩

#print axioms orbit_values
#print axioms carries_fin
#print axioms actual_columns
#print axioms canonical
#print axioms left_canonical
#print axioms right_canonical
#print axioms admissible
#print axioms left_admissible
#print axioms right_admissible
#print axioms widths
#print axioms seven_complete_carries
#print axioms initial_pair_values
#print axioms initial_pair_difference_active
#print axioms next_integer_values
#print axioms next_integers_differ
#print axioms numeric_orbit_representation
#print axioms eighth_carry_differs
#print axioms seven_carry_counterexample

end CarryPrefixThresholds.SevenCarryWitness
