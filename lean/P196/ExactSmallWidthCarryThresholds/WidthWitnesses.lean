import P196.Agent10EightCarry.ActualCarryObservability

/-!
Five canonical pairs give lower bounds at the exact initial widths four
through eight. The pairs at widths four and six share five complete carry
observations; the other three pairs share six. An explicitly selected active
pair coefficient differs, and the ordinary next integers differ in every case.

The finite claims below evaluate the imported actual `iterPairs` recursion.
All observed incoming carries, including the terminal carry, are included.
The finite index bound applies only during this observed segment. The imported
representation theorem supplies ordinary numeric semantics at every later
time, with continued iteration after palindromes.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace ExactSmallWidthCarryThresholds.Witnesses

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual

/-- The five exact initial widths, in increasing order. -/
def width (w : Fin 5) : Nat := w.val + 4

/-- The witnessed lower observation count at the selected exact width. -/
def observations (w : Fin 5) : Nat :=
  if w.val = 0 ∨ w.val = 2 then 5 else 6

/-- `false` selects the left input and `true` the right input. -/
def seed (w : Fin 5) (b : Bool) : Nat :=
  match w.val, b with
  | 0, false => 1096
  | 0, true => 1087
  | 1, false => 10438
  | 1, true => 10348
  | 2, false => 100050
  | 2, true => 100051
  | 3, false => 1006236
  | 3, true => 1007046
  | _, false => 10059561
  | _, true => 10059471

/-- Ordinary decimal digits in least-significant-first order. -/
def digits (w : Fin 5) (b : Bool) (i : Nat) : Nat :=
  seed w b / 10 ^ i % 10

abbrev columns (w : Fin 5) (b : Bool) : Nat → Nat :=
  columnSum (digits w b) (width w)

private theorem initial_data :
    ∀ w : Fin 5, ∀ b : Bool,
      0 < width w ∧ 0 < digits w b (width w - 1) ∧
        value (digits w b) (width w) = seed w b := by
  decide +kernel

/-- Each specified integer has the stated positive canonical width. -/
theorem canonical (w : Fin 5) (b : Bool) :
    Canonical (seed w b) (digits w b) (width w) := by
  obtain ⟨hwidth, hlead, hvalue⟩ := initial_data w b
  refine ⟨hwidth, ?_, hlead, hvalue⟩
  intro i _
  have h := Nat.mod_lt (seed w b / 10 ^ i) (by decide : 0 < 10)
  change seed w b / 10 ^ i % 10 ≤ 9
  omega

/-- The column profiles are instances of the original admissibility predicate. -/
theorem admissible (w : Fin 5) (b : Bool) :
    Admissible (width w) (columns w b) :=
  NormalizationBridge.canonical_admissible
    (seed w b) (digits w b) (width w) (canonical w b)

private theorem observation_bound (w : Fin 5) : observations w ≤ 6 := by
  unfold observations
  split <;> omega

private theorem observed_instances :
    ∀ w : Fin 5, ∀ t : Fin 6, t.val < observations w →
      (iterPairs (columns w false) (width w) t.val).1 ≤ 10 ∧
        ∀ i : Fin 11,
          i.val ≤ (iterPairs (columns w false) (width w) t.val).1 →
            carry (iterPairs (columns w false) (width w) t.val).2 i.val =
              carry (iterPairs (columns w true) (width w) t.val).2 i.val := by
  refine Fin.cases ?_ (Fin.cases ?_ (Fin.cases ?_ (Fin.cases ?_
    (Fin.cases ?_ (fun i => Fin.elim0 i))))) <;> decide +kernel

/-- All five or six complete carry observations agree at the chosen exact width. -/
theorem complete_carries (w : Fin 5) :
    ∀ t, t < observations w →
      ∀ i, i ≤ (iterPairs (columns w false) (width w) t).1 →
        carry (iterPairs (columns w false) (width w) t).2 i =
          carry (iterPairs (columns w true) (width w) t).2 i := by
  intro t ht i hi
  have ht6 : t < 6 := Nat.lt_of_lt_of_le ht (observation_bound w)
  obtain ⟨hw, hc⟩ := observed_instances w ⟨t, ht6⟩ ht
  have hi11 : i < 11 := by
    change (iterPairs (columns w false) (width w) t).1 ≤ 10 at hw
    omega
  exact hc ⟨i, hi11⟩ hi

/-- The first or second pair coefficient witnesses the required separation. -/
def differenceIndex (w : Fin 5) : Nat :=
  if w.val = 0 ∨ w.val = 2 then 0 else 1

/-- The selected coefficient is initially active and differs between the inputs. -/
theorem initial_pair_difference_active :
    ∀ w : Fin 5, differenceIndex w < width w ∧
      columns w false (differenceIndex w) ≠ columns w true (differenceIndex w) := by
  decide +kernel

/-- Exact next integers for all five specified canonical pairs. -/
theorem next_integer_values :
    Lychrel196.step 1096 = 7997 ∧ Lychrel196.step 1087 = 8888 ∧
    Lychrel196.step 10438 = 93839 ∧ Lychrel196.step 10348 = 94649 ∧
    Lychrel196.step 100050 = 150051 ∧ Lychrel196.step 100051 = 250052 ∧
    Lychrel196.step 1006236 = 7332237 ∧ Lychrel196.step 1007046 = 7414047 ∧
    Lychrel196.step 10059561 = 26654562 ∧
    Lychrel196.step 10059471 = 27554472 := by
  decide +kernel

theorem next_integers_differ :
    ∀ w : Fin 5,
      Lychrel196.step (seed w false) ≠ Lychrel196.step (seed w true) := by
  decide +kernel

/-- Ordinary continued reverse-and-add realizes each witness at every time. -/
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
#print axioms observed_instances
#print axioms complete_carries
#print axioms initial_pair_difference_active
#print axioms next_integer_values
#print axioms next_integers_differ
#print axioms numeric_orbit_representation

end ExactSmallWidthCarryThresholds.Witnesses
