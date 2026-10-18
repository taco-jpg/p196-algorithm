import P196.Drafts.D20261015ExternalIntrinsicReviewSources.IntrinsicSeam

/-!
An arbitrary-width counterfamily to persistence of nonzero seam defects.
The word (10,9^k,10) has k singleton defect coefficients equal to one.
For k>0 its next pair word is (1,1,0^(k-1),1,1), which is already in the
exact immediate-palindrome predecessor class. Even k gives canonical
pair words, so every canonical decimal realization reaches a palindrome
after exactly two updates, despite arbitrarily many initial seam defects.
-/

namespace SeamAnnihilation

open DecimalDigits RawSymmetryObstruction IntrinsicSeam FoldedDecimal

/-- Two coefficients 10 enclose k coefficients 9; width is k+2. -/
def framedNine (k i : Nat) : Nat := if i = 0 ∨ i = k + 1 then 10 else 9

/-- The exact next pair word when k>0; width is k+3. -/
def nextFrame (k i : Nat) : Nat :=
  if i = 0 ∨ i = 1 ∨ i = k + 1 ∨ i = k + 2 then 1 else 0

/-- Sum of outgoing seam-defect coefficients in a finite prefix. -/
def defectMass (q : Nat → Nat) (cut : Nat → Bool) : Nat → Int
  | 0 => 0
  | n + 1 => defectMass q cut n + seamDefect q cut n

theorem framedNine_bounded (k i : Nat) : framedNine k i ≤ 18 := by
  simp only [framedNine]
  split <;> omega

theorem framedNine_carry (k i : Nat) :
    carry (framedNine k) i = if i = 0 then 0 else 1 := by
  induction i with
  | zero => simp [carry]
  | succ i ih =>
      by_cases hz : i = 0
      · subst i
        simp [carry, framedNine]
      · have hp : carry (framedNine k) i = 1 := by simpa [hz] using ih
        simp only [carry, hp, framedNine]
        split <;> simp

theorem framedNine_output (k i : Nat) :
    output (framedNine k) i = if i = k + 1 then 1 else 0 := by
  simp only [output, framedNine_carry, framedNine]
  split <;> split <;> split <;> simp_all <;> omega

theorem framedNine_extended (k i : Nat) :
    extended (framedNine k) (k + 2) i =
      if i = k + 1 ∨ k + 2 ≤ i then 1 else 0 := by
  simp only [extended, framedNine_output, framedNine_carry]
  split <;> split <;> (try split) <;> simp_all <;> omega

theorem framedNine_nextWidth (k : Nat) :
    nextWidth (framedNine k) (k + 2) = k + 3 := by
  simp [nextWidth, framedNine_carry]

/-- Exact one-update transport, valid at every finite width in the family. -/
theorem framedNine_nextColumns (k i : Nat) (hk : 0 < k) (hi : i < k + 3) :
    nextColumns (framedNine k) (k + 2) i = nextFrame k i := by
  have hc : carry (framedNine k) (k + 2) = 1 := by simp [framedNine_carry]
  simp only [nextColumns, hc, Nat.one_ne_zero, if_false, columnSum, reflected,
    framedNine_extended, nextFrame]
  split <;> split <;> split <;> omega

theorem nextFrame_small (k i : Nat) : nextFrame k i ≤ 1 := by
  simp only [nextFrame]
  split <;> omega

theorem framedNine_next_small (k i : Nat) :
    nextColumns (framedNine k) (k + 2) i ≤ 2 := by
  have hc : carry (framedNine k) (k + 2) = 1 := by simp [framedNine_carry]
  simp only [nextColumns, hc, Nat.one_ne_zero, if_false, columnSum, reflected,
    framedNine_extended]
  split <;> split <;> omega

theorem framedNine_singleton_defect (k i : Nat) :
    seamDefect (framedNine k) (fun _ => true) i =
      if i = 0 ∨ i = k + 1 then 0 else 1 := by
  simp only [seamDefect, singleton_resetOut, framedNine_carry, framedNine]
  split <;> split <;> simp_all <;> omega

theorem framedNine_prefix_mass (k n : Nat) (hn : n ≤ k) :
    defectMass (framedNine k) (fun _ => true) (n + 1) = (n : Int) := by
  induction n with
  | zero => simp [defectMass, framedNine_singleton_defect]
  | succ n ih =>
      have hp := ih (by omega)
      rw [defectMass, hp, framedNine_singleton_defect]
      have hr : ¬ (n + 1 = 0 ∨ n + 1 = k + 1) := by omega
      simp only [if_neg hr, Int.natCast_add, Int.natCast_one]

