import Agent9WindowIntervalCounts
import Mathlib.Topology.Instances.Real.Lemmas
import Mathlib.Order.LiminfLimsup
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-!
# Real lower densities from uniformly occupied finite windows

This module reuses Agent 9's unchanged count of qualifying natural times in
half-open intervals. Both density endpoints are actual real filter liminfs.
The infimum over starting times is taken before the Banach-density liminf.
No existence of an ordinary asymptotic-density limit is asserted.
-/

namespace P196.Agent52.Density

open P196.Agent9.IntervalCounts
open Filter

/-- Real frequency in the natural-time interval `[s,s+N)`; at `N=0` it is zero. -/
noncomputable def intervalDensity (P : Nat → Prop) [DecidablePred P]
    (s N : Nat) : ℝ :=
  (intervalCount P s N : ℝ) / (N : ℝ)

/-- Lower asymptotic density, using initial half-open intervals. -/
noncomputable def lowerAsymptoticDensity (P : Nat → Prop) [DecidablePred P] : ℝ :=
  Filter.liminf (intervalDensity P 0) Filter.atTop

/-- Lower Banach density, using the infimum over all natural starting times. -/
noncomputable def lowerBanachDensity (P : Nat → Prop) [DecidablePred P] : ℝ :=
  Filter.liminf (fun N => iInf (fun s : Nat => intervalDensity P s N)) Filter.atTop

variable (P : Nat → Prop) [DecidablePred P]

@[simp] theorem intervalDensity_zero_length (s : Nat) :
    intervalDensity P s 0 = 0 := by
  simp [intervalDensity]

/-- Every finite interval frequency is nonnegative, including the empty interval. -/
theorem intervalDensity_nonneg (s N : Nat) : 0 ≤ intervalDensity P s N := by
  unfold intervalDensity
  positivity

