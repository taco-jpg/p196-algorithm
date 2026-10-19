import P196.MirroredCarryCensus.Neutral

/-!
# Exact joint census at mirrored internal carry positions

The middle involution fixes the first observed carry. Away from a neutral
middle it exchanges the two values of the second carry. A neutral middle
contributes only to the diagonal, so the existing marginal census and the
neutral census determine each joint count.
-/

set_option autoImplicit false

namespace MirroredCarryCensus

open DecimalDigits Agent124.PrefixK SevenColumn.ShortBoundary
open SymmetricCarryCensus

private theorem diagonal_balance (L j a : Nat)
    (hj : 0 < j) (hjj : 2 * j ≤ L) (ha : a ≤ 1) :
    (symWords L).countP (fun w =>
      (carry (wordFun w) j == a) && (carry (wordFun w) (L - j) == a)) =
        (symWords L).countP (fun w =>
          (carry (wordFun w) j == a) && !(carry (wordFun w) (L - j) == a)) +
        neutralCount L j a := by
  let p : List Nat → Bool := fun w => carry (wordFun w) j == a
  let d : List Nat → Bool := fun w => carry (wordFun w) (L - j) == a
  let n : List Nat → Bool := neutralMiddle L j
  let s : List Nat → Bool := fun w =>
    p (middleComplement L j w) && d (middleComplement L j w)
  have hswap : (symWords L).countP s =
      (symWords L).countP (fun w => p w && d w) := by
    simpa only [s, List.countP_map, Function.comp_def] using
      (middleComplement_perm L j hj hjj).countP_eq (fun w => p w && d w)
  have hpoint : ∀ w ∈ symWords L,
      ((s w && n w) ↔ (p w && n w)) ∧
      ((s w && !n w) ↔ (p w && !d w)) := by
    intro w hw
    have hs := middle_complement_spec L j w hj hjj hw
    have hadm := ((mem_symWords_iff L w).mp hw).2
    have htadm := ((mem_symWords_iff L (middleComplement L j w)).mp hs.1).2
    have hr := carry_bounded (wordFun w) L hadm.2.2.1
      (L - j) (Nat.sub_le L j)
    have htr := carry_bounded (wordFun (middleComplement L j w)) L htadm.2.2.1
      (L - j) (Nat.sub_le L j)
    have hleft := hs.2.2.1
    have hsum := hs.2.2.2
    dsimp only [s, p, d, n]
    rw [hleft]
    cases hn : neutralMiddle L j w <;>
      simp [hn] at hsum ⊢ <;> omega
  have hneutral : (symWords L).countP (fun w => s w && n w) =
      neutralCount L j a := by
    apply List.countP_congr
    intro w hw
    exact (hpoint w hw).1
  have hoff : (symWords L).countP (fun w => s w && !n w) =
      (symWords L).countP (fun w => p w && !d w) := by
    apply List.countP_congr
    intro w hw
    exact (hpoint w hw).2
  have hsplit := List.countP_eq_countP_filter_add (symWords L) s n
  rw [List.countP_filter, List.countP_filter, hneutral, hoff, hswap] at hsplit
  change (symWords L).countP (fun w => p w && d w) =
    (symWords L).countP (fun w => p w && !d w) + neutralCount L j a
  omega

