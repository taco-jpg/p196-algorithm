import Agent107TransducerPath

/-!
Reverse interpretation of a complete accepting input. An accepting path
reads only the lower folded half and optional center. Its unexamined high
half must therefore be reconstructed, not silently assumed symmetric.
The original `valid_word_realizable` theorem supplies an ordinary positive
finite integer once these exact accepted-input conditions are established.
-/

namespace Agent107.FoldedTransducer

open DecimalDigits FoldedDecimal

def symmetrize (L : Nat) (q : Nat → Nat) (i : Nat) : Nat :=
  if i ≤ L - 1 - i then q i else q (L - 1 - i)

theorem symmetrize_eq_min (L : Nat) (q : Nat → Nat) (i : Nat) :
    symmetrize L q i = q (min i (L - 1 - i)) := by
  unfold symmetrize
  by_cases h : i ≤ L - 1 - i
  · simp [h, Nat.min_eq_left h]
  · have hr : L - 1 - i ≤ i := by omega
    simp [h, Nat.min_eq_right hr]

theorem symmetrize_pair (L : Nat) (q : Nat → Nat)
    (i : Nat) (hi : i < L / 2) : symmetrize L q i = q i := by
  have he : i ≤ L - 1 - i := by omega
  simp [symmetrize, he]

theorem symmetrize_center (L : Nat) (q : Nat → Nat)
    (hodd : L % 2 ≠ 0) : symmetrize L q (L / 2) = q (L / 2) := by
  have he : L / 2 ≤ L - 1 - L / 2 := by omega
  simp [symmetrize, he]

theorem symmetrize_symmetric (L : Nat) (q : Nat → Nat)
    (i : Nat) (hi : i < L) :
    symmetrize L q i = symmetrize L q (L - 1 - i) := by
  have he : L - 1 - (L - 1 - i) = i := by omega
  rw [symmetrize_eq_min, symmetrize_eq_min, he, Nat.min_comm]

theorem inputCenter_symmetrize (L : Nat) (q : Nat → Nat) :
    inputCenter L (symmetrize L q) = inputCenter L q := by
  by_cases he : L % 2 = 0
  · simp [inputCenter, he]
  · simp [inputCenter, he, symmetrize_center L q he]

/-- The acceptance relation itself, including its center, reads exactly
the coefficients preserved by reconstruction. -/
theorem accepts_symmetrize (L : Nat) (q : Nat → Nat) (p : Nat → State) :
    Accepts L (symmetrize L q) p ↔ Accepts L q p := by
  constructor
  · intro hp
    refine ⟨hp.1, ?_, ?_⟩
    · intro i hi
      simpa only [symmetrize_pair L q i hi] using hp.2.1 i hi
    · simpa only [inputCenter_symmetrize] using hp.2.2
  · intro hp
    refine ⟨hp.1, ?_, ?_⟩
    · intro i hi
      simpa only [symmetrize_pair L q i hi] using hp.2.1 i hi
    · simpa only [inputCenter_symmetrize] using hp.2.2

theorem foldPrefix_symmetrize (L : Nat) (q : Nat → Nat) :
    foldPrefix L (symmetrize L q) = foldPrefix L q := by
  unfold foldPrefix
  rw [inputCenter_symmetrize]
  congr 1
  funext i
  exact symmetrize_pair L q i.val i.isLt

theorem pathOutput_symmetrize (L : Nat) (q : Nat → Nat) (p : Nat → State) :
    pathOutput L (symmetrize L q) p = pathOutput L q p := by
  unfold pathOutput
  rw [inputCenter_symmetrize]
  congr 2
  funext i
  rw [symmetrize_pair L q i.val i.isLt]

theorem accepting_width_positive (L : Nat) (q : Nat → Nat)
    (p : Nat → State) (hp : Accepts L q p) : 0 < L := by
  by_cases hL : 0 < L
  · exact hL
  · have he : L = 0 := by omega
    subst L
    obtain ⟨h, _, hs⟩ := hp.1
    have ht := hp.2.2
    simp [Terminal, inputCenter, hs, initial] at ht