/-- Filtering cannot count more than the interval length. -/
theorem intervalCount_le_length (s N : Nat) : intervalCount P s N ≤ N := by
  simpa [intervalCount] using
    (List.length_filter_le (fun t => decide (P t)) (List.range' s N))

/-- Every finite interval frequency is at most one. -/
theorem intervalDensity_le_one (s N : Nat) : intervalDensity P s N ≤ 1 := by
  by_cases hN : N = 0
  · simp [hN]
  · have hNr : (0 : ℝ) < N := by exact_mod_cast Nat.pos_of_ne_zero hN
    apply (div_le_iff₀ hNr).2
    simpa only [one_mul] using
      (show (intervalCount P s N : ℝ) ≤ (N : ℝ) by
        exact_mod_cast intervalCount_le_length P s N)

/-- The indexed family has a genuine lower bound, so its real infimum is controlled. -/
theorem intervalDensity_bddBelow (N : Nat) :
    BddBelow (Set.range (fun s : Nat => intervalDensity P s N)) := by
  refine ⟨0, ?_⟩
  rintro x ⟨s, rfl⟩
  exact intervalDensity_nonneg P s N

theorem iInf_intervalDensity_nonneg (N : Nat) :
    0 ≤ iInf (fun s : Nat => intervalDensity P s N) :=
  le_ciInf (fun s => intervalDensity_nonneg P s N)

theorem iInf_intervalDensity_le (s N : Nat) :
    iInf (fun a : Nat => intervalDensity P a N) ≤ intervalDensity P s N :=
  ciInf_le (intervalDensity_bddBelow P N) s

theorem iInf_intervalDensity_le_one (N : Nat) :
    iInf (fun s : Nat => intervalDensity P s N) ≤ 1 :=
  (iInf_intervalDensity_le P 0 N).trans (intervalDensity_le_one P 0 N)

/-- Nonnegativity of the actual lower asymptotic density. -/
theorem lowerAsymptoticDensity_nonneg : 0 ≤ lowerAsymptoticDensity P := by
  apply le_liminf_of_le
    (isCoboundedUnder_ge_of_le atTop (intervalDensity_le_one P 0))
  exact Eventually.of_forall (intervalDensity_nonneg P 0)

/-- The actual lower asymptotic density is at most one. -/
theorem lowerAsymptoticDensity_le_one : lowerAsymptoticDensity P ≤ 1 := by
  exact liminf_le_of_frequently_le
    (Eventually.of_forall (intervalDensity_le_one P 0)).frequently
    (isBoundedUnder_of ⟨0, intervalDensity_nonneg P 0⟩)

/-- Nonnegativity of the actual lower Banach density. -/
theorem lowerBanachDensity_nonneg : 0 ≤ lowerBanachDensity P := by
  apply le_liminf_of_le
    (isCoboundedUnder_ge_of_le atTop (iInf_intervalDensity_le_one P))
  exact Eventually.of_forall (iInf_intervalDensity_nonneg P)

/-- The actual lower Banach density is at most one. -/
theorem lowerBanachDensity_le_one : lowerBanachDensity P ≤ 1 := by
  exact liminf_le_of_frequently_le
    (Eventually.of_forall (iInf_intervalDensity_le_one P)).frequently
    (isBoundedUnder_of ⟨0, iInf_intervalDensity_nonneg P⟩)

/-- Taking all translates before the liminf can only decrease the density. -/
theorem lowerBanachDensity_le_lowerAsymptoticDensity :
    lowerBanachDensity P ≤ lowerAsymptoticDensity P := by
  exact liminf_le_liminf
    (Eventually.of_forall (fun N => iInf_intervalDensity_le P 0 N))
    (isBoundedUnder_of ⟨0, iInf_intervalDensity_nonneg P⟩)
    (isCoboundedUnder_ge_of_le atTop (intervalDensity_le_one P 0))

/-- Real finite-length consequence of Agent 9's exact complete-block count. -/
theorem count_intervalDensity_lower_bound
    (H : Nat) (hH : 0 < H)
    (hc : ∀ s N, N / H ≤ intervalCount P s N)
    (s N : Nat) (hN : 0 < N) :
    1 / (H : ℝ) - 1 / (N : ℝ) ≤ intervalDensity P s N := by
  have hHr : (0 : ℝ) < H := by exact_mod_cast hH
  have hNr : (0 : ℝ) < N := by exact_mod_cast hN
  have hcount : ((N / H : Nat) : ℝ) ≤ (intervalCount P s N : ℝ) := by
    exact_mod_cast hc s N
  have hd : (H : ℝ) * ((N / H : Nat) : ℝ) + ((N % H : Nat) : ℝ) = N := by
    exact_mod_cast Nat.div_add_mod N H
  have hr : ((N % H : Nat) : ℝ) < H := by
    exact_mod_cast Nat.mod_lt N hH
  have hn : (N : ℝ) ≤ ((intervalCount P s N : ℝ) + 1) * (H : ℝ) := by
    nlinarith
  have hq : (N : ℝ) / (H : ℝ) ≤ (intervalCount P s N : ℝ) + 1 :=
    (div_le_iff₀ hHr).2 hn
  unfold intervalDensity
  apply (le_div_iff₀ hNr).2
  simp only [sub_mul, div_mul_eq_mul_div₀, one_mul, div_self (ne_of_gt hNr)]
  linarith

/-- One threshold works for every interval start: the error tends uniformly to zero. -/
theorem count_intervalDensity_eventually_lower_bound
    (H : Nat) (hH : 0 < H)
    (hc : ∀ s N, N / H ≤ intervalCount P s N)
    (ε : ℝ) (hε : 0 < ε) :
    ∃ N₀ : Nat, ∀ N ≥ N₀, ∀ s : Nat,
      1 / (H : ℝ) - ε ≤ intervalDensity P s N := by
  obtain ⟨n, hn⟩ := exists_nat_one_div_lt hε
  refine ⟨n + 1, ?_⟩
  intro N hN s
  have hNp : 0 < N := lt_of_lt_of_le (Nat.succ_pos n) hN
  have hnpos : (0 : ℝ) < (n : ℝ) + 1 := by positivity
  have hcast : (n : ℝ) + 1 ≤ (N : ℝ) := by exact_mod_cast hN
  have hinv : 1 / (N : ℝ) ≤ 1 / ((n : ℝ) + 1) :=
    one_div_le_one_div_of_le hnpos hcast
  have hfinite := count_intervalDensity_lower_bound P H hH hc s N hNp
  linarith

/-- Exact complete-block counts force a positive real lower Banach density. -/
theorem count_lowerBanachDensity
    (H : Nat) (hH : 0 < H)
    (hc : ∀ s N, N / H ≤ intervalCount P s N) :
    1 / (H : ℝ) ≤ lowerBanachDensity P := by
  apply (le_liminf_iff'
    (isCoboundedUnder_ge_of_le atTop (iInf_intervalDensity_le_one P))
    (isBoundedUnder_of ⟨0, iInf_intervalDensity_nonneg P⟩)).2
  intro y hy
  obtain ⟨N₀, hN₀⟩ := count_intervalDensity_eventually_lower_bound P H hH hc
    (1 / (H : ℝ) - y) (sub_pos.mpr hy)
  apply eventually_atTop.2
  refine ⟨N₀, ?_⟩
  intro N hN
  apply le_ciInf
  intro s
  have h := hN₀ N hN s
  linarith

/-- Exact complete-block counts force a positive real lower asymptotic density. -/
theorem count_lowerAsymptoticDensity
    (H : Nat) (hH : 0 < H)
    (hc : ∀ s N, N / H ≤ intervalCount P s N) :
    1 / (H : ℝ) ≤ lowerAsymptoticDensity P :=
  (count_lowerBanachDensity P H hH hc).trans
    (lowerBanachDensity_le_lowerAsymptoticDensity P)

/-- The uniform-window hypothesis supplies the exact finite-count premise. -/
theorem window_intervalDensity_lower_bound
    (H : Nat) (hH : 0 < H)
    (hw : ∀ a, ∃ t, a ≤ t ∧ t < a + H ∧ P t)
    (s N : Nat) (hN : 0 < N) :
    1 / (H : ℝ) - 1 / (N : ℝ) ≤ intervalDensity P s N :=
  count_intervalDensity_lower_bound P H hH
    (window_property_interval_count P H hH hw) s N hN

/-- The same length threshold controls every translate of an occupied window. -/
theorem window_intervalDensity_eventually_lower_bound
    (H : Nat) (hH : 0 < H)
    (hw : ∀ a, ∃ t, a ≤ t ∧ t < a + H ∧ P t)
    (ε : ℝ) (hε : 0 < ε) :
    ∃ N₀ : Nat, ∀ N ≥ N₀, ∀ s : Nat,
      1 / (H : ℝ) - ε ≤ intervalDensity P s N :=
  count_intervalDensity_eventually_lower_bound P H hH
    (window_property_interval_count P H hH hw) ε hε

/-- Uniformly occupied windows force a positive real lower Banach density. -/
theorem window_lowerBanachDensity
    (H : Nat) (hH : 0 < H)
    (hw : ∀ a, ∃ t, a ≤ t ∧ t < a + H ∧ P t) :
    1 / (H : ℝ) ≤ lowerBanachDensity P :=
  count_lowerBanachDensity P H hH (window_property_interval_count P H hH hw)

/-- Uniformly occupied windows force a positive real lower asymptotic density. -/
theorem window_lowerAsymptoticDensity
    (H : Nat) (hH : 0 < H)
    (hw : ∀ a, ∃ t, a ≤ t ∧ t < a + H ∧ P t) :
    1 / (H : ℝ) ≤ lowerAsymptoticDensity P :=
  count_lowerAsymptoticDensity P H hH (window_property_interval_count P H hH hw)

#print axioms intervalDensity_zero_length
#print axioms intervalDensity_nonneg
#print axioms intervalCount_le_length
#print axioms intervalDensity_le_one
#print axioms intervalDensity_bddBelow
#print axioms iInf_intervalDensity_nonneg
#print axioms iInf_intervalDensity_le
#print axioms iInf_intervalDensity_le_one
#print axioms lowerAsymptoticDensity_nonneg
#print axioms lowerAsymptoticDensity_le_one
#print axioms lowerBanachDensity_nonneg
#print axioms lowerBanachDensity_le_one
#print axioms lowerBanachDensity_le_lowerAsymptoticDensity
#print axioms count_intervalDensity_lower_bound
#print axioms count_intervalDensity_eventually_lower_bound
#print axioms count_lowerBanachDensity
#print axioms count_lowerAsymptoticDensity
#print axioms window_intervalDensity_lower_bound
#print axioms window_intervalDensity_eventually_lower_bound
#print axioms window_lowerBanachDensity
#print axioms window_lowerAsymptoticDensity

end P196.Agent52.Density