private theorem joint_count_formula (L j a b : Nat)
    (hj : 0 < j) (hjj : 2 * j ≤ L) (ha : a ≤ 1) (hb : b ≤ 1) :
    (symWords L).countP (fun w =>
      (carry (wordFun w) j == a) && (carry (wordFun w) (L - j) == b)) =
        if a = b then
          ((symWords L).countP (fun w => carry (wordFun w) j == a) +
            neutralCount L j a) / 2
        else
          ((symWords L).countP (fun w => carry (wordFun w) j == a) -
            neutralCount L j a) / 2 := by
  let p : List Nat → Bool := fun w => carry (wordFun w) j == a
  let d : List Nat → Bool := fun w => carry (wordFun w) (L - j) == a
  have hbalance : (symWords L).countP (fun w => p w && d w) =
      (symWords L).countP (fun w => p w && !d w) + neutralCount L j a :=
    diagonal_balance L j a hj hjj ha
  have hpart := List.countP_eq_countP_filter_add (symWords L) p d
  rw [List.countP_filter, List.countP_filter] at hpart
  by_cases hab : a = b
  · subst b
    rw [if_pos rfl]
    change (symWords L).countP (fun w => p w && d w) =
      ((symWords L).countP p + neutralCount L j a) / 2
    omega
  · rw [if_neg hab]
    have hoff : (symWords L).countP (fun w =>
        (carry (wordFun w) j == a) && (carry (wordFun w) (L - j) == b)) =
          (symWords L).countP (fun w => p w && !d w) := by
      apply List.countP_congr
      intro w hw
      have hadm := ((mem_symWords_iff L w).mp hw).2
      have hr := carry_bounded (wordFun w) L hadm.2.2.1
        (L - j) (Nat.sub_le L j)
      dsimp only [p, d]
      simp <;> omega
    rw [hoff]
    change (symWords L).countP (fun w => p w && !d w) =
      ((symWords L).countP p - neutralCount L j a) / 2
    omega

/-- At even width, the all-nine middle gives the exact diagonal excess. -/
theorem mirrored_count_even (m j a b : Nat)
    (hj : 0 < j) (hjm : j ≤ m) (ha : a ≤ 1) (hb : b ≤ 1) :
    (symWords (2 * m)).countP (fun w =>
      (carry (wordFun w) j == a) &&
      (carry (wordFun w) (2 * m - j) == b)) =
        if a = b then (9 * 19 ^ (m - 1) + 9 * 19 ^ (j - 1)) / 2
        else (9 * 19 ^ (m - 1) - 9 * 19 ^ (j - 1)) / 2 := by
  have hmarg : (symWords (2 * m)).countP (fun w => carry (wordFun w) j == a) =
      9 * 19 ^ (m - 1) := by
    have h := internal_carry_count (2 * m) j a hj (by omega) ha
    have hdiv : (2 * m) / 2 = m := by omega
    have hmod : (2 * m) % 2 = 0 := by omega
    simpa only [hdiv, hmod, if_true, Nat.mul_one] using h
  simpa only [hmarg, neutral_count_even m j a hj hjm ha] using
    joint_count_formula (2 * m) j a b hj (by omega) ha hb

/-- At odd width, all four mirrored internal carry pairs occur equally often. -/
theorem mirrored_count_odd (m j a b : Nat)
    (hj : 0 < j) (hjm : j ≤ m) (ha : a ≤ 1) (hb : b ≤ 1) :
    (symWords (2 * m + 1)).countP (fun w =>
      (carry (wordFun w) j == a) &&
      (carry (wordFun w) (2 * m + 1 - j) == b)) =
        45 * 19 ^ (m - 1) := by
  have hmarg :
      (symWords (2 * m + 1)).countP (fun w => carry (wordFun w) j == a) =
        90 * 19 ^ (m - 1) := by
    have h := internal_carry_count (2 * m + 1) j a hj (by omega) ha
    have hdiv : (2 * m + 1) / 2 = m := by omega
    have hmod : (2 * m + 1) % 2 = 1 := by omega
    simp only [hdiv, hmod, if_neg (by decide : ¬ (1 = 0))] at h
    omega
  have h := joint_count_formula (2 * m + 1) j a b hj (by omega) ha hb
  rw [hmarg, neutral_count_odd m j a hj hjm ha] at h
  by_cases hab : a = b
  · rw [if_pos hab, Nat.add_zero] at h
    omega
  · rw [if_neg hab, Nat.sub_zero] at h
    omega

#print axioms mirrored_count_even
#print axioms mirrored_count_odd

end MirroredCarryCensus
