import P196.Agent105UniformSafeReturn.Agent105UniformReturn

/-!
Agent #105 / source_scout, session 8f1107db019a.

The plain-return clause of VARIABLE_RETURN_THEOREMS.md section 1 is separate
from its optional safe-return strengthening. The return hypotheses below do
not require the positive ordinary outputs to avoid palindromes. Both clauses
reuse the proved actual-word closure, tail stability, shape and time bound.
-/

namespace Agent105.UniformReturn

open Agent102 Agent105.AffineDynamics Agent105.AffineShape Agent105.TailSelection

/-- A bounded positive return cover has one positive return time valid on
an entire tail, without a safety premise. -/
theorem uniform_bounded_return (Q : Nat → List Nat)
    (hQ : HasAffineRuns Q 18) (s B : Nat)
    (hcover : Eventually (fun k => ∃ t, 1 ≤ t ∧ t ≤ B ∧
      Agent8.orbit (Q k) t = Q (k + s))) :
    ∃ t, 1 ≤ t ∧ t ≤ B ∧ ∃ K, ∀ k, K ≤ k →
      Agent8.orbit (Q k) t = Q (k + s) := by
  exact uniform_bounded_tail_selection B
    (fun t _ _ => actual_return_tailStable Q hQ s t) hcover

/-- The plain positive-return conclusion of the written affine-ray theorem.
Safety is optional and belongs to the separate safe-return theorem. The exact
common time bound is derived from the actual head and width increment. -/
theorem uniform_return_wordAt (rs : List RunSpec)
    (hrs : SpecBound rs 18) (s : Nat)
    (hA : 0 < widthSlope rs) (hs : 0 < s)
    (hcanonical : Eventually (fun k => Agent8.CanonicalPair (wordAt rs k)))
    (hreturn : Eventually (fun k => ∃ t, 0 < t ∧
      Agent8.orbit (wordAt rs k) t = wordAt rs (k + s))) :
    ∃ t, 1 ≤ t ∧ t ≤ 4 * widthSlope rs * s ∧ ∃ K, ∀ k, K ≤ k →
      Agent8.orbit (wordAt rs k) t = wordAt rs (k + s) := by
  obtain ⟨Kc, hc⟩ := hcanonical
  obtain ⟨Kr, hr⟩ := hreturn
  obtain ⟨d, Kw, hw⟩ := wordAt_head_width_eventually rs
  have hcover : Eventually (fun k => ∃ t, 1 ≤ t ∧
      t ≤ 4 * widthSlope rs * s ∧
      Agent8.orbit (wordAt rs k) t = wordAt rs (k + s)) := by
    refine ⟨max Kw (max Kc Kr), ?_⟩
    intro k hk
    have hkw : Kw ≤ k := Nat.le_trans (Nat.le_max_left _ _) hk
    have hkc : Kc ≤ k := Nat.le_trans
      (Nat.le_trans (Nat.le_max_left _ _) (Nat.le_max_right _ _)) hk
    have hkr : Kr ≤ k := Nat.le_trans
      (Nat.le_trans (Nat.le_max_right _ _) (Nat.le_max_right _ _)) hk
    obtain ⟨t, ht, hret⟩ := hr k hkr
    have hhead : (wordAt rs (k + s)).headD 0 = (wordAt rs k).headD 0 := by
      rw [(hw (k + s) (by omega)).1, (hw k hkw).1]
    have hwidth := (hw k hkw).2 s
    have hbound := Agent105.ReturnTimeBound.word_family_return_time_bound
      (wordAt rs) k s (widthSlope rs) t hA hs ht (hc k hkc) hret hhead hwidth
    exact ⟨t, hbound.2.1, hbound.2.2, hret⟩
  exact uniform_bounded_return (wordAt rs)
    (hasAffineRuns_wordAt rs 18 hrs) s (4 * widthSlope rs * s) hcover

end Agent105.UniformReturn

#print axioms Agent105.UniformReturn.uniform_bounded_return
#print axioms Agent105.UniformReturn.uniform_return_wordAt
