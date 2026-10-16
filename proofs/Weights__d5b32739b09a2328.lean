import Counting
import Mathlib.Data.Real.Sqrt
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-! Exact real safe incoming-weight obstruction for actual decimal reverse-add.
Source: FINITE_SEED_OBSTRUCTIONS.md section 3. Agent #13.
The full incoming fiber is defined independently of the constructed subfamily. -/

namespace Agent13SafeWeights
open Agent13SafeFamily Lychrel196
open scoped BigOperators

noncomputable section

/-- Every positive predecessor is in this finite set; zero is excluded by Safe. -/
def safeFiber (y : Nat) : Finset Nat := by
  classical
  exact (Finset.range (y+1)).filter (fun n => Safe n ∧ step n = y)

/-- The source's entire safe incoming sum, not only the exhibited family. -/
def incoming (w : Nat → ℝ) (y : Nat) : ℝ := ∑ n ∈ safeFiber y, w n

def PositiveOnSafe (w : Nat → ℝ) : Prop := ∀ n, Safe n → 0 < w n

def AntitoneOnSafe (w : Nat → ℝ) : Prop :=
  ∀ n y, Safe n → Safe y → n ≤ y → w y ≤ w n

/-- Ordinary addition already suffices for the finite search bound. -/
theorem predecessor_le (n y : Nat) (h : step n = y) : n ≤ y := by
  unfold step at h
  omega

/-- Exact membership: the finite encoding omits no actual safe predecessor. -/
theorem mem_safeFiber_iff (n y : Nat) : n ∈ safeFiber y ↔ Safe n ∧ step n = y := by
  classical
  simp only [safeFiber, Finset.mem_filter, Finset.mem_range]
  constructor
  · exact fun h => h.2
  · intro h
    exact ⟨by have := predecessor_le n y h.2; omega, h⟩

theorem full_safe_fiber_finite (y : Nat) : Set.Finite {n | Safe n ∧ step n = y} := by
  have hset : {n | Safe n ∧ step n = y} = (safeFiber y : Set Nat) := by
    ext n
    exact (mem_safeFiber_iff n y).symm
  rw [hset]
  exact Finset.finite_toSet _

theorem incoming_nonneg (w : Nat → ℝ) (hp : PositiveOnSafe w) (y : Nat) :
    0 ≤ incoming w y := by
  apply Finset.sum_nonneg
  intro n hn
  exact (hp n ((mem_safeFiber_iff n y).mp hn).1).le

/-- An injective safe predecessor family contributes a genuine partial sum. -/
theorem family_sum_le_incoming (w : Nat → ℝ) (hp : PositiveOnSafe w)
    (y N : Nat) (f : Fin N → Nat) (hf : Function.Injective f)
    (hpre : ∀ i, Safe (f i) ∧ step (f i) = y) :
    (∑ i, w (f i)) ≤ incoming w y := by
  classical
  have heq : (∑ n ∈ Finset.univ.image f, w n) = ∑ i, w (f i) :=
    Finset.sum_image (fun i _ j _ h => hf h)
  rw [← heq]
  apply Finset.sum_le_sum_of_subset_of_nonneg
  · intro n hn
    obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hn
    exact (mem_safeFiber_iff (f i) y).mpr (hpre i)
  · intro n hn _
    exact (hp n ((mem_safeFiber_iff n y).mp hn).1).le

/-- Finite-sum comparison, with monotonicity assumed only on actual safe seeds. -/
theorem finite_family_weight_lower (w : Nat → ℝ) (hp : PositiveOnSafe w)
    (hm : AntitoneOnSafe w) (y N : Nat) (hy : Safe y)
    (f : Fin N → Nat) (hf : Function.Injective f)
    (hpre : ∀ i, Safe (f i) ∧ step (f i) = y) :
    (N : ℝ) * w y ≤ incoming w y := by
  have hlow : (N : ℝ) * w y ≤ ∑ i, w (f i) := by
    calc
      (N : ℝ) * w y = ∑ _ : Fin N, w y := by simp
      _ ≤ ∑ i, w (f i) := by
        apply Finset.sum_le_sum
        intro i _
        exact hm (f i) y (hpre i).1 hy (predecessor_le (f i) y (hpre i).2)
  exact hlow.trans (family_sum_le_incoming w hp y N f hf hpre)

/-- Original exact multiplication inequality for every width parameter m>=2. -/
theorem incoming_weight_lower (w : Nat → ℝ) (hp : PositiveOnSafe w)
    (ha : AntitoneOnSafe w) (m : Nat) (hm : 2 ≤ m) :
    ((9*10^(m-2) : Nat) : ℝ) * w (10^(2*m)+99*10^(m-1)-1) ≤
      incoming w (10^(2*m)+99*10^(m-1)-1) := by
  obtain ⟨f, hfi, hy, hpre⟩ := safe_predecessor_family m hm
  exact finite_family_weight_lower w hp ha _ _ hy f
    (fun _ _ h => hfi _ _ h) (fun i => ⟨(hpre i).1, (hpre i).2.1⟩)

/-- Original real-valued incoming amplification, with a proved positive divisor. -/
theorem incoming_weight_ratio (w : Nat → ℝ) (hp : PositiveOnSafe w)
    (ha : AntitoneOnSafe w) (m : Nat) (hm : 2 ≤ m) :
    ((9*10^(m-2) : Nat) : ℝ) ≤
      incoming w (10^(2*m)+99*10^(m-1)-1) / w (10^(2*m)+99*10^(m-1)-1) := by
  obtain ⟨_, _, hy, _⟩ := safe_predecessor_family m hm
  exact (le_div_iff₀ (hp _ hy)).mpr (incoming_weight_lower w hp ha m hm)

/-- No finite real multiplier controls the full incoming sum at all safe seeds. -/
theorem no_uniform_multiplier (w : Nat → ℝ) (hp : PositiveOnSafe w)
    (ha : AntitoneOnSafe w) (C : ℝ) :
    ∃ y, Safe y ∧ C * w y < incoming w y := by
  obtain ⟨N, hN⟩ := exists_nat_gt C
  obtain ⟨y, hy, f, hfi, hpre⟩ := safe_fibers_unbounded N
  have hlow := finite_family_weight_lower w hp ha y N hy f
    (fun _ _ h => hfi _ _ h) (fun i => ⟨(hpre i).1, (hpre i).2.1⟩)
  exact ⟨y, hy, (mul_lt_mul_of_pos_right hN (hp y hy)).trans_le hlow⟩

theorem not_exists_uniform_bound (w : Nat → ℝ) (hp : PositiveOnSafe w)
    (ha : AntitoneOnSafe w) :
    ¬ ∃ C : ℝ, ∀ y, Safe y → incoming w y ≤ C * w y := by
  rintro ⟨C, hC⟩
  obtain ⟨y, hy, h⟩ := no_uniform_multiplier w hp ha C
  exact (not_lt_of_ge (hC y hy)) h

end
end Agent13SafeWeights
