import P196.Drafts.Agent105ActualHighReturn.NeutralExterior
import P196.Drafts.Agent105ActualHighReturn.HighReturnPrefix
import P196.Drafts.Agent7RunPopulationRenewal.SmallWidth
import P196.Drafts.Agent7RunPopulationRenewal.NumericHigh

/-! Complete actual-orbit bridge to the existing three-return rank bound.
The only dynamical hypotheses are admissibility and high-region membership
at the stated even times. Second-step nonoverflow is proved, not assumed. -/

namespace Agent105.ActualHighReturn

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
  HighCarryReduction Agent105.HighReturnPrefix Agent105.NeutralExterior

theorem iterPairs_add (q : Nat → Nat) (L a b : Nat) :
    iterPairs q L (a + b) =
      iterPairs (iterPairs q L a).2 (iterPairs q L a).1 b := by
  induction b with
  | zero => simp [iterPairs]
  | succ b ih =>
    rw [Nat.add_succ]
    change (nextWidth (iterPairs q L (a + b)).2 (iterPairs q L (a + b)).1,
      nextColumns (iterPairs q L (a + b)).2 (iterPairs q L (a + b)).1) = _
    rw [ih]
    rfl

theorem iterPairs_width_ge (q : Nat → Nat) (L t : Nat) :
    L ≤ (iterPairs q L t).1 := by
  induction t with
  | zero => exact Nat.le_refl L
  | succ t ih =>
    simp only [iterPairs]
    unfold nextWidth
    split <;> omega

/-- A genuine high return forces the second normalization not to overflow. -/
theorem high_return_no_second_overflow (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hq : HighCarryWord q L)
    (hr : HighCarryWord (iterPairs q L 2).2 (iterPairs q L 2).1) :
    carry (nextColumns q L) (L + 1) = 0 := by
  have hw := HighCarryReduction.nextWidth_eq q L ha.1 hq
  have hp : Admissible (L + 1) (nextColumns q L) := by
    simpa only [hw] using NormalizationBridge.admissible_next q L ha
  have hout : nextColumns q L 0 ≤ 9 := by
    rw [HighCarryReduction.nextColumns_zero q L ha.1 hq]
    have hb := (hq.1 0 ha.1).2
    omega
  change HighCarryWord (nextColumns (nextColumns q L) (nextWidth q L))
    (nextWidth (nextColumns q L) (nextWidth q L)) at hr
  rw [hw] at hr
  exact low_outer_high_next_no_overflow (nextColumns q L) (L + 1)
    hp.1 hp.2.2.1 hp.2.2.2.1 hout (fun i hi => (hr.1 i hi).1)

/-- The actual width grows by exactly one on every two-step high return. -/
theorem high_return_state (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hq : HighCarryWord q L)
    (hr : HighCarryWord (iterPairs q L 2).2 (iterPairs q L 2).1) :
    iterPairs q L 2 = (L + 1, successor q L) := by
  have hw := HighCarryReduction.nextWidth_eq q L ha.1 hq
  have hc := high_return_no_second_overflow q L ha hq hr
  change (nextWidth (nextColumns q L) (nextWidth q L),
    nextColumns (nextColumns q L) (nextWidth q L)) = _
  rw [hw]
  simp only [nextWidth, hc, if_true, successor]

/-- No hypothetical control or graph-edge premise remains in this bridge. -/
theorem actual_return_rank_decreases (q : Nat → Nat) (L : Nat)
    (hL : 3 ≤ L) (ha : Admissible L q) (hq : HighCarryWord q L)
    (hr : HighCarryWord (iterPairs q L 2).2 (iterPairs q L 2).1) :
    HighReturnRank.rank (code (iterPairs q L 2).2) < HighReturnRank.rank (code q) := by
  have hc := high_return_no_second_overflow q L ha hq hr
  have hs := high_return_state q L ha hq hr
  rw [hs] at hr ⊢
  exact actual_prefix_rank_decreases q L hL ha hq hc hr

