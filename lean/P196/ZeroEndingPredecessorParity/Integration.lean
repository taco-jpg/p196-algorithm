import P196.ZeroEndingPredecessorParity.FiniteInvolution
import P196.ZeroEndingPredecessorParity.Reversal
import P196.Agent105AllPredecessors.Agent105Predecessors9df76b

set_option autoImplicit false

/-!
# Parity of complete predecessor fibers for targets ending in zero

Agent #6: ordinary decimal reversal acts as an involution on the existing
complete positive predecessor list when the target ends in zero. Its only
possible fixed point is half of the target. The fiber therefore has odd
cardinality exactly when that half is a palindrome. All source widths are
included through the imported complete predecessor enumeration. This is
a one-step counting result, not an orbit or Lychrel assertion.
-/

namespace ZeroEndingPredecessorParity

open Lychrel196 DecimalDigits Agent105Predecessors9df76b

/-- The only possible reversal-fixed positive predecessor is half of the
target; it occurs exactly when that half is palindromic. -/
theorem fixed_predecessor_iff (Y : Nat) (e : Nat → Nat) (W n : Nat)
    (hY : Canonical Y e W) (hzero : Y % 10 = 0) :
    (n ∈ predecessors e W ∧ reverse10 n = n) ↔
      n = Y / 2 ∧ Palindrome (Y / 2) := by
  constructor
  · rintro ⟨hn, hfixed⟩
    have hstep := ((mem_predecessors Y e W n hY).mp hn).2
    have hsum : n + n = Y := by
      simpa only [step, hfixed] using hstep
    have hhalf : n = Y / 2 := by omega
    refine ⟨hhalf, ?_⟩
    rw [← hhalf]
    exact hfixed
  · rintro ⟨rfl, hpal⟩
    have hpositive : 0 < Y := by
      have hp := value_positive e W hY.1 hY.2.2.1
      simpa only [hY.2.2.2] using hp
    have hhalfpos : 0 < Y / 2 := by omega
    have hdouble : Y / 2 + Y / 2 = Y := by omega
    change reverse10 (Y / 2) = Y / 2 at hpal
    refine ⟨(mem_predecessors Y e W (Y / 2) hY).mpr ⟨hhalfpos, ?_⟩, hpal⟩
    simpa only [step, hpal] using hdouble

/-- Exact fixed-point sublist of the complete ordinary predecessor fiber.
The imported duplicate-free enumeration rules out repeated fixed points. -/
theorem fixed_predecessor_filter (Y : Nat) (e : Nat → Nat) (W : Nat)
    (hY : Canonical Y e W) (hzero : Y % 10 = 0) :
    (predecessors e W).filter (fun n => decide (reverse10 n = n)) =
      if Palindrome (Y / 2) then [Y / 2] else [] := by
  let xs := (predecessors e W).filter (fun n => decide (reverse10 n = n))
  have hmem : ∀ n, n ∈ xs ↔ n = Y / 2 ∧ Palindrome (Y / 2) := by
    intro n
    change n ∈ (predecessors e W).filter (fun n => decide (reverse10 n = n)) ↔ _
    simpa only [List.mem_filter, decide_eq_true_eq] using
      fixed_predecessor_iff Y e W n hY hzero
  have hnd : xs.Nodup :=
    List.Pairwise.filter (fun n => decide (reverse10 n = n))
      (predecessors_nodup Y e W hY)
  change xs = if Palindrome (Y / 2) then [Y / 2] else []
  by_cases hpal : Palindrome (Y / 2)
  · rw [if_pos hpal]
    have hrep : xs = List.replicate xs.length (Y / 2) :=
      List.eq_replicate_of_mem (fun n hn => ((hmem n).mp hn).1)
    have hle : xs.length ≤ 1 := by
      apply List.nodup_replicate.mp
      rw [← hrep]
      exact hnd
    have hpos : 0 < xs.length :=
      List.length_pos_iff_exists_mem.mpr
        ⟨Y / 2, (hmem (Y / 2)).mpr ⟨rfl, hpal⟩⟩
    have hlen : xs.length = 1 := by omega
    simpa only [hlen, List.replicate_succ, List.replicate_zero] using hrep
  · rw [if_neg hpal]
    apply List.eq_nil_iff_forall_not_mem.mpr
    intro n hn
    exact hpal ((hmem n).mp hn).2

/-- A positive target ending in zero has an odd number of positive
ordinary reverse-and-add predecessors exactly when its half is a palindrome. -/
theorem predecessor_count_parity (Y : Nat) (e : Nat → Nat) (W : Nat)
    (hY : Canonical Y e W) (hzero : Y % 10 = 0) :
    (predecessors e W).length % 2 = if Palindrome (Y / 2) then 1 else 0 := by
  have hmap : ∀ n, n ∈ predecessors e W → reverse10 n ∈ predecessors e W := by
    intro n hn
    obtain ⟨hpos, hstep⟩ := (mem_predecessors Y e W n hY).mp hn
    exact (mem_predecessors Y e W (reverse10 n) hY).mpr
      (reverse10_preserves_predecessor Y n hzero hpos hstep)
  have hinv : ∀ n, n ∈ predecessors e W → reverse10 (reverse10 n) = n := by
    intro n hn
    obtain ⟨hpos, hstep⟩ := (mem_predecessors Y e W n hY).mp hn
    exact reverse10_involutive_of_units_ne_zero n hpos
      (predecessor_units_ne_zero Y n hzero hpos hstep)
  have hparity := involution_fixed_filter_parity (predecessors e W) reverse10
    (predecessors_nodup Y e W hY) hmap hinv
  rw [fixed_predecessor_filter Y e W hY hzero] at hparity
  by_cases hpal : Palindrome (Y / 2) <;> simpa [hpal] using hparity

end ZeroEndingPredecessorParity

#print axioms ZeroEndingPredecessorParity.fixed_predecessor_iff
#print axioms ZeroEndingPredecessorParity.fixed_predecessor_filter
#print axioms ZeroEndingPredecessorParity.predecessor_count_parity
