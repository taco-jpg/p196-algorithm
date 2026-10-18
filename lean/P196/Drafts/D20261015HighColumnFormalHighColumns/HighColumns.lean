import P196.Foundations.LychrelDigitSums

/-! A decimal interval of pair coefficients forces a palindrome within
two positive steps. No assertion about palindrome status at time zero
is made; no persistent seam certificate is inferred. -/

namespace HighColumns

open DecimalDigits FoldedDecimal OverflowCarryNormalization Lychrel196

def HighColumnWord (q : Nat → Nat) (L : Nat) : Prop :=
  (∀ i, i < L → 9 ≤ q i ∧ q i ≤ 13) ∧ 10 ≤ q 0

theorem carry_one (q : Nat → Nat) (L : Nat) (hq : HighColumnWord q L) :
    ∀ i, 0 < i → i ≤ L → carry q i = 1 := by
  intro i
  induction i with
  | zero => intro hi _; omega
  | succ i ih =>
    intro _ hi
    have hqi := hq.1 i (by omega)
    by_cases hz : i = 0
    · subst i
      have hfirst := hq.2
      simp only [carry, Nat.add_zero]
      omega
    · have hc := ih (by omega) (by omega)
      simp only [carry, hc]
      omega

theorem output_zero_formula (q : Nat → Nat) (L : Nat) (hL : 0 < L)
    (hq : HighColumnWord q L) : output q 0 = q 0 - 10 := by
  have hfirst := hq.2
  have hb := hq.1 0 hL
  simp only [output, carry, Nat.add_zero]
  omega

theorem output_positive_formula (q : Nat → Nat) (L i : Nat)
    (hq : HighColumnWord q L) (hipos : 0 < i) (hi : i < L) :
    output q i = q i - 9 := by
  have hc := carry_one q L hq i hipos (by omega)
  have hb := hq.1 i hi
  simp only [output, hc]
  omega

theorem output_le_four (q : Nat → Nat) (L i : Nat)
    (hq : HighColumnWord q L) (hi : i < L) : output q i ≤ 4 := by
  have hb := hq.1 i hi
  by_cases hz : i = 0
  · subst i
    rw [output_zero_formula q L (by omega) hq]
    omega
  · rw [output_positive_formula q L i hq (by omega) hi]
    omega

theorem nextWidth_eq (q : Nat → Nat) (L : Nat) (hL : 0 < L)
    (hq : HighColumnWord q L) : nextWidth q L = L + 1 := by
  have hc := carry_one q L hq L hL (Nat.le_refl L)
  simp [nextWidth, hc]

/-- Includes the actual leading overflow digit at position `L`. -/
theorem extended_le_four (q : Nat → Nat) (L i : Nat) (hL : 0 < L)
    (hq : HighColumnWord q L) : extended q L i ≤ 4 := by
  unfold extended
  split
  · rename_i hi
    exact output_le_four q L i hq hi
  · rw [carry_one q L hq L hL (Nat.le_refl L)]
    decide

theorem nextColumns_le_eight (q : Nat → Nat) (L i : Nat) (hL : 0 < L)
    (hq : HighColumnWord q L) : nextColumns q L i ≤ 8 := by
  have hc := carry_one q L hq L hL (Nat.le_refl L)
  have ha := extended_le_four q L i hL hq
  have hb := extended_le_four q L (L + 1 - 1 - i) hL hq
  simp only [nextColumns, hc, Nat.one_ne_zero, if_false, columnSum, reflected]
  omega

/-- The second ordinary output is palindromic for every canonical seed
realizing this coefficient range. The seed itself may already be palindromic. -/
theorem numeric_second_palindrome (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hq : HighColumnWord q L) : Palindrome (orbit n 2) := by
  apply iterPairs_low_palindrome n d q L 1 hc hrep
  intro i _
  change nextColumns q L i ≤ 9
  have hb := nextColumns_le_eight q L i hc.1 hq
  omega

/-- Within the high-column range, constant eleven is precisely the
immediate-palindrome case. This concerns positive time one, not time zero. -/
theorem numeric_first_palindrome_iff (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hq : HighColumnWord q L) :
    Palindrome (step n) ↔ ∀ i, i < L → q i = 11 := by
  constructor
  · intro hp
    have hp' : Palindrome (step (value d L)) := by simpa only [hc.2.2.2] using hp
    rcases (step_palindrome_iff d L hc.1 hc.2.1 hc.2.2.1).mp hp'
      with hsmall | ⟨_, hspecial⟩
    · have hzero := hsmall 0 hc.1
      rw [hrep 0 hc.1] at hzero
      have hfirst := hq.2
      omega
    · intro i hi
      have hspeciali := hspecial i hi
      rw [hrep i hi] at hspeciali
      have hbound := hq.1 i hi
      rcases hspeciali with hzero | heleven <;> omega
  · intro heleven
    have hp : Palindrome (step (value d L)) := by
      apply (step_palindrome_iff d L hc.1 hc.2.1 hc.2.2.1).mpr
      right
      constructor
      · rw [hrep 0 hc.1, heleven 0 hc.1]
      · intro i hi
        exact Or.inr ((hrep i hi).trans (heleven i hi))
    simpa only [hc.2.2.2] using hp

theorem numeric_first_positive_time_two (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hq : HighColumnWord q L) (hnot : ∃ i, i < L ∧ q i ≠ 11) :
    ¬ Palindrome (orbit n 1) ∧ Palindrome (orbit n 2) := by
  refine ⟨?_, numeric_second_palindrome n d q L hc hrep hq⟩
  intro hp
  have hall := (numeric_first_palindrome_iff n d q L hc hrep hq).mp hp
  obtain ⟨i, hi, hne⟩ := hnot
  exact hne (hall i hi)

theorem time_zero_control :
    Palindrome 55 ∧ step 55 = 110 ∧ ¬ Palindrome (step 55) ∧
      orbit 55 2 = 121 ∧ Palindrome (orbit 55 2) := by decide

theorem constant_eleven_control :
    step 56 = 121 ∧ Palindrome (step 56) ∧
      orbit 56 2 = 242 ∧ Palindrome (orbit 56 2) := by decide

theorem seam_family_control :
    ¬ Palindrome 999011 ∧ step 999011 = 1110010 ∧ ¬ Palindrome (step 999011) ∧
      orbit 999011 2 = 1210121 ∧ Palindrome (orbit 999011 2) := by decide

/-- The broader bound 14 would not give a uniform two-step conclusion. -/
theorem upper_bound_control :
    step 77 = 154 ∧ orbit 77 2 = 605 ∧ ¬ Palindrome (orbit 77 2) := by decide

end HighColumns
