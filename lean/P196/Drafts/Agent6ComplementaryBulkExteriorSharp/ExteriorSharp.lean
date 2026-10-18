import P196.Drafts.Agent110ReviewRadix.ExteriorCoverage

namespace P196.Agent6
set_option maxRecDepth 100000
set_option maxHeartbeats 0

/-- A concrete canonical exterior requires fifteen transitions to exceed length four. -/
theorem capFour_sharp_path :
    Canonical ⟨2,[4,0,1]⟩ ∧
    escapes 4 14 ⟨2,[4,0,1]⟩ = false ∧
    escapes 4 15 ⟨2,[4,0,1]⟩ = true := by
  constructor
  · simp [Canonical,trim]
  · decide +kernel

#print axioms capFour_sharp_path
end P196.Agent6
