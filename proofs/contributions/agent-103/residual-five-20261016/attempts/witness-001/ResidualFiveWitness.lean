import LychrelDigitSums
import TemporalResidues

/-!
# A six-step witness for the limits of the modulo-99 obstruction

Agent #103, task `agent103-residual-five-20261016`.

The concrete integers are transcribed from section 4 of
`proofs/chat-6acee928/originals/p196_all_palindromes_and_eight_families.md`.
All additions, reversals, iterates, and palindrome tests below use the original
`Lychrel196` definitions.  The six additions and the finite palindrome tests
are proved by kernel reduction.  The all-time modulo-99 comparison reuses
Agent #423's original `orbit_mod99_pow_of_dvd11` theorem.

The starting integer is different from 196.  This witness refutes exclusion
of the residual family based solely on the modulo-99 trajectory shared with
196 from time three; it makes no assertion that 196 reaches that family.
-/

namespace Agent103.ResidualFiveWitness

open Lychrel196

/-- The ordinary positive integer printed in the written counterexample. -/
def seed : Nat := 71647625487907287180977453773517

theorem seed_positive : 0 < seed := by decide

theorem seed_ne_196 : seed ≠ 196 := by decide

theorem step_zero :
    step seed = 143185360965815465451955906448134 := by decide

theorem step_one :
    step 143185360965815465451955906448134 =
      575029970524970029970524970029475 := by decide

theorem step_two :
    step 575029970524970029970524970029475 =
      1149950049950049950049950049950050 := by decide

theorem step_three :
    step 1149950049950049950049950049950050 =
      1650549450549450549450549450549461 := by decide

theorem step_four :
    step 1650549450549450549450549450549461 =
      3300000000000000000000000000000022 := by decide

theorem step_five :
    step 3300000000000000000000000000000022 =
      5500000000000000000000000000000055 := by decide

theorem orbit_zero : orbit seed 0 = seed := rfl

theorem orbit_one : orbit seed 1 = 143185360965815465451955906448134 :=
  step_zero

theorem orbit_two : orbit seed 2 = 575029970524970029970524970029475 := by
  change step (orbit seed 1) = _
  rw [orbit_one]
  exact step_one

theorem orbit_three : orbit seed 3 = 1149950049950049950049950049950050 := by
  change step (orbit seed 2) = _
  rw [orbit_two]
  exact step_two

theorem orbit_four : orbit seed 4 = 1650549450549450549450549450549461 := by
  change step (orbit seed 3) = _
  rw [orbit_three]
  exact step_three

theorem orbit_five : orbit seed 5 = 3300000000000000000000000000000022 := by
  change step (orbit seed 4) = _
  rw [orbit_four]
  exact step_four

theorem orbit_six : orbit seed 6 = 5500000000000000000000000000000055 := by
  change step (orbit seed 5) = _
  rw [orbit_five]
  exact step_five

theorem predecessor_at_five : orbit seed 5 = 33 * 10 ^ 32 + 22 := by
  rw [orbit_five]
  decide

theorem target_at_six : orbit seed 6 = 55 * (10 ^ 32 + 1) := by
  rw [orbit_six]
  decide

/-- The target is the residual family member with parameter `r = 15`. -/
theorem family_at_six : orbit seed 6 = 11 * 5 * (10 ^ (2 * 15 + 2) + 1) := by
  rw [orbit_six]
  decide

theorem palindrome_at_six : Palindrome (orbit seed 6) := by
  rw [orbit_six]
  decide

/-- The starting integer is also tested, not just the positive times. -/
theorem nonpal_before_six (i : Nat) (hi : i < 6) : ¬ Palindrome (orbit seed i) := by
  have hc : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 := by omega
  rcases hc with rfl | rfl | rfl | rfl | rfl | rfl
  all_goals
    simp only [orbit_zero, orbit_one, orbit_two, orbit_three, orbit_four, orbit_five]
    decide

