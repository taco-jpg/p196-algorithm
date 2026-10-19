import P196.Foundations.IncomingCarry
import P196.TerminalCarryCensus.Scan

/-!
Complementary finite blocks with one common incoming carry bit. Existing
input synchronization reduces every nonneutral block to the zero-input
scan theorem. An all-nine block retains both copies of its incoming bit,
including when the block is empty. No carry recurrence is reproved.
-/

set_option autoImplicit false

namespace MirroredCarryCensus

open IncomingCarry

/-- Equal incoming bits survive twice exactly on the neutral block;
otherwise complementary blocks have outgoing carry sum one. -/
theorem complementary_carryIn_sum (q r : Nat → Nat) (c n : Nat)
    (hc : c ≤ 1) (hcomp : ∀ i, i < n → q i + r i = 18) :
    carryIn q c n + carryIn r c n =
      if (List.range n).all (fun i => q i == 9) then 2 * c else 1 := by
  by_cases hn : (List.range n).all (fun i => q i == 9) = true
  · have hq9 : ∀ i, i < n → q i = 9 := by
      simpa only [List.all_eq_true, List.mem_range, beq_iff_eq] using hn
    have hr9 : ∀ i, i < n → r i = 9 := by
      intro i hi
      have hs := hcomp i hi
      have hqi := hq9 i hi
      omega
    rw [if_pos hn, carryIn_nines q c n hc hq9, carryIn_nines r c n hc hr9]
    omega
  · have hnon : ∃ i, i < n ∧ q i ≠ 9 := by
      apply Classical.byContradiction
      intro hnone
      apply hn
      simp only [List.all_eq_true, List.mem_range, beq_iff_eq]
      intro i hi
      apply Classical.byContradiction
      intro hqi
      exact hnone ⟨i, hi, hqi⟩
    obtain ⟨i, hi, hni⟩ := hnon
    have hqb : ∀ k, k < n → q k ≤ 18 := by
      intro k hk
      have hs := hcomp k hk
      omega
    have hrb : ∀ k, k < n → r k ≤ 18 := by
      intro k hk
      have hs := hcomp k hk
      omega
    have hnr : r i ≠ 9 := by
      have hs := hcomp i hi
      omega
    rw [carryIn_eq_of_nonNine q c 0 n i hc (by omega) hqb hi hni,
      carryIn_eq_of_nonNine r c 0 n i hc (by omega) hrb hi hnr,
      carryIn_zero_eq_carry q n, carryIn_zero_eq_carry r n]
    simpa only [if_neg hn] using
      TerminalCarryCensus.complementary_carry_sum q r n hcomp

#print axioms complementary_carryIn_sum

end MirroredCarryCensus
