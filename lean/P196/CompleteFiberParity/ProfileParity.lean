import P196.Agent101DigitSplit.Agent101NumericFibers

set_option autoImplicit false

/-!
# Exact parity of canonical digit-splitting profiles

Agent #6: the existing multiplicity product is odd precisely when every
factor is odd. The nonzero leading digit changes the outer pair condition
at the decimal cutoff nine. Empty profiles and single-digit profiles keep
their existing positivity and optional-center conventions.
-/

namespace CompleteFiberParity

open Agent101

/-- A finite coefficient test for odd canonical digit-splitting multiplicity.
The optional zero center is valid whenever an outer pair is present. -/
def oddProfile : List Nat → Option Nat → Bool
  | [], none => false
  | [], some s => decide (0 < s ∧ centerCount (some s) = 1)
  | s :: h, c =>
      decide ((s ≤ 9 ∧ s % 2 = 1) ∨
        (10 ≤ s ∧ s ≤ 18 ∧ s % 2 = 0)) &&
      decide (centerCount c = 1) &&
      h.all (fun t => decide (t ≤ 18 ∧ t % 2 = 0))

private theorem pairCount_inner_mod_two (s : Nat) :
    pairCount false s % 2 = if s ≤ 18 ∧ s % 2 = 0 then 1 else 0 := by
  by_cases h9 : s ≤ 9
  · have h18 : s ≤ 18 := by omega
    by_cases he : s % 2 = 0 <;> simp [pairCount, h9, h18, he] <;> omega
  · by_cases h18 : s ≤ 18
    · by_cases he : s % 2 = 0 <;> simp [pairCount, h9, h18, he] <;> omega
    · simp [pairCount, h9, h18]

private theorem pairCount_outer_mod_two (s : Nat) :
    pairCount true s % 2 =
      if (s ≤ 9 ∧ s % 2 = 1) ∨ (10 ≤ s ∧ s ≤ 18 ∧ s % 2 = 0)
      then 1 else 0 := by
  by_cases h9 : s ≤ 9
  · have h10 : ¬ 10 ≤ s := by omega
    by_cases ho : s % 2 = 1 <;> simp [pairCount, h9, h10, ho] <;> omega
  · have h10 : 10 ≤ s := by omega
    by_cases h18 : s ≤ 18
    · by_cases he : s % 2 = 0 <;> simp [pairCount, h9, h10, h18, he] <;> omega
    · simp [pairCount, h9, h18]

private theorem centerCount_mod_two (c : Option Nat) :
    centerCount c % 2 = if centerCount c = 1 then 1 else 0 := by
  have hb := centerCount_le c
  split <;> omega

private theorem innerProduct_mod_two (h : List Nat) :
    natProduct (h.map (pairCount false)) % 2 =
      if h.all (fun t => decide (t ≤ 18 ∧ t % 2 = 0)) then 1 else 0 := by
  induction h with
  | nil => rfl
  | cons s h ih =>
      rw [List.map_cons, natProduct, Nat.mul_mod, pairCount_inner_mod_two, ih]
      by_cases hs : s ≤ 18 ∧ s % 2 = 0 <;>
        cases hh : h.all (fun t => decide (t ≤ 18 ∧ t % 2 = 0)) <;>
        simp [-List.all_eq_true, -Bool.decide_and, List.all_cons, hs, hh]

/-- The exact multiplicity has the parity computed by the coefficient test,
including invalid coefficients, empty profiles, and every center boundary. -/
theorem profileCount_mod_two (h : List Nat) (c : Option Nat) :
    profileCount h c % 2 = if oddProfile h c then 1 else 0 := by
  cases h with
  | nil =>
      cases c with
      | none => rfl
      | some s =>
          by_cases hs : 0 < s
          · simp only [profileCount, if_pos hs]
            rw [centerCount_mod_two]
            simp [oddProfile, hs]
          · simp [profileCount, oddProfile, hs]
  | cons s h =>
      change (pairCount true s * centerCount c *
        natProduct (h.map (pairCount false))) % 2 = _
      rw [Nat.mul_mod, Nat.mul_mod (pairCount true s) (centerCount c) 2,
        pairCount_outer_mod_two, centerCount_mod_two, innerProduct_mod_two]
      by_cases hs : (s ≤ 9 ∧ s % 2 = 1) ∨ (10 ≤ s ∧ s ≤ 18 ∧ s % 2 = 0) <;>
        by_cases hc : centerCount c = 1 <;>
        cases hh : h.all (fun t => decide (t ≤ 18 ∧ t % 2 = 0)) <;>
        simp [-List.all_eq_true, -Bool.decide_and, oddProfile, hs, hc, hh]

/-- The same finite coefficient test computes parity of the existing complete
ordinary-integer fiber at the prescribed source profile. -/
theorem numericFiber_mod_two (h : List Nat) (c : Option Nat) :
    (numericFiber h c).length % 2 = if oddProfile h c then 1 else 0 := by
  rw [length_numericFiber, profileCount_mod_two]

/-- Odd multiplicity of the complete ordinary-integer profile fiber is
equivalent to acceptance by the explicit finite coefficient test. -/
theorem numericFiber_odd_iff (h : List Nat) (c : Option Nat) :
    (numericFiber h c).length % 2 = 1 ↔ oddProfile h c = true := by
  rw [numericFiber_mod_two]
  cases hp : oddProfile h c <;> simp [hp]

end CompleteFiberParity

#print axioms CompleteFiberParity.oddProfile
#print axioms CompleteFiberParity.profileCount_mod_two
#print axioms CompleteFiberParity.numericFiber_mod_two
#print axioms CompleteFiberParity.numericFiber_odd_iff
