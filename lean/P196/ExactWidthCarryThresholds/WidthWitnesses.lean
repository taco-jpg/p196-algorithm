import P196.Agent10EightCarry.ActualCarryObservability

/-!
Five canonical pairs witness the missing lower bounds at exact widths ten,
eleven, twelve, fourteen and sixteen. The width-ten pair has six equal
complete carry observations; each other pair has seven. The selected active
pair coefficients and ordinary next integers differ in every instance.

The certificate evaluates the existing actual pair recursion. Its finite
index range includes the terminal carry at every observed width. The bound
of twenty applies only to the observed segment. The existing representation
theorem relates these pair orbits to continued ordinary iteration at every
time, including after a palindrome, with no bound on later widths.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace ExactWidthCarryThresholds.Witnesses

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual

/-- The five additional exact widths in increasing order. -/
def width (w : Fin 5) : Nat :=
  match w.val with
  | 0 => 10
  | 1 => 11
  | 2 => 12
  | 3 => 14
  | _ => 16

/-- One fewer observation than the proposed exact-width reconstruction bound. -/
def observations (w : Fin 5) : Nat := if w.val = 0 then 6 else 7

/-- The Boolean selects the left or right canonical input. -/
def seed (w : Fin 5) (b : Bool) : Nat :=
  match w.val, b with
  | 0, false => 1000599561
  | 0, true => 1000599471
  | 1, false => 49000269199
  | 1, true => 48000187399
  | 2, false => 900000790209
  | 2, true => 900000872109
  | 3, false => 90000008433999
  | 3, true => 90000009252999
  | _, false => 9090000079020909
  | _, true => 9090000087210909

/-- Digits of the specified ordinary input, starting at the units column. -/
def digits (w : Fin 5) (b : Bool) (i : Nat) : Nat :=
  seed w b / 10 ^ i % 10

abbrev columns (w : Fin 5) (b : Bool) : Nat → Nat :=
  columnSum (digits w b) (width w)

private theorem input_certificate :
    ∀ w : Fin 5, ∀ b : Bool,
      0 < width w ∧ 0 < digits w b (width w - 1) ∧
        value (digits w b) (width w) = seed w b := by
  decide +kernel

/-- The ordinary inputs have their specified exact canonical widths. -/
theorem canonical (w : Fin 5) (b : Bool) :
    Canonical (seed w b) (digits w b) (width w) := by
  obtain ⟨hwidth, hlead, hvalue⟩ := input_certificate w b
  refine ⟨hwidth, ?_, hlead, hvalue⟩
  intro i _
  have h := Nat.mod_lt (seed w b / 10 ^ i) (by decide : 0 < 10)
  change seed w b / 10 ^ i % 10 ≤ 9
  omega

/-- These are admissible instances of the existing pair dynamics. -/
theorem admissible (w : Fin 5) (b : Bool) :
    Admissible (width w) (columns w b) :=
  NormalizationBridge.canonical_admissible
    (seed w b) (digits w b) (width w) (canonical w b)

private theorem observation_bound (w : Fin 5) : observations w ≤ 7 := by
  unfold observations
  split <;> omega

private theorem finite_carry_certificate :
    ∀ w : Fin 5, ∀ t : Fin 7, t.val < observations w →
      (iterPairs (columns w false) (width w) t.val).1 ≤ 20 ∧
        ∀ i : Fin 21,
          i.val ≤ (iterPairs (columns w false) (width w) t.val).1 →
            carry (iterPairs (columns w false) (width w) t.val).2 i.val =
              carry (iterPairs (columns w true) (width w) t.val).2 i.val := by
  refine Fin.cases ?_ (Fin.cases ?_ (Fin.cases ?_ (Fin.cases ?_
    (Fin.cases ?_ (fun i => Fin.elim0 i))))) <;> decide +kernel

/-- Equality of all six or seven complete actual carry words, terminal included. -/
theorem complete_carries (w : Fin 5) :
    ∀ t, t < observations w →
      ∀ i, i ≤ (iterPairs (columns w false) (width w) t).1 →
        carry (iterPairs (columns w false) (width w) t).2 i =
          carry (iterPairs (columns w true) (width w) t).2 i := by
  intro t ht i hi
  have ht7 : t < 7 := Nat.lt_of_lt_of_le ht (observation_bound w)
  obtain ⟨hw, hc⟩ := finite_carry_certificate w ⟨t, ht7⟩ ht
  have hi21 : i < 21 := by
    change (iterPairs (columns w false) (width w) t).1 ≤ 20 at hw
    omega
  exact hc ⟨i, hi21⟩ hi

/-- The first differing active pair index for each of the five inputs. -/
def differenceIndex (w : Fin 5) : Nat :=
  if w.val = 0 then 1 else w.val

/-- Each selected pair difference occurs inside the initial word. -/
theorem initial_pair_difference_active :
    ∀ w : Fin 5, differenceIndex w < width w ∧
      columns w false (differenceIndex w) ≠ columns w true (differenceIndex w) := by
  decide +kernel

/-- The ten exact next ordinary integers. -/
theorem next_integer_values :
    Lychrel196.step 1000599561 = 2660549562 ∧
    Lychrel196.step 1000599471 = 2750549472 ∧
    Lychrel196.step 49000269199 = 148196469293 ∧
    Lychrel196.step 48000187399 = 147378287483 ∧
    Lychrel196.step 900000790209 = 1802097790218 ∧
    Lychrel196.step 900000872109 = 1801278872118 ∧
    Lychrel196.step 90000008433999 = 189933488434008 ∧
    Lychrel196.step 90000009252999 = 189925299253008 ∧
    Lychrel196.step 9090000079020909 = 18180209779021818 ∧
    Lychrel196.step 9090000087210909 = 18180127887211818 := by
  decide +kernel

theorem next_integers_differ :
    ∀ w : Fin 5,
      Lychrel196.step (seed w false) ≠ Lychrel196.step (seed w true) := by
  decide +kernel

/-- Every pair iterate represents continued ordinary reverse-and-add iteration. -/
theorem numeric_orbit_representation (w : Fin 5) (b : Bool) (t : Nat) :
    ∃ d, Canonical (Lychrel196.orbit (seed w b) t) d
        (iterPairs (columns w b) (width w) t).1 ∧
      ∀ i, i < (iterPairs (columns w b) (width w) t).1 →
        columnSum d (iterPairs (columns w b) (width w) t).1 i =
          (iterPairs (columns w b) (width w) t).2 i :=
  iterPairs_representation (seed w b) (digits w b) (columns w b)
    (width w) t (canonical w b) (by intro i _; rfl)

#print axioms canonical
#print axioms admissible
#print axioms finite_carry_certificate
#print axioms complete_carries
#print axioms initial_pair_difference_active
#print axioms next_integer_values
#print axioms next_integers_differ
#print axioms numeric_orbit_representation

end ExactWidthCarryThresholds.Witnesses
