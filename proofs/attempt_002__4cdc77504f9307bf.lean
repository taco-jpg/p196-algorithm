import RegenerationGate

/-! Actual decimal semantics and safety of the all-gap +4 regeneration gate.
The exact carry and update cover every natural gap, including zero.
No recurrent closure or decimal Lychrel existence is claimed. -/

namespace RegenerationGate

open DecimalDigits FoldedDecimal IntrinsicSeam

theorem actual_carry (g i : Nat) : carry (source g) i = incoming g i := by
  induction i with
  | zero => exact (incoming_zero g).symm
  | succ i ih =>
      have he := exact_column_equation g i
      have hd := normalized_bounded g i
      simp only [carry, ih]
      omega

theorem actual_output (g i : Nat) : output (source g) i = normalized g i := by
  have he := exact_column_equation g i
  have hd := normalized_bounded g i
  simp only [output, actual_carry]
  omega

theorem no_overflow (g : Nat) : carry (source g) (width g) = 0 := by
  rw [actual_carry, incoming_terminal]

theorem actual_width (g : Nat) : nextWidth (source g) (width g) = width g := by
  simp only [nextWidth, no_overflow, if_true]

theorem source_symmetric (g i : Nat) (hi : i < width g) :
    source g i = source g (width g - 1 - i) := by
  let j := width g - 1 - i
  have hj : j = 2 * g + 18 - i := by simp [j, width]
  have hib : i < 2 * g + 19 := hi
  have h1 : (i = 0 ∨ i = 2 * g + 18) ↔ (j = 0 ∨ j = 2 * g + 18) := by omega
  have h9 : (i = 1 ∨ i = 2 * g + 17 ∨ (6 ≤ i ∧ i < g + 6) ∨
      (g + 13 ≤ i ∧ i < 2 * g + 13)) ↔
      (j = 1 ∨ j = 2 * g + 17 ∨ (6 ≤ j ∧ j < g + 6) ∨
      (g + 13 ≤ j ∧ j < 2 * g + 13)) := by omega
  have h12 : (i = 2 ∨ i = 2 * g + 16) ↔ (j = 2 ∨ j = 2 * g + 16) := by omega
  have h3 : (i = 3 ∨ i = 2 * g + 15) ↔ (j = 3 ∨ j = 2 * g + 15) := by omega
  have h14 : (i = 4 ∨ i = 5 ∨ i = 2 * g + 13 ∨ i = 2 * g + 14) ↔
      (j = 4 ∨ j = 5 ∨ j = 2 * g + 13 ∨ j = 2 * g + 14) := by omega
  have h4 : (i = g + 6 ∨ i = g + 7 ∨ i = g + 11 ∨ i = g + 12) ↔
      (j = g + 6 ∨ j = g + 7 ∨ j = g + 11 ∨ j = g + 12) := by omega
  have h15 : (i = g + 8 ∨ i = g + 10) ↔ (j = g + 8 ∨ j = g + 10) := by omega
  have h10 : i = g + 9 ↔ j = g + 9 := by omega
  change source g i = source g j
  simp only [source, h1, h9, h12, h3, h14, h4, h15, h10]

theorem source_center (g : Nat) : source g (g + 9) = 10 := by
  unfold source
  repeat first | omega | split

theorem source_admissible (g : Nat) : Admissible (width g) (source g) := by
  refine ⟨by unfold width; omega, by simp [source],
    (fun i _ => source_bounded g i), source_symmetric g, ?_⟩
  intro i hi heq
  have he : i = g + 9 := by unfold width at hi heq; omega
  subst i
  rw [source_center]

theorem target_symmetric (g i : Nat) (hi : i < width g) :
    target g i = target g (width g - 1 - i) := by
  let j := width g - 1 - i
  have hj : j = 2 * g + 18 - i := by simp [j, width]
  have hib : i < 2 * g + 19 := hi
  have h3 : (i = 0 ∨ i = 2 * g + 18) ↔ (j = 0 ∨ j = 2 * g + 18) := by omega
  have h9 : (i = 1 ∨ i = 2 * g + 17 ∨ (4 ≤ i ∧ i < g + 8) ∨
      (g + 11 ≤ i ∧ i < 2 * g + 15)) ↔
      (j = 1 ∨ j = 2 * g + 17 ∨ (4 ≤ j ∧ j < g + 8) ∨
      (g + 11 ≤ j ∧ j < 2 * g + 15)) := by omega
  have h4 : (i = 2 ∨ i = 2 * g + 16) ↔ (j = 2 ∨ j = 2 * g + 16) := by omega
  have h8 : (i = 3 ∨ i = 2 * g + 15) ↔ (j = 3 ∨ j = 2 * g + 15) := by omega
  have h11 : (i = g + 8 ∨ i = g + 10) ↔ (j = g + 8 ∨ j = g + 10) := by omega
  have h2 : i = g + 9 ↔ j = g + 9 := by omega
  change target g i = target g j
  simp only [target, h3, h9, h4, h8, h11, h2]

set_option maxHeartbeats 1000000 in
theorem left_pair_equation (g i : Nat) (hi : i ≤ g + 9) :
    normalized g i + normalized g (width g - 1 - i) = target g i := by
  have hcases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨
      (6 ≤ i ∧ i < g + 6) ∨ i = g + 6 ∨ i = g + 7 ∨ i = g + 8 ∨ i = g + 9 := by omega
  rcases hcases with h | h | h | h | h | h | h | h | h | h | h
  all_goals (try subst i)
  all_goals simp (disch := omega) [normalized, target, width]
  all_goals (repeat first | omega | split)

theorem exact_pair_equation (g i : Nat) (hi : i < width g) :
    columnSum (normalized g) (width g) i = target g i := by
  by_cases hleft : i ≤ g + 9
  · exact left_pair_equation g i hleft
  · have hm : width g - 1 - i ≤ g + 9 := by unfold width at hi ⊢; omega
    have he := left_pair_equation g (width g - 1 - i) hm
    have hdouble : width g - 1 - (width g - 1 - i) = i := by omega
    rw [hdouble] at he
    rw [target_symmetric g i hi]
    simpa only [columnSum, reflected, Nat.add_comm] using he

/-- The exact actual successor is the target with both gaps enlarged by four. -/
theorem actual_update (g i : Nat) (hi : i < width g) :
    nextColumns (source g) (width g) i = target g i := by
  simp only [nextColumns, no_overflow, if_true, columnSum, reflected, actual_output]
  exact exact_pair_equation g i hi

end RegenerationGate
