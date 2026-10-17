import P196.Foundations.LychrelDigitSums
import P196.Agent2SaturatedProfile.SaturationTheorem

namespace P196.Agent4.WholeWord
open DecimalDigits FoldedDecimal OverflowCarryNormalization
open P196.Agent4.Saturation

def prefix3 (q : Nat → Nat) : Prefix := ⟨q 0,q 1,q 2⟩

/-- Exact three-column projection of the existing whole-word normalization map.
No choice of a carry word or approximate transition is assumed. -/
theorem nextColumns_prefix3 (q : Nat → Nat) (L : Nat)
    (hL : 3 ≤ L) (hb : ∀ i < L, q i ≤ 18)
    (hs : ∀ i < L, q i = q (L-1-i)) :
    advance (prefix3 q) (carry q (L-3)) =
      (prefix3 (nextColumns q L), carry q L) := by
  have hr2 : carry q (L-2) = (q 2+carry q (L-3))/10 := by
    have h := (folded_carry_transition q L 2 (by omega) hs).2
    simpa only [Nat.sub_sub, Nat.reduceAdd] using h
  have hr1 : carry q (L-1) = (q 1+carry q (L-2))/10 := by
    have h := (folded_carry_transition q L 1 (by omega) hs).2
    simpa only [Nat.sub_sub, Nat.reduceAdd] using h
  have hr0 : carry q L = (q 0+carry q (L-1))/10 := by
    have h := (folded_carry_transition q L 0 (by omega) hs).2
    simpa only [Nat.sub_zero] using h
  have hl1 : carry q 1 = q 0/10 := by simp [carry]
  have hl2 : carry q 2 = (q 1+carry q 1)/10 := rfl
  have hbit := carry_bounded q L hb L (by omega)
  unfold advance prefix3
  dsimp only
  rw [←hr2, ←hr1, ←hr0, ←hl1, ←hl2]
  by_cases hg : carry q L = 0
  · rw [if_pos hg]
    have h0 := folded_emission_no_overflow q L 0 (by omega) hs hg
    have h1 := folded_emission_no_overflow q L 1 (by omega) hs hg
    have h2 := folded_emission_no_overflow q L 2 (by omega) hs hg
    simp only [Nat.sub_zero, Nat.sub_sub, Nat.reduceAdd, carry,
      Nat.add_zero] at h0
    simp only [Nat.sub_sub, Nat.reduceAdd] at h1 h2
    rw [h0, h1, h2]
  · have hgone : carry q L = 1 := by omega
    rw [if_neg hg]
    have h0 := folded_emission_overflow q L 0 (by omega) hgone
    have h1 := folded_emission_overflow q L 1 (by omega) hgone
    have h2 := folded_emission_overflow q L 2 (by omega) hgone
    have hd0 := folded_delay_update q L 0 (by omega) hs
    have hd1 := folded_delay_update q L 1 (by omega) hs
    simp only [Nat.zero_add, Nat.sub_zero] at hd0
    simp only [Nat.reduceAdd, Nat.sub_sub] at hd1
    simp only [Nat.sub_zero, extended, Nat.lt_irrefl, if_false,
      hgone, carry, Nat.add_zero] at h0
    rw [hd0] at h1
    rw [hd1] at h2
    rw [h0, h1, h2]


/-- Canonical width never decreases, even if the orbit is continued past a palindrome. -/
theorem iterPairs_width_ge (q : Nat → Nat) (L n : Nat) :
    L ≤ (iterPairs q L n).1 := by
  induction n with
  | zero => simp [iterPairs]
  | succ n ih =>
    simp only [iterPairs, nextWidth]
    split <;> omega

def overflowAt (q : Nat → Nat) (L i : Nat) : Nat :=
  carry (iterPairs q L i).2 (iterPairs q L i).1

theorem actual_width_overflow_identity (q : Nat → Nat) (L n : Nat)
    (ha : Admissible L q) :
    (iterPairs q L n).1 = L + total (overflowAt q L) n := by
  induction n with
  | zero => simp [iterPairs, total]
  | succ n ih =>
    have had := CarryHistory.iterPairs_admissible q L n ha
    have hc := carry_bounded (iterPairs q L n).2 (iterPairs q L n).1
      had.2.2.1 (iterPairs q L n).1 (by omega)
    simp only [iterPairs, nextWidth, total, overflowAt]
    split <;> omega

