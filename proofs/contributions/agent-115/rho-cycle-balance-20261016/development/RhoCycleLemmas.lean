import RhoCycleTargets

/-!
Agent #115 experimental Lean attempt for the *exact* Agent7/Agent115 exterior map.
Not accepted until official Lean 4.19.0 compilation, axiom audit and review.
The original imported source is pinned by Agent6's coordinate registry.
-/
namespace Agent115.RhoCycle

open P196.Agent7.Finite Agent115.ExteriorFactorization Agent6.ExteriorCoordinates

/-- The proposed high carry is exactly the existing original right-normalization carry. -/
theorem gamma_eq_overflow (s : Outer) :
    gamma s = overflow s.c s.B := by
  change (highValue s.B + phaseCarry s.c) / 10 ^ s.B.length = overflow s.c s.B
  exact (overflow_eq_highValue s.c s.B).symm

/-- On coefficient words bounded by 18, the high carry is a Boolean bit. -/
theorem gamma_le_one (s : Outer)
    (hB : ∀ x ∈ s.B, x ≤ 18) : gamma s ≤ 1 := by
  rw [gamma_eq_overflow]
  exact overflow_le_one s.c s.B hB

/-- The proposed rational high-side flow is positive for *every* positive phase,
without any coefficient or canonicality assumption. -/
theorem psi_pos_of_phase_pos (s : Outer) (hc : 0 < s.c) : 0 < psi s := by
  have ht := phaseDigit_pos s.c hc
  change 0 < s.c - 9 * (if 10 ≤ s.c then 1 else 0) at ht
  have hn : 0 < 90 * revN s.B.length (lowValue s.B) +
      9 * (s.c + lowValue s.B / 10 ^ s.B.length -
        10 * (if 10 ≤ s.c then 1 else 0)) +
      (s.c - 9 * (if 10 ≤ s.c then 1 else 0)) := by omega
  have hd : 0 < 90 * 10 ^ s.B.length :=
    Nat.mul_pos (by decide) (Nat.pow_pos (by decide))
  have hn' : (0 : Rat) <
      (↑(90 * revN s.B.length (lowValue s.B) +
        9 * (s.c + lowValue s.B / 10 ^ s.B.length -
          10 * (if 10 ≤ s.c then 1 else 0)) +
        (s.c - 9 * (if 10 ≤ s.c then 1 else 0))) : Rat) := by
    exact_mod_cast hn
  have hd' : (0 : Rat) < (↑(90 * 10 ^ s.B.length) : Rat) := by
    exact_mod_cast hd
  change (0 : Rat) <
    (↑(90 * revN s.B.length (lowValue s.B) +
        9 * (s.c + lowValue s.B / 10 ^ s.B.length -
          10 * (if 10 ≤ s.c then 1 else 0)) +
        (s.c - 9 * (if 10 ≤ s.c then 1 else 0))) : Rat) /
      (↑(90 * 10 ^ s.B.length) : Rat)
  exact div_pos hn' hd'

#print axioms gamma_eq_overflow
#print axioms gamma_le_one
#print axioms psi_pos_of_phase_pos

end Agent115.RhoCycle
