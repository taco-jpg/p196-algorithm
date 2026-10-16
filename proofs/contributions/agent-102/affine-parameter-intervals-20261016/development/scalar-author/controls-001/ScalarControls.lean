import Agent102AffineInequalityIntervals

namespace Agent102.ParameterSets.ScalarControls

theorem positive_endpoints :
    ltInterval ⟨2, 0⟩ ⟨0, 0⟩ = (⟨0, some 0⟩ : Interval) ∧
    ltInterval ⟨2, 0⟩ ⟨0, 1⟩ = (⟨0, some 1⟩ : Interval) ∧
    ltInterval ⟨2, 0⟩ ⟨0, 4⟩ = (⟨0, some 2⟩ : Interval) ∧
    ltInterval ⟨2, 0⟩ ⟨0, 5⟩ = (⟨0, some 3⟩ : Interval) := by
  decide

theorem negative_endpoints :
    ltInterval ⟨-2, 0⟩ ⟨0, 0⟩ = (⟨1, none⟩ : Interval) ∧
    ltInterval ⟨-2, 0⟩ ⟨0, -4⟩ = (⟨3, none⟩ : Interval) ∧
    ltInterval ⟨-2, 0⟩ ⟨0, -3⟩ = (⟨2, none⟩ : Interval) ∧
    ltInterval ⟨-2, 0⟩ ⟨0, 1⟩ = Interval.univ := by
  decide

theorem equal_slope_endpoints :
    ltInterval ⟨7, 0⟩ ⟨7, -1⟩ = Interval.empty ∧
    ltInterval ⟨7, 0⟩ ⟨7, 0⟩ = Interval.empty ∧
    ltInterval ⟨7, 0⟩ ⟨7, 1⟩ = Interval.univ := by
  decide

theorem nonstrict_boundary_endpoints :
    leInterval ⟨2, 0⟩ ⟨0, 4⟩ = (⟨0, some 3⟩ : Interval) ∧
    leInterval ⟨-2, 0⟩ ⟨0, -4⟩ = (⟨2, none⟩ : Interval) ∧
    leInterval ⟨7, -3⟩ ⟨7, -3⟩ = Interval.univ := by
  decide

def H : Nat :=
  10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

theorem huge_endpoints :
    ltInterval ⟨1, 0⟩ ⟨0, (H : Int)⟩ = (⟨0, some H⟩ : Interval) ∧
    leInterval ⟨-1, (H : Int)⟩ ⟨0, 0⟩ = (⟨H, none⟩ : Interval) ∧
    ltInterval ⟨(H : Int) + 1, 0⟩ ⟨0, (H : Int)⟩ = (⟨0, some 1⟩ : Interval) ∧
    ltInterval ⟨-((H : Int) + 1), (H : Int)⟩ ⟨0, 0⟩ = (⟨1, none⟩ : Interval) := by
  decide

#print axioms positive_endpoints
#print axioms negative_endpoints
#print axioms equal_slope_endpoints
#print axioms nonstrict_boundary_endpoints
#print axioms huge_endpoints

end Agent102.ParameterSets.ScalarControls
