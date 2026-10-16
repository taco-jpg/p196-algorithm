import EventualCorrespondence

namespace Agent112.Eventual
open Agent109
open Agent112.Admissibility

/-- An arbitrary finite coefficient bound, not necessarily the decimal pair bound. -/
def BoundedBy (w : Word) (B : Nat) : Prop := ∀ x ∈ w, x ≤ B

theorem norm_carry_bound (w : Word) (B e : Nat) (hw : BoundedBy w B) (he : e ≤ B / 9) :
    (norm w e).2 ≤ B / 9 := by
  induction w generalizing e with
  | nil => exact he
  | cons x xs ih =>
    change (norm xs ((x + e) / 10)).2 ≤ B / 9
    apply ih _ (fun y hy => hw y (by simp [hy]))
    have hx := hw x (by simp)
    omega

theorem normalize_bound (w : Word) (B : Nat) (hw : BoundedBy w B) :
    BoundedBy (normalize w 0) (max 9 (B / 9)) := by
  intro x hx
  rw [normalize_eq_norm] at hx
  rcases List.mem_append.mp hx with hx | hx
  · have := norm_digit_lt w 0 x hx
    omega
  · have hc := norm_carry_bound w B 0 hw (Nat.zero_le _)
    unfold carryWord at hx
    split at hx
    · simp at hx
    · simp only [List.mem_singleton] at hx
      omega

theorem pair_bound (D : Word) (B : Nat) (hD : BoundedBy D B) : BoundedBy (pair D) (2 * B) := by
  have aux : ∀ a b : Word, BoundedBy a B → BoundedBy b B → BoundedBy (zipAdd a b) (2 * B) := by
    intro a
    induction a with
    | nil => intro b ha hb; cases b <;> intro x hx <;> simp [zipAdd] at hx
    | cons a as ih =>
      intro b ha hb
      cases b with
      | nil => intro x hx; simp [zipAdd] at hx
      | cons b bs =>
        intro x hx
        simp only [zipAdd, List.mem_cons] at hx
        rcases hx with hx | hx
        · have h1 := ha a (by simp)
          have h2 := hb b (by simp)
          omega
        · exact ih bs (fun y hy => ha y (by simp [hy]))
            (fun y hy => hb y (by simp [hy])) x hx
  exact aux D D.reverse hD (fun x hx => hD x (List.mem_reverse.mp hx))

/-- A single symbolic step contracts every bound above 18. -/
theorem stepWord_contracts (w : Word) (B : Nat) (hw : BoundedBy w B) :
    BoundedBy (stepWord w) (2 * max 9 (B / 9)) :=
  pair_bound _ _ (normalize_bound w B hw)

theorem contracted_bound_lt (B : Nat) (hB : 18 < B) : 2 * max 9 (B / 9) < B := by
  omega

/-- Every finite natural-coefficient word enters the 0..18 coefficient domain,
without positivity, symmetry, or canonical-head assumptions. -/
theorem eventually_bounded_of_bound (B : Nat) (w : Word) (hw : BoundedBy w B) :
    ∃ t, t ≤ B ∧ Bounded (orbitWord w t) := by
  induction B using Nat.strongRecOn generalizing w with
  | ind B ih =>
    by_cases hB : B ≤ 18
    · refine ⟨0, Nat.zero_le _, ?_⟩
      intro x hx
      have := hw x hx
      omega
    · have hlt := contracted_bound_lt B (by omega)
      obtain ⟨t, ht, hb⟩ := ih _ hlt (stepWord w) (stepWord_contracts w B hw)
      refine ⟨1 + t, by omega, ?_⟩
      rw [orbitWord_add]
      exact hb

theorem exists_coefficient_bound (w : Word) : ∃ B, BoundedBy w B := by
  induction w with
  | nil => exact ⟨0, by intro x hx; simp at hx⟩
  | cons x xs ih =>
    obtain ⟨B, hB⟩ := ih
    refine ⟨max x B, ?_⟩
    intro y hy
    rcases List.mem_cons.mp hy with rfl | hy
    · exact Nat.le_max_left _ _
    · exact Nat.le_trans (hB y hy) (Nat.le_max_right _ _)

/-- Finite positive natural-coefficient words eventually become an ordinary
positive decimal pair-word orbit, with no coefficient-bound hypothesis. -/
theorem arbitrary_eventual_realization (w : Word) (hp : 0 < evalL w) :
    ∃ t n, 1 ≤ t ∧ 0 < n ∧
      ∀ k, pairWord (orbit n k) = orbitWord w (t + k) := by
  obtain ⟨B, hB⟩ := exists_coefficient_bound w
  obtain ⟨a, _, ha⟩ := eventually_bounded_of_bound B w hB
  obtain ⟨b, n, hb, _, hn, he⟩ := eventual_realization (orbitWord w a) ha
    (orbitWord_value_growth w hp a).1
  refine ⟨a + b, n, by omega, hn, ?_⟩
  intro k
  rw [Nat.add_assoc, orbitWord_add]
  exact he k

/-- The only remaining hypothesis beyond finite-word positivity is the full
infinite normalized-word safety property itself. No such safe word is supplied. -/
theorem arbitrary_safe_symbolic_positive_seed (w : Word) (hp : 0 < evalL w)
    (hs : ∀ k, (normalize (orbitWord w k) 0).reverse ≠ normalize (orbitWord w k) 0) :
    ∃ m, 0 < m ∧ ∀ k, ¬ Palindrome (orbit m k) := by
  obtain ⟨t, n, _, hn, he⟩ := arbitrary_eventual_realization w hp
  refine ⟨step n, ?_, ?_⟩
  · unfold step; omega
  · intro k
    rw [orbit_step, step_palindrome_iff, he k]
    exact hs (t + k)

end Agent112.Eventual
#print axioms Agent112.Eventual.BoundedBy
#print axioms Agent112.Eventual.norm_carry_bound
#print axioms Agent112.Eventual.normalize_bound
#print axioms Agent112.Eventual.pair_bound
#print axioms Agent112.Eventual.stepWord_contracts
#print axioms Agent112.Eventual.contracted_bound_lt
#print axioms Agent112.Eventual.eventually_bounded_of_bound
#print axioms Agent112.Eventual.exists_coefficient_bound
#print axioms Agent112.Eventual.arbitrary_eventual_realization
#print axioms Agent112.Eventual.arbitrary_safe_symbolic_positive_seed
