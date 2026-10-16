import TerminatingCountermap
import FixedTarget

/-!
Agent #122. Quantitative growth of the same total countermap, not a claim
that its trajectories equal actual reverse-and-add trajectories.
Existing positive-reversal and true-orbit growth results are reused.
-/
namespace Agent122.Countermodel

open Lychrel196 DecimalDigits DecimalQuantitativeMass ModularAutonomy FoldedDecimal

/-- The canonical exit has exactly one more digit than its final chain node. -/
theorem terminal_width (a k : Nat) (ha : 3 ≤ a) :
    decimalLength (terminal a k) = a+k+2 := by
  have hp : 0 < 10^(a+k+1) := Nat.pow_pos (by decide)
  have ht : 10 ≤ 10^(a+k+1) :=
    Nat.pow_le_pow_right (by decide : 0 < 10) (show 1 ≤ a+k+1 by omega)
  obtain ⟨d,hc⟩ := canonical_of_pow_bounds (terminal a k) (a+k+2) (by omega)
    (by simpa [terminal, show a+k+2-1 = a+k+1 by omega] using
      (Nat.le_add_right (10^(a+k+1)) 2))
    (by unfold terminal; rw [show a+k+2 = (a+k+1)+1 by omega, Nat.pow_succ]; omega)
  exact decimalLength_of_canonical _ _ _ hc

/-- Convenience bounds specialized to the actual decimalLength definition. -/
theorem positive_width_bounds (n : Nat) (hn : 0 < n) :
    10^(decimalLength n-1) ≤ n ∧ n < 10^(decimalLength n) := by
  obtain ⟨d,L,hc⟩ := canonical_exists n hn
  rw [decimalLength_of_canonical n d L hc]
  exact canonical_pow_bounds n d L hc

/-- Replication of the elementary order fact, using the pinned canonical API. -/
theorem positive_width_mono (n m : Nat) (hn : 0 < n) (h : n ≤ m) :
    decimalLength n ≤ decimalLength m := by
  have hm : 0 < m := by omega
  have bn := positive_width_bounds n hn
  have bm := positive_width_bounds m hm
  have hp : 10^(decimalLength n-1) < 10^(decimalLength m) := by omega
  have he := (Nat.pow_lt_pow_iff_right (by decide : 1 < 10)).mp hp
  omega

/-- The actual map can preserve the width or add just one digit. -/
theorem actual_step_width (n : Nat) (hn : 0 < n) :
    decimalLength (step n) = decimalLength n ∨
    decimalLength (step n) = decimalLength n+1 := by
  obtain ⟨d,L,hc⟩ := canonical_exists n hn
  rw [decimalLength_of_canonical n d L hc]
  rcases actual_overflow_cases d L hc.2.1 with h | h
  · exact Or.inl (decimalLength_of_canonical _ _ _ (canonical_next_no_overflow n d L hc h))
  · exact Or.inr (decimalLength_of_canonical _ _ _ (canonical_next_overflow n d L hc h))

theorem actual_step_lt_eleven (n : Nat) (hn : 0 < n) : step n < 11*n := by
  obtain ⟨d,L,hc⟩ := canonical_exists n hn
  have hL := hc.1
  have hlo := (canonical_pow_bounds n d L hc).1
  have hr : reverse10 n < 10^L := by
    rw [← hc.2.2.2, reverse10_value d L hc.2.1 (Or.inr hc.2.2.1)]
    apply value_lt_pow
    intro i hi
    exact hc.2.1 (L-1-i) (by omega)
  rw [show L = (L-1)+1 by omega, Nat.pow_succ] at hr
  unfold step
  omega

/-- Every modified (non-B) step increases width by exactly one. -/
theorem F_width_outside_B (ell : Nat → Nat) (n : Nat) (hn : 0 < n) (hb : ¬ B n) :
    decimalLength (F ell n) = decimalLength n+1 := by
  classical
  by_cases hc : IsNode ell n
  · obtain ⟨⟨a,j⟩,ha,hj,heq⟩ := hc
    change n = node a j at heq
    change 3 ≤ a at ha
    change j ≤ ell a at hj
    rw [heq, F_node ell a j ha hj, node_width a j ha]
    split
    · rw [node_width a (j+1) ha]
      omega
    · have he : j = ell a := by omega
      rw [terminal_width a (ell a) ha, he]
  · rw [F_generic ell n hb hc]
    split
    · rename_i hw
      have he : decimalLength 19 = 2 := by simp [decimalLength]
      rw [he, hw]
    · split
      · rename_i h1 hw
        have he : decimalLength 109 = 3 := by simp [decimalLength]
        rw [he, hw]
      · have hp := decimalLength_positive n hn
        rw [node_width (decimalLength n) 0 (by omega)]

theorem F_width_bounds (ell : Nat → Nat) (n : Nat) (hn : 0 < n) :
    decimalLength n ≤ decimalLength (F ell n) ∧
    decimalLength (F ell n) ≤ decimalLength n+1 := by
  classical
  by_cases hb : B n
  · rw [F_of_B ell n hb]
    have h := actual_step_width n hn
    omega
  · rw [F_width_outside_B ell n hn hb]
    omega

private theorem marker_lt_previous_shift (k : Nat) :
    10*(k+3)+9 < 10^(k+2) := by
  induction k with
  | zero => decide
  | succ k ih =>
    rw [show k+1+2 = (k+2)+1 by omega, Nat.pow_succ]
    omega

