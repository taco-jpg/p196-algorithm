import P196.Agent5EvenBaseAbsorption.GeneralMomentAbsorption

namespace P196.Agent216

open P196.Agent5.General P196.Agent5.General.Moment

/-- A zero mod-22 moment does not characterize an overflow state.
The state (m,c,B)=(9,2,[1]) has moment 0 mod 22, but its exact
exterior normalization has no overflow. -/
theorem zero_moment_without_overflow :
    moment 2 [1] % 22 = 0 ∧ exteriorOverflow 9 2 [1] = 0 := by
  decide +kernel

/-- The decimal m=9 absorption theorem is genuinely one-way:
overflow forces the next moment to vanish modulo 22, while vanishing
moment alone does not imply overflow. -/
theorem decimal_absorption_is_not_a_converse :
    moment 2 [1] % 22 = 0 ∧ exteriorOverflow 9 2 [1] ≠ 1 := by
  refine ⟨zero_moment_without_overflow.1, ?_⟩
  rw [zero_moment_without_overflow.2]
  decide

#print axioms zero_moment_without_overflow
#print axioms decimal_absorption_is_not_a_converse

end P196.Agent216
