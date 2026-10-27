import P196.ManagerShortTwoRunReturns.ShortCatalog
import P196.ManagerShortTwoRunReturns.ActualTrace
import P196.ManagerTwoRunObstruction.TwoRunObstruction

/-!
Literal decimal equal-two-run returns need at least eight actual additions
once each run has at least five digits. This strengthens the earlier r>=3,
P>=5 theorem without changing it. No intermediate template assumption is used.
-/

namespace P196.ManagerShortTwoRun

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open P196.Agent4.WholeWord P196.ManagerTwoRun

/-- A returned outside prefix with width gain two cannot have period5,6,or7. -/
theorem actual_short_prefix_obstruction (q : Nat → Nat) (L P : Nat)
    (ha : Admissible L q) (hL : 5 ≤ L)
    (hclose : ∀ i, i < 5 → (iterPairs q L P).2 i = q i)
    (hwidth : (iterPairs q L P).1 = L + 2) : P ≠ 5 ∧ P ≠ 6 ∧ P ≠ 7 := by
  constructor
  · intro h
    subst P
    have hm := actual_prefix_member q L 5 2 5 ha hL hclose hwidth
    rw [no_p5_g2_five_columns] at hm
    exact List.not_mem_nil hm
  · constructor
    · intro h
      subst P
      have hm := actual_prefix_member q L 6 2 3 ha (by omega)
        (by intro i hi; exact hclose i (by omega)) hwidth
      rw [no_p6_g2_three_columns] at hm
      exact List.not_mem_nil hm
    · intro h
      subst P
      have hm := actual_prefix_member q L 7 2 2 ha (by omega)
        (by intro i hi; exact hclose i (by omega)) hwidth
      rw [no_p7_g2_two_columns] at hm
      exact List.not_mem_nil hm

/-- The catalog obstruction applies to actual numeric reverse-and-add,
with canonical endpoints and no surrogate transition premise. -/
theorem numeric_short_prefix_obstruction
    (n : Nat) (d e : Nat → Nat) (L W P : Nat)
    (hsource : Canonical n d L)
    (htarget : Canonical (Lychrel196.orbit n P) e W)
    (hL : 5 ≤ L) (hwidth : W = L + 2)
    (hreturn : ∀ i, i < 5 → columnSum e W i = columnSum d L i) :
    P ≠ 5 ∧ P ≠ 6 ∧ P ≠ 7 := by
  let q := columnSum d L
  have ha := NormalizationBridge.canonical_admissible n d L hsource
  obtain ⟨f, hf, hr⟩ := iterPairs_representation n d q L P hsource (fun _ _ => rfl)
  obtain ⟨hw, hd⟩ := SevenColumnKernel.PalindromeBridge.canonical_unique hf htarget
  have hge := iterPairs_width_ge q L P
  apply actual_short_prefix_obstruction q L P ha hL
  · intro i hi
    calc
      (iterPairs q L P).2 i = columnSum f (iterPairs q L P).1 i :=
        (hr i (by omega)).symm
      _ = columnSum e W i := by
        unfold columnSum reflected
        rw [hd i (by omega), hd ((iterPairs q L P).1 - 1 - i) (by omega), hw]
      _ = q i := hreturn i hi
  · omega

theorem twoRun_low_digit_k (U M V : List Nat) (x y r k i : Nat)
    (hr : k ≤ r) (hi : i < k) :
    twoRunDigit U x M y V r i = if i < U.length then U[i]! else x := by
  unfold twoRunDigit
  split
  · rfl
  · rw [if_pos (by omega)]

theorem twoRun_high_digit_k (U M V : List Nat) (x y r k i : Nat)
    (hr : k ≤ r) (hi : i < k) :
    twoRunDigit U x M y V r (twoRunWidth U M V r - 1 - i) =
      if i < V.length then V[V.length - 1 - i]! else y := by
  unfold twoRunDigit twoRunWidth
  rw [if_neg (by omega), if_neg (by omega), if_neg (by omega)]
  by_cases hV : i < V.length
  · rw [if_neg (by omega), if_pos hV]
    congr 1
    omega
  · rw [if_pos (by omega), if_neg hV]

/-- Arbitrarily many outside pair columns stabilize when both literal runs
are at least that long, including empty fixed blocks and low zero digits. -/
theorem twoRun_outer_columns_stable (U M V : List Nat) (x y r s k : Nat)
    (hr : k ≤ r) (hs : k ≤ s) :
    ∀ i, i < k →
      columnSum (twoRunDigit U x M y V r) (twoRunWidth U M V r) i =
        columnSum (twoRunDigit U x M y V s) (twoRunWidth U M V s) i := by
  intro i hi
  unfold columnSum reflected
  rw [twoRun_low_digit_k U M V x y r k i hr hi,
    twoRun_low_digit_k U M V x y s k i hs hi,
    twoRun_high_digit_k U M V x y r k i hr hi,
    twoRun_high_digit_k U M V x y s k i hs hi]

/-- A single canonical literal two-run return at r>=5 with positive common
increment requires P>=8. Fixed block widths are unrestricted. -/
theorem twoRun_positive_return_period_ge_eight
    (U M V : List Nat) (x y r S P n m : Nat)
    (hr : 5 ≤ r) (hS : 0 < S)
    (hsource : Canonical n (twoRunDigit U x M y V r) (twoRunWidth U M V r))
    (htarget : Canonical m (twoRunDigit U x M y V (r + S))
      (twoRunWidth U M V (r + S)))
    (hreturn : Lychrel196.orbit n P = m) : 8 ≤ P := by
  have hb := twoRun_return_constraints U M V x y r S P n m
    (by omega) hsource htarget hreturn
  have hp := twoRun_positive_return_period_ge_five U M V x y r S P n m
    (by omega) hS hsource htarget hreturn
  by_cases h : 8 ≤ P
  · exact h
  have hS1 : S = 1 := by omega
  subst S
  have htarget' : Canonical (Lychrel196.orbit n P)
      (twoRunDigit U x M y V (r + 1)) (twoRunWidth U M V (r + 1)) := by
    rw [hreturn]
    exact htarget
  have hno := numeric_short_prefix_obstruction n
    (twoRunDigit U x M y V r) (twoRunDigit U x M y V (r + 1))
    (twoRunWidth U M V r) (twoRunWidth U M V (r + 1)) P
    hsource htarget' (by unfold twoRunWidth; omega)
    (by unfold twoRunWidth; omega)
    (twoRun_outer_columns_stable U M V x y (r + 1) r 5 (by omega) hr)
  omega

/-- An eventual universal literal family can choose a run length at least5;
therefore its positive common-increment period is also at least8. -/
theorem eventual_twoRun_period_ge_eight
    (U M V : List Nat) (x y S P r0 : Nat) (hS : 0 < S)
    (hfamily : ∀ r, r0 ≤ r → ∃ n m,
      Canonical n (twoRunDigit U x M y V r) (twoRunWidth U M V r) ∧
      Canonical m (twoRunDigit U x M y V (r + S)) (twoRunWidth U M V (r + S)) ∧
      Lychrel196.orbit n P = m) : 8 ≤ P := by
  obtain ⟨n, m, hn, hm, hret⟩ := hfamily (r0 + 5) (by omega)
  exact twoRun_positive_return_period_ge_eight U M V x y (r0 + 5) S P n m
    (by omega) hS hn hm hret

#print axioms actual_short_prefix_obstruction
#print axioms numeric_short_prefix_obstruction
#print axioms twoRun_positive_return_period_ge_eight
#print axioms eventual_twoRun_period_ge_eight

end P196.ManagerShortTwoRun
