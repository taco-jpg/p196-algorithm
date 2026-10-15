import SymbolicGrowth

/-!
Agent #112. Eventual ordinary-decimal realization of arbitrary finite positive
coefficient words. Initial symmetry, canonical heads, and integer realizability
are not hypotheses. Core Lean 4.19.0 only.
-/
namespace Agent112.Eventual
open Agent109
open Agent112.Admissibility

/-- Normalization of a bounded coefficient word produces decimal digits,
including a possible one-bit overflow. -/
theorem normalize_digits (w : Word) (hw : Bounded w) :
    ∀ x ∈ normalize w 0, x < 10 := by
  intro x hx
  rw [normalize_eq_norm] at hx
  rcases List.mem_append.mp hx with hx | hx
  · exact norm_digit_lt w 0 x hx
  · have hc := norm_carry_le w 0 hw (by decide)
    unfold carryWord at hx
    split at hx
    · simp at hx
    · simp only [List.mem_singleton] at hx
      omega

theorem pair_bounded_of_digits (D : Word) (hD : ∀ x ∈ D, x < 10) : Bounded (pair D) := by
  have aux : ∀ a b : Word, (∀ x ∈ a, x < 10) → (∀ x ∈ b, x < 10) → Bounded (zipAdd a b) := by
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

theorem stepWord_bounded (w : Word) (hw : Bounded w) : Bounded (stepWord w) :=
  pair_bounded_of_digits _ (normalize_digits w hw)

theorem orbitWord_bounded (w : Word) (hw : Bounded w) : ∀ k, Bounded (orbitWord w k) := by
  intro k
  induction k with
  | zero => exact hw
  | succ k ih => exact stepWord_bounded _ ih

/-- A positive symbolic value grows by at least one at each step. -/
theorem orbitWord_value_growth (w : Word) (hw : 0 < evalL w) :
    ∀ k, 0 < evalL (orbitWord w k) ∧ evalL w + k ≤ evalL (orbitWord w k) := by
  intro k
  induction k with
  | zero => exact ⟨hw, Nat.le_refl _⟩
  | succ k ih =>
    have hs := stepWord_strict _ ih.1
    change 0 < evalL (stepWord (orbitWord w k)) ∧
      evalL w + (k + 1) ≤ evalL (stepWord (orbitWord w k))
    omega

theorem stepWord_length (w : Word) :
    (stepWord w).length = w.length + (carryWord (norm w 0).2).length := by
  unfold stepWord pair
  rw [zipAdd_length _ _ (by simp), normalize_eq_norm, List.length_append, norm_length]

theorem stepWord_length_of_zero_carry (w : Word) (hc : (norm w 0).2 = 0) :
    (stepWord w).length = w.length := by
  rw [stepWord_length, hc]
  simp [carryWord]

/-- A positive bounded finite word has a genuine one-bit overflow before the
explicit value bound. This is proved uniformly, not by enumerating that bound. -/
theorem overflow_before_bound (w : Word) (hb : Bounded w) (hp : 0 < evalL w) :
    ∃ j, j < 2 * 10 ^ w.length ∧ (norm (orbitWord w j) 0).2 = 1 := by
  apply Classical.byContradiction
  intro hn
  have hz : ∀ j, j < 2 * 10 ^ w.length → (norm (orbitWord w j) 0).2 = 0 := by
    intro j hj
    have hc := norm_carry_le (orbitWord w j) 0 (orbitWord_bounded w hb j) (by decide)
    have hne : (norm (orbitWord w j) 0).2 ≠ 1 := fun h => hn ⟨j, hj, h⟩
    omega
  have hl : ∀ k, k ≤ 2 * 10 ^ w.length → (orbitWord w k).length = w.length := by
    intro k
    induction k with
    | zero => intro _; rfl
    | succ k ih =>
      intro hk
      change (stepWord (orbitWord w k)).length = w.length
      rw [stepWord_length_of_zero_carry _ (hz k (by omega)), ih (by omega)]
  have hg := (orbitWord_value_growth w hp (2 * 10 ^ w.length)).2
  have he := bounded_evalL (orbitWord w (2 * 10 ^ w.length)) (orbitWord_bounded w hb _)
  rw [hl _ (Nat.le_refl _)] at he
  omega

end Agent112.Eventual
#print axioms Agent112.Eventual.normalize_digits
#print axioms Agent112.Eventual.pair_bounded_of_digits
#print axioms Agent112.Eventual.stepWord_bounded
#print axioms Agent112.Eventual.orbitWord_bounded
#print axioms Agent112.Eventual.orbitWord_value_growth
#print axioms Agent112.Eventual.stepWord_length
#print axioms Agent112.Eventual.stepWord_length_of_zero_carry
#print axioms Agent112.Eventual.overflow_before_bound