/-- The exact defining conjunction of the original
`DecimalDelayBridge.FirstPositiveHit seed 6`, written without importing its
unneeded delay/cutoff development.  No new first-hit predicate is introduced. -/
theorem first_positive_hit_six :
    0 < (6 : Nat) ∧ Palindrome (orbit seed 6) ∧
      ∀ i, 0 < i → i < 6 → ¬ Palindrome (orbit seed i) := by
  exact ⟨by decide, palindrome_at_six, fun i _ hi => nonpal_before_six i hi⟩

theorem seed_mod99 : seed % 99 = 11 := by decide

/-- The explicitly listed residue phases, including the returned phase at six. -/
theorem mod99_trace :
    (List.range 7).map (fun i => orbit seed i % 99) = [11, 22, 44, 88, 77, 55, 11] := by
  change [orbit seed 0 % 99, orbit seed 1 % 99, orbit seed 2 % 99,
    orbit seed 3 % 99, orbit seed 4 % 99, orbit seed 5 % 99, orbit seed 6 % 99] = _
  rw [orbit_zero, orbit_one, orbit_two, orbit_three, orbit_four, orbit_five, orbit_six]
  decide

/-- The modulo-99 match with 196 persists for every later iterate, not just
the six additions displayed in the written witness. -/
theorem mod99_matches_196 (i : Nat) :
    orbit seed i % 99 = orbit 196 (3 + i) % 99 := by
  have h196 : orbit 196 3 = 7436 := by decide
  rw [LychrelCertificates.orbit_add, h196]
  rw [Agent423.TemporalResidues.orbit_mod99_pow_of_dvd11 seed i (by decide),
    Agent423.TemporalResidues.orbit_mod99_pow_of_dvd11 7436 i (by decide)]
  have hs : seed % 99 = 7436 % 99 := by decide
  calc
    (2 ^ i * seed) % 99 = (2 ^ i % 99 * (seed % 99)) % 99 := Nat.mul_mod _ _ _
    _ = (2 ^ i % 99 * (7436 % 99)) % 99 := by rw [hs]
    _ = (2 ^ i * 7436) % 99 := (Nat.mul_mod _ _ _).symm

/-- Modulo-99 agreement with the whole future trajectory of 196 from time
three is insufficient, by itself, to exclude this residual-family target. -/
theorem mod99_trajectory_insufficient :
    ¬ (∀ n : Nat, 0 < n →
      (∀ i, orbit n i % 99 = orbit 196 (3 + i) % 99) →
      ∀ t, orbit n t ≠ 55 * (10 ^ 32 + 1)) := by
  intro h
  exact h seed seed_positive mod99_matches_196 6 target_at_six

/-- A concrete positive integer with the same entire modulo-99 trajectory
as the time-three tail of 196 and a first positive palindrome at time six. -/
theorem residual_five_witness :
    ∃ n : Nat, 0 < n ∧ n ≠ 196 ∧
      (∀ i, orbit n i % 99 = orbit 196 (3 + i) % 99) ∧
      orbit n 6 = 55 * (10 ^ 32 + 1) ∧
      Palindrome (orbit n 6) ∧ (∀ i, i < 6 → ¬ Palindrome (orbit n i)) := by
  exact ⟨seed, seed_positive, seed_ne_196, mod99_matches_196, target_at_six,
    palindrome_at_six, nonpal_before_six⟩

#print axioms seed_positive
#print axioms seed_ne_196
#print axioms step_zero
#print axioms step_one
#print axioms step_two
#print axioms step_three
#print axioms step_four
#print axioms step_five
#print axioms orbit_zero
#print axioms orbit_one
#print axioms orbit_two
#print axioms orbit_three
#print axioms orbit_four
#print axioms orbit_five
#print axioms orbit_six
#print axioms predecessor_at_five
#print axioms target_at_six
#print axioms family_at_six
#print axioms palindrome_at_six
#print axioms nonpal_before_six
#print axioms first_positive_hit_six
#print axioms seed_mod99
#print axioms mod99_trace
#print axioms mod99_matches_196
#print axioms mod99_trajectory_insufficient
#print axioms residual_five_witness

end Agent103.ResidualFiveWitness
