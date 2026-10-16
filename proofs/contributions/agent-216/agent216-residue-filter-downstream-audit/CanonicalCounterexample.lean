import GeneralResidueFilter
import ExteriorCoverage

namespace P196.Agent216

/-- A canonical, admissible exterior can already lie in the mod-22
absorbing residue class without having undergone an exterior overflow. -/
theorem canonical_zero_moment_without_overflow :
    P196.Agent6.Canonical ⟨2,[1]⟩ ∧
    P196.Agent5.General.Moment.moment 2 [1] % 22 = 0 ∧
    P196.Agent5.General.exteriorOverflow 9 2 [1] = 0 := by
  constructor
  · simp [P196.Agent6.Canonical, P196.Agent6.trim]
  constructor <;> decide

/-- Hence even after restricting to canonical exteriors, zero mod-22
moment is not equivalent to an actual overflow event. -/
theorem canonical_zero_moment_not_overflow :
    ¬ (P196.Agent5.General.Moment.moment 2 [1] % 22 = 0 →
      P196.Agent5.General.exteriorOverflow 9 2 [1] = 1) := by
  intro h
  have hz := canonical_zero_moment_without_overflow.2.1
  have hov := h hz
  have hn := canonical_zero_moment_without_overflow.2.2
  omega

#print axioms canonical_zero_moment_without_overflow
#print axioms canonical_zero_moment_not_overflow

end P196.Agent216
