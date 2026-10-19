import P196.UniformCarryWindows.ActualCarryBudget
import P196.Agent9DigitSumWindows.SharpUniformDecimal
import P196.Agent9DigitSumWindows.Agent9WindowIntervalCounts

set_option autoImplicit false

/-!
# Uniform windows with many outgoing decimal carries

A ceiling on the first twelve total carry counts bounds the initial digit
sum by eleven times that ceiling, independently of decimal width. Applying
the existing uniform digit-sum escape theorem then gives a uniform window
containing a carry count above any prescribed threshold. Complete disjoint
windows give the stated finite interval count.

The counts include every outgoing carry position, including the terminal
carry. The ordinary integer orbit continues after a palindrome. No optimal
constant, density limit, divergence of every carry count, or palindrome
avoidance assertion is made.
-/

namespace UniformCarryWindows

open Lychrel196 DecimalMass CarryCountGrowth CarryCountDecoding

private theorem weightedCount_ceiling (c : Nat → Nat) (B N : Nat) :
    (∀ t, t < N → c t ≤ B) → weightedCount c N + B ≤ 2 ^ N * B := by
  induction N with
  | zero =>
    intro _
    simp [weightedCount]
  | succ N ih =>
    intro h
    have hp := ih (fun t ht => h t (by omega))
    have hl := h N (by omega)
    calc
      weightedCount c (N + 1) + B ≤ 2 * (weightedCount c N + B) := by
        simp only [weightedCount]
        omega
      _ ≤ 2 * (2 ^ N * B) := Nat.mul_le_mul_left 2 hp
      _ = 2 ^ (N + 1) * B := by
        simp only [Nat.pow_succ, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]

/-- An eight-step lower bound on weighted outgoing carry accumulation. -/
theorem eight_carry_budget (n : Nat) :
    47 * digitSum n ≤
      5 * weightedCount (fun t => outgoingCarryCount (orbit n t)) 8 := by
  have h := weighted_mass_bound n 8
  change 256 * (2 * digitSum n) ≤ 162 * (2 * digitSum n) +
    20 * weightedCount (fun t => outgoingCarryCount (orbit n t)) 8 at h
  omega

/-- Twelve observations give a stronger ratio between initial digit sum
and weighted outgoing carry accumulation. -/
theorem twelve_carry_budget (n : Nat) :
    1931 * digitSum n ≤
      5 * weightedCount (fun t => outgoingCarryCount (orbit n t)) 12 := by
  have h := weighted_mass_bound n 12
  change 4096 * (2 * digitSum n) ≤ 234 * (2 * digitSum n) +
    20 * weightedCount (fun t => outgoingCarryCount (orbit n t)) 12 at h
  omega

/-- A fixed short carry ceiling bounds the initial digit sum without
any hypothesis on the number of decimal digits. The zero seed is included. -/
theorem digitSum_le_of_twelve_carry_ceiling (n B : Nat)
    (h : ∀ t, t < 12 → outgoingCarryCount (orbit n t) ≤ B) :
    digitSum n ≤ 11 * B := by
  have hw := weightedCount_ceiling
    (fun t => outgoingCarryCount (orbit n t)) B 12 h
  change weightedCount (fun t => outgoingCarryCount (orbit n t)) 12 + B ≤
    4096 * B at hw
  have hm := twelve_carry_budget n
  omega

/-- Large initial digit sum forces a large carry count strictly before
the end of a twelve-step window. -/
theorem outgoingCarryCount_escape_of_digitSum (n B : Nat)
    (hlarge : 11 * B < digitSum n) :
    ∃ t, t < 12 ∧ B < outgoingCarryCount (orbit n t) := by
  apply Classical.byContradiction
  intro hnone
  have hceiling : ∀ t, t < 12 → outgoingCarryCount (orbit n t) ≤ B := by
    intro t ht
    by_cases hb : outgoingCarryCount (orbit n t) ≤ B
    · exact hb
    · exact False.elim (hnone ⟨t, ht, by omega⟩)
  have hsmall := digitSum_le_of_twelve_carry_ceiling n B hceiling
  omega

/-- A carry escape horizon depending only on the requested count ceiling. -/
def uniformCarryEscapeBound (B : Nat) : Nat :=
  DecimalUniformEscape.sharpDigitSumEscapeBound (11 * B) + 12

/-- Every positive decimal orbit exceeds the prescribed total outgoing
carry count within the same width-independent window. -/
theorem outgoingCarryCount_uniform_escape (n : Nat) (hn : 0 < n) (B : Nat) :
    ∃ t, t < uniformCarryEscapeBound B ∧
      B < outgoingCarryCount (orbit n t) := by
  obtain ⟨j, hj, hm⟩ := DecimalUniformEscape.digitSum_uniform_escape_sharp
    n hn (11 * B)
  obtain ⟨k, hk, hc⟩ := outgoingCarryCount_escape_of_digitSum (orbit n j) B hm
  refine ⟨j + k, ?_, ?_⟩
  · unfold uniformCarryEscapeBound
    omega
  · simpa only [LychrelCertificates.orbit_add] using hc

/-- The uniform waiting-time bound applies after every starting time;
the interval is half-open at its right endpoint. -/
theorem outgoingCarryCount_uniform_window (n : Nat) (hn : 0 < n)
    (B start : Nat) :
    ∃ t, start ≤ t ∧ t < start + uniformCarryEscapeBound B ∧
      B < outgoingCarryCount (orbit n t) := by
  obtain ⟨j, hj, hc⟩ := outgoingCarryCount_uniform_escape
    (orbit n start) (DecimalDigits.orbit_positive n hn start) B
  refine ⟨start + j, by omega, by omega, ?_⟩
  simpa only [LychrelCertificates.orbit_add] using hc

/-- Every complete uniform window contributes a qualifying time in the
finite interval `[start, start + N)`. Empty intervals are included. -/
theorem outgoingCarryCount_interval_count (n : Nat) (hn : 0 < n)
    (B start N : Nat) :
    N / uniformCarryEscapeBound B ≤
      ((List.range' start N).filter
        (fun t => decide (B < outgoingCarryCount (orbit n t)))).length := by
  exact P196.Agent9.IntervalCounts.window_property_interval_count
    (fun t => B < outgoingCarryCount (orbit n t)) (uniformCarryEscapeBound B)
    (by unfold uniformCarryEscapeBound; omega)
    (fun a => outgoingCarryCount_uniform_window n hn B a) start N

#print axioms eight_carry_budget
#print axioms twelve_carry_budget
#print axioms digitSum_le_of_twelve_carry_ceiling
#print axioms outgoingCarryCount_escape_of_digitSum
#print axioms outgoingCarryCount_uniform_escape
#print axioms outgoingCarryCount_uniform_window
#print axioms outgoingCarryCount_interval_count

end UniformCarryWindows
