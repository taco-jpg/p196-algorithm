import TemplateStep
#print axioms Agent109.norm_template
#print axioms Agent109.normalize_template
#print axioms Agent109.gamma_le
#print axioms Agent109.pair_split
#print axioms Agent109.stepWord_template
#print axioms Agent109.pairWord_step
#print axioms Agent109.pairWord_orbit
#print axioms Agent109.orbit_succ_value
#print axioms Agent109.actual_template_step
#print axioms Agent109.palindrome_iff
#print axioms Agent109.step_palindrome_iff
#print axioms Agent109.actual_template_palindrome_iff
-- kernel sanity instance (ordinary `decide`, no native_decide)
open Agent109 in
example : stepWord (template 2 [1] [3] [4] 3 2) =
    template (tOf 2 + tOf 2) (Br 2 [1] [3] [4]) (Ar 2 [1] [3] [4]) (Cr 2 [1] [3] [4])
      (1 + (data 2 [1] [3] [4]).γ) (0 + (data 2 [1] [3] [4]).γ) := by decide
