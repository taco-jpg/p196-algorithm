import P196.Drafts.Agent5.GeneralResidueFilter
import P196.Drafts.Agent110ReviewRadix.ExteriorCoverage

namespace P196.Agent216

/-- The canonical counterexample is also an exact edge of Agent6's Nat-valued
exterior map: no overflow occurs and the exterior advances from [1] to [2]. -/
theorem canonical_counterexample_actual_edge :
    P196.Agent6.advance ⟨2,[1]⟩ = ⟨4,[2]⟩ ∧
    P196.Agent5.General.nextExterior 9 2 [1] = [2] ∧
    P196.Agent5.General.exteriorOverflow 9 2 [1] = 0 := by
  decide

/-- The mod-22 zero class is therefore encountered by the exact Nat-valued
exterior dynamics before any overflow is needed. -/
theorem canonical_counterexample_actual_zero :
    P196.Agent5.General.Moment.moment 2 [1] % 22 = 0 ∧
    P196.Agent5.General.Moment.moment 4 [2] % 22 = 0 := by
  decide

#print axioms canonical_counterexample_actual_edge
#print axioms canonical_counterexample_actual_zero

end P196.Agent216
