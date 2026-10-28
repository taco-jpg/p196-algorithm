import P196.AbsorbingBand.Base13

/-!
# Base 13: the explicit 151-digit seed of W3's replay

`N0` has base-13 digits (least significant first) as recorded in `cert_b13_rec0.json`.
Its mirrored digit sums are the pair word of the template with band length `l = 1`, so one
ordinary reverse-and-add step gives `seed`, and `seed` is Lychrel by `lychrel_seed`.
-/

namespace AbsorbingBand.Base13

open AbsorbingBand Agent120.Neutral

def N0digits : List Nat := [9, 4, 4, 9, 6, 9, 5, 4, 7, 0, 11, 6, 3, 10, 1, 5, 6, 0, 0, 8, 0, 0, 5, 8, 4, 1, 2, 11, 7, 7, 0, 5, 11, 4, 6, 5, 9, 2, 9, 9, 9, 10, 10, 11, 9, 0, 8, 2, 10, 8, 1, 11, 12, 11, 8, 9, 6, 0, 7, 3, 1, 8, 7, 4, 8, 0, 11, 6, 10, 11, 3, 6, 8, 8, 8, 8, 8, 8, 8, 6, 3, 12, 10, 6, 12, 1, 8, 5, 8, 8, 2, 3, 7, 1, 6, 10, 9, 12, 12, 11, 2, 9, 11, 2, 9, 1, 10, 12, 11, 11, 10, 10, 10, 2, 9, 6, 6, 5, 11, 6, 1, 7, 7, 12, 3, 1, 5, 8, 5, 1, 0, 9, 1, 0, 6, 5, 2, 11, 4, 6, 12, 1, 7, 5, 6, 10, 7, 10, 4, 5, 10]

def N0 : Nat := val 13 N0digits

set_option maxRecDepth 100000 in
theorem N0_step : step 13 N0 = seed := by decide

set_option maxRecDepth 100000 in
theorem N0_not_pal : ¬ IsPal 13 N0 := by decide

theorem lychrel_N0 : Lychrel 13 N0 :=
  lychrel_of_entry 13 N0 1 seed
    (by
      intro k hk
      have h0 : k = 0 := by omega
      subst h0
      exact N0_not_pal)
    N0_step lychrel_seed

theorem exists_lychrel_N0 : ∃ n, Lychrel 13 n := ⟨N0, lychrel_N0⟩

end AbsorbingBand.Base13

#print axioms AbsorbingBand.Base13.N0_step
#print axioms AbsorbingBand.Base13.N0_not_pal
#print axioms AbsorbingBand.Base13.lychrel_N0
