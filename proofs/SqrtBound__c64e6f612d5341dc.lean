import Weights

namespace Agent13SafeWeights
open Agent13SafeFamily

/-- Integral form of the source's strict target-size estimate. -/
theorem target_size_bound_nat (m : Nat) (hm : 2 ≤ m) :
    10 * (10^(2*m)+99*10^(m-1)-1) < 11*10^(2*m) := by
  have hpow : 10^3 ≤ 10^(m+1) :=
    Nat.pow_le_pow_right (by decide) (by omega)
  have hmul := Nat.mul_le_mul_left (10^(m-1)) hpow
  have hexp : 10^(m-1)*10^(m+1) = 10^(2*m) := by
    rw [← Nat.pow_add]
    congr 1
    omega
  rw [hexp] at hmul
  norm_num only at hmul
  have hpos : 0 < 10^(m-1) := Nat.pow_pos (by decide)
  omega

/-- Exact real coercion; no floating-point approximation occurs. -/
theorem target_size_bound_real (m : Nat) (hm : 2 ≤ m) :
    ((10^(2*m)+99*10^(m-1)-1 : Nat) : ℝ) < (11/10 : ℝ)*(10 : ℝ)^(2*m) := by
  have h : ((10 * (10^(2*m)+99*10^(m-1)-1) : Nat) : ℝ) <
      ((11*10^(2*m) : Nat) : ℝ) := by
    exact_mod_cast target_size_bound_nat m hm
  push_cast at h
  nlinarith

theorem family_size_scaled_power (m : Nat) (hm : 2 ≤ m) :
    ((9*10^(m-2) : Nat) : ℝ) = (9/100 : ℝ)*(10 : ℝ)^m := by
  have hpow : (10 : ℝ)^m = (10 : ℝ)^(m-2)*100 := by
    calc
      (10 : ℝ)^m = (10 : ℝ)^((m-2)+2) := by congr 1; omega
      _ = (10 : ℝ)^(m-2)*100 := by rw [pow_add]; norm_num
  push_cast
  rw [hpow]
  ring

/-- Strict square-root size comparison for the exact constructed family. -/
theorem sqrt_scale_lt_family_size (m : Nat) (hm : 2 ≤ m) :
    (9/100 : ℝ)*Real.sqrt (10/11)*Real.sqrt ((10^(2*m)+99*10^(m-1)-1 : Nat) : ℝ) <
      ((9*10^(m-2) : Nat) : ℝ) := by
  have hsize := target_size_bound_real m hm
  have hpow : (10 : ℝ)^(2*m) = ((10 : ℝ)^m)^2 := by
    rw [show 2*m = m*2 by omega, pow_mul]
  rw [hpow] at hsize
  have hsq : (10/11 : ℝ)*((10^(2*m)+99*10^(m-1)-1 : Nat) : ℝ) < ((10 : ℝ)^m)^2 := by
    nlinarith
  have hy : (0 : ℝ) ≤ ((10^(2*m)+99*10^(m-1)-1 : Nat) : ℝ) := Nat.cast_nonneg _
  have hp : (0 : ℝ) ≤ (10 : ℝ)^m := pow_nonneg (by norm_num) _
  have hs := (Real.sqrt_lt (mul_nonneg (by norm_num : (0 : ℝ) ≤ 10/11) hy) hp).mpr hsq
  rw [Real.sqrt_mul (by norm_num : (0 : ℝ) ≤ 10/11)] at hs
  have h := mul_lt_mul_of_pos_left hs (by norm_num : (0 : ℝ) < 9/100)
  rw [family_size_scaled_power m hm]
  simpa only [mul_assoc] using h

/-- The original strict quantitative incoming-weight lower bound. -/
theorem incoming_weight_sqrt_lower (w : Nat → ℝ) (hp : PositiveOnSafe w)
    (ha : AntitoneOnSafe w) (m : Nat) (hm : 2 ≤ m) :
    (9/100 : ℝ)*Real.sqrt (10/11)*Real.sqrt ((10^(2*m)+99*10^(m-1)-1 : Nat) : ℝ) <
      incoming w (10^(2*m)+99*10^(m-1)-1) / w (10^(2*m)+99*10^(m-1)-1) := by
  exact (sqrt_scale_lt_family_size m hm).trans_le (incoming_weight_ratio w hp ha m hm)

end Agent13SafeWeights
