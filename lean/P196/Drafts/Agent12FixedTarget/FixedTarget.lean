import P196.Drafts.ResearchMainExistenceAttempt.FiniteAncestry

/-!
Agent #12. Exact numerical fixed-target ancestry bounds and a complete finite
list of ancestor/depth pairs. Source: FINITE_SEED_OBSTRUCTIONS.md section 4.
The existing, stronger width bound is reused, not claimed as new discovery.
The map is Lychrel196.step on ordinary decimal natural numbers. Its iteration
continues after a palindrome. Positive seeds and time zero are explicit.
-/
namespace P196.Agent12.FixedTarget

open Lychrel196 DecimalDigits DecimalQuantitativeMass DecimalFiniteAncestry

/-- A nonzero unprocessed input or accumulator gives a positive reversal. -/
theorem reverseAux_positive (n acc : Nat) (h : 0 < n ∨ 0 < acc) :
    0 < reverseAux n acc := by
  induction n using Nat.strongRecOn generalizing acc with
  | ind n ih =>
    by_cases hn : n = 0
    · subst n
      have ha : 0 < acc := by omega
      simpa [reverseAux] using ha
    · rw [reverseAux]
      simp only [hn, ↓reduceDIte]
      apply ih (n / 10) (Nat.div_lt_self (by omega) (by decide))
      have hd := Nat.mod_add_div n 10
      omega

theorem reverse10_positive (n : Nat) (hn : 0 < n) :
    0 < reverse10 n := by
  rw [reverse10, reverseFuel_correct n n 0 (by omega)]
  exact reverseAux_positive n 0 (Or.inl hn)

theorem step_strictly_increases (n : Nat) (hn : 0 < n) : n < step n := by
  have hp := reverse10_positive n hn
  simp only [step]
  omega

/-- At least one unit of numerical growth occurs at every actual step. -/
theorem orbit_ge_seed_add_time (n t : Nat) (hn : 0 < n) :
    n + t ≤ orbit n t := by
  induction t with
  | zero => simp [orbit]
  | succ t ih =>
    have hg := step_strictly_increases (orbit n t) (orbit_positive n hn t)
    simp only [orbit]
    omega

theorem ancestor_seed_add_depth_le (a p t : Nat) (ha : 0 < a)
    (hreach : orbit a t = p) : a + t ≤ p := by
  simpa [hreach] using orbit_ge_seed_add_time a t ha

theorem ancestor_numeric_depth_le (a p t : Nat) (ha : 0 < a)
    (hreach : orbit a t = p) : t ≤ p - 1 := by
  have h := ancestor_seed_add_depth_le a p t ha hreach
  omega

/-- The original report's floor inequality, with no postulated growth premise. -/
theorem ancestor_width_floor (a p t : Nat) (ha : 0 < a)
    (hreach : orbit a t = p) : 1 + t / 5 ≤ decimalLength p := by
  have hw := numeric_width_five_floor a t ha
  have hp := decimalLength_positive a ha
  rw [hreach] at hw
  omega

theorem ancestor_five_width_depth_le (a p t : Nat) (ha : 0 < a)
    (hreach : orbit a t = p) : t ≤ 5 * decimalLength p - 1 := by
  have hw := ancestor_width_floor a p t ha hreach
  omega

/-- This is exactly the quantitative depth bound advertised in section 4. -/
theorem ancestor_depth_min_bound (a p t : Nat) (ha : 0 < a)
    (hreach : orbit a t = p) :
    t ≤ min (p - 1) (5 * decimalLength p - 1) := by
  exact Nat.le_min.mpr ⟨ancestor_numeric_depth_le a p t ha hreach,
    ancestor_five_width_depth_le a p t ha hreach⟩

/-- Also record the stronger already available width contribution. -/
theorem ancestor_depth_stronger_bound (a p t : Nat) (ha : 0 < a)
    (hreach : orbit a t = p) :
    t ≤ min (p - 1) (4 * decimalLength p) := by
  exact Nat.le_min.mpr ⟨ancestor_numeric_depth_le a p t ha hreach,
    numeric_ancestor_depth_le a p t ha hreach⟩

def depthCap (p : Nat) : Nat := min (p - 1) (5 * decimalLength p - 1)

/-- All positive ancestors, with their depth, in a finite explicit rectangle.
The finite list is an exact enumeration, not a bounded substitute for ancestry. -/
def ancestorPairs (p : Nat) : List (Nat × Nat) :=
  ((List.range (p + 1)).flatMap fun a =>
    (List.range (depthCap p + 1)).map fun t => (a, t)).filter
      (fun pair => decide (0 < pair.1 ∧ orbit pair.1 pair.2 = p))

theorem mem_ancestorPairs (p a t : Nat) :
    (a, t) ∈ ancestorPairs p ↔ 0 < a ∧ orbit a t = p := by
  simp only [ancestorPairs, List.mem_filter, List.mem_flatMap, List.mem_map,
    List.mem_range, decide_eq_true_eq]
  constructor
  · rintro ⟨_, h⟩
    exact h
  · intro h
    have hnum := ancestor_seed_add_depth_le a p t h.1 h.2
    have hdepth := ancestor_depth_min_bound a p t h.1 h.2
    refine ⟨?_, h⟩
    exact ⟨a, by omega, t, by simpa [depthCap] using Nat.lt_succ_of_le hdepth, rfl⟩

/-- The complete inverse tree has finitely many (seed,depth) labels. -/
theorem finite_inverse_tree (p : Nat) :
    ∃ pairs : List (Nat × Nat), ∀ a t,
      (a, t) ∈ pairs ↔ 0 < a ∧ orbit a t = p := by
  exact ⟨ancestorPairs p, mem_ancestorPairs p⟩

theorem no_positive_ancestor_of_zero (a t : Nat) (ha : 0 < a) :
    orbit a t ≠ 0 := by
  have h := orbit_ge_seed_add_time a t ha
  omega

theorem initial_target_in_enumeration (p : Nat) (hp : 0 < p) :
    (p, 0) ∈ ancestorPairs p := by
  exact (mem_ancestorPairs p p 0).mpr ⟨hp, rfl⟩

end P196.Agent12.FixedTarget