/-- Every finite admissible decimal pair word has at most three consecutive
two-step high-region returns. Widths one and two are included. -/
theorem actual_high_returns_le_three (q : Nat → Nat) (L R : Nat)
    (ha : Admissible L q)
    (hH : ∀ j, j ≤ R →
      HighCarryWord (iterPairs q L (2 * j)).2 (iterPairs q L (2 * j)).1) :
    R ≤ 3 := by
  by_cases hR : R ≤ 3
  · exact hR
  have hq : HighCarryWord q L := hH 0 (Nat.zero_le _)
  by_cases hL : 3 ≤ L
  · let r := fun j => HighReturnRank.rank (code (iterPairs q L (2 * j)).2)
    have hdesc : ∀ j, j < R → r (j + 1) < r j := by
      intro j hj
      have ha' := iterPairs_admissible q L (2 * j) ha
      have hw : 3 ≤ (iterPairs q L (2 * j)).1 :=
        Nat.le_trans hL (iterPairs_width_ge q L (2 * j))
      have hs : iterPairs (iterPairs q L (2 * j)).2
          (iterPairs q L (2 * j)).1 2 = iterPairs q L (2 * (j + 1)) := by
        rw [← iterPairs_add]
        simp only [Nat.mul_add, Nat.mul_one]
      have hr : HighCarryWord
          (iterPairs (iterPairs q L (2 * j)).2 (iterPairs q L (2 * j)).1 2).2
          (iterPairs (iterPairs q L (2 * j)).2 (iterPairs q L (2 * j)).1 2).1 := by
        rw [hs]
        exact hH (j + 1) (by omega)
      have hd := actual_return_rank_decreases (iterPairs q L (2 * j)).2
        (iterPairs q L (2 * j)).1 hw ha' (hH j (by omega)) hr
      rw [hs] at hd
      exact hd
    have hb : ∀ k, k ≤ R → r k + k ≤ r 0 := by
      intro k
      induction k with
      | zero => intro _; omega
      | succ k ih =>
        intro hk
        have hi := ih (by omega)
        have hd := hdesc k (by omega)
        omega
    have hsum := hb R (Nat.le_refl R)
    have hrank : r 0 ≤ 3 := HighReturnRank.rank_le_three (code q)
      (code_properties q L hL hq).1
    omega
  · have hsmall : L = 1 ∨ L = 2 := by have := ha.1; omega
    exact False.elim (Agent105.SmallWidth.no_two_high_returns q L ha hsmall hq
      ⟨hH 1 (by omega), hH 2 (by omega)⟩)

/-- Ordinary finite positive integers, with no representation or certificate
premise left to supply. This is a high-region bound, not a palindrome theorem. -/
theorem numeric_high_returns_le_three (n R : Nat) (hn : 0 < n)
    (hH : ∀ j, j ≤ R → Agent105.NumericHigh.NumericHigh (Lychrel196.orbit n (2 * j))) :
    R ≤ 3 := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  apply actual_high_returns_le_three (columnSum d L) L R
    (NormalizationBridge.canonical_admissible n d L hc)
  intro j hj
  exact (Agent105.NumericHigh.numericHigh_orbit_iff_columns n d L (2 * j) hc).mp
    (hH j hj)

/-- The same obstruction applies from every starting time of a positive orbit. -/
theorem numeric_high_returns_after_le_three (n start R : Nat) (hn : 0 < n)
    (hH : ∀ j, j ≤ R →
      Agent105.NumericHigh.NumericHigh (Lychrel196.orbit n (start + 2 * j))) : R ≤ 3 := by
  apply numeric_high_returns_le_three (Lychrel196.orbit n start) R
    (orbit_positive n hn start)
  intro j hj
  rw [← LychrelCertificates.orbit_add]
  exact hH j hj

theorem no_perpetual_high_returns (n start : Nat) (hn : 0 < n) :
    ¬ (∀ j, Agent105.NumericHigh.NumericHigh (Lychrel196.orbit n (start + 2 * j))) := by
  intro hH
  have hb := numeric_high_returns_after_le_three n start 4 hn (fun j _ => hH j)
  omega

#print axioms actual_high_returns_le_three
#print axioms numeric_high_returns_le_three
#print axioms numeric_high_returns_after_le_three
#print axioms no_perpetual_high_returns

end Agent105.ActualHighReturn
