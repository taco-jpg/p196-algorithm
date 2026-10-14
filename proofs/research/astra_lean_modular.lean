import Lychrel196Research

/-!
Unconditional decimal modular theorems, connected to the executable ordinary
reversal and canonical numeral semantics in `Lychrel196Research`.

This file does not formalize arbitrary-modulus palindrome residue saturation,
and does not prove a decimal Lychrel existence statement.
-/

namespace DecimalModular

set_option maxRecDepth 10000

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization

theorem ten_pow_mod99 (L : Nat) :
    10 ^ L % 99 = if L % 2 = 0 then 1 else 10 := by
  induction L with
  | zero => decide
  | succ L ih =>
    rw [Nat.pow_succ, Nat.mul_mod, ih]
    by_cases h : L % 2 = 0
    · have hs : (L + 1) % 2 ≠ 0 := by omega
      simp [h, hs]
    · have hs : (L + 1) % 2 = 0 := by omega
      simp [h, hs]

/-- Exact reflection arithmetic; no bounded-digit assumption is needed. -/
theorem reflected_mod99 (d : Nat → Nat) (L : Nat) :
    value (reflected d L) L % 99 =
      ((if L % 2 = 0 then 10 else 1) * value d L) % 99 := by
  induction L generalizing d with
  | zero => simp [value]
  | succ L ih =>
    have ht := ih (fun i => d (i + 1))
    have hp := ten_pow_mod99 L
    rw [reflected_value_shift, value_shift]
    by_cases h : L % 2 = 0
    · have hs : (L + 1) % 2 ≠ 0 := by omega
      simp only [h, hs, ↓reduceIte] at ht hp ⊢
      simp only [Nat.add_mod, Nat.mul_mod, hp, ht, Nat.mod_mod,
        Nat.one_mul, Nat.mul_one]
      simp only [Nat.reduceMod] at *
      omega
    · have hs : (L + 1) % 2 = 0 := by omega
      simp only [h, hs, ↓reduceIte] at ht hp ⊢
      simp only [Nat.add_mod, Nat.mul_mod, hp, ht, Nat.mod_mod,
        Nat.one_mul, Nat.mul_one]
      simp only [Nat.reduceMod] at *
      omega

/-- Ordinary reversal is determined modulo 99 by residue and exact width. -/
theorem reverse10_mod99 (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) :
    reverse10 n % 99 = ((if L % 2 = 0 then 10 else 1) * n) % 99 := by
  rcases hc with ⟨hL, hd, hp, rfl⟩
  rw [reverse10_value d L hd (Or.inr hp)]
  exact reflected_mod99 d L

/-- Each even-width step multiplies the residue by 11; each odd-width step
multiplies it by 2. This statement concerns actual finite decimal integers. -/
theorem step_mod99 (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) :
    step n % 99 = ((if L % 2 = 0 then 11 else 2) * n) % 99 := by
  have hr := reverse10_mod99 n d L hc
  change (n + reverse10 n) % 99 = _
  rw [Nat.add_mod, hr]
  by_cases h : L % 2 = 0
  · simp only [if_pos h]
    omega
  · simp only [if_neg h, Nat.one_mul]
    omega

theorem reverse10_mod_of_dvd99 (M n : Nat) (d : Nat → Nat) (L : Nat)
    (hM : M ∣ 99) (hc : Canonical n d L) :
    reverse10 n % M = ((if L % 2 = 0 then 10 else 1) * n) % M := by
  have h := congrArg (fun x => x % M) (reverse10_mod99 n d L hc)
  simpa only [Nat.mod_mod_of_dvd _ hM] using h

theorem step_mod_of_dvd99 (M n : Nat) (d : Nat → Nat) (L : Nat)
    (hM : M ∣ 99) (hc : Canonical n d L) :
    step n % M = ((if L % 2 = 0 then 11 else 2) * n) % M := by
  have h := congrArg (fun x => x % M) (step_mod99 n d L hc)
  simpa only [Nat.mod_mod_of_dvd _ hM] using h

