import P196.Drafts.Agent112TwoPhaseObstruction.ActualInfiniteStrip

/-!
Agent #112: the nonperiodic obstruction stated using canonical digits of the
original natural-number orbit. The digit functions may be chosen arbitrarily
outside their canonical widths. Numeric controls retain the convention that
iteration continues after a palindrome.
-/
namespace Agent112.TwoPhase.Numeric

open DecimalDigits FoldedDecimal OverflowCarryNormalization Lychrel196
open Agent104.TemporalStripObligations

/-- Compare the exact pair iteration with any canonical digit representation
of the original numeric iterate. Width and digits are derived, not assumed. -/
theorem numeric_representation (n : Nat) (D : Nat → Nat → Nat) (W : Nat → Nat)
    (hc : ∀ t, Canonical (orbit n t) (D t) (W t)) (t : Nat) :
    widthAt (columnSum (D 0) (W 0)) (W 0) t = W t ∧
    ∀ i, i < W t → qAt (columnSum (D 0) (W 0)) (W 0) t i =
      columnSum (D t) (W t) i := by
  have hzero : Canonical n (D 0) (W 0) := hc 0
  obtain ⟨e,he,heq⟩ := iterPairs_representation n (D 0) (columnSum (D 0) (W 0))
    (W 0) t hzero (fun _ _ => rfl)
  have hw : widthAt (columnSum (D 0) (W 0)) (W 0) t = W t := by
    exact (DecimalQuantitativeMass.decimalLength_of_canonical _ _ _ he).symm.trans
      (DecimalQuantitativeMass.decimalLength_of_canonical _ _ _ (hc t))
  change Canonical (orbit n t) e (widthAt _ _ t) at he
  change ∀ i, i < widthAt _ _ t → columnSum e (widthAt _ _ t) i = qAt _ _ t i at heq
  rw [hw] at he heq
  have hde : ∀ i, i < W t → e i = D t i :=
    value_injective e (D t) (W t) he.2.1 (hc t).2.1
      (he.2.2.2.trans (hc t).2.2.2.symm)
  refine ⟨hw, ?_⟩
  intro i hi
  rw [← heq i hi]
  simp only [columnSum, reflected, hde i hi, hde (W t-1-i) (by omega)]

/-- An ordinary positive decimal orbit cannot exhibit all three features:
indefinitely alternating nonoverflow/overflow steps, one fixed interior cut,
and a persistent adjacent-column 6/12 band. No temporal period, returned
prefix, or independently postulated pair-word correspondence is required. -/
theorem no_numeric_persistent_alternating_band
    (n : Nat) (D : Nat → Nat → Nat) (W : Nat → Nat)
    (hc : ∀ t, Canonical (orbit n t) (D t) (W t))
    (width : Nat) (hp : 0 < width)
    (hw : ∀ j, width < W (2*j) ∧ width < W (2*j+1))
    (hg : ∀ j, carry (columnSum (D (2*j)) (W (2*j))) (W (2*j)) = 0 ∧
      carry (columnSum (D (2*j+1)) (W (2*j+1))) (W (2*j+1)) = 1)
    (ht : (∀ j,
        columnSum (D (2*j)) (W (2*j)) (width-1) = 6 ∧
        columnSum (D (2*j)) (W (2*j)) width = 6 ∧
        columnSum (D (2*j+1)) (W (2*j+1)) (width-1) = 12 ∧
        columnSum (D (2*j+1)) (W (2*j+1)) width = 12) ∨
      (∀ j,
        columnSum (D (2*j)) (W (2*j)) (width-1) = 12 ∧
        columnSum (D (2*j)) (W (2*j)) width = 12 ∧
        columnSum (D (2*j+1)) (W (2*j+1)) (width-1) = 6 ∧
        columnSum (D (2*j+1)) (W (2*j+1)) width = 6)) : False := by
  let q := columnSum (D 0) (W 0)
  have hrep := numeric_representation n D W hc
  have hw' : ∀ j, width < widthAt q (W 0) (2*j) ∧
      width < widthAt q (W 0) (2*j+1) := by
    intro j
    rw [(hrep (2*j)).1, (hrep (2*j+1)).1]
    exact hw j
  have hcarry : ∀ t, carry (qAt q (W 0) t) (widthAt q (W 0) t) =
      carry (columnSum (D t) (W t)) (W t) := by
    intro t
    rw [(hrep t).1]
    exact carry_congr_upto _ _ _ (hrep t).2 _ (by omega)
  apply Agent112.TwoPhase.no_actual_persistent_alternating_band q (W 0) width
    (NormalizationBridge.canonical_admissible n (D 0) (W 0) (hc 0)) hp hw'
    (by intro j; rw [hcarry (2*j), hcarry (2*j+1)]; exact hg j)
  rcases ht with ht | ht
  · left
    intro j
    rw [(hrep (2*j)).2 (width-1) (by have := (hw j).1; omega),
      (hrep (2*j)).2 width (hw j).1,
      (hrep (2*j+1)).2 (width-1) (by have := (hw j).2; omega),
      (hrep (2*j+1)).2 width (hw j).2]
    exact ht j
  · right
    intro j
    rw [(hrep (2*j)).2 (width-1) (by have := (hw j).1; omega),
      (hrep (2*j)).2 width (hw j).1,
      (hrep (2*j+1)).2 (width-1) (by have := (hw j).2; omega),
      (hrep (2*j+1)).2 width (hw j).2]
    exact ht j