theorem marker_lt_previous (a : Nat) (ha : 3 ≤ a) : 10*a+9 < 10^(a-1) := by
  obtain ⟨k,rfl⟩ := Nat.exists_eq_add_of_le ha
  simpa only [Nat.add_comm 3 k, show k+3-1 = k+2 by omega] using marker_lt_previous_shift k

theorem F_numeric_growth (ell : Nat → Nat) (n : Nat) (hn : 0 < n) :
    n < F ell n ∧ F ell n < 11*n := by
  classical
  by_cases hb : B n
  · rw [F_of_B ell n hb]
    exact ⟨P196.Agent12.FixedTarget.step_strictly_increases n hn,
      actual_step_lt_eleven n hn⟩
  · have hg := F_width_outside_B ell n hn hb
    have hinc : n < F ell n := by
      apply Classical.byContradiction
      intro h
      have hm := positive_width_mono (F ell n) n (F_positive ell n hn) (by omega)
      omega
    refine ⟨hinc, ?_⟩
    by_cases hc : IsNode ell n
    · obtain ⟨⟨a,j⟩,ha,hj,heq⟩ := hc
      change n = node a j at heq
      change 3 ≤ a at ha
      change j ≤ ell a at hj
      rw [heq, F_node ell a j ha hj]
      split
      · unfold node
        rw [show a+(j+1) = (a+j)+1 by omega, Nat.pow_succ]
        omega
      · have he : j = ell a := by omega
        rw [he]
        unfold terminal node
        rw [Nat.pow_succ]
        omega
    · have hw := positive_width_bounds n hn
      rw [F_generic ell n hb hc]
      split
      · have hn1 : n ≠ 1 := by
          intro h
          subst n
          exact hb (by decide)
        omega
      · split
        · rename_i h1 h2
          rw [h2] at hw
          simp at hw
          omega
        · have hp := decimalLength_positive n hn
          have hm := marker_lt_previous (decimalLength n) (by omega)
          have he : decimalLength n = (decimalLength n-1)+1 := by omega
          unfold node
          simp only [Nat.add_zero]
          rw [he, Nat.pow_succ]
          omega

theorem run_width_mono (ell : Nat → Nat) (n s t : Nat) (hn : 0 < n) (hst : s ≤ t) :
    decimalLength (run ell n s) ≤ decimalLength (run ell n t) := by
  obtain ⟨k,rfl⟩ := Nat.exists_eq_add_of_le hst
  induction k with
  | zero => simp
  | succ k ih =>
    have h := (F_width_bounds ell (run ell n (s+k)) (run_positive ell n (s+k) hn)).1
    change decimalLength (run ell n s) ≤ decimalLength (F ell (run ell n (s+k)))
    omega

/-- If a finite countermap prefix only uses B inputs, it is a true RAA prefix. -/
theorem run_eq_actual_of_B_prefix (ell : Nat → Nat) (n t : Nat)
    (hB : ∀ k, k < t → B (run ell n k)) : run ell n t = orbit n t := by
  induction t with
  | zero => rfl
  | succ t ih =>
    rw [run, F_of_B ell _ (hB t (by omega)), ih (by intro k hk; exact hB k (by omega))]
    rfl

/-- Every five countermap steps increase decimal width by at least one. -/
theorem F_five_steps_increase_width (ell : Nat → Nat) (n : Nat) (hn : 0 < n) :
    decimalLength n+1 ≤ decimalLength (run ell n 5) := by
  classical
  apply Classical.byContradiction
  intro h
  have hmono := run_width_mono ell n 0 5 hn (by decide)
  have heq : decimalLength (run ell n 5) = decimalLength n := by
    change decimalLength n ≤ decimalLength (run ell n 5) at hmono
    omega
  have hB : ∀ k, k < 5 → B (run ell n k) := by
    intro k hk
    apply Classical.byContradiction
    intro hb
    have hg := F_width_outside_B ell (run ell n k) (run_positive ell n k hn) hb
    have hm1 := run_width_mono ell n 0 k hn (by omega)
    have hm2 := run_width_mono ell n (k+1) 5 hn (by omega)
    change decimalLength n ≤ decimalLength (run ell n k) at hm1
    change decimalLength (F ell (run ell n k)) ≤ decimalLength (run ell n 5) at hm2
    omega
  have hr := run_eq_actual_of_B_prefix ell n 5 hB
  have ht := DecimalFiniteAncestry.numeric_width_five_floor n 5 hn
  rw [← hr] at ht
  omega

/-- The historical countermodel's all-time lower width clock, fully discharged. -/
theorem run_width_five_floor (ell : Nat → Nat) (n t : Nat) (hn : 0 < n) :
    decimalLength n+t/5 ≤ decimalLength (run ell n t) := by
  have hblock : ∀ k, decimalLength n+k ≤ decimalLength (run ell n (5*k)) := by
    intro k
    induction k with
    | zero => simp [run]
    | succ k ih =>
      have h := F_five_steps_increase_width ell (run ell n (5*k)) (run_positive ell n _ hn)
      rw [← run_add] at h
      have he : 5*(k+1) = 5*k+5 := by omega
      rw [he]
      omega
  have hb := hblock (t/5)
  have hm := run_width_mono ell n (5*(t/5)) t hn (by omega)
  omega

end Agent122.Countermodel
