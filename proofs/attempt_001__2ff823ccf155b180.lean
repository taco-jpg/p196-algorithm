import RawSymmetryObstruction

/-!
Partition-free characterization of a nonzero decimal seam carry defect.

For arbitrary bounded coefficient words, some partition has a nonzero
defect exactly when a coefficient at least 10 is immediately followed by
9. The singleton partition maximizes every defect coefficient. No symmetry
or canonicality is needed for this characterization. Canonicality enters
only in the ordinary reverse-and-add safety bridge.
-/

namespace IntrinsicSeam

open DecimalDigits RawSymmetryObstruction

/-- A coefficient 9 receiving the actual whole-word carry one. -/
def ActiveNine (q : Nat → Nat) (L : Nat) : Prop :=
  ∃ i, i < L ∧ q i = 9 ∧ carry q i = 1

/-- An adjacent high coefficient followed by a 9, in low-to-high order. -/
def HighNine (q : Nat → Nat) (L : Nat) : Prop :=
  ∃ i, i + 1 < L ∧ 10 ≤ q i ∧ q (i + 1) = 9

theorem singleton_resetOut (q : Nat → Nat) (i : Nat) :
    resetOut q (fun _ => true) i = q i / 10 := by
  rw [resetOut_equation]
  simp [incoming]

theorem singleton_resetOut_minimal (q : Nat → Nat) (cut : Nat → Bool) (i : Nat) :
    resetOut q (fun _ => true) i ≤ resetOut q cut i := by
  rw [singleton_resetOut, resetOut_equation]
  omega

/-- Singleton blocks simultaneously maximize every outgoing-carry defect. -/
theorem singleton_defect_maximal (q : Nat → Nat) (cut : Nat → Bool) (i : Nat) :
    0 ≤ seamDefect q cut i ∧
      seamDefect q cut i ≤ seamDefect q (fun _ => true) i := by
  have ha := resetOut_le_actual q cut i
  have hs := singleton_resetOut_minimal q cut i
  simp only [seamDefect]
  constructor <;> omega

theorem singleton_defect_iff (q : Nat → Nat) (L i : Nat)
    (hb : ∀ j, j < L → q j ≤ 18) (hi : i < L) :
    seamDefect q (fun _ => true) i ≠ 0 ↔ q i = 9 ∧ carry q i = 1 := by
  have hq := hb i hi
  have hc := carry_bounded q L hb i (by omega)
  simp only [seamDefect, singleton_resetOut, carry]
  omega

theorem singleton_defect_one_iff (q : Nat → Nat) (L i : Nat)
    (hb : ∀ j, j < L → q j ≤ 18) (hi : i < L) :
    seamDefect q (fun _ => true) i = 1 ↔ q i = 9 ∧ carry q i = 1 := by
  have hq := hb i hi
  have hc := carry_bounded q L hb i (by omega)
  simp only [seamDefect, singleton_resetOut, carry]
  omega

/-- Quantification over all partitions reduces to the actual incoming carry. -/
theorem exists_defect_iff_activeNine (q : Nat → Nat) (L : Nat)
    (hb : ∀ j, j < L → q j ≤ 18) :
    (∃ cut i, i < L ∧ seamDefect q cut i ≠ 0) ↔ ActiveNine q L := by
  constructor
  · rintro ⟨cut, i, hi, hn⟩
    have hm := singleton_defect_maximal q cut i
    have hs : seamDefect q (fun _ => true) i ≠ 0 := by omega
    exact ⟨i, hi, (singleton_defect_iff q L i hb hi).mp hs⟩
  · rintro ⟨i, hi, hq, hc⟩
    exact ⟨(fun _ => true), i, hi,
      (singleton_defect_iff q L i hb hi).mpr ⟨hq, hc⟩⟩

/-- Following an active 9 backwards through its 9-run reaches an H9 edge. -/
theorem activeNine_iff_highNine (q : Nat → Nat) (L : Nat)
    (hb : ∀ j, j < L → q j ≤ 18) : ActiveNine q L ↔ HighNine q L := by
  constructor
  · have hback : ∀ i, i < L → q i = 9 → carry q i = 1 →
        ∃ j, j < i ∧ 10 ≤ q j ∧ q (j + 1) = 9 := by
      intro i
      induction i with
      | zero =>
          intro _ _ hc
          change 0 = 1 at hc
          omega
      | succ i ih =>
          intro hi hq hc
          by_cases hh : 10 ≤ q i
          · exact ⟨i, by omega, hh, hq⟩
          · have hp := carry_bounded q L hb i (by omega)
            have he : (q i + carry q i) / 10 = 1 := hc
            have hnine : q i = 9 := by omega
            have hone : carry q i = 1 := by omega
            obtain ⟨j, hj, hjq, hjn⟩ := ih (by omega) hnine hone
            exact ⟨j, by omega, hjq, hjn⟩
    rintro ⟨i, hi, hq, hc⟩
    obtain ⟨j, hj, hjq, hjn⟩ := hback i hi hq hc
    exact ⟨j, by omega, hjq, hjn⟩
  · rintro ⟨i, hi, hh, hn⟩
    have hq := hb i (by omega)
    have hc := carry_bounded q L hb i (by omega)
    refine ⟨i + 1, hi, hn, ?_⟩
    simp only [carry]
    omega

/-- Exact intrinsic characterization, with no partition search remaining. -/
theorem exists_defect_iff_highNine (q : Nat → Nat) (L : Nat)
    (hb : ∀ j, j < L → q j ≤ 18) :
    (∃ cut i, i < L ∧ seamDefect q cut i ≠ 0) ↔ HighNine q L := by
  exact (exists_defect_iff_activeNine q L hb).trans (activeNine_iff_highNine q L hb)

theorem no_highNine_iff_every_defect_zero (q : Nat → Nat) (L : Nat)
    (hb : ∀ j, j < L → q j ≤ 18) :
    ¬ HighNine q L ↔ ∀ cut i, i < L → seamDefect q cut i = 0 := by
  constructor
  · intro hn cut i hi
    by_contra hd
    exact hn ((exists_defect_iff_highNine q L hb).mp ⟨cut, i, hi, hd⟩)
  · intro hz hh
    obtain ⟨cut, i, hi, hd⟩ := (exists_defect_iff_highNine q L hb).mpr hh
    exact hd (hz cut i hi)

theorem highNine_not_bad (q : Nat → Nat) (L : Nat)
    (hb : ∀ j, j < L → q j ≤ 18) (hh : HighNine q L) :
    ¬ FoldedDecimal.BadWord L q := by
  obtain ⟨cut, i, hi, hd⟩ := (exists_defect_iff_highNine q L hb).mpr hh
  exact nonzero_defect_not_bad q cut L hb ⟨i, hi, hd⟩

/-- Ordinary one-step safety from a local H9 pattern in canonical pair sums. -/
theorem numeric_highNine_safe (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) (hh : HighNine (columnSum d L) L) :
    ¬ Lychrel196.Palindrome (Lychrel196.step n) := by
  obtain ⟨cut, i, hi, hd⟩ := (exists_defect_iff_highNine (columnSum d L) L
    (columnSum_bounded d L hc.2.1)).mpr hh
  exact numeric_nonzero_defect_safe n d L cut hc ⟨i, hi, hd⟩

end IntrinsicSeam
