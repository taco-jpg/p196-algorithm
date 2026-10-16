import LychrelDigitSums

/-! Fixed finite targets have bounded backward ancestry. This says nothing
about infinite forward reverse-and-add orbits or palindrome avoidance. -/

namespace DecimalFiniteAncestry

open Lychrel196 DecimalDigits DecimalQuantitativeMass
  FoldedDecimal OverflowCarryNormalization CarryHistory

theorem decimalLength_positive (n : Nat) (hn : 0 < n) :
    0 < decimalLength n := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  rw [decimalLength_of_canonical n d L hc]
  exact hc.1

/-- Direct ordinary-decimal bridge; all growth hypotheses are discharged. -/
theorem numeric_width_clock (n r : Nat) (hn : 0 < n) :
    r + 4 * decimalLength n ≤ 4 * decimalLength (orbit n r) + 4 := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  obtain ⟨e, W, he, hg, _⟩ := DecimalWidthGrowth.numeric_width_bounds n d L r hc
  rw [decimalLength_of_canonical n d L hc,
    decimalLength_of_canonical (orbit n r) e W he]
  exact hg

theorem numeric_width_five_floor (n r : Nat) (hn : 0 < n) :
    decimalLength n + r / 5 ≤ decimalLength (orbit n r) := by
  cases r with
  | zero => simp [orbit]
  | succ r =>
    have hg := numeric_width_clock n (r + 1) hn
    omega

/-- Any positive ancestor of this fixed finite target has depth at most 4L. -/
theorem numeric_ancestor_depth_le (a target r : Nat) (ha : 0 < a)
    (hreach : orbit a r = target) : r ≤ 4 * decimalLength target := by
  have hg := numeric_width_clock a r ha
  have hp := decimalLength_positive a ha
  rw [hreach] at hg
  omega

theorem numeric_no_ancestor_after_four_width (target r : Nat)
    (hr : 4 * decimalLength target < r) :
    ¬ ∃ a, 0 < a ∧ orbit a r = target := by
  rintro ⟨a, ha, he⟩
  have hb := numeric_ancestor_depth_le a target r ha he
  omega

theorem numeric_no_ancestor_at_five_width (target r : Nat) (ht : 0 < target)
    (hr : 5 * decimalLength target ≤ r) :
    ¬ ∃ a, 0 < a ∧ orbit a r = target := by
  apply numeric_no_ancestor_after_four_width
  have hp := decimalLength_positive target ht
  omega

def HasAncestor (target r : Nat) : Prop :=
  ∃ a, 0 < a ∧ orbit a r = target

private theorem orbit_shift (a r : Nat) : orbit (step a) r = orbit a (r + 1) := by
  have he := LychrelCertificates.orbit_add a 1 r
  simpa [orbit, Nat.add_comm] using he.symm

theorem hasAncestor_descending (target r : Nat) :
    HasAncestor target (r + 1) → HasAncestor target r := by
  rintro ⟨a, ha, he⟩
  refine ⟨step a, ?_, ?_⟩
  · simpa [orbit] using orbit_positive a ha 1
  · rw [orbit_shift]
    exact he

/-- Empty intersection of the descending images, with a concrete failing depth. -/
theorem numeric_ancestry_intersection_empty (target : Nat) :
    ¬ ∀ r, HasAncestor target r := by
  intro hall
  exact numeric_no_ancestor_after_four_width target
    (4 * decimalLength target + 1) (by omega) (hall _)

def HasSafeAncestor (Safe : Nat → Prop) (target r : Nat) : Prop :=
  ∃ a, 0 < a ∧ orbit a r = target ∧ ∀ k, k ≤ r → Safe (orbit a k)

theorem hasSafeAncestor_descending (Safe : Nat → Prop) (target r : Nat) :
    HasSafeAncestor Safe target (r + 1) → HasSafeAncestor Safe target r := by
  rintro ⟨a, ha, he, hs⟩
  refine ⟨step a, ?_, ?_, ?_⟩
  · simpa [orbit] using orbit_positive a ha 1
  · rw [orbit_shift]
    exact he
  · intro k hk
    rw [orbit_shift]
    exact hs (k + 1) (by omega)

theorem safe_ancestry_intersection_empty (Safe : Nat → Prop) (target : Nat) :
    ¬ ∀ r, HasSafeAncestor Safe target r := by
  intro hall
  apply numeric_ancestry_intersection_empty target
  intro r
  obtain ⟨a, ha, he, _⟩ := hall r
  exact ⟨a, ha, he⟩

/-- Finite-word equality is asserted only on the target's actual width. -/
def PairHasAncestor (q : Nat → Nat) (L r : Nat) : Prop :=
  ∃ p K, Admissible K p ∧ (iterPairs p K r).1 = L ∧
    ∀ i, i < L → (iterPairs p K r).2 i = q i

theorem pair_ancestor_depth_le (q : Nat → Nat) (L r : Nat)
    (ha : PairHasAncestor q L r) : r ≤ 4 * L := by
  obtain ⟨p, K, hp, hw, _⟩ := ha
  have hg := DecimalWidthGrowth.width_lower_bound p K r hp
  have hK := hp.1
  rw [hw] at hg
  omega

theorem pair_no_ancestor_at_five_width (q : Nat → Nat) (L r : Nat)
    (hL : 0 < L) (hr : 5 * L ≤ r) : ¬ PairHasAncestor q L r := by
  intro ha
  have hb := pair_ancestor_depth_le q L r ha
  omega

theorem pair_ancestry_intersection_empty (q : Nat → Nat) (L : Nat) :
    ¬ ∀ r, PairHasAncestor q L r := by
  intro hall
  have hb := pair_ancestor_depth_le q L (4 * L + 1) (hall _)
  omega

def PairHasSafeAncestor (Safe : Nat → (Nat → Nat) → Prop)
    (q : Nat → Nat) (L r : Nat) : Prop :=
  ∃ p K, Admissible K p ∧ (iterPairs p K r).1 = L ∧
    (∀ i, i < L → (iterPairs p K r).2 i = q i) ∧
    ∀ k, k ≤ r → Safe (iterPairs p K k).1 (iterPairs p K k).2

theorem pair_safe_ancestry_intersection_empty
    (Safe : Nat → (Nat → Nat) → Prop) (q : Nat → Nat) (L : Nat) :
    ¬ ∀ r, PairHasSafeAncestor Safe q L r := by
  intro hall
  apply pair_ancestry_intersection_empty q L
  intro r
  obtain ⟨p, K, hp, hw, he, _⟩ := hall r
  exact ⟨p, K, hp, hw, he⟩

#print axioms numeric_width_five_floor
#print axioms numeric_ancestor_depth_le
#print axioms numeric_no_ancestor_at_five_width
#print axioms hasAncestor_descending
#print axioms numeric_ancestry_intersection_empty
#print axioms hasSafeAncestor_descending
#print axioms safe_ancestry_intersection_empty
#print axioms pair_ancestor_depth_le
#print axioms pair_no_ancestor_at_five_width
#print axioms pair_ancestry_intersection_empty
#print axioms pair_safe_ancestry_intersection_empty

end DecimalFiniteAncestry