theorem even_width_step_dvd11 (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) (he : L % 2 = 0) : 11 ∣ step n := by
  have h := step_mod_of_dvd99 11 n d L (by decide) hc
  simp only [if_pos he] at h
  exact Nat.dvd_of_mod_eq_zero (by omega)

theorem step_preserves_dvd11 (n : Nat) (h : 11 ∣ n) : 11 ∣ step n := by
  by_cases hn : n = 0
  · subst n
    decide
  · obtain ⟨d, L, hc⟩ := canonical_exists n (by omega)
    have hr := step_mod_of_dvd99 11 n d L (by decide) hc
    have hz := Nat.mod_eq_zero_of_dvd h
    apply Nat.dvd_of_mod_eq_zero
    by_cases he : L % 2 = 0
    · simp only [if_pos he] at hr
      omega
    · simp only [if_neg he] at hr
      omega

theorem orbit_preserves_dvd11 (n k : Nat) (h : 11 ∣ n) :
    11 ∣ orbit n k := by
  induction k with
  | zero => exact h
  | succ k ih => exact step_preserves_dvd11 (orbit n k) ih

/-- If all widths seen so far are odd, width cannot yet have increased. -/
theorem all_odd_widths_constant (q : Nat → Nat) (L K : Nat)
    (h : ∀ k, k ≤ K → (iterPairs q L k).1 % 2 ≠ 0) :
    (iterPairs q L K).1 = L := by
  induction K with
  | zero => rfl
  | succ K ih =>
    have hi := ih (fun k hk => h k (by omega))
    have ho := h K (by omega)
    have hn := h (K + 1) (by omega)
    simp only [iterPairs, nextWidth] at hn ⊢
    by_cases hb : carry (iterPairs q L K).2 (iterPairs q L K).1 = 0
    · simp only [if_pos hb] at hn ⊢
      omega
    · simp only [if_neg hb] at hn ⊢
      omega

/-- Every admissible decimal orbit encounters an even input width by time 5. -/
theorem exists_even_width_by_five (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) :
    ∃ k, k ≤ 5 ∧ (iterPairs q L k).1 % 2 = 0 := by
  apply Classical.byContradiction
  intro h
  have ho : ∀ k, k ≤ 5 → (iterPairs q L k).1 % 2 ≠ 0 := by
    intro k hk he
    exact h ⟨k, hk, he⟩
  have hc := all_odd_widths_constant q L 5 ho
  have hg := DecimalWidthGrowth.width_lower_bound q L 5 ha
  omega

/-- Uniform numeric theorem: after six reverse-and-add steps every positive
integer is divisible by 11, and this remains true at every later time. -/
theorem orbit_six_dvd11 (n : Nat) (hn : 0 < n) : 11 ∣ orbit n 6 := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  have ha := NormalizationBridge.canonical_admissible n d L hc
  obtain ⟨k, hk, he⟩ := exists_even_width_by_five (columnSum d L) L ha
  obtain ⟨e, hec, _⟩ := iterPairs_representation n d (columnSum d L) L k hc
    (fun _ _ => rfl)
  have hd : 11 ∣ orbit n (k + 1) := even_width_step_dvd11
    (orbit n k) e (iterPairs (columnSum d L) L k).1 hec he
  have ht := orbit_preserves_dvd11 (orbit n (k + 1)) (5 - k) hd
  rw [← LychrelCertificates.orbit_add] at ht
  have hi : k + 1 + (5 - k) = 6 := by omega
  rwa [hi] at ht

theorem orbit_eventually_dvd11 (n k : Nat) (hn : 0 < n) :
    11 ∣ orbit n (6 + k) := by
  have h := orbit_preserves_dvd11 (orbit n 6) k (orbit_six_dvd11 n hn)
  simpa only [← LychrelCertificates.orbit_add] using h

theorem orbit_mod11_eq_zero_of_six_le (n k : Nat) (hn : 0 < n)
    (hk : 6 ≤ k) : orbit n k % 11 = 0 := by
  have h := orbit_eventually_dvd11 n (k - 6) hn
  have he : 6 + (k - 6) = k := by omega
  rw [he] at h
  exact Nat.mod_eq_zero_of_dvd h