/-- Exact projection along every actual iterated whole-word state. -/
theorem iterPairs_prefix_evolution (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hL : 3 ≤ L) :
    advance (prefix3 (iterPairs q L i).2)
      (carry (iterPairs q L i).2 ((iterPairs q L i).1-3)) =
      (prefix3 (iterPairs q L (i+1)).2, overflowAt q L i) := by
  have had := CarryHistory.iterPairs_admissible q L i ha
  have hw := iterPairs_width_ge q L i
  exact nextColumns_prefix3 (iterPairs q L i).2 (iterPairs q L i).1
    (by omega) had.2.2.1 had.2.2.2.1

/-- A theorem about the actual whole-word dynamics, with no abstract transition
premise: a returned three-column prefix at saturated width growth has 8|n. -/
theorem actual_saturated_prefix_return (q : Nat → Nat) (L n : Nat)
    (ha : Admissible L q) (hL : 3 ≤ L)
    (hreturn : prefix3 (iterPairs q L n).2 = prefix3 q)
    (hwidth : 2*(iterPairs q L n).1 = 2*L+n) : n%8=0 := by
  let s := fun i => prefix3 (iterPairs q L i).2
  let e := fun i => carry (iterPairs q L i).2 ((iterPairs q L i).1-3)
  have hv : ∀ i < n, Valid (s i) := by
    intro i hi
    have had := CarryHistory.iterPairs_admissible q L i ha
    have hw := iterPairs_width_ge q L i
    exact ⟨had.2.1,had.2.2.1 0 (by omega),had.2.2.1 1 (by omega),
      had.2.2.1 2 (by omega)⟩
  have he : ∀ i < n, e i ≤ 1 := by
    intro i hi
    have had := CarryHistory.iterPairs_admissible q L i ha
    exact carry_bounded (iterPairs q L i).2 (iterPairs q L i).1
      had.2.2.1 ((iterPairs q L i).1-3) (by omega)
  have hs : ∀ i < n, (advance (s i) (e i)).1 = s (i+1) := by
    intro i hi
    exact congrArg Prod.fst (iterPairs_prefix_evolution q L i ha hL)
  have hg : (fun i => (advance (s i) (e i)).2) = overflowAt q L := by
    funext i
    exact congrArg Prod.snd (iterPairs_prefix_evolution q L i ha hL)
  have hclose : s n = s 0 := by simpa [s,iterPairs] using hreturn
  have hid := actual_width_overflow_identity q L n ha
  apply saturated_closed_prefix_period s e n hv he hs hclose
  rw [hg]
  omega

/-- Numeric reverse-and-add specialization. The returned prefix and the width
are those of the actual canonical representation, not a surrogate sequence. -/
theorem numeric_saturated_prefix_obstruction (n : Nat) (d : Nat → Nat) (L P : Nat)
    (hc : Canonical n d L) (hL : 3 ≤ L) :
    ∃ e W, Canonical (Lychrel196.orbit n P) e W ∧
      (prefix3 (columnSum e W) = prefix3 (columnSum d L) →
        2*W = 2*L+P → P%8=0) := by
  let q := columnSum d L
  have ha := NormalizationBridge.canonical_admissible n d L hc
  obtain ⟨e,he,hr⟩ := iterPairs_representation n d q L P hc (fun _ _ => rfl)
  refine ⟨e,(iterPairs q L P).1,he,?_⟩
  intro hp hw
  have hge := iterPairs_width_ge q L P
  have hrp : prefix3 (columnSum e (iterPairs q L P).1) =
      prefix3 (iterPairs q L P).2 := by
    unfold prefix3
    rw [hr 0 (by omega),hr 1 (by omega),hr 2 (by omega)]
  rw [hrp] at hp
  exact actual_saturated_prefix_return q L P ha hL hp hw

#print axioms nextColumns_prefix3
#print axioms iterPairs_width_ge
#print axioms actual_width_overflow_identity
#print axioms iterPairs_prefix_evolution
#print axioms actual_saturated_prefix_return
#print axioms numeric_saturated_prefix_obstruction
end P196.Agent4.WholeWord
