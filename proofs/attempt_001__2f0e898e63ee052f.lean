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

end ModularAutonomy