set_option maxHeartbeats 0 in
/-- Six cannot be replaced by five in the uniform theorem. -/
theorem six_step_bound_sharp :
    (∀ k ∈ List.range 6, ¬ 11 ∣ orbit 100 k) ∧ 11 ∣ orbit 100 6 := by
  decide

/-- The units digit of an ordinary reversal is its nonzero original lead. -/
theorem reverse10_mod10 (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) : reverse10 n % 10 = d (L - 1) := by
  rcases hc with ⟨hL, hd, hp, rfl⟩
  rw [reverse10_value d L hd (Or.inr hp)]
  obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : L ≠ 0)
  rw [value_shift]
  have hb := hd k (by omega)
  simp only [reflected, Nat.add_sub_cancel, Nat.succ_sub_one, Nat.sub_zero]
  omega

/-- A zero units digit cannot persist for two successive positive iterates. -/
theorem zero_units_step_nonzero (n : Nat) (hn : 0 < n)
    (hz : n % 10 = 0) : step n % 10 ≠ 0 := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  have hr := reverse10_mod10 n d L hc
  have hp := hc.2.2.1
  have hL := hc.1
  have hb := hc.2.1 (L - 1) (by omega)
  change (n + reverse10 n) % 10 ≠ 0
  omega

theorem no_consecutive_zero_units (n : Nat) (hn : 0 < n) (k : Nat) :
    ¬ (10 ∣ orbit n k ∧ 10 ∣ orbit n (k + 1)) := by
  intro h
  have hpos := DecimalDigits.orbit_positive n hn k
  have hh := zero_units_step_nonzero (orbit n k) hpos
    (Nat.mod_eq_zero_of_dvd h.1)
  exact hh (Nat.mod_eq_zero_of_dvd h.2)

/-- At every sufficiently late time, one of two consecutive iterates meets
both local compatibility conditions of fixed-modulus palindrome saturation. -/
theorem late_compatible_state (n k : Nat) (hn : 0 < n) :
    ∃ j, 6 + k ≤ j ∧ j ≤ 7 + k ∧
      11 ∣ orbit n j ∧ ¬ 10 ∣ orbit n j := by
  by_cases hz : 10 ∣ orbit n (6 + k)
  · refine ⟨7 + k, by omega, by omega, ?_, ?_⟩
    · have h := orbit_eventually_dvd11 n (k + 1) hn
      have hi : 6 + (k + 1) = 7 + k := by omega
      rwa [hi] at h
    · intro hb
      apply no_consecutive_zero_units n hn (6 + k)
      refine ⟨hz, ?_⟩
      have hi : 6 + k + 1 = 7 + k := by omega
      rwa [hi]
  · exact ⟨6 + k, by omega, by omega, orbit_eventually_dvd11 n k hn, hz⟩

/-- Actual orbit states satisfy all the arithmetic compatibility conditions
at arbitrarily large canonical widths, with an explicit linear time bound.
This is not a palindrome-existence or palindrome-avoidance theorem. -/
theorem large_width_compatible_state (n B : Nat) (hn : 0 < n) :
    ∃ j e W, 6 + 4 * B ≤ j ∧ j ≤ 7 + 4 * B ∧
      Canonical (orbit n j) e W ∧ B ≤ W ∧
      11 ∣ orbit n j ∧ ¬ 10 ∣ orbit n j := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  obtain ⟨j, hjlo, hjhi, h11, h10⟩ := late_compatible_state n (4 * B) hn
  obtain ⟨e, W, he, hg, _⟩ := DecimalWidthGrowth.numeric_width_bounds n d L j hc
  refine ⟨j, e, W, hjlo, hjhi, he, ?_, h11, h10⟩
  omega

