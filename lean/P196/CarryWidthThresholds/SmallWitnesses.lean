import P196.Agent10EightCarry.ActualCarryObservability

/-!
Three small canonical counterexamples supply the strict lower bounds for
initial-width classes one, two, and three. The inputs are 3/4, 16/17, and
809/719, respectively. They share three, four, and six complete carry words,
while both their exterior pair coefficients and their next integers differ.

The finite certificates evaluate the existing actual pair recursion directly.
Its imported representation theorem supplies ordinary numeric semantics at
every time. There is no alternate transition model or stopping rule at a
palindrome, and no palindrome-avoidance or initial-integer injectivity claim.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace CarryWidthThresholds.SmallWitnesses

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual

/-- The three witnesses have initial widths one, two, and three. -/
def width (w : Fin 3) : Nat := w.val + 1

/-- Number of common complete carry observations for each witness. -/
def observations (w : Fin 3) : Nat :=
  if w.val = 0 then 3 else if w.val = 1 then 4 else 6

/-- `false` selects the left canonical input and `true` the right. -/
def seed (w : Fin 3) (b : Bool) : Nat :=
  if w.val = 0 then (if b then 4 else 3)
  else if w.val = 1 then (if b then 17 else 16)
  else if b then 719 else 809

/-- Least-significant-first decimal digits of the selected ordinary input. -/
def digits (w : Fin 3) (b : Bool) (i : Nat) : Nat :=
  seed w b / 10 ^ i % 10

abbrev columns (w : Fin 3) (b : Bool) : Nat → Nat :=
  columnSum (digits w b) (width w)

private theorem canonical_data :
    ∀ w : Fin 3, ∀ b : Bool,
      0 < width w ∧ 0 < digits w b (width w - 1) ∧
      value (digits w b) (width w) = seed w b := by
  decide +kernel

/-- Each input is represented by its ordinary canonical decimal digits. -/
theorem canonical (w : Fin 3) (b : Bool) :
    Canonical (seed w b) (digits w b) (width w) := by
  have h := canonical_data w b
  refine ⟨h.1, ?_, h.2.1, h.2.2⟩
  intro i _
  have hm := Nat.mod_lt (seed w b / 10 ^ i) (by decide : 0 < 10)
  change seed w b / 10 ^ i % 10 ≤ 9
  omega

theorem admissible (w : Fin 3) (b : Bool) :
    Admissible (width w) (columns w b) :=
  NormalizationBridge.canonical_admissible
    (seed w b) (digits w b) (width w) (canonical w b)

private theorem observations_le_six :
    ∀ w : Fin 3, observations w ≤ 6 := by
  decide +kernel

/-- The finite domain includes every observed time and every incoming carry,
including the terminal carry. No bound is imposed on subsequent orbit widths. -/
private theorem observed_data :
    ∀ w : Fin 3, ∀ t : Fin 6, t.val < observations w →
      (iterPairs (columns w false) (width w) t.val).1 ≤ 6 ∧
      ∀ i : Fin 7, i.val ≤ (iterPairs (columns w false) (width w) t.val).1 →
        carry (iterPairs (columns w false) (width w) t.val).2 i.val =
          carry (iterPairs (columns w true) (width w) t.val).2 i.val := by
  decide +kernel

/-- The existing actual recursion has three, four, or six common complete
carry words, according to the selected initial width. -/
theorem complete_carries (w : Fin 3) :
    ∀ t, t < observations w →
      ∀ i, i ≤ (iterPairs (columns w false) (width w) t).1 →
        carry (iterPairs (columns w false) (width w) t).2 i =
          carry (iterPairs (columns w true) (width w) t).2 i := by
  intro t ht i hi
  have hK := observations_le_six w
  have h := observed_data w ⟨t, by omega⟩ ht
  have hw : (iterPairs (columns w false) (width w) t).1 ≤ 6 := h.1
  exact h.2 ⟨i, by omega⟩ hi

/-- Each pair already differs at the active exterior coefficient. -/
theorem initial_pair_difference_active :
    ∀ w : Fin 3, 0 < width w ∧ columns w false 0 ≠ columns w true 0 := by
  decide +kernel

/-- Exact unequal next integers for the three selected pairs. -/
theorem next_integer_values :
    Lychrel196.step 3 = 6 ∧ Lychrel196.step 4 = 8 ∧
    Lychrel196.step 16 = 77 ∧ Lychrel196.step 17 = 88 ∧
    Lychrel196.step 809 = 1717 ∧ Lychrel196.step 719 = 1636 := by
  decide +kernel

theorem next_integers_differ :
    ∀ w : Fin 3, Lychrel196.step (seed w false) ≠
      Lychrel196.step (seed w true) := by
  decide +kernel

/-- Ordinary continued reverse-and-add realizes the pair recursion at every
time, including times after the finitely observed segment. -/
theorem numeric_orbit_representation (w : Fin 3) (b : Bool) (t : Nat) :
    ∃ d, Canonical (Lychrel196.orbit (seed w b) t) d
        (iterPairs (columns w b) (width w) t).1 ∧
      ∀ i, i < (iterPairs (columns w b) (width w) t).1 →
        columnSum d (iterPairs (columns w b) (width w) t).1 i =
          (iterPairs (columns w b) (width w) t).2 i :=
  iterPairs_representation (seed w b) (digits w b) (columns w b)
    (width w) t (canonical w b) (by intro i hi; rfl)

/-- Canonical witnesses against three, four, and six observations in the
initial-width classes one, two, and three, respectively. -/
theorem small_carry_counterexample (w : Fin 3) :
    Canonical (seed w false) (digits w false) (width w) ∧
    Canonical (seed w true) (digits w true) (width w) ∧
    Admissible (width w) (columns w false) ∧
    Admissible (width w) (columns w true) ∧
    (∀ t, t < observations w →
      ∀ i, i ≤ (iterPairs (columns w false) (width w) t).1 →
        carry (iterPairs (columns w false) (width w) t).2 i =
          carry (iterPairs (columns w true) (width w) t).2 i) ∧
    (0 < width w ∧ columns w false 0 ≠ columns w true 0) ∧
    Lychrel196.step (seed w false) ≠ Lychrel196.step (seed w true) :=
  ⟨canonical w false, canonical w true, admissible w false, admissible w true,
    complete_carries w, initial_pair_difference_active w, next_integers_differ w⟩

#print axioms canonical
#print axioms admissible
#print axioms observed_data
#print axioms complete_carries
#print axioms initial_pair_difference_active
#print axioms next_integer_values
#print axioms next_integers_differ
#print axioms numeric_orbit_representation
#print axioms small_carry_counterexample

end CarryWidthThresholds.SmallWitnesses
