import P196.Foundations.Agent1PeriodicQuotient

/-!
A finite control for a proposed local center-count restriction. The source
center is already maximally stripped, yet its actual nine-preserving image
removes two mirrored period pairs and has a nonempty center. A further
actual transition still has period nine. No return or infinite continuation
is supplied, and no differently restricted temporal bound is refuted.
-/

namespace Agent1.Periodic
open Agent8

/-- A normalized valid center can undergo extra stripping without immediately
leaving the nine phase. All operations and carry bits are the original ones. -/
theorem nines_extra_strip_control :
    let B : Word := [1]
    let H : Word := [9,9,9,14,18,18,14,9,9,9]
    let w : Word := [9,9,9,9]
    ValidPeriodic B H w ∧
    stripPeriodCenter w H = (H, 0) ∧
    leftEntry B + rightEntry B H w = 1 ∧
    rawPeriod B H w = w ∧
    centerPeriods B H w = 2 ∧
    quotientCenter B H w = [18,18] ∧
    quotientOuter B H w = [3] ∧
    rawPeriod (quotientOuter B H w) (quotientCenter B H w)
      (rawPeriod B H w) = w := by
  dsimp only
  refine ⟨?_, by decide, by decide, by decide, by decide,
    by decide, by decide, by decide⟩
  constructor
  · intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
    subst x
    decide
  · intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
    omega
  · intro x hx
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
    omega
  · rfl
  · rfl
  · intro h
    contradiction
  · decide

end Agent1.Periodic

#print axioms Agent1.Periodic.nines_extra_strip_control
