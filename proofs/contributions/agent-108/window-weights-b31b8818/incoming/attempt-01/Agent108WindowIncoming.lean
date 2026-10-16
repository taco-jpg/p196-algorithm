import Agent108WindowEmbedding
import Agent108WindowFamilyRatio
import Mathlib.Algebra.BigOperators.Fin

/-!
Agent #108, session b31b8818. Actual finite-window incoming obstruction.

The state space, safe incoming fiber, arithmetic transition, and selected
predecessor inclusion are the original Agent13ProductWeights definitions
from commit 12a32789056f5eec8247166564ac2ef745c3c9d6. This module assigns
literal complete (b+1)-window weights to their finite half-words and applies
the proved long-buffer embedding and exact window-family total.

The width factor is arbitrary and positive at positive even widths. Odd
safe states have an arbitrary positive extension. The lower bound uses
the original full incoming fiber, including all admissible source widths.
-/

namespace Agent108.WindowWeights

open Agent13ProductWeights
open scoped BigOperators

/-- Complete consecutive windows of the finite half-word at even width,
with an arbitrary extension at odd width. -/
noncomputable def finiteWindowWeight (b : Nat) (A : Nat → ℝ)
    (psi : List Nat → ℝ) (oddWeight : FiniteWord → ℝ) (s : FiniteWord) : ℝ :=
  if s.1 % 2 = 0 then A s.1 * windowProduct b psi (finiteStateHalf s)
  else oddWeight s

theorem finiteStateHalf_bounded (s : FiniteWord) :
    ∀ x ∈ finiteStateHalf s, x ≤ 18 := by
  intro x hx
  obtain ⟨i, _, rfl⟩ := List.mem_map.mp hx
  exact digits_bounded s i

/-- Positivity requires the potential only on legal windows of length b+1. -/
theorem finiteWindowWeight_pos (b : Nat) (A : Nat → ℝ)
    (psi : List Nat → ℝ) (oddWeight : FiniteWord → ℝ)
    (hA : ∀ L, 0 < L → L % 2 = 0 → 0 < A L)
    (hp : PositivePotential b psi)
    (ho : ∀ s, SafeState s → s.1 % 2 ≠ 0 → 0 < oddWeight s)
    (s : FiniteWord) (hs : SafeState s) :
    0 < finiteWindowWeight b A psi oddWeight s := by
  unfold finiteWindowWeight
  split
  · exact mul_pos (hA _ hs.1.1 ‹_›)
      (windowProduct_pos hp _ (finiteStateHalf_bounded s))
  · exact ho s hs ‹_›

/-- Specialize the original partial-sum inclusion to positive window weights. -/
theorem finiteWindowWeight_partial_sum_le_incoming {ι : Type} [Fintype ι]
    (b : Nat) (A : Nat → ℝ) (psi : List Nat → ℝ) (oddWeight : FiniteWord → ℝ)
    (hA : ∀ L, 0 < L → L % 2 = 0 → 0 < A L)
    (hp : PositivePotential b psi)
    (ho : ∀ s, SafeState s → s.1 % 2 ≠ 0 → 0 < oddWeight s)
    (t : FiniteWord) (f : ι → FiniteWord) (hf : Function.Injective f)
    (hm : ∀ i, SafeState (f i) ∧ MapsTo (f i) t) :
    (∑ i, finiteWindowWeight b A psi oddWeight (f i)) ≤
      incoming (finiteWindowWeight b A psi oddWeight) t := by
  exact partial_sum_le_incoming (finiteWindowWeight b A psi oddWeight)
    (fun s hs => (finiteWindowWeight_pos b A psi oddWeight hA hp ho s hs).le)
    t f hf hm

/-- Read a listed binary choice on its proved exact finite domain. -/
def choiceBits (r : Nat) (i : Fin (choices r).length) : Fin r → Bool :=
  fun j => bitsFromList ((choices r).get i) j.val

private theorem ofFn_bitsFromList (es : List Bool) (r : Nat) (hr : es.length = r) :
    List.ofFn (fun j : Fin r => bitsFromList es j.val) = es := by
  subst r
  calc
    List.ofFn (fun j : Fin es.length => bitsFromList es j.val) =
        List.ofFn es.get := by
      congr 1
      funext j
      simp [bitsFromList, List.getElem?_eq_getElem j.isLt]
    _ = es := List.ofFn_get es

theorem choiceBits_ofFn (r : Nat) (i : Fin (choices r).length) :
    List.ofFn (choiceBits r i) = (choices r).get i := by
  exact ofFn_bitsFromList _ r (choices_mem_length r (List.get_mem _ i))