/-- The whole initial singleton seam mass is exactly k, with no bound on k. -/
theorem framedNine_mass (k : Nat) :
    defectMass (framedNine k) (fun _ => true) (k + 2) = (k : Int) := by
  have hp := framedNine_prefix_mass k k (Nat.le_refl k)
  change defectMass (framedNine k) (fun _ => true) ((k + 1) + 1) = (k : Int)
  rw [defectMass, hp, framedNine_singleton_defect]
  simp

theorem framedNine_highNine (k : Nat) (hk : 0 < k) :
    HighNine (framedNine k) (k + 2) := by
  refine ⟨0, by omega, ?_, ?_⟩
  · simp [framedNine]
  · simp only [Nat.zero_add, framedNine]
    split <;> omega

/-- After one update every partition has identically zero seam defect. -/
theorem framedNine_next_every_defect_zero (k : Nat) (cut : Nat → Bool) (i : Nat)
    (hi : i < nextWidth (framedNine k) (k + 2)) :
    seamDefect (nextColumns (framedNine k) (k + 2)) cut i = 0 := by
  have hb : ∀ j, j < nextWidth (framedNine k) (k + 2) →
      nextColumns (framedNine k) (k + 2) j ≤ 18 := by
    intro j _
    have h := framedNine_next_small k j
    omega
  have hn : ¬ HighNine (nextColumns (framedNine k) (k + 2))
      (nextWidth (framedNine k) (k + 2)) := by
    rintro ⟨j, _, hj, _⟩
    have h := framedNine_next_small k j
    omega
  exact (no_highNine_iff_every_defect_zero _ _ hb).mp hn cut i hi

/-- Even interior length makes the family a canonical mirrored pair word. -/
theorem framedNine_even_admissible (r : Nat) :
    Admissible (2 * r + 2) (framedNine (2 * r)) := by
  refine ⟨by omega, ?_, (fun i _ => framedNine_bounded _ i), ?_, ?_⟩
  · simp [framedNine]
  · intro i hi
    simp only [framedNine]
    split <;> split <;> omega
  · intro i hi heq
    omega

/-- Every ordinary realization of this word is safe once, then palindromic. -/
theorem framedNine_realization_two_steps (k n : Nat) (d : Nat → Nat)
    (hk : 0 < k) (hc : Canonical n d (k + 2))
    (hr : ∀ i, i < k + 2 → columnSum d (k + 2) i = framedNine k i) :
    ¬ Lychrel196.Palindrome (Lychrel196.step n) ∧
      Lychrel196.Palindrome (Lychrel196.step (Lychrel196.step n)) := by
  have hfirst : HighNine (columnSum d (k + 2)) (k + 2) := by
    obtain ⟨i, hi, hh, hn⟩ := framedNine_highNine k hk
    exact ⟨i, hi, by rw [hr i (by omega)]; exact hh, by rw [hr (i + 1) hi]; exact hn⟩
  refine ⟨numeric_highNine_safe n d (k + 2) hc hfirst, ?_⟩
  obtain ⟨e, he, hn⟩ := representation_next n d (framedNine k) (k + 2) hc hr
  rw [← he.2.2.2]
  apply (step_palindrome_iff e _ he.1 he.2.1 he.2.2.1).mpr
  left
  intro i hi
  rw [hn i hi]
  have h := framedNine_next_small k i
  omega

/-- Nonvacuity at every positive parameter: an actual finite decimal seed. -/
theorem even_family_realized (r : Nat) (hr : 0 < r) :
    ∃ n d, 0 < n ∧ Canonical n d (2 * r + 2) ∧
      (∀ i, i < 2 * r + 2 → columnSum d (2 * r + 2) i = framedNine (2 * r) i) ∧
      ¬ Lychrel196.Palindrome (Lychrel196.step n) ∧
      Lychrel196.Palindrome (Lychrel196.step (Lychrel196.step n)) := by
  obtain ⟨hL, ho, hb, hs, hm⟩ := framedNine_even_admissible r
  obtain ⟨n, d, hp, hc, hq⟩ := valid_word_realizable _ _ hL ho hb hs hm
  exact ⟨n, d, hp, hc, hq, framedNine_realization_two_steps (2 * r) n d
    (by omega) hc hq⟩

end SeamAnnihilation
