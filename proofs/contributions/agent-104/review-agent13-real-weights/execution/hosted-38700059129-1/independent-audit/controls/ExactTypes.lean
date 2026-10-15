import SqrtBound

/-! Exact source statements applied to all explicit arguments.
Independent review harness; compilation pending the pinned executor. -/
namespace Agent104.RealWeightsExactTypes
open Agent13SafeFamily Agent13SafeWeights Lychrel196
open scoped BigOperators

theorem predecessor_le_type (n y : Nat) (h : step n = y) : n ≤ y :=
  Agent13SafeWeights.predecessor_le n y h

theorem mem_safeFiber_iff_type (n y : Nat) : n ∈ safeFiber y ↔ Safe n ∧ step n = y :=
  Agent13SafeWeights.mem_safeFiber_iff n y

theorem full_safe_fiber_finite_type (y : Nat) : Set.Finite {n | Safe n ∧ step n = y} :=
  Agent13SafeWeights.full_safe_fiber_finite y

theorem incoming_nonneg_type (w : Nat → ℝ) (hp : PositiveOnSafe w) (y : Nat) :
    0 ≤ incoming w y :=
  Agent13SafeWeights.incoming_nonneg w hp y

theorem family_sum_le_incoming_type (w : Nat → ℝ) (hp : PositiveOnSafe w)
    (y N : Nat) (f : Fin N → Nat) (hf : Function.Injective f)
    (hpre : ∀ i, Safe (f i) ∧ step (f i) = y) :
    (∑ i, w (f i)) ≤ incoming w y :=
  Agent13SafeWeights.family_sum_le_incoming w hp y N f hf hpre

theorem finite_family_weight_lower_type (w : Nat → ℝ) (hp : PositiveOnSafe w)
    (hm : AntitoneOnSafe w) (y N : Nat) (hy : Safe y)
    (f : Fin N → Nat) (hf : Function.Injective f)
    (hpre : ∀ i, Safe (f i) ∧ step (f i) = y) :
    (N : ℝ) * w y ≤ incoming w y :=
  Agent13SafeWeights.finite_family_weight_lower w hp hm y N hy f hf hpre

theorem incoming_weight_lower_type (w : Nat → ℝ) (hp : PositiveOnSafe w)
    (ha : AntitoneOnSafe w) (m : Nat) (hm : 2 ≤ m) :
    ((9*10^(m-2) : Nat) : ℝ) * w (10^(2*m)+99*10^(m-1)-1) ≤
      incoming w (10^(2*m)+99*10^(m-1)-1) :=
  Agent13SafeWeights.incoming_weight_lower w hp ha m hm

theorem incoming_weight_ratio_type (w : Nat → ℝ) (hp : PositiveOnSafe w)
    (ha : AntitoneOnSafe w) (m : Nat) (hm : 2 ≤ m) :
    ((9*10^(m-2) : Nat) : ℝ) ≤
      incoming w (10^(2*m)+99*10^(m-1)-1) / w (10^(2*m)+99*10^(m-1)-1) :=
  Agent13SafeWeights.incoming_weight_ratio w hp ha m hm

theorem no_uniform_multiplier_type (w : Nat → ℝ) (hp : PositiveOnSafe w)
    (ha : AntitoneOnSafe w) (C : ℝ) :
    ∃ y, Safe y ∧ C * w y < incoming w y :=
  Agent13SafeWeights.no_uniform_multiplier w hp ha C

theorem not_exists_uniform_bound_type (w : Nat → ℝ) (hp : PositiveOnSafe w)
    (ha : AntitoneOnSafe w) :
    ¬ ∃ C : ℝ, ∀ y, Safe y → incoming w y ≤ C * w y :=
  Agent13SafeWeights.not_exists_uniform_bound w hp ha

theorem target_size_bound_nat_type (m : Nat) (hm : 2 ≤ m) :
    10 * (10^(2*m)+99*10^(m-1)-1) < 11*10^(2*m) :=
  Agent13SafeWeights.target_size_bound_nat m hm

theorem target_size_bound_real_type (m : Nat) (hm : 2 ≤ m) :
    ((10^(2*m)+99*10^(m-1)-1 : Nat) : ℝ) < (11/10 : ℝ)*(10 : ℝ)^(2*m) :=
  Agent13SafeWeights.target_size_bound_real m hm

theorem family_size_scaled_power_type (m : Nat) (hm : 2 ≤ m) :
    ((9*10^(m-2) : Nat) : ℝ) = (9/100 : ℝ)*(10 : ℝ)^m :=
  Agent13SafeWeights.family_size_scaled_power m hm

theorem sqrt_scale_lt_family_size_type (m : Nat) (hm : 2 ≤ m) :
    (9/100 : ℝ)*Real.sqrt (10/11)*Real.sqrt ((10^(2*m)+99*10^(m-1)-1 : Nat) : ℝ) <
      ((9*10^(m-2) : Nat) : ℝ) :=
  Agent13SafeWeights.sqrt_scale_lt_family_size m hm

theorem incoming_weight_sqrt_lower_type (w : Nat → ℝ) (hp : PositiveOnSafe w)
    (ha : AntitoneOnSafe w) (m : Nat) (hm : 2 ≤ m) :
    (9/100 : ℝ)*Real.sqrt (10/11)*Real.sqrt ((10^(2*m)+99*10^(m-1)-1 : Nat) : ℝ) <
      incoming w (10^(2*m)+99*10^(m-1)-1) / w (10^(2*m)+99*10^(m-1)-1) :=
  Agent13SafeWeights.incoming_weight_sqrt_lower w hp ha m hm

end Agent104.RealWeightsExactTypes
