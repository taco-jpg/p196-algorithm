import P196.Foundations.LychrelDigitSums

/-!
Exact digit-sum bound for the sparse target in CONGRUENCE_PATHS.md §3.

The source is the preserved written argument at Git blob
fc8bef244f236095de36b9319f07147f23d41d1a.  The target is an ordinary
natural number; its digit sum is the unchanged DecimalMass.digitSum.
The padded digit representations below serve only to apply the existing
digitSum_value theorem.  No artificial path is identified with an actual
reverse-and-add orbit.
-/

namespace Agent106.CongruenceBudget

open DecimalDigits DecimalMass

/-- Parity-dependent tail from the original congruence-preserving path. -/
def rho (a : Nat) : Nat := if a % 2 = 1 then 89 else 989

/-- The artificial target of the entry jump, with its original arithmetic. -/
def sparse (a : Nat) : Nat := 10 ^ a + 990 * a + rho a

theorem rho_le (a : Nat) : rho a ≤ 989 := by
  unfold rho
  split <;> omega

/-- The source's exponential tail bound, with the lower endpoint shifted to zero. -/
private theorem sparse_tail_bound_shift (j : Nat) :
    990 * (j + 9) + 989 < 10 ^ (j + 4) := by
  induction j with
  | zero => decide
  | succ j ih =>
    have he : j + 1 + 4 = (j + 4) + 1 := by omega
    rw [he, Nat.pow_succ]
    omega

/-- All a ≥ 9 satisfy the original quantitative separation from the leading digit. -/
theorem sparse_tail_bound (a : Nat) (ha : 9 ≤ a) :
    990 * a + 989 < 10 ^ (a - 5) := by
  have h := sparse_tail_bound_shift (a - 9)
  have he : a - 9 + 9 = a := by omega
  have hp : a - 9 + 4 = a - 5 := by omega
  simpa only [he, hp] using h

/-- Every n below 10^k has a k-position ordinary decimal representation.
Leading zero padding is permitted, as in DecimalMass.digitSum_value. -/
private theorem target_bounded_representation (n k : Nat) (hn : n < 10 ^ k) :
    ∃ d : Nat → Nat, (∀ i, i < k → d i ≤ 9) ∧ value d k = n := by
  induction k generalizing n with
  | zero =>
    have hz : n = 0 := by simpa using Nat.eq_zero_of_le_zero (by simpa using hn)
    refine ⟨fun _ => 0, ?_, ?_⟩
    · intro i hi
      omega
    · simp [value, hz]
  | succ k ih =>
    have hquot : n / 10 < 10 ^ k := by
      rw [Nat.pow_succ] at hn
      omega
    obtain ⟨d, hd, hv⟩ := ih (n / 10) hquot
    let e : Nat → Nat := fun i => match i with
      | 0 => n % 10
      | j + 1 => d j
    refine ⟨e, ?_, ?_⟩
    · intro i hi
      cases i with
      | zero =>
        change n % 10 ≤ 9
        omega
      | succ j =>
        exact hd j (by omega)
    · rw [value_shift]
      change n % 10 + 10 * value d k = n
      rw [hv]
      exact Nat.mod_add_div n 10

private theorem target_wordSum_le_nine (d : Nat → Nat) (k : Nat)
    (hd : ∀ i, i < k → d i ≤ 9) : wordSum d k ≤ 9 * k := by
  induction k with
  | zero => simp [wordSum]
  | succ k ih =>
    have hp := ih (fun i hi => hd i (by omega))
    have hk := hd k (by omega)
    simp only [wordSum]
    omega

/-- A value bound on the original decimal digit sum, derived from actual digits. -/
theorem target_digitSum_le_of_lt_pow (n k : Nat) (hn : n < 10 ^ k) :
    digitSum n ≤ 9 * k := by
  obtain ⟨d, hd, hv⟩ := target_bounded_representation n k hn
  rw [← hv, digitSum_value d k hd]
  exact target_wordSum_le_nine d k hd

/-- A separated leading one adds exactly one to the actual digit sum. -/
theorem target_digitSum_pow_add (a n : Nat) (hn : n < 10 ^ a) :
    digitSum (10 ^ a + n) = 1 + digitSum n := by
  obtain ⟨d, hd, hv⟩ := target_bounded_representation n a hn
  let e : Nat → Nat := fun i => if i < a then d i else 1
  have he : ∀ i, i < a → e i = d i := by
    intro i hi
    simp [e, hi]
  have hea : e a = 1 := by simp [e]
  have hb : ∀ i, i < a + 1 → e i ≤ 9 := by
    intro i hi
    by_cases hia : i < a
    · rw [he i hia]
      exact hd i hia
    · simp [e, hia]
  have hval : value e a = n := (value_congr e d a he).trans hv
  have hsum : wordSum e a = wordSum d a := wordSum_congr e d a he
  have hfull : value e (a + 1) = 10 ^ a + n := by
    simp only [value, hea, hval, Nat.one_mul]
    omega
  calc
    digitSum (10 ^ a + n) = digitSum (value e (a + 1)) := by rw [hfull]
    _ = wordSum e (a + 1) := digitSum_value e (a + 1) hb
    _ = wordSum d a + 1 := by rw [wordSum, hea, hsum]
    _ = 1 + digitSum n := by
      rw [← digitSum_value d a hd, hv]
      omega

/-- Uniform sparse-target bound.  This retains the exact constant 44 in the source. -/
theorem sparse_digitSum_bound (a : Nat) (ha : 9 ≤ a) :
    digitSum (sparse a) + 44 ≤ 9 * a := by
  have hr := rho_le a
  have ht := sparse_tail_bound a ha
  have htail : 990 * a + rho a < 10 ^ (a - 5) := by omega
  have hsum := target_digitSum_le_of_lt_pow (990 * a + rho a) (a - 5) htail
  have hpow : 10 ^ (a - 5) ≤ 10 ^ a :=
    Nat.pow_le_pow_right (by decide : 0 < 10) (Nat.sub_le a 5)
  have hsep : 990 * a + rho a < 10 ^ a := Nat.lt_of_lt_of_le htail hpow
  rw [sparse, Nat.add_assoc, target_digitSum_pow_add a (990 * a + rho a) hsep]
  omega

/-- R=3 gives a=8, outside the general a≥9 tail estimate. -/
theorem sparse_eight_digitSum : digitSum (sparse 8) = 27 := by
  change digitSum 100008909 = 27
  simp [digitSum]

#print axioms sparse_tail_bound
#print axioms target_digitSum_le_of_lt_pow
#print axioms target_digitSum_pow_add
#print axioms sparse_digitSum_bound
#print axioms sparse_eight_digitSum

end Agent106.CongruenceBudget
