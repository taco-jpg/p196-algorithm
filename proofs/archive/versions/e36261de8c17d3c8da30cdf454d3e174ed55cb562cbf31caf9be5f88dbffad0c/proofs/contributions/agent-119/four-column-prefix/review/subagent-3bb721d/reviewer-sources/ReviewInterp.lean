import FourColumnConclusion

/-! Reviewer interpretation tests: `Starts3` reads digits from the MOST
significant end of the canonical numeral (1209 begins 1,2,0 and not 9,0,2),
and `Starts2 3 3` holds for the two-digit palindrome 33 itself. -/

open FourColumnKernel DecimalDigits SevenColumnKernel.PalindromeBridge

def revDig (n i : Nat) : Nat := (n / 10 ^ i) % 10

theorem can1209 : Canonical 1209 (revDig 1209) 4 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i _
  exact Nat.le_of_lt_succ (Nat.mod_lt _ (by decide))

theorem starts3_1209_pos : Starts3 1 2 0 1209 :=
  ⟨revDig 1209, 4, can1209, by decide, by decide, by decide, by decide⟩

theorem starts3_1209_not_reversed : ¬ Starts3 9 0 2 1209 := by
  rintro ⟨e, W, hc, _, h1, _, _⟩
  obtain ⟨hw, hd⟩ := canonical_unique can1209 hc
  subst hw
  change e 3 = 9 at h1
  rw [← hd 3 (by decide)] at h1
  exact absurd h1 (by decide)

theorem can33 : Canonical 33 (revDig 33) 2 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i _
  exact Nat.le_of_lt_succ (Nat.mod_lt _ (by decide))

theorem starts2_33 : FourColumnKernel.Certificate.Starts2 3 3 33 :=
  ⟨revDig 33, 2, can33, by decide, by decide, by decide⟩

theorem not_starts3_33 : ¬ Starts3 3 3 3 33 := by
  rintro ⟨e, W, hc, hW, _, _, _⟩
  obtain ⟨hw, _⟩ := canonical_unique can33 hc
  omega

/-- Instance of the headline theorem at P = 33 (width 2). -/
example : ∀ A t, 0 < A → Lychrel196.orbit A t = 33 → t ≤ 5 := fun A t hA h =>
  FourColumnKernel.Certificate.ancestry_bound_33 A 33 t hA (by decide) starts2_33 h

#print axioms starts3_1209_pos
#print axioms starts3_1209_not_reversed
#print axioms starts2_33
#print axioms not_starts3_33
