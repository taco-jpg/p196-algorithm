import LychrelDigitSums

/-!
Agent #106. Exact ordinary-decimal facts for the dense first output in
CONGRUENCE_PATHS.md, Section 3. The source family is 11 * (10^k - 1).
The digit sum and canonical width below use the existing repository
definitions. No surrogate reverse-and-add map is introduced.

Claim: coordination commit 2d9f553521404c98c119ed92e4c0538dce17aea4.
Written source: Git blob fc8bef244f236095de36b9319f07147f23d41d1a.
-/

namespace Agent106.CongruenceBudget

open DecimalDigits DecimalMass DecimalQuantitativeMass

private theorem digitSum_append_digit (n d : Nat) (hd : d < 10) :
    digitSum (10 * n + d) = digitSum n + d := by
  have hm : (10 * n + d) % 10 = d := by omega
  have hq : (10 * n + d) / 10 = n := by omega
  rw [digitSum_mod_div, hm, hq]
  omega

private theorem decimalLength_append_digit (n d : Nat)
    (hn : 0 < n) (hd : d < 10) :
    decimalLength (10 * n + d) = decimalLength n + 1 := by
  have hp : 10 * n + d ≠ 0 := by omega
  have hq : (10 * n + d) / 10 = n := by omega
  rw [decimalLength]
  simp only [hp, ↓reduceDIte, hq]

private theorem prefix_positive (r : Nat) : 0 < 11 * 10 ^ r - 1 := by
  have hp : 0 < 10 ^ r := Nat.pow_pos (by decide)
  omega

private theorem prefix_succ (r : Nat) :
    11 * 10 ^ (r + 1) - 1 = 10 * (11 * 10 ^ r - 1) + 9 := by
  have hp : 0 < 10 ^ r := Nat.pow_pos (by decide)
  rw [Nat.pow_succ]
  omega

private theorem prefix_digitSum (r : Nat) :
    digitSum (11 * 10 ^ r - 1) = 9 * r + 1 := by
  induction r with
  | zero => simp [digitSum]
  | succ r ih =>
    rw [prefix_succ, digitSum_append_digit _ 9 (by decide), ih]
    omega

private theorem prefix_decimalLength (r : Nat) :
    decimalLength (11 * 10 ^ r - 1) = r + 2 := by
  induction r with
  | zero => simp [decimalLength]
  | succ r ih =>
    rw [prefix_succ,
      decimalLength_append_digit _ 9 (prefix_positive r) (by decide), ih]

private theorem denseOutput_expand (r : Nat) :
    11 * (10 ^ (r + 2) - 1) =
      10 * (10 * (11 * 10 ^ r - 1) + 8) + 9 := by
  have hp : 0 < 10 ^ r := Nat.pow_pos (by decide)
  rw [show r + 2 = (r + 1) + 1 by omega, Nat.pow_succ, Nat.pow_succ]
  omega

/-- The exact ordinary digit sum of 1,0,9^(k-2),8,9. -/
theorem denseOutput_digitSum (k : Nat) (hk : 2 ≤ k) :
    DecimalMass.digitSum (11 * (10 ^ k - 1)) = 9 * k := by
  obtain ⟨r, rfl⟩ : ∃ r, k = r + 2 := ⟨k - 2, by omega⟩
  rw [denseOutput_expand,
    digitSum_append_digit _ 9 (by decide),
    digitSum_append_digit _ 8 (by decide), prefix_digitSum]
  omega

/-- Its width is k+2, including the zero in the second leading position. -/
theorem denseOutput_decimalLength (k : Nat) (hk : 2 ≤ k) :
    DecimalQuantitativeMass.decimalLength (11 * (10 ^ k - 1)) = k + 2 := by
  obtain ⟨r, rfl⟩ : ∃ r, k = r + 2 := ⟨k - 2, by omega⟩
  have hp := prefix_positive r
  rw [denseOutput_expand,
    decimalLength_append_digit _ 9 (by omega) (by decide),
    decimalLength_append_digit _ 8 hp (by decide), prefix_decimalLength]

/-- Positive ordinary inputs have an actual canonical representation at
the exact width used by the carry-count budget. -/
theorem denseOutput_canonical (k : Nat) (hk : 2 ≤ k) :
    ∃ d, DecimalDigits.Canonical (11 * (10 ^ k - 1)) d (k + 2) := by
  have hp : 0 < 11 * (10 ^ k - 1) := by
    obtain ⟨r, rfl⟩ : ∃ r, k = r + 2 := ⟨k - 2, by omega⟩
    rw [denseOutput_expand]
    omega
  obtain ⟨d, L, hc⟩ := canonical_exists (11 * (10 ^ k - 1)) hp
  have hw := decimalLength_of_canonical (11 * (10 ^ k - 1)) d L hc
  have he := denseOutput_decimalLength k hk
  have hL : L = k + 2 := by omega
  rw [hL] at hc
  exact ⟨d, hc⟩

#print axioms denseOutput_digitSum
#print axioms denseOutput_decimalLength
#print axioms denseOutput_canonical

end Agent106.CongruenceBudget
