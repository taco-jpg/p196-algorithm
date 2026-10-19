import P196.SymmetricCarryCensus.Counts
import P196.SymmetricCarryCensus.Complement

/-!
# Exact internal-carry census for the original symmetric-word enumeration

The complement involution permutes the original list and exchanges its two
actual carry classes at every strictly internal position. The exact total
therefore splits equally. A checked terminal example records the necessary
strict upper bound on the observed carry position.
-/

set_option autoImplicit false

namespace SymmetricCarryCensus

open DecimalDigits FoldedDecimal Agent124.PrefixK SevenColumn.ShortBoundary

private theorem complement_perm (L : Nat) (hL : 2 ≤ L) :
    ((symWords L).map complementWord).Perm (symWords L) := by
  refine perm_of_nodup_mem_iff _ _ ?_ (symWords_nodup L) ?_
  · apply nodup_map_of_injOn _ _ (symWords_nodup L)
    intro a ha b hb heq
    have h := congrArg complementWord heq
    simpa only [(complement_spec L a hL ha).2.1,
      (complement_spec L b hL hb).2.1] using h
  · intro w
    constructor
    · intro hw
      obtain ⟨v, hv, rfl⟩ := List.mem_map.mp hw
      exact (complement_spec L v hL hv).1
    · intro hw
      exact List.mem_map.mpr ⟨complementWord w,
        (complement_spec L w hL hw).1,
        (complement_spec L w hL hw).2.1⟩

/-- Each bit occurs in exactly half the admissible words at every internal carry. -/
theorem internal_carry_count (L j b : Nat)
    (hj0 : 0 < j) (hjL : j < L) (hb : b ≤ 1) :
    (symWords L).countP (fun w => carry (wordFun w) j == b) =
      9 * 19 ^ (L / 2 - 1) * (if L % 2 = 0 then 1 else 10) := by
  have hL : 2 ≤ L := by omega
  have hswap := (complement_perm L hL).countP_eq
    (fun w => carry (wordFun w) j == 0)
  rw [List.countP_map] at hswap
  have hcomp :
      (symWords L).countP (fun w => carry (wordFun (complementWord w)) j == 0) =
        (symWords L).countP (fun w => carry (wordFun w) j == 1) := by
    apply List.countP_congr
    intro w hw
    have hsum := (complement_spec L w hL hw).2.2 j hj0 hjL
    simp only [beq_iff_eq]
    omega
  have heq :
      (symWords L).countP (fun w => carry (wordFun w) j == 0) =
        (symWords L).countP (fun w => carry (wordFun w) j == 1) :=
    hswap.symm.trans hcomp
  have hnot :
      (symWords L).countP (fun w => ¬(carry (wordFun w) j == 0)) =
        (symWords L).countP (fun w => carry (wordFun w) j == 1) := by
    apply List.countP_congr
    intro w hw
    have hsum := (complement_spec L w hL hw).2.2 j hj0 hjL
    simp only [decide_eq_true_eq, beq_iff_eq]
    omega
  have hpart := List.length_eq_countP_add_countP
    (fun w : List Nat => carry (wordFun w) j == 0) (l := symWords L)
  rw [hnot] at hpart
  have hlen := symWords_length L
  rw [wordCount, if_neg (by omega : L ≠ 0), if_neg (by omega : L ≠ 1)] at hlen
  have hclosed : (symWords L).length =
      2 * (9 * 19 ^ (L / 2 - 1) * (if L % 2 = 0 then 1 else 10)) := by
    rw [hlen]
    simp only [Nat.mul_assoc]
    omega
  have hzero :
      (symWords L).countP (fun w => carry (wordFun w) j == 0) =
        9 * 19 ^ (L / 2 - 1) * (if L % 2 = 0 then 1 else 10) := by
    omega
  have hbit : b = 0 ∨ b = 1 := by omega
  rcases hbit with rfl | rfl
  · exact hzero
  · exact heq.symm.trans hzero

/-- Terminal carries need not be complementary, even for an admissible pair. -/
theorem terminal_counterexample :
    [9, 18, 9] ∈ symWords 3 ∧
    complementWord [9, 18, 9] = [10, 0, 10] ∧
    carry (wordFun [9, 18, 9]) 3 = 1 ∧
    carry (wordFun [10, 0, 10]) 3 = 1 := by
  decide +kernel

#print axioms internal_carry_count
#print axioms terminal_counterexample

end SymmetricCarryCensus
