import P196.Foundations.LychrelDigitSums

/-! Exact-width residue compatibility and conditional consequences of
palindrome saturation. This module does not prove saturation existence. -/
namespace ExactLengthResidues

open Lychrel196 DecimalDigits

/-- The necessary residue restrictions for a positive palindrome of exact
width L. -/
def Compatible (M L a : Nat) : Prop :=
  ¬ (10 ∣ M ∧ 10 ∣ a) ∧ (L % 2 = 0 → Nat.gcd M 11 ∣ a)

/-- Every compatible residue has a positive palindrome representative at
each exact width above B. Existence of such a B is a separate obligation. -/
def SaturationAbove (M B : Nat) : Prop :=
  ∀ L, B ≤ L → ∀ a, Compatible M L a →
    ∃ p d, 0 < p ∧ Canonical p d L ∧ Palindrome p ∧ p % M = a % M

/-- A genuine positive canonical palindrome has a nonzero units digit. -/
theorem palindrome_not_dvd10 (p L : Nat) (d : Nat → Nat)
    (hc : Canonical p d L) (hp : Palindrome p) : ¬ 10 ∣ p := by
  have hr := AstraModular.reverse10_mod10 p d L hc
  change reverse10 p = p at hp
  rw [hp] at hr
  intro hd
  have hz := Nat.mod_eq_zero_of_dvd hd
  have hlead := hc.2.2.1
  omega

/-- The exact-width parity restriction for an ordinary palindrome. -/
theorem even_palindrome_dvd11 (p L : Nat) (d : Nat → Nat)
    (hc : Canonical p d L) (hp : Palindrome p) (he : L % 2 = 0) : 11 ∣ p := by
  have hr := AstraModular.reverse10_mod_of_dvd99 11 p d L (by decide) hc
  change reverse10 p = p at hp
  rw [hp, if_pos he] at hr
  apply Nat.dvd_of_mod_eq_zero
  omega

/-- Necessity is transported along actual congruence modulo M. -/
theorem palindrome_residue_compatible (M L a p : Nat) (d : Nat → Nat)
    (hc : Canonical p d L) (hp : Palindrome p)
    (hr : p % M = a % M) : Compatible M L a := by
  constructor
  · intro h
    have hm : 10 ∣ p % M := by
      rw [hr]
      exact (Nat.dvd_mod_iff h.1).mpr h.2
    exact palindrome_not_dvd10 p L d hc hp ((Nat.dvd_mod_iff h.1).mp hm)
  · intro he
    have hd : Nat.gcd M 11 ∣ p :=
      Nat.dvd_trans (Nat.gcd_dvd_right M 11) (even_palindrome_dvd11 p L d hc hp he)
    apply (Nat.dvd_mod_iff (Nat.gcd_dvd_left M 11)).mp
    rw [← hr]
    exact (Nat.dvd_mod_iff (Nat.gcd_dvd_left M 11)).mpr hd

/-- Once a saturation bound is supplied, it gives the exact iff at every
width above that bound. -/
theorem palindrome_residue_iff_of_saturation (M B L a : Nat)
    (hs : SaturationAbove M B) (hL : B ≤ L) :
    (∃ p d, 0 < p ∧ Canonical p d L ∧ Palindrome p ∧ p % M = a % M) ↔
      Compatible M L a := by
  constructor
  · rintro ⟨p, d, _, hc, hp, hr⟩
    exact palindrome_residue_compatible M L a p d hc hp hr
  · exact hs L hL a

/-- Conditional matching of a sufficiently late actual orbit state with a
positive palindrome of the same exact width and residue. This does not say
that the orbit reaches the constructed palindrome. -/
theorem orbit_matches_palindrome_of_saturation (M n B : Nat) (hn : 0 < n)
    (hs : SaturationAbove M B) :
    ∃ t p d e L, 6 + 4 * B ≤ t ∧ t ≤ 7 + 4 * B ∧ B ≤ L ∧
      Canonical (orbit n t) d L ∧ Canonical p e L ∧
      0 < p ∧ Palindrome p ∧ orbit n t % M = p % M := by
  obtain ⟨t, d, L, ht0, ht1, hc, hB, h10, h11⟩ :=
    AstraModular.large_width_compatible_residue M n B hn
  obtain ⟨p, e, hp, hpc, hpal, hr⟩ := hs L hB (orbit n t % M) ⟨h10, h11⟩
  refine ⟨t, p, d, e, L, ht0, ht1, hB, hc, hpc, hp, hpal, ?_⟩
  simpa only [Nat.mod_mod] using hr.symm

/-- At exact widths at least B, membership is constant on each residue
class. Different exact widths may use different allowed residue classes. -/
def SetSaturatedAbove (S : Nat → Prop) (M B : Nat) : Prop :=
  ∀ L, B ≤ L → ∀ n m (d e : Nat → Nat),
    Canonical n d L → Canonical m e L → n % M = m % M → (S n ↔ S m)

/-- A saturation bound may always be increased. -/
theorem saturationAbove_mono (M B C : Nat) (hs : SaturationAbove M B)
    (hBC : B ≤ C) : SaturationAbove M C := by
  intro L hCL a ha
  exact hs L (Nat.le_trans hBC hCL) a ha

/-- Conditional obstruction to nonempty positive forward-closed sets whose
membership eventually depends only on exact width and residue modulo M. -/
theorem closed_saturated_contains_palindrome_of_saturation (M : Nat)
    (S : Nat → Prop) (hpal : ∃ B, SaturationAbove M B)
    (hne : ∃ n, 0 < n ∧ S n)
    (hclosed : ∀ n, 0 < n → S n → S (step n))
    (hsat : ∃ B, SetSaturatedAbove S M B) :
    ∃ p, 0 < p ∧ S p ∧ Palindrome p := by
  obtain ⟨B, hB⟩ := hpal
  obtain ⟨C, hC⟩ := hsat
  obtain ⟨n, hn, hs⟩ := hne
  obtain ⟨t, p, d, e, L, _, _, hL, hc, hpc, hp, hpal, hr⟩ :=
    orbit_matches_palindrome_of_saturation M n (max B C) hn
      (saturationAbove_mono M B (max B C) hB (Nat.le_max_left B C))
  have hmem : ∀ k, S (orbit n k) := by
    intro k
    induction k with
    | zero => exact hs
    | succ k ih => exact hclosed (orbit n k) (orbit_positive n hn k) ih
  refine ⟨p, hp, ?_, hpal⟩
  exact (hC L (Nat.le_trans (Nat.le_max_right B C) hL)
    (orbit n t) p d e hc hpc hr).mp (hmem t)

end ExactLengthResidues

#print axioms ExactLengthResidues.palindrome_not_dvd10
#print axioms ExactLengthResidues.even_palindrome_dvd11
#print axioms ExactLengthResidues.palindrome_residue_compatible
#print axioms ExactLengthResidues.palindrome_residue_iff_of_saturation
#print axioms ExactLengthResidues.orbit_matches_palindrome_of_saturation
#print axioms ExactLengthResidues.saturationAbove_mono
#print axioms ExactLengthResidues.closed_saturated_contains_palindrome_of_saturation
