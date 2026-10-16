import TemplateStep
open Agent109
#print axioms Agent109.norm_template
#print axioms Agent109.normalize_template
#print axioms Agent109.pair_split
#print axioms Agent109.stepWord_template
-- sanity: concrete instance evaluated by kernel `decide`
example : stepWord (template 2 [1] [3] [4] 3 2) =
    template (tOf 2 + tOf 2) (Br 2 [1] [3] [4]) (Ar 2 [1] [3] [4]) (Cr 2 [1] [3] [4])
      (1 + (data 2 [1] [3] [4]).γ) (0 + (data 2 [1] [3] [4]).γ) := by decide
