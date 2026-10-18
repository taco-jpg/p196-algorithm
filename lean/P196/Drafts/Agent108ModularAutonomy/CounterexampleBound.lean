import P196.Drafts.Agent108ModularAutonomy.ModularAutonomy

/-!
A quantitative strengthening: one sufficiently wide exact-width class
already forces the complete modulus classification. All witnesses are
ordinary finite decimal integers with the existing Canonical semantics.
-/
namespace ModularAutonomy

open Lychrel196 DecimalDigits

def ReverseResidueDetAt (M L : Nat) : Prop :=
  ∀ n m (d e : Nat → Nat), Canonical n d L → Canonical m e L →
    n % M = m % M → reverse10 n % M = reverse10 m % M

def StepResidueDetAt (M L : Nat) : Prop :=
  ∀ n m (d e : Nat → Nat), Canonical n d L → Canonical m e L →
    n % M = m % M → step n % M = step m % M

theorem leading_residue_witnesses_at (M L : Nat) (hM : 0 < M)
    (hL : 0 < L) (hsize : M < 10 ^ (L - 1)) :
    ∃ n m, ∃ d e : Nat → Nat,
      Canonical n d L ∧ Canonical m e L ∧ n % M = m % M ∧
      reverse10 n % 10 = 1 ∧ reverse10 m % 10 = 2 := by
  obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : L ≠ 0)
  let P := 10 ^ k
  let n := (P / M + 1) * M
  let m := ((2 * P) / M + 1) * M
  have hlarge : M < P := by
    simpa only [Nat.add_sub_cancel] using hsize
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
  refine ⟨n, m, d, e, hd, he, ?_, ?_, ?_⟩
  · simp [n, m]
  · simpa only [Nat.add_sub_cancel, hlead1] using hr1
  · simpa only [Nat.add_sub_cancel, hlead2] using hr2

theorem at_not_dvd_two (M L : Nat) (hM : 0 < M)
    (hL : 0 < L) (hsize : M < 10 ^ (L - 1))
    (hdet : ReverseResidueDetAt M L) : ¬ 2 ∣ M := by
  intro hdiv
  obtain ⟨n, m, d, e, hn, hm, heq, hr1, hr2⟩ :=
    leading_residue_witnesses_at M L hM hL hsize
  have hrev := hdet n m d e hn hm heq
  have hsmall := congrArg (fun x => x % 2) hrev
  simp only [Nat.mod_mod_of_dvd _ hdiv] at hsmall
  have hfirst := congrArg (fun x => x % 2) hr1
  have hsecond := congrArg (fun x => x % 2) hr2
  simp only [Nat.mod_mod_of_dvd _ (by decide : 2 ∣ 10)] at hfirst hsecond
  omega

theorem at_not_dvd_five (M L : Nat) (hM : 0 < M)
    (hL : 0 < L) (hsize : M < 10 ^ (L - 1))
    (hdet : ReverseResidueDetAt M L) : ¬ 5 ∣ M := by
  intro hdiv
  obtain ⟨n, m, d, e, hn, hm, heq, hr1, hr2⟩ :=
    leading_residue_witnesses_at M L hM hL hsize
  have hrev := hdet n m d e hn hm heq
  have hsmall := congrArg (fun x => x % 5) hrev
  simp only [Nat.mod_mod_of_dvd _ hdiv] at hsmall
  have hfirst := congrArg (fun x => x % 5) hr1
  have hsecond := congrArg (fun x => x % 5) hr2
  simp only [Nat.mod_mod_of_dvd _ (by decide : 5 ∣ 10)] at hfirst hsecond
  omega

