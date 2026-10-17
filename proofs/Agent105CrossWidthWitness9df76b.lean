import Lychrel196Research

/-!
Kernel controls for the original decimal cross-width examples.
The nonpalindromic example is already recorded in persist_inverse_notes.txt
sections 1--2, source blob ecd101823b261fdac15d185fea963d9c9f16c601.
This module formalizes that retained example; it does not claim discovery.
All uses of actual reverse10 are transported through canonical digit
reflection. No large reverseFuel numeral is unfolded by a decision tactic.
-/

namespace Agent105.CrossWidthWitness9df76b

open DecimalDigits FoldedDecimal Lychrel196

/-- Positional digits used only to state these literal kernel controls. -/
def literalDigit (n i : Nat) : Nat := n / 10 ^ i % 10

theorem literalDigit_bounded (n i : Nat) : literalDigit n i ≤ 9 := by
  unfold literalDigit
  omega

private theorem reverse_eq_from_canonical {n r L : Nat}
    (hc : Canonical n (literalDigit n) L)
    (hr : value (reflected (literalDigit n) L) L = r) :
    reverse10 n = r := by
  have h := reverse10_value (literalDigit n) L hc.2.1 (Or.inr hc.2.2.1)
  rw [hc.2.2.2, hr] at h
  exact h

theorem short_canonical : Canonical 200799 (literalDigit 200799) 6 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i _
  exact literalDigit_bounded _ i

theorem long_canonical : Canonical 1098900 (literalDigit 1098900) 7 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i _
  exact literalDigit_bounded _ i

theorem target_canonical : Canonical 1197801 (literalDigit 1197801) 7 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i _
  exact literalDigit_bounded _ i

theorem short_reverse : reverse10 200799 = 997002 :=
  reverse_eq_from_canonical short_canonical (by decide)

theorem long_reverse : reverse10 1098900 = 98901 :=
  reverse_eq_from_canonical long_canonical (by decide)

theorem target_reverse : reverse10 1197801 = 1087911 :=
  reverse_eq_from_canonical target_canonical (by decide)

theorem short_step : step 200799 = 1197801 := by
  change 200799 + reverse10 200799 = 1197801
  rw [short_reverse]

theorem long_step : step 1098900 = 1197801 := by
  change 1098900 + reverse10 1098900 = 1197801
  rw [long_reverse]

theorem target_not_palindrome : ¬ Palindrome 1197801 := by
  intro h
  change reverse10 1197801 = 1197801 at h
  rw [target_reverse] at h
  exact (by decide : 1087911 ≠ 1197801) h

/-- Exact profiles printed in the original note, using its low-to-high order. -/
theorem retained_profiles :
    (∀ i : Fin 6,
      columnSum (literalDigit 200799) 6 i.val =
        ([11, 9, 7, 7, 9, 11] : List Nat)[i.val]?.getD 0) ∧
    (∀ i : Fin 7,
      columnSum (literalDigit 1098900) 7 i.val =
        ([1, 0, 18, 16, 18, 0, 1] : List Nat)[i.val]?.getD 0) := by
  decide

/-- The two actual additions use opposite terminal carry cases. -/
theorem terminal_carries :
    carry (columnSum (literalDigit 200799) 6) 6 = 1 ∧
    carry (columnSum (literalDigit 1098900) 7) 7 = 0 := by
  decide

theorem nonpalindromic_cross_width_witness :
    0 < (200799 : Nat) ∧ 0 < (1098900 : Nat) ∧
    Canonical 200799 (literalDigit 200799) 6 ∧
    Canonical 1098900 (literalDigit 1098900) 7 ∧
    Canonical 1197801 (literalDigit 1197801) 7 ∧
    step 200799 = 1197801 ∧ step 1098900 = 1197801 ∧
    ¬ Palindrome 1197801 := by
  exact ⟨by decide, by decide, short_canonical, long_canonical,
    target_canonical, short_step, long_step, target_not_palindrome⟩

theorem boundary_short_canonical : Canonical 29 (literalDigit 29) 2 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i _
  exact literalDigit_bounded _ i

theorem boundary_long_canonical : Canonical 110 (literalDigit 110) 3 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i _
  exact literalDigit_bounded _ i

theorem boundary_target_canonical : Canonical 121 (literalDigit 121) 3 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i _
  exact literalDigit_bounded _ i

theorem boundary_reversals :
    reverse10 29 = 92 ∧ reverse10 110 = 11 ∧ reverse10 121 = 121 :=
  ⟨reverse_eq_from_canonical boundary_short_canonical (by decide),
    reverse_eq_from_canonical boundary_long_canonical (by decide),
    reverse_eq_from_canonical boundary_target_canonical (by decide)⟩

/-- Small adjacent-width collision, including the shortest permitted width. -/
theorem palindromic_boundary_witness :
    Canonical 29 (literalDigit 29) 2 ∧
    Canonical 110 (literalDigit 110) 3 ∧
    Canonical 121 (literalDigit 121) 3 ∧
    step 29 = 121 ∧ step 110 = 121 ∧ Palindrome 121 := by
  refine ⟨boundary_short_canonical, boundary_long_canonical,
    boundary_target_canonical, ?_, ?_, boundary_reversals.2.2⟩
  · change 29 + reverse10 29 = 121
    rw [boundary_reversals.1]
  · change 110 + reverse10 110 = 121
    rw [boundary_reversals.2.1]

#print axioms literalDigit_bounded
#print axioms short_canonical
#print axioms long_canonical
#print axioms target_canonical
#print axioms short_reverse
#print axioms long_reverse
#print axioms target_reverse
#print axioms short_step
#print axioms long_step
#print axioms target_not_palindrome
#print axioms retained_profiles
#print axioms terminal_carries
#print axioms nonpalindromic_cross_width_witness
#print axioms boundary_short_canonical
#print axioms boundary_long_canonical
#print axioms boundary_target_canonical
#print axioms boundary_reversals
#print axioms palindromic_boundary_witness

end Agent105.CrossWidthWitness9df76b