theorem accepting_outer_positive (L : Nat) (q : Nat → Nat)
    (p : Nat → State) (hp : Accepts L q p) : 0 < q 0 := by
  obtain ⟨h, _, hs⟩ := hp.1
  by_cases hk : 0 < L / 2
  · exact (hp.2.1 0 hk).2.1 (by simp [hs, initial])
  · have hL := accepting_width_positive L q p hp
    have he : L = 1 := by omega
    have ht := hp.2.2
    simp [he, inputCenter, Terminal, hs, initial] at ht
    exact ht.1

theorem accepting_center_valid (L : Nat) (q : Nat → Nat)
    (p : Nat → State) (hp : Accepts L q p) (hodd : L % 2 ≠ 0) :
    q (L / 2) ≤ 18 ∧ q (L / 2) % 2 = 0 := by
  have ht := hp.2.2
  simp only [Terminal, inputCenter, hodd, if_false] at ht
  exact ⟨ht.2.1, ht.2.2.1⟩

/-- No hypothesis on the original unexamined high half is required. -/
theorem reconstructed_admissible (L : Nat) (q : Nat → Nat)
    (p : Nat → State) (hp : Accepts L q p) :
    Admissible L (symmetrize L q) := by
  have hL := accepting_width_positive L q p hp
  have ho := accepting_outer_positive L q p hp
  refine ⟨hL, ?_, ?_, symmetrize_symmetric L q, ?_⟩
  · simpa [symmetrize] using ho
  · intro i hi
    rw [symmetrize_eq_min]
    let j := min i (L - 1 - i)
    have hj : j ≤ L / 2 := by dsimp [j]; omega
    by_cases hjlt : j < L / 2
    · exact (hp.2.1 j hjlt).1
    · have hje : j = L / 2 := by omega
      have hodd : L % 2 ≠ 0 := by dsimp [j] at hjlt; omega
      change q j ≤ 18
      rw [hje]
      exact (accepting_center_valid L q p hp hodd).1
  · intro i hi he
    have hodd : L % 2 ≠ 0 := by omega
    have hik : i = L / 2 := by omega
    rw [hik, symmetrize_center L q hodd]
    exact (accepting_center_valid L q p hp hodd).2

/-- Every complete accepting folded input is represented by an actual
positive finite canonical decimal integer, after reconstructing its high
half. This instantiates the old realizability theorem with premises derived
from literal acceptance; it assumes no symmetry of the unread input data. -/
theorem accepting_input_realizable (L : Nat) (q : Nat → Nat)
    (p : Nat → State) (hp : Accepts L q p) :
    ∃ n d, 0 < n ∧ Canonical n d L ∧
      (∀ i, i < L → columnSum d L i = symmetrize L q i) ∧
      Accepts L (symmetrize L q) p ∧
      foldPrefix L (symmetrize L q) = foldPrefix L q ∧
      pathOutput L (symmetrize L q) p = pathOutput L q p := by
  have ha := reconstructed_admissible L q p hp
  obtain ⟨n, d, hn, hc, hr⟩ := valid_word_realizable (symmetrize L q) L
    ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2
  exact ⟨n, d, hn, hc, hr, (accepts_symmetrize L q p).2 hp,
    foldPrefix_symmetrize L q, pathOutput_symmetrize L q p⟩

#print axioms symmetrize_eq_min
#print axioms symmetrize_pair
#print axioms symmetrize_center
#print axioms symmetrize_symmetric
#print axioms inputCenter_symmetrize
#print axioms accepts_symmetrize
#print axioms foldPrefix_symmetrize
#print axioms pathOutput_symmetrize
#print axioms accepting_width_positive
#print axioms accepting_outer_positive
#print axioms accepting_center_valid
#print axioms reconstructed_admissible
#print axioms accepting_input_realizable

end Agent107.FoldedTransducer
