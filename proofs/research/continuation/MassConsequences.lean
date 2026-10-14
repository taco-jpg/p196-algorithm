import UnboundedMass

namespace DecimalUnboundedMass

open DecimalMass DecimalDigits Lychrel196

/-- The digit sums exceed any bound arbitrarily late in every positive
ordinary decimal reverse-and-add orbit. -/
theorem digitSum_unbounded_after (n : Nat) (hn : 0 < n) (B start : Nat) :
    ∃ t, start ≤ t ∧ B < digitSum (orbit n t) := by
  obtain ⟨k, hk⟩ := digitSum_unbounded (orbit n start)
    (orbit_positive n hn start) B
  refine ⟨start + k, by omega, ?_⟩
  rw [LychrelCertificates.orbit_add]
  exact hk

/-- No positive orbit can eventually remain below a fixed digit-sum bound. -/
theorem not_eventually_bounded_digitSum (n : Nat) (hn : 0 < n) :
    ¬ ∃ start B, ∀ t, start ≤ t → digitSum (orbit n t) ≤ B := by
  rintro ⟨start, B, hb⟩
  obtain ⟨t, ht, hgt⟩ := digitSum_unbounded_after n hn B start
  have hle := hb t ht
  omega

/-- A genuine all-time statement about 196, independent of whether its
orbit ever reaches a palindrome. -/
theorem digitSum_196_unbounded_after (B start : Nat) :
    ∃ t, start ≤ t ∧ B < digitSum (orbit 196 t) :=
  digitSum_unbounded_after 196 (by decide) B start

#print axioms digitSum_unbounded_after
#print axioms not_eventually_bounded_digitSum
#print axioms digitSum_196_unbounded_after

end DecimalUnboundedMass