theorem at_forces_scaled_99 (M L : Nat) (hM : 0 < M)
    (hL : 3 ≤ L) (hspace : M + 10 < 10 ^ (L - 1))
    (hunit : M % 10 ≠ 0) (hdet : ReverseResidueDetAt M L) :
    M ∣ 99 * 10 ^ (L - 2) := by
  have hpow : 10 ^ (L - 1) = 10 ^ (L - 2) * 10 := by
    have he : L - 1 = (L - 2) + 1 := by omega
    rw [he, Nat.pow_succ]
  have hpowL : 10 ^ L = 10 ^ (L - 1) * 10 := by
    have he : L = (L - 1) + 1 := by omega
    conv => lhs; rw [he, Nat.pow_succ]
  have hpmod : 10 ^ (L - 1) % 10 = 0 := by rw [hpow]; omega
  have hunits : (10 ^ (L - 1) + 9 + M) % 10 ≤ 8 := by omega
  obtain ⟨e, he⟩ := canonical_of_pow_bounds (10 ^ (L - 1) + 9 + M) L
    (by omega) (by omega) (by rw [hpowL]; omega)
  have heplus := canonical_incrementUnits _ _ e he hunits
  have hn := single_nine_canonical L hL
  have hnplus := single_nine_successor_canonical L hL
  have hmod0 : (10 ^ (L - 1) + 9) % M =
      (10 ^ (L - 1) + 9 + M) % M := by simp
  have hmod1 : (10 ^ (L - 1) + 10) % M =
      (10 ^ (L - 1) + 9 + M + 1) % M := by
    have heq : 10 ^ (L - 1) + 9 + M + 1 = 10 ^ (L - 1) + 10 + M := by omega
    rw [heq]
    simp
  have hAC := hdet _ _ _ _ hn he hmod0
  have hBD := hdet _ _ _ _ hnplus heplus hmod1
  have hfirst := single_nine_reverse_increment L hL
  have hsecond := reverse10_succ_of_units_le_eight _ _ e he hunits
  exact scaled_99_of_difference_residues M _ _ _ _ _ _ hM
    hAC hBD hfirst hsecond (by omega)

theorem reverse_residue_det_at_iff (M L : Nat) (hM : 0 < M)
    (hL : 3 ≤ L) (hspace : M + 10 < 10 ^ (L - 1)) :
    ReverseResidueDetAt M L ↔ M ∣ 99 := by
  constructor
  · intro hdet
    have h2 := at_not_dvd_two M L hM (by omega) (by omega) hdet
    have h5 := at_not_dvd_five M L hM (by omega) (by omega) hdet
    have hcop := gcd_ten_eq_one_of_not_two_not_five M h2 h5
    have hunit : M % 10 ≠ 0 := by
      intro hz
      exact h2 (Nat.dvd_trans (by decide : 2 ∣ 10) (Nat.dvd_of_mod_eq_zero hz))
    exact cancel_ten_power_from_scaled_99 M (L - 2) hcop
      (at_forces_scaled_99 M L hM hL hspace hunit hdet)
  · intro hdiv n m d e hn hm heq
    rw [AstraModular.reverse10_mod_of_dvd99 M n d L hdiv hn,
      AstraModular.reverse10_mod_of_dvd99 M m e L hdiv hm,
      Nat.mul_mod _ n, Nat.mul_mod _ m, heq]

theorem step_residue_det_at_iff_reverse (M L : Nat) :
    StepResidueDetAt M L ↔ ReverseResidueDetAt M L := by
  constructor
  · intro hdet n m d e hn hm heq
    have hs := hdet n m d e hn hm heq
    change (n + reverse10 n) % M = (m + reverse10 m) % M at hs
    rw [Nat.add_mod n, Nat.add_mod m, heq] at hs
    have hh := add_mod_left_cancel _ _ _ _ hs
    simpa only [Nat.mod_mod] using hh
  · intro hdet n m d e hn hm heq
    have hr := hdet n m d e hn hm heq
    change (n + reverse10 n) % M = (m + reverse10 m) % M
    rw [Nat.add_mod n, Nat.add_mod m, heq, hr]

theorem step_residue_det_at_iff (M L : Nat) (hM : 0 < M)
    (hL : 3 ≤ L) (hspace : M + 10 < 10 ^ (L - 1)) :
    StepResidueDetAt M L ↔ M ∣ 99 := by
  rw [step_residue_det_at_iff_reverse, reverse_residue_det_at_iff M L hM hL hspace]

theorem step_counterexamples_at_every_large_width (M L : Nat) (hM : 0 < M)
    (hbad : ¬ M ∣ 99) (hL : 3 ≤ L) (hspace : M + 10 < 10 ^ (L - 1)) :
    ∃ n m, ∃ d e : Nat → Nat,
      Canonical n d L ∧ Canonical m e L ∧ n % M = m % M ∧
      step n % M ≠ step m % M := by
  classical
  apply Classical.byContradiction
  intro hnone
  apply hbad
  apply (step_residue_det_at_iff M L hM hL hspace).mp
  intro n m d e hn hm heq
  apply Classical.byContradiction
  intro hne
  exact hnone ⟨n, m, d, e, hn, hm, heq, hne⟩

#print axioms leading_residue_witnesses_at
#print axioms at_not_dvd_two
#print axioms at_not_dvd_five
#print axioms at_forces_scaled_99
#print axioms reverse_residue_det_at_iff
#print axioms step_residue_det_at_iff_reverse
#print axioms step_residue_det_at_iff
#print axioms step_counterexamples_at_every_large_width

end ModularAutonomy