theorem choiceBits_injective (r : Nat) : Function.Injective (choiceBits r) := by
  intro i j hij
  apply (choices_nodup r).get_inj_iff.mp
  calc
    (choices r).get i = List.ofFn (choiceBits r i) := (choiceBits_ofFn r i).symm
    _ = List.ofFn (choiceBits r j) := congrArg List.ofFn hij
    _ = (choices r).get j := choiceBits_ofFn r j

private theorem sum_choices_get (r : Nat) (f : List Bool → ℝ) :
    (∑ i : Fin (choices r).length, f ((choices r).get i)) =
      ((choices r).map f).sum := by
  rw [← Fin.sum_ofFn, ← List.map_ofFn, List.ofFn_get]

theorem embeddedState_window_weight (b p k r : Nat) (A : Nat → ℝ)
    (psi : List Nat → ℝ) (oddWeight : FiniteWord → ℝ) (e : Fin r → Bool) :
    finiteWindowWeight b A psi oddWeight (embeddedState p k r e) =
      A (embeddedTarget p k r).1 *
        windowProduct b psi (inputHalf (4*p) k (List.ofFn e)) := by
  have he : (embeddedState p k r e).1 % 2 = 0 := by
    rw [embeddedState_width]
    omega
  simp only [finiteWindowWeight, he, if_true, embedded_width_eq, embeddedState_half]

theorem embeddedTarget_window_weight (b p k r : Nat) (A : Nat → ℝ)
    (psi : List Nat → ℝ) (oddWeight : FiniteWord → ℝ) :
    finiteWindowWeight b A psi oddWeight (embeddedTarget p k r) =
      A (embeddedTarget p k r).1 * windowProduct b psi (targetHalf (4*p) k r) := by
  have he : (embeddedTarget p k r).1 % 2 = 0 := by
    rw [embeddedTarget_width]
    omega
  simp only [finiteWindowWeight, he, if_true, embeddedTarget_half]

/-- The finite enumeration has no repetitions and carries the literal list sum. -/
theorem embedded_choice_weight_sum (b p k r : Nat) (A : Nat → ℝ)
    (psi : List Nat → ℝ) (oddWeight : FiniteWord → ℝ) :
    (∑ i : Fin (choices r).length,
      finiteWindowWeight b A psi oddWeight (embeddedState p k r (choiceBits r i))) =
      A (embeddedTarget p k r).1 *
        ((choices r).map (fun es => windowProduct b psi (inputHalf (4*p) k es))).sum := by
  calc
    _ = ∑ i : Fin (choices r).length,
        A (embeddedTarget p k r).1 *
          windowProduct b psi (inputHalf (4*p) k ((choices r).get i)) := by
      apply Finset.sum_congr rfl
      intro i _
      rw [embeddedState_window_weight, choiceBits_ofFn]
    _ = _ := by rw [← Finset.mul_sum, sum_choices_get]

/-- Every selected state contributes to the original full safe incoming fiber. -/
theorem embedded_window_family_le_incoming (b p k r : Nat) (A : Nat → ℝ)
    (psi : List Nat → ℝ) (oddWeight : FiniteWord → ℝ)
    (hA : ∀ L, 0 < L → L % 2 = 0 → 0 < A L)
    (hp : PositivePotential b psi)
    (ho : ∀ s, SafeState s → s.1 % 2 ≠ 0 → 0 < oddWeight s) (hk : 0 < k) :
    (∑ i : Fin (choices r).length,
      finiteWindowWeight b A psi oddWeight (embeddedState p k r (choiceBits r i))) ≤
      incoming (finiteWindowWeight b A psi oddWeight) (embeddedTarget p k r) := by
  exact finiteWindowWeight_partial_sum_le_incoming b A psi oddWeight hA hp ho
    (embeddedTarget p k r) (fun i => embeddedState p k r (choiceBits r i))
    ((embeddedState_injective p k r).comp (choiceBits_injective r))
    (fun i => embeddedState_spec p k r (choiceBits r i) hk)

/-- Exact total on the actual long-buffer family, with its arbitrary common
width factor incorporated into the target weight. -/
theorem actual_window_family_total (b k r : Nat) (A : Nat → ℝ)
    (psi : List Nat → ℝ) (oddWeight : FiniteWord → ℝ) (hp : PositivePotential b psi) :
    (∑ i : Fin (choices r).length,
      finiteWindowWeight b A psi oddWeight
        (embeddedState (b+1) k r (choiceBits r i))) =
      endpointConstant b k psi *
        finiteWindowWeight b A psi oddWeight (embeddedTarget (b+1) k r) *
          (1 + localBeta b psi)^r := by
  rw [embedded_choice_weight_sum, embeddedTarget_window_weight]
  have hb : 4*(b+1) = b+(3*b+4) := by omega
  rw [hb, inputHalf_exact_total b (3*b+4) k r psi hp]
  ring

