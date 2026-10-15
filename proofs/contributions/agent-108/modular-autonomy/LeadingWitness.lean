import AutonomyDefs

/-!
Exact-width interval witnesses for the necessary coprimality obstruction.
The integer witnesses are constructed, not assumed to exist.
-/
namespace ModularAutonomy

open Lychrel196 DecimalDigits

theorem value_lt_pow (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i ≤ 9) : value d L < 10 ^ L := by
  induction L with
  | zero => simp [value]
  | succ L ih =>
    have hprev := ih (fun i hi => hd i (by omega))
    have htop := Nat.mul_le_mul_right (10 ^ L) (hd L (by omega))
    simp only [value, Nat.pow_succ]
    omega

theorem canonical_pow_bounds (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) : 10 ^ (L - 1) ≤ n ∧ n < 10 ^ L := by
  have hupper := value_lt_pow d L hc.2.1
  have hL := hc.1
  have hlead := hc.2.2.1
  have hv := hc.2.2.2
  constructor
  · obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : L ≠ 0)
    have hmul := Nat.mul_le_mul_right (10 ^ k) (show 1 ≤ d k by simpa using hlead)
    simp only [Nat.one_mul] at hmul
    simp only [value] at hv
    simpa only [Nat.add_sub_cancel] using (show 10 ^ k ≤ n by omega)
  · omega

theorem canonical_of_pow_bounds (n L : Nat) (hL : 0 < L)
    (hlo : 10 ^ (L - 1) ≤ n) (hhi : n < 10 ^ L) :
    ∃ d, Canonical n d L := by
  have hp : 0 < 10 ^ (L - 1) := Nat.pow_pos (by decide)
  obtain ⟨d, K, hc⟩ := canonical_exists n (by omega)
  have hb := canonical_pow_bounds n d K hc
  have hK := hc.1
  have hpow1 : 10 ^ (L - 1) < 10 ^ K := by omega
  have hpow2 : 10 ^ (K - 1) < 10 ^ L := by omega
  have he1 := (Nat.pow_lt_pow_iff_right (by decide : 1 < 10)).mp hpow1
  have he2 := (Nat.pow_lt_pow_iff_right (by decide : 1 < 10)).mp hpow2
  have heq : K = L := by omega
  subst K
  exact ⟨d, hc⟩

theorem canonical_lead_of_interval (n k a : Nat) (d : Nat → Nat)
    (hc : Canonical n d (k + 1))
    (hlo : a * 10 ^ k ≤ n) (hhi : n < (a + 1) * 10 ^ k) : d k = a := by
  have hrest := value_lt_pow d k (fun i hi => hc.2.1 i (by omega))
  have hv := hc.2.2.2
  simp only [value] at hv
  by_cases he : d k = a
  · exact he
  · have hcases : d k < a ∨ a < d k := by omega
    rcases hcases with hlow | hhigh
    · have hm := Nat.mul_le_mul_right (10 ^ k) (show d k + 1 ≤ a by omega)
      simp only [Nat.add_mul, Nat.one_mul] at hm
      omega
    · have hm := Nat.mul_le_mul_right (10 ^ k) (show a + 1 ≤ d k by omega)
      omega

/-- Every residue modulus admits arbitrarily wide, equally congruent inputs
whose ordinary reversals have distinct units digits one and two. -/
theorem leading_residue_witnesses (M B : Nat) (hM : 0 < M) :
    ∃ L n m, ∃ d e : Nat → Nat, B ≤ L ∧
      Canonical n d L ∧ Canonical m e L ∧ n % M = m % M ∧
      reverse10 n % 10 = 1 ∧ reverse10 m % 10 = 2 := by
  let k := B + M
  let P := 10 ^ k
  let n := (P / M + 1) * M
  let m := ((2 * P) / M + 1) * M
  have hlarge : M < P := by
    have hp : k < 10 ^ k := Nat.lt_pow_self (by decide)
    dsimp [P, k] at *
    omega
  have hmod1 := Nat.mod_lt P hM
  have hmod2 := Nat.mod_lt (2 * P) hM
  have hdiv1 : P % M + (P / M) * M = P := by
    simpa only [Nat.mul_comm] using Nat.mod_add_div P M
  have hdiv2 : (2 * P) % M + ((2 * P) / M) * M = 2 * P := by
    simpa only [Nat.mul_comm] using Nat.mod_add_div (2 * P) M
  have hn : P ≤ n ∧ n < 2 * P := by
    dsimp [n]
    simp only [Nat.add_mul, Nat.one_mul]
    omega
  have hm : 2 * P ≤ m ∧ m < 3 * P := by
    dsimp [m]
    simp only [Nat.add_mul, Nat.one_mul]
    omega
  obtain ⟨d, hd⟩ := canonical_of_pow_bounds n (k + 1) (by omega)
    (by simpa only [Nat.add_sub_cancel] using hn.1)
    (by rw [Nat.pow_succ]; change n < P * 10; omega)
  obtain ⟨e, he⟩ := canonical_of_pow_bounds m (k + 1) (by omega)
    (by simp only [Nat.add_sub_cancel]; change P ≤ m; omega)
    (by rw [Nat.pow_succ]; change m < P * 10; omega)
  have hlead1 := canonical_lead_of_interval n k 1 d hd (by simpa using hn.1) hn.2
  have hlead2 := canonical_lead_of_interval m k 2 e he hm.1 hm.2
  have hr1 := AstraModular.reverse10_mod10 n d (k + 1) hd
  have hr2 := AstraModular.reverse10_mod10 m e (k + 1) he
  refine ⟨k + 1, n, m, d, e, ?_, hd, he, ?_, ?_, ?_⟩
  · dsimp [k]; omega
  · simp [n, m]
  · simpa only [Nat.add_sub_cancel, hlead1] using hr1
  · simpa only [Nat.add_sub_cancel, hlead2] using hr2

theorem eventual_reverse_not_dvd_two (M : Nat) (hM : 0 < M)
    (hdet : EventualReverseResidueDet M) : ¬ 2 ∣ M := by
  intro hdiv
  obtain ⟨B, hB⟩ := hdet
  obtain ⟨L, n, m, d, e, hL, hn, hm, heq, hr1, hr2⟩ :=
    leading_residue_witnesses M B hM
  have hrev := hB L hL n m d e hn hm heq
  have hsmall := congrArg (fun x => x % 2) hrev
  simp only [Nat.mod_mod_of_dvd _ hdiv] at hsmall
  have hfirst := congrArg (fun x => x % 2) hr1
  have hsecond := congrArg (fun x => x % 2) hr2
  simp only [Nat.mod_mod_of_dvd _ (by decide : 2 ∣ 10)] at hfirst hsecond
  omega

theorem eventual_reverse_not_dvd_five (M : Nat) (hM : 0 < M)
    (hdet : EventualReverseResidueDet M) : ¬ 5 ∣ M := by
  intro hdiv
  obtain ⟨B, hB⟩ := hdet
  obtain ⟨L, n, m, d, e, hL, hn, hm, heq, hr1, hr2⟩ :=
    leading_residue_witnesses M B hM
  have hrev := hB L hL n m d e hn hm heq
  have hsmall := congrArg (fun x => x % 5) hrev
  simp only [Nat.mod_mod_of_dvd _ hdiv] at hsmall
  have hfirst := congrArg (fun x => x % 5) hr1
  have hsecond := congrArg (fun x => x % 5) hr2
  simp only [Nat.mod_mod_of_dvd _ (by decide : 5 ∣ 10)] at hfirst hsecond
  omega

end ModularAutonomy
