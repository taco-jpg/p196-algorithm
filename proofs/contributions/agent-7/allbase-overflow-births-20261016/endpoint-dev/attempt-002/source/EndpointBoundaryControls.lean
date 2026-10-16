import OverflowEndpoints

namespace P196.Agent7.AllBaseOverflow.EndpointControls

open ResetNormalization PhysicalWidth ReverseAdd

/-- A nonsymmetric bounded binary source can realize the exceptional maximum;
endpoint classification deliberately does not ask for coefficient symmetry. -/
theorem binary_max_without_symmetry :
    terminal 2 0 (ordinaryTags [(1, false), (2, false)]) = 1 ∧
    Bounded 2 [(1, false), (2, false)] ∧
    pairs (actualDigits 2 [(1, false), (2, false)]) = [2, 0, 2] := by
  refine ⟨by decide, ?_, by decide⟩
  intro p hp
  simp only [List.mem_cons, List.mem_singleton] at hp
  rcases hp with rfl | rfl <;> decide

/-- The other two bounded binary head coefficients do not create a maximal
endpoint. The width-one source also checks that the two endpoint indices differ. -/
theorem binary_nonmaximum_heads :
    pairs (actualDigits 2 [(0, false), (2, false)]) = [1, 0, 1] ∧
    pairs (actualDigits 2 [(2, false)]) = [1, 1] := by
  decide

/-- Dropping the coefficient bound would make the claimed old coefficient
q0=1 false, even though an actual binary endpoint is maximal. -/
theorem binary_bound_is_needed :
    terminal 2 0 (ordinaryTags [(3, false)]) = 1 ∧
    ¬ Bounded 2 [(3, false)] ∧
    pairs (actualDigits 2 [(3, false)]) = [2, 2] ∧
    ([(3, false)].getD 0 (0, false)).1 ≠ (1 : Int) := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro hbound
  have hbad := hbound (3, false) (by simp)
  omega

/-- Base three is the first base with uniform exclusion of maximal endpoints;
the endpoint reaches its residue upper bound three but remains below four. -/
theorem ternary_boundary :
    terminal 3 0 (ordinaryTags [(2, false), (3, false)]) = 1 ∧
    Bounded 3 [(2, false), (3, false)] ∧
    pairs (actualDigits 3 [(2, false), (3, false)]) = [3, 0, 3] := by
  refine ⟨by decide, ?_, by decide⟩
  intro p hp
  simp only [List.mem_cons, List.mem_singleton] at hp
  rcases hp with rfl | rfl <;> decide

/-- Signed, unbounded old coefficients are still covered by the base-three
nonextremity theorem, since the ordinary remainder is nonnegative. -/
theorem signed_unbounded_nonextreme :
    let xs : List (Int × Bool) := [(-1, false), (4, false)]
    ((pairs (actualDigits 3 xs)).getD 0 0 ≠ 0 ∧
      (pairs (actualDigits 3 xs)).getD 0 0 ≠ 4) ∧
    ((pairs (actualDigits 3 xs)).getD xs.length 0 ≠ 0 ∧
      (pairs (actualDigits 3 xs)).getD xs.length 0 ≠ 4) := by
  exact actual_overflow_endpoints_nonextreme 3 [(-1, false), (4, false)]
    (by decide) (by decide)

end P196.Agent7.AllBaseOverflow.EndpointControls
