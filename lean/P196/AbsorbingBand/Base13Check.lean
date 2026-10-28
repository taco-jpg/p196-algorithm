import P196.AbsorbingBand.Base13

/-!
# Direct kernel checks of the base-13 template dynamics (independent of the general theorems)

These `decide` statements compute ordinary reverse-and-add on the integer `seed` (using the repo's
`step`, `orbit`, `digits`, `revNat`) and compare with the template values predicted by the cycle:
after 1 step the template is `(B1, 8, 2)`, after 10 steps `(B0, 16, 4)`, after 20 steps `(B0, 16, 7)`,
after 30 steps `(B0, 16, 10)`.  The band length grows by `sum gam = 3` per period.
-/

namespace AbsorbingBand.Base13

open AbsorbingBand Agent120.Neutral

set_option maxRecDepth 100000 in
theorem check_step1 : step 13 seed = val 13 (ltmpl B1 8 2) := by decide

set_option maxRecDepth 100000 in
theorem check_orbit10 : orbit 13 seed 10 = val 13 (ltmpl B0 16 4) := by decide

set_option maxRecDepth 100000 in
theorem check_orbit20 : orbit 13 seed 20 = val 13 (ltmpl B0 16 7) := by decide

set_option maxRecDepth 100000 in
theorem check_orbit30 : orbit 13 seed 30 = val 13 (ltmpl B0 16 10) := by decide

set_option maxRecDepth 100000 in
theorem check_seed_not_pal : ¬ IsPal 13 seed := by decide

#print Agent120.Neutral.Lychrel
#print axioms AbsorbingBand.Base13.check_orbit30
#print axioms AbsorbingBand.Base13.check_seed_not_pal

end AbsorbingBand.Base13