/-- A proved geometric lower bound for the original actual incoming operator. -/
theorem incoming_window_lower_bound (b : Nat) (A : Nat → ℝ)
    (psi : List Nat → ℝ) (oddWeight : FiniteWord → ℝ)
    (hA : ∀ L, 0 < L → L % 2 = 0 → 0 < A L)
    (hp : PositivePotential b psi)
    (ho : ∀ s, SafeState s → s.1 % 2 ≠ 0 → 0 < oddWeight s)
    (r k : Nat) (hk : 0 < k) :
    endpointConstant b k psi *
      finiteWindowWeight b A psi oddWeight (embeddedTarget (b+1) k r) *
        (1 + localBeta b psi)^r ≤
      incoming (finiteWindowWeight b A psi oddWeight) (embeddedTarget (b+1) k r) := by
  rw [← actual_window_family_total b k r A psi oddWeight hp]
  exact embedded_window_family_le_incoming b (b+1) k r A psi oddWeight hA hp ho hk

/-- The arbitrary width-only factor cancels in the actual incoming ratio. -/
theorem incoming_window_ratio (b : Nat) (A : Nat → ℝ)
    (psi : List Nat → ℝ) (oddWeight : FiniteWord → ℝ)
    (hA : ∀ L, 0 < L → L % 2 = 0 → 0 < A L)
    (hp : PositivePotential b psi)
    (ho : ∀ s, SafeState s → s.1 % 2 ≠ 0 → 0 < oddWeight s)
    (r k : Nat) (hk : 0 < k) :
    endpointConstant b k psi * (1 + localBeta b psi)^r ≤
      incoming (finiteWindowWeight b A psi oddWeight) (embeddedTarget (b+1) k r) /
        finiteWindowWeight b A psi oddWeight (embeddedTarget (b+1) k r) := by
  have ht := finiteWindowWeight_pos b A psi oddWeight hA hp ho _
    (embeddedTarget_safe (b+1) k r hk)
  apply (le_div_iff₀ ht).2
  calc
    _ = endpointConstant b k psi *
        finiteWindowWeight b A psi oddWeight (embeddedTarget (b+1) k r) *
          (1 + localBeta b psi)^r := by ring
    _ ≤ _ := incoming_window_lower_bound b A psi oddWeight hA hp ho r k hk

/-- Every real proposed multiplier is violated at an actual safe target. -/
theorem no_uniform_window_multiplier (b : Nat) (A : Nat → ℝ)
    (psi : List Nat → ℝ) (oddWeight : FiniteWord → ℝ)
    (hA : ∀ L, 0 < L → L % 2 = 0 → 0 < A L)
    (hp : PositivePotential b psi)
    (ho : ∀ s, SafeState s → s.1 % 2 ≠ 0 → 0 < oddWeight s) (K : ℝ) :
    ∃ t, SafeState t ∧ K * finiteWindowWeight b A psi oddWeight t <
      incoming (finiteWindowWeight b A psi oddWeight) t := by
  obtain ⟨r, hr⟩ := incoming_exceeds_every_constant
    (endpointConstant b 1 psi) (localBeta b psi)
    (endpoint_constant_pos b 1 psi hp) (localBeta_pos b psi hp)
    (fun r => finiteWindowWeight b A psi oddWeight (embeddedTarget (b+1) 1 r))
    (fun r => incoming (finiteWindowWeight b A psi oddWeight) (embeddedTarget (b+1) 1 r))
    (fun r => finiteWindowWeight_pos b A psi oddWeight hA hp ho _
      (embeddedTarget_safe (b+1) 1 r (by omega)))
    (fun r => incoming_window_lower_bound b A psi oddWeight hA hp ho r 1 (by omega)) K
  exact ⟨embeddedTarget (b+1) 1 r, embeddedTarget_safe (b+1) 1 r (by omega), hr⟩

/-- No finite real uniform incoming multiplier exists for positive finite-window
weights on the full original actual folded safe state space. -/
theorem not_exists_uniform_window_bound (b : Nat) (A : Nat → ℝ)
    (psi : List Nat → ℝ) (oddWeight : FiniteWord → ℝ)
    (hA : ∀ L, 0 < L → L % 2 = 0 → 0 < A L)
    (hp : PositivePotential b psi)
    (ho : ∀ s, SafeState s → s.1 % 2 ≠ 0 → 0 < oddWeight s) :
    ¬ ∃ K : ℝ, ∀ t, SafeState t →
      incoming (finiteWindowWeight b A psi oddWeight) t ≤
        K * finiteWindowWeight b A psi oddWeight t := by
  rintro ⟨K, hK⟩
  obtain ⟨t, ht, hgt⟩ := no_uniform_window_multiplier b A psi oddWeight hA hp ho K
  exact (not_lt_of_ge (hK t ht)) hgt

end Agent108.WindowWeights
