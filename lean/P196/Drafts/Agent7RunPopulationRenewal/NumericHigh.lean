import P196.Drafts.Agent7RunPopulationRenewal.HighCarryReduction

/-! The high-carry predicate as a property of an ordinary natural number.
Canonical decimal representations have a unique width and unique used digits,
so this predicate is independent of the chosen representing digit function.
The final equivalences connect it to the exact `iterPairs` numeric orbit. -/

namespace Agent105.NumericHigh

open DecimalDigits FoldedDecimal OverflowCarryNormalization Lychrel196
  HighCarryReduction

/-- An ordinary integer is high when its canonical decimal pair word is high. -/
def NumericHigh (n : Nat) : Prop :=
  ∃ d L, Canonical n d L ∧ HighCarryWord (columnSum d L) L

/-- Two canonical decimal representations of one number have the same width. -/
theorem canonical_width_eq (n : Nat) (d e : Nat → Nat) (L W : Nat)
    (hd : Canonical n d L) (he : Canonical n e W) : L = W := by
  exact (DecimalQuantitativeMass.decimalLength_of_canonical n d L hd).symm.trans
    (DecimalQuantitativeMass.decimalLength_of_canonical n e W he)

/-- The pair coefficients used by canonical representations are unique. -/
theorem canonical_columns_eq (n : Nat) (d e : Nat → Nat) (L W : Nat)
    (hd : Canonical n d L) (he : Canonical n e W) :
    ∀ i, i < L → columnSum d L i = columnSum e W i := by
  have hw := canonical_width_eq n d e L W hd he
  subst W
  have hdigits := value_injective d e L hd.2.1 he.2.1
    (hd.2.2.2.trans he.2.2.2.symm)
  intro i hi
  simp only [columnSum, reflected, hdigits i hi,
    hdigits (L - 1 - i) (by omega)]

/-- A nonempty finite word's high predicate uses only its in-range entries. -/
theorem highCarryWord_iff_of_eq (q r : Nat → Nat) (L : Nat) (hL : 0 < L)
    (hqr : ∀ i, i < L → q i = r i) :
    HighCarryWord q L ↔ HighCarryWord r L := by
  constructor
  · rintro ⟨hq, hzero⟩
    constructor
    · intro i hi
      rw [← hqr i hi]
      exact hq i hi
    · rw [← hqr 0 hL]
      exact hzero
  · rintro ⟨hr, hzero⟩
    constructor
    · intro i hi
      rw [hqr i hi]
      exact hr i hi
    · rw [hqr 0 hL]
      exact hzero

/-- The numeric predicate can be checked using any canonical representation. -/
theorem numericHigh_iff (n : Nat) (d : Nat → Nat) (L : Nat)
    (hd : Canonical n d L) :
    NumericHigh n ↔ HighCarryWord (columnSum d L) L := by
  constructor
  · rintro ⟨e, W, he, hhigh⟩
    have hw := canonical_width_eq n e d W L he hd
    subst W
    exact (highCarryWord_iff_of_eq (columnSum e L) (columnSum d L) L hd.1
      (canonical_columns_eq n e d L L he hd)).mp hhigh
  · intro hhigh
    exact ⟨d, L, hd, hhigh⟩

/-- A represented finite word is high exactly when its ordinary number is. -/
theorem numericHigh_iff_represented (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hd : Canonical n d L)
    (hrep : ∀ i, i < L → columnSum d L i = q i) :
    NumericHigh n ↔ HighCarryWord q L := by
  exact (numericHigh_iff n d L hd).trans
    (highCarryWord_iff_of_eq (columnSum d L) q L hd.1 hrep)

/-- Exact transfer between the integer orbit and its changing-width pair orbit. -/
theorem numericHigh_orbit_iff (n : Nat) (d q : Nat → Nat) (L t : Nat)
    (hd : Canonical n d L)
    (hrep : ∀ i, i < L → columnSum d L i = q i) :
    NumericHigh (orbit n t) ↔
      HighCarryWord (iterPairs q L t).2 (iterPairs q L t).1 := by
  obtain ⟨e, he, her⟩ := iterPairs_representation n d q L t hd hrep
  exact numericHigh_iff_represented (orbit n t) e (iterPairs q L t).2
    (iterPairs q L t).1 he her

/-- Canonical-column specialization, with no arbitrary pair representation. -/
theorem numericHigh_orbit_iff_columns (n : Nat) (d : Nat → Nat) (L t : Nat)
    (hd : Canonical n d L) :
    NumericHigh (orbit n t) ↔
      HighCarryWord (iterPairs (columnSum d L) L t).2
        (iterPairs (columnSum d L) L t).1 := by
  exact numericHigh_orbit_iff n d (columnSum d L) L t hd (fun _ _ => rfl)

#print axioms canonical_width_eq
#print axioms canonical_columns_eq
#print axioms highCarryWord_iff_of_eq
#print axioms numericHigh_iff
#print axioms numericHigh_iff_represented
#print axioms numericHigh_orbit_iff
#print axioms numericHigh_orbit_iff_columns

end Agent105.NumericHigh
