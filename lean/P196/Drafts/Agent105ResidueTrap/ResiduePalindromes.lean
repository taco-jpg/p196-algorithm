import P196.Drafts.Agent108ModularAutonomy.DigitPerturbation

/-! Exact-width palindromes representing every multiple-of-eleven residue
modulo 99 at every positive even width. These are ordinary finite integers;
the construction is not an assertion that an orbit visits them. -/

namespace Agent105.ResiduePalindromes

open Lychrel196 DecimalDigits ModularAutonomy

def edgeDigits (L a i : Nat) : Nat :=
  digitSpike 0 a i + digitSpike (L - 1) a i

theorem edge_canonical (L a : Nat) (hL : 2 ≤ L)
    (ha : 0 < a) (hb : a ≤ 9) :
    Canonical (a + a * 10 ^ (L - 1)) (edgeDigits L a) L := by
  refine ⟨by omega, ?_, ?_, ?_⟩
  · intro i _
    by_cases h0 : i = 0
    · simp [edgeDigits, digitSpike, h0, show 0 ≠ L - 1 by omega]
      exact hb
    · by_cases hl : i = L - 1
      · simp [edgeDigits, digitSpike, h0, hl, show L - 1 ≠ 0 by omega]
        exact hb
      · simp [edgeDigits, digitSpike, h0, hl]
  · simpa [edgeDigits, digitSpike, show L - 1 ≠ 0 by omega] using ha
  · change value (fun i => digitSpike 0 a i + digitSpike (L - 1) a i) L = _
    rw [value_add, value_digitSpike, value_digitSpike]
    simp [show 0 < L by omega, show L - 1 < L by omega]

theorem edge_palindrome (L a : Nat) (hL : 2 ≤ L)
    (ha : 0 < a) (hb : a ≤ 9) :
    Palindrome (a + a * 10 ^ (L - 1)) := by
  have hc := edge_canonical L a hL ha hb
  rw [← hc.2.2.2]
  apply (palindrome_value_iff _ _ hc.2.1 (Or.inr hc.2.2.1)).mpr
  intro i hi
  have h0 : (L - 1 - i = 0) ↔ i = L - 1 := by omega
  have hl : (L - 1 - i = L - 1) ↔ i = 0 := by omega
  simp only [edgeDigits, digitSpike, h0, hl, Nat.add_comm]

theorem edge_mod99 (L a : Nat) (hL : 0 < L) (he : L % 2 = 0) :
    (a + a * 10 ^ (L - 1)) % 99 = (11 * a) % 99 := by
  have ho : (L - 1) % 2 ≠ 0 := by omega
  have hp : 10 ^ (L - 1) % 99 = 10 := by
    simpa [ho] using AstraModular.ten_pow_mod99 (L - 1)
  calc
    (a + a * 10 ^ (L - 1)) % 99 = (a + a * 10) % 99 := by
      rw [Nat.add_mod a (a * 10 ^ (L - 1)),
        Nat.mul_mod a (10 ^ (L - 1)), hp,
        Nat.add_mod a (a * 10), Nat.mul_mod a 10]
    _ = (11 * a) % 99 := by congr 1; omega

/-- Every multiple of eleven has a same-residue ordinary palindrome at
each positive even canonical width, including width two. -/
theorem matching_even_palindrome (n L : Nat) (hL : 0 < L)
    (he : L % 2 = 0) (hn : 11 ∣ n) :
    ∃ p d, 0 < p ∧ Canonical p d L ∧ Palindrome p ∧ p % 99 = n % 99 := by
  have hL2 : 2 ≤ L := by omega
  have hm : (n % 99) % 11 = 0 := by
    rw [Nat.mod_mod_of_dvd _ (by decide : 11 ∣ 99)]
    exact Nat.mod_eq_zero_of_dvd hn
  have hbound := Nat.mod_lt n (by decide : 0 < 99)
  obtain ⟨a, ha, hb, hr⟩ : ∃ a, 0 < a ∧ a ≤ 9 ∧ (11 * a) % 99 = n % 99 := by
    by_cases hz : n % 99 = 0
    · exact ⟨9, by decide, by decide, by simp [hz]⟩
    · refine ⟨(n % 99) / 11, by omega, by omega, ?_⟩
      have hh : 11 * ((n % 99) / 11) = n % 99 := by omega
      rw [hh, Nat.mod_mod]
  refine ⟨a + a * 10 ^ (L - 1), edgeDigits L a, by omega,
    edge_canonical L a hL2 ha hb, edge_palindrome L a hL2 ha hb, ?_⟩
  rw [edge_mod99 L a hL he, hr]

#print axioms edge_canonical
#print axioms edge_palindrome
#print axioms edge_mod99
#print axioms matching_even_palindrome

end Agent105.ResiduePalindromes