/-- The preceding orbit state also meets the compatibility conditions after
reduction modulo any fixed M, including the even-width factor gcd(M,11). -/
theorem large_width_compatible_residue (M n B : Nat) (hn : 0 < n) :
    ∃ j e W, 6 + 4 * B ≤ j ∧ j ≤ 7 + 4 * B ∧
      Canonical (orbit n j) e W ∧ B ≤ W ∧
      ¬ (10 ∣ M ∧ 10 ∣ (orbit n j % M)) ∧
      (W % 2 = 0 → Nat.gcd M 11 ∣ (orbit n j % M)) := by
  obtain ⟨j, e, W, hjlo, hjhi, hc, hB, h11, h10⟩ :=
    large_width_compatible_state n B hn
  refine ⟨j, e, W, hjlo, hjhi, hc, hB, ?_, ?_⟩
  · intro h
    exact h10 ((Nat.dvd_mod_iff h.1).mp h.2)
  · intro _
    exact (Nat.dvd_mod_iff (Nat.gcd_dvd_left M 11)).mpr
      (Nat.dvd_trans (Nat.gcd_dvd_right M 11) h11)

/-- Every symmetric even-width coefficient word has value divisible by 11;
coefficients can be arbitrary natural numbers, not just decimal digits. -/
theorem even_symmetric_value_dvd11 (d : Nat → Nat) (L : Nat)
    (he : L % 2 = 0) (hs : ∀ i, i < L → d i = d (L - 1 - i)) :
    11 ∣ value d L := by
  have hv : value (reflected d L) L = value d L := by
    apply value_congr
    intro i hi
    exact (hs i hi).symm
  have hr := reflected_mod99 d L
  rw [hv, if_pos he] at hr
  apply Nat.dvd_of_mod_eq_zero
  omega

theorem value_scale (a : Nat) (d : Nat → Nat) (L : Nat) :
    value (fun i => a * d i) L = a * value d L := by
  induction L with
  | zero => simp [value]
  | succ L ih => simp only [value, ih, Nat.mul_add, Nat.mul_assoc]

/-- An overflow to a palindrome from an even input width forces a second
factor of 11, beyond the universal eventual single factor. -/
theorem even_width_palindromic_overflow_dvd121
    (n : Nat) (d : Nat → Nat) (L : Nat) (hc : Canonical n d L)
    (he : L % 2 = 0) (ho : carry (columnSum d L) L = 1)
    (hp : Palindrome (step n)) : 121 ∣ step n := by
  have hpc : Palindrome (step (value d L)) := by rwa [hc.2.2.2]
  have hq := (step_palindrome_iff_overflow d L hc.1 hc.2.1 hc.2.2.1 ho).mp hpc
  let b : Nat → Nat := fun i => columnSum d L i / 11
  have hb : ∀ i, i < L → b i = b (L - 1 - i) := by
    intro i hi
    exact congrArg (fun x => x / 11) (columnSum_symmetric d L i hi)
  have hd := even_symmetric_value_dvd11 b L he hb
  have hscale : value (columnSum d L) L = 11 * value b L := by
    rw [← value_scale]
    apply value_congr
    intro i hi
    have hqi := hq.2 i hi
    dsimp [b]
    omega
  have hstep := FoldedDecimal.step_eq_word_value n d (columnSum d L) L hc
    (fun _ _ => rfl)
  rcases hd with ⟨k, hk⟩
  refine ⟨k, ?_⟩
  rw [hstep, hscale, hk]
  omega

theorem even_width_overflow_not_palindrome_of_not_dvd121
    (n : Nat) (d : Nat → Nat) (L : Nat) (hc : Canonical n d L)
    (he : L % 2 = 0) (ho : carry (columnSum d L) L = 1)
    (h : ¬ 121 ∣ step n) : ¬ Palindrome (step n) := by
  intro hp
  exact h (even_width_palindromic_overflow_dvd121 n d L hc he ho hp)

#print axioms reverse10_mod99
#print axioms step_mod99
#print axioms orbit_eventually_dvd11
#print axioms orbit_mod11_eq_zero_of_six_le
#print axioms six_step_bound_sharp
#print axioms no_consecutive_zero_units
#print axioms late_compatible_state
#print axioms large_width_compatible_residue
#print axioms even_width_palindromic_overflow_dvd121

end DecimalModular
