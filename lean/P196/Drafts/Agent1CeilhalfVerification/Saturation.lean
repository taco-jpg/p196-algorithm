import P196.Drafts.Agent1CeilhalfVerification.ModulusSplit
import P196.Drafts.Agent1CeilhalfVerification.PeriodExistence
import P196.Drafts.Agent1CeilhalfVerification.ArithmeticCRT
import P196.Drafts.Agent1CeilhalfVerification.DigitPools
import P196.Drafts.Agent1CeilhalfVerification.Attempt01

/-! The complete fixed-modulus obstruction. These statements use genuine
ordinary finite decimal integers. They do not assert an actual palindrome
hit, decimal Lychrel existence, or the 196 conjecture. -/
namespace ExactLengthResidues

open Lychrel196 DecimalDigits

/-- Explicit saturation bound for any valid decimal-factor decomposition
and any positive period of ten modulo its coprime factor. -/
theorem saturation_of_split (M k u q r : Nat)
    (hk : 1 ≤ k) (hu : 0 < u) (hq : 0 < q) (hM : M = u*q)
    (hdiv : u ∣ 10^k) (hcop : Nat.gcd u q = 1)
    (hr : 0 < r) (hperiod : 10^r%q=1%q) :
    SaturationAbove M (2*k+4*q*r) := by
  intro L hL a hcompat
  have hk0 : 0 < k := by omega
  have hLk : 2*k ≤ L := by omega
  have hL2 : 2 ≤ L := by omega
  have huM : u ∣ M := ⟨q, hM⟩
  have hqM : q ∣ M := ⟨u, by simpa [Nat.mul_comm] using hM⟩
  have houter : ¬(10 ∣ u ∧ 10 ∣ a) := by
    intro h
    exact hcompat.1 ⟨Nat.dvd_trans h.1 huM, h.2⟩
  obtain ⟨A, hA, hAu, hA0⟩ := outer_block_exists u k a hu hk hdiv houter
  have hga : Nat.gcd q (Nat.gcd (pairWeight0 L) (pairWeight1 L)) ∣ a := by
    rw [pair_weights_gcd_modulus q L hL2]
    split
    · rename_i he
      have hd : Nat.gcd q 11 ∣ Nat.gcd M 11 :=
        Nat.dvd_gcd (Nat.dvd_trans (Nat.gcd_dvd_left q 11) hqM)
          (Nat.gcd_dvd_right q 11)
      exact Nat.dvd_trans hd (hcompat.2 he)
    · exact Nat.one_dvd _
  have hgC : Nat.gcd q (Nat.gcd (pairWeight0 L) (pairWeight1 L)) ∣
      outerValue A k L := by
    rw [pair_weights_gcd_modulus q L hL2]
    split
    · rename_i he
      exact Nat.dvd_trans (Nat.gcd_dvd_right q 11) (outerValue_dvd11 A k L hLk he)
    · exact Nat.one_dvd _
  obtain ⟨x, hx, y, hy, hxy⟩ := shifted_modular_span q
    (pairWeight0 L) (pairWeight1 L) a (outerValue A k L) hq hga hgC
  obtain ⟨P, d, hc, hp, hPu, hPq⟩ := residue_pools_realize A k L u q r x y
    hk0 hr hL hA hA0 hdiv (by omega) (by omega) hperiod
  refine ⟨P, d, ?_, hc, hp, ?_⟩
  · rw [← hc.2.2.2]
    exact value_positive d L hc.1 hc.2.2.1
  · rw [hM]
    exact crt_mod_eq u q P a hu hq hcop (hPu.trans hAu) (hPq.trans hxy)

/-- Every fixed positive modulus has an exact-width saturation threshold.
No modulus-autonomy assumption or restriction to divisors of 99 remains. -/
theorem exists_saturation_bound (M : Nat) (hM : 0 < M) :
    ∃ B, SaturationAbove M B := by
  obtain ⟨k, u, q, hk, hu, hq, heq, hdiv, hqcop, hcop⟩ :=
    decimal_modulus_decomposition_coprime M hM
  obtain ⟨r, hr, hperiod⟩ := exists_positive_ten_period q hq hqcop
  exact ⟨2*k+4*q*r, saturation_of_split M k u q r hk hu hq heq hdiv hcop hr hperiod⟩

/-- Necessary and sufficient conditions for every sufficiently large exact
decimal length, uniformly in the requested residue class. -/
theorem exact_length_palindrome_residues (M : Nat) (hM : 0 < M) :
    ∃ B, ∀ L, B ≤ L → ∀ a,
      (∃ p d, 0 < p ∧ Canonical p d L ∧ Palindrome p ∧ p%M=a%M) ↔
        (¬(10 ∣ M ∧ 10 ∣ a) ∧ (L%2=0 → Nat.gcd M 11 ∣ a)) := by
  obtain ⟨B, hB⟩ := exists_saturation_bound M hM
  exact ⟨B, fun L hL a => palindrome_residue_iff_of_saturation M B L a hB hL⟩

/-- Each positive actual orbit has a sufficiently late state sharing exact
width and residue with a palindrome. The state need not be that palindrome. -/
theorem every_orbit_matches_palindrome (M : Nat) (hM : 0 < M) :
    ∃ B, ∀ n, 0 < n → ∃ t p d e L,
      6+4*B ≤ t ∧ t ≤ 7+4*B ∧ B ≤ L ∧
      Canonical (orbit n t) d L ∧ Canonical p e L ∧
      0 < p ∧ Palindrome p ∧ orbit n t%M=p%M := by
  obtain ⟨B, hB⟩ := exists_saturation_bound M hM
  exact ⟨B, fun n hn => orbit_matches_palindrome_of_saturation M n B hn hB⟩

/-- A nonempty positive forward-closed set whose eventual membership uses
only exact width and one fixed positive modulus contains a palindrome. -/
theorem fixed_modulus_closed_set_contains_palindrome (M : Nat) (hM : 0 < M)
    (S : Nat → Prop) (hne : ∃ n, 0 < n ∧ S n)
    (hclosed : ∀ n, 0 < n → S n → S (step n))
    (hsat : ∃ B, SetSaturatedAbove S M B) :
    ∃ p, 0 < p ∧ S p ∧ Palindrome p := by
  exact closed_saturated_contains_palindrome_of_saturation M S
    (exists_saturation_bound M hM) hne hclosed hsat

#print axioms saturation_of_split
#print axioms exists_saturation_bound
#print axioms exact_length_palindrome_residues
#print axioms every_orbit_matches_palindrome
#print axioms fixed_modulus_closed_set_contains_palindrome

end ExactLengthResidues