def digits15 (i : Nat) : Nat := if i = 0 then 5 else if i = 1 then 1 else 0

def digits1330 (i : Nat) : Nat :=
  if i = 0 then 0 else if i = 1 ∨ i = 2 then 3 else if i = 3 then 1 else 0

theorem canonical15 : Canonical 15 digits15 2 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i _
  unfold digits15
  split
  · decide
  · split <;> decide

theorem canonical1330 : Canonical 1330 digits1330 4 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i _
  unfold digits1330
  split
  · decide
  · split
    · decide
    · split <;> decide

/-- Nonvacuity control for the finite prefix theorem: 15 has one actual
alternating-overflow pair and the stated band, but its prefix does not return. -/
theorem finite_scope_control :
    step 15 = 66 ∧ step 66 = 132 ∧
    let q := columnSum digits15 2
    carry (qAt q 2 0) (widthAt q 2 0) = 0 ∧
    carry (qAt q 2 1) (widthAt q 2 1) = 1 ∧
    qAt q 2 0 0 = 6 ∧ qAt q 2 0 1 = 6 ∧
    qAt q 2 1 0 = 12 ∧ qAt q 2 1 1 = 12 ∧
    qAt q 2 2 0 = 3 := by decide

/-- Adjacent band phases 6 then12 do NOT imply alternating overflows.
The concrete ordinary orbit 1330 -> 1661 -> 3322 has two successive
nonoverflow steps while the same middle two pair-sum columns read6 then12. -/
theorem phase_alone_not_overflow_alternation :
    step 1330 = 1661 ∧ step 1661 = 3322 ∧
    let q := columnSum digits1330 4
    carry (qAt q 4 0) (widthAt q 4 0) = 0 ∧
    carry (qAt q 4 1) (widthAt q 4 1) = 0 ∧
    qAt q 4 0 1 = 6 ∧ qAt q 4 0 2 = 6 ∧
    qAt q 4 1 1 = 12 ∧ qAt q 4 1 2 = 12 := by decide

#print axioms numeric_representation
#print axioms no_numeric_persistent_alternating_band
#print axioms canonical15
#print axioms canonical1330
#print axioms finite_scope_control
#print axioms phase_alone_not_overflow_alternation

end Agent112.TwoPhase.Numeric
