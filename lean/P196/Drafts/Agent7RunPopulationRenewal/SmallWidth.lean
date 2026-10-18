import P196.Drafts.Agent7RunPopulationRenewal.HighCarryReduction

/-! Small-width cases for actual high-region returns.  The congruence
lemmas respect the finite width: no condition is imposed on the infinite
tail of a coefficient function.  The only finite check is kernel `decide`
on the exact `iterPairs` dynamics. -/

namespace Agent105.SmallWidth

open DecimalDigits FoldedDecimal OverflowCarryNormalization HighCarryReduction

/-- Equal finite words have the same next width and next finite word. -/
theorem next_congr_upto (q r : Nat → Nat) (L : Nat)
    (h : ∀ i, i < L → q i = r i) :
    nextWidth q L = nextWidth r L ∧
      ∀ i, i < nextWidth q L → nextColumns q L i = nextColumns r L i := by
  have hc := carry_congr_upto q r L h L (Nat.le_refl L)
  constructor
  · simp only [nextWidth, hc]
  · intro i hi
    by_cases hz : carry q L = 0
    · have hrz : carry r L = 0 := by rw [← hc]; exact hz
      have hiL : i < L := by simpa only [nextWidth, hz, if_true] using hi
      have hm : L - 1 - i < L := by omega
      simp only [nextColumns, hz, hrz, if_true, columnSum, reflected,
        output_congr_upto q r L h i hiL,
        output_congr_upto q r L h (L - 1 - i) hm]
    · have hrz : carry r L ≠ 0 := by rw [← hc]; exact hz
      simp only [nextColumns, hz, hrz, if_false, columnSum, reflected,
        extended_congr_upto q r L h]

/-- Exact iteration depends only on the finite input word. -/
theorem iterPairs_congr_upto (q r : Nat → Nat) (L t : Nat)
    (h : ∀ i, i < L → q i = r i) :
    (iterPairs q L t).1 = (iterPairs r L t).1 ∧
      ∀ i, i < (iterPairs q L t).1 →
        (iterPairs q L t).2 i = (iterPairs r L t).2 i := by
  induction t with
  | zero => exact ⟨rfl, h⟩
  | succ t ih =>
    obtain ⟨hw, hp⟩ := ih
    have hn := next_congr_upto (iterPairs q L t).2 (iterPairs r L t).2
      (iterPairs q L t).1 hp
    simpa only [iterPairs, hw] using hn

/-- A decidable necessary condition for high-region membership. -/
def FiniteHigh (s : Nat × (Nat → Nat)) : Prop :=
  ∀ i : Fin s.1, 9 ≤ s.2 i

instance finiteHighDecidable (s : Nat × (Nat → Nat)) : Decidable (FiniteHigh s) := by
  unfold FiniteHigh
  infer_instance

set_option maxRecDepth 10000 in
set_option maxHeartbeats 4000000 in
/-- The closed finite calculation uses the actual maps, including overflow
and its resulting reflection width, at every one of the four updates. -/
theorem constant_no_two_returns :
    ∀ (L : Fin 3) (a : Fin 19),
      (L.val = 1 ∨ L.val = 2) → 10 ≤ a.val →
      ¬ (FiniteHigh (iterPairs (fun _ => a.val) L.val 2) ∧
         FiniteHigh (iterPairs (fun _ => a.val) L.val 4)) := by
  decide

/-- Widths one and two cannot have two consecutive two-step high returns.
The statement applies to arbitrary infinite tails representing the same
admissible finite input, and uses the exact changing-width dynamics. -/
theorem no_two_high_returns (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hL : L = 1 ∨ L = 2)
    (hq : HighCarryWord q L) :
    ¬ (HighCarryWord (iterPairs q L 2).2 (iterPairs q L 2).1 ∧
       HighCarryWord (iterPairs q L 4).2 (iterPairs q L 4).1) := by
  have heq : ∀ i, i < L → q i = (fun _ => q 0) i := by
    intro i hi
    rcases hL with hL | hL
    · have hi0 : i = 0 := by omega
      subst i
      rfl
    · have hs := ha.2.2.2.1 i hi
      have hi01 : i = 0 ∨ i = 1 := by omega
      rcases hi01 with rfl | rfl
      · rfl
      · simpa only [hL] using hs
  have hbound := (hq.1 0 ha.1).2
  have hfinite := constant_no_two_returns ⟨L, by omega⟩ ⟨q 0, by omega⟩ hL hq.2
  rintro ⟨h2, h4⟩
  apply hfinite
  constructor
  · intro i
    obtain ⟨hw, hp⟩ := iterPairs_congr_upto q (fun _ => q 0) L 2 heq
    have hi : i.val < (iterPairs q L 2).1 := by rw [hw]; exact i.isLt
    rw [← hp i.val hi]
    exact (h2.1 i.val hi).1
  · intro i
    obtain ⟨hw, hp⟩ := iterPairs_congr_upto q (fun _ => q 0) L 4 heq
    have hi : i.val < (iterPairs q L 4).1 := by rw [hw]; exact i.isLt
    rw [← hp i.val hi]
    exact (h4.1 i.val hi).1

#print axioms no_two_high_returns

end Agent105.SmallWidth
