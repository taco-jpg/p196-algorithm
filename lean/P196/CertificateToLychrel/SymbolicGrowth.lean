import P196.CertificateToLychrel.AdmissibleCenters

namespace Agent112.Admissibility
open Agent109 Agent109.Cert

/-- Positivity of a natural-coefficient radix word is independent of order. -/
theorem evalL_pos_iff (w : Word) : 0 < evalL w ↔ ∃ x ∈ w, 0 < x := by
  induction w with
  | nil => simp [evalL]
  | cons x xs ih =>
    simp only [evalL, List.mem_cons, exists_eq_or_imp]
    rw [← ih]
    omega

theorem evalL_reverse_pos (w : Word) (hw : 0 < evalL w) : 0 < evalL w.reverse := by
  obtain ⟨x, hx, hp⟩ := (evalL_pos_iff w).mp hw
  exact (evalL_pos_iff w.reverse).mpr ⟨x, by simpa using hx, hp⟩

theorem stepWord_value (w : Word) :
    evalL (stepWord w) = evalL w + evalL (normalize w 0).reverse := by
  unfold stepWord pair
  rw [evalL_zipAdd _ _ (by simp), evalL_norm, Nat.add_zero]

/-- Word evaluation strictly grows even before canonical admissibility is known. -/
theorem stepWord_strict (w : Word) (hw : 0 < evalL w) : evalL w < evalL (stepWord w) := by
  have hn : 0 < evalL (normalize w 0) := by simpa [evalL_norm] using hw
  have := evalL_reverse_pos _ hn
  rw [stepWord_value]
  omega

theorem bounded_evalL (w : Word) (hw : Bounded w) : evalL w + 2 ≤ 2 * 10 ^ w.length := by
  induction w with
  | nil => simp [evalL]
  | cons x xs ih =>
    have hx := hw x (by simp)
    have ht := ih (fun y hy => hw y (by simp [hy]))
    simp only [evalL, List.length_cons, Nat.pow_succ]
    have hm := Nat.mul_le_mul_left 10 ht
    omega

/-- No positive symbolic orbit can remain forever inside a fixed digit-width
and coefficient bound, without assuming it already realizes a canonical integer. -/
theorem no_bounded_width_orbit (w : Word) (hw : 0 < evalL w) (L : Nat)
    (hb : ∀ k, Bounded (orbitWord w k))
    (hl : ∀ k, (orbitWord w k).length = L) : False := by
  have hg : ∀ k, 0 < evalL (orbitWord w k) ∧ k ≤ evalL (orbitWord w k) := by
    intro k
    induction k with
    | zero => exact ⟨hw, Nat.zero_le _⟩
    | succ k ih =>
      have hs := stepWord_strict (orbitWord w k) ih.1
      change 0 < evalL (stepWord (orbitWord w k)) ∧ k + 1 ≤ evalL (stepWord (orbitWord w k))
      omega
  have hg' := (hg (2 * 10 ^ L)).2
  have he := bounded_evalL (orbitWord w (2 * 10 ^ L)) (hb _)
  rw [hl] at he
  omega

end Agent112.Admissibility
#print axioms Agent112.Admissibility.evalL_pos_iff
#print axioms Agent112.Admissibility.evalL_reverse_pos
#print axioms Agent112.Admissibility.stepWord_value
#print axioms Agent112.Admissibility.stepWord_strict
#print axioms Agent112.Admissibility.bounded_evalL
#print axioms Agent112.Admissibility.no_bounded_width_orbit
