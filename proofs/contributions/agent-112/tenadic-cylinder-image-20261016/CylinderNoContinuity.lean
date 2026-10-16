import CylinderImage

/-!
Agent #112: a fully ordinary-Nat, quantified nonlocal-constancy consequence
of the exact nine-residue cylinder image theorem.

STATUS: NEW SOURCE, NOT YET LEAN-CHECKED. Rebuild this module using pinned
Lean 4.19.0 and the exact CylinderImage source commit. This is not yet a
topology library theorem; it states the arithmetic obstruction itself.
-/

namespace Agent112.CylinderImage

open Lychrel196 DecimalDigits

/-- Any cylinder of positive decimal precision contains two positive
integers with different reverse-and-add units digits. -/
theorem two_distinct_cylinder_outputs (k a : Nat)
    (hk : 0 < k) (ha : a < 10 ^ k) :
    ∃ m₁ m₂ : Nat, 0 < m₁ ∧ 0 < m₂ ∧
      m₁ % (10 ^ k) = a ∧ m₂ % (10 ^ k) = a ∧
      step m₁ % 10 ≠ step m₂ % 10 := by
  obtain ⟨m₁, hm₁, hres₁, hs₁⟩ :=
    occurs_for_leading_digit k a 1 hk ha (by decide) (by decide)
  obtain ⟨m₂, hm₂, hres₂, hs₂⟩ :=
    occurs_for_leading_digit k a 2 hk ha (by decide) (by decide)
  refine ⟨m₁, m₂, hm₁, hm₂, hres₁, hres₂, ?_⟩
  rw [hs₁, hs₂]
  omega

/-- At every *ordinary natural number*, and for every positive decimal
precision k, there exists a positive integer agreeing through its last k
digits whose reverse-and-add units digit disagrees. This includes n=0.
It rules out local constancy of the output units residue even at a natural
point, without relying on a topological completion or an abstract orbit. -/
theorem no_local_mod10_constancy (n k : Nat) (hk : 0 < k) :
    ∃ m : Nat, 0 < m ∧ m % (10 ^ k) = n % (10 ^ k) ∧
      step m % 10 ≠ step n % 10 := by
  let a : Nat := n % (10 ^ k)
  have ha : a < 10 ^ k := Nat.mod_lt n (Nat.pow_pos (by decide))
  obtain ⟨m₁, m₂, hm₁, hm₂, hr₁, hr₂, hneq⟩ :=
    two_distinct_cylinder_outputs k a hk ha
  by_cases hs : step m₁ % 10 = step n % 10
  · refine ⟨m₂, hm₂, hr₂, ?_⟩
    intro hm₂same
    exact hneq (hs.trans hm₂same.symm)
  · exact ⟨m₁, hm₁, hr₁, hs⟩

#print axioms two_distinct_cylinder_outputs
#print axioms no_local_mod10_constancy

end Agent112.CylinderImage
