import ResidualFiveHitDynamics
import ResidualFiveInitialPalindromes
import ResidualFivePhaseCompatibility

set_option autoImplicit false

/-!
Complete finite fibers with their original positive first-hit semantics and
their full modulo-99 trajectory. No new first-hit predicate is introduced.
-/
namespace Agent103.ResidualFiveFirstHit

open Lychrel196 Agent119.EightFamilies
open Agent103.ResidualFiveFibers Agent103.ResidualFiveHitDynamics
open Agent103.ResidualFivePhaseCompatibility Agent103.ResidualFiveResidueCount

/-- The defining conjunction of the original positive first-hit predicate,
applied to the whole ordinary predecessor fiber, including its boundary. -/
theorem first_positive_hit_two (r n : Nat) (hn : n ∈ fiber r) :
    0 < (2 : Nat) ∧ Palindrome (orbit n 2) ∧
      ∀ i, 0 < i → i < 2 → ¬ Palindrome (orbit n i) := by
  exact ⟨by decide, fiber_time_two_palindrome r n hn,
    fiber_no_positive_palindrome_before_two r n hn⟩

/-- Exact complete enumeration, cardinality, initial-palindrome boundary,
positive first-hit time, and full residue trace, with no reachability premise. -/
theorem complete_modular_first_hit_fiber (r : Nat) :
    (modularFiber r).Nodup ∧
    (modularFiber r).length =
      (if r % 2 = 0 then (14 * 10 ^ r + 8) / 11 else (14 * 10 ^ r - 8) / 11) ∧
    (∀ n, n ∈ modularFiber r ↔
      step n = 33 * 10 ^ (2 * r + 2) + 22 ∧ n % 99 = 77) ∧
    (∀ n, n ∈ modularFiber r →
      (Palindrome n ↔ r = 0 ∧ n = 1661) ∧
      orbit n 2 = fam 5 r ∧
      (0 < (2 : Nat) ∧ Palindrome (orbit n 2) ∧
        ∀ i, 0 < i → i < 2 → ¬ Palindrome (orbit n i)) ∧
      (∀ i, orbit n i % 99 = orbit 196 (7 + i) % 99)) := by
  have hc := complete_modular_predecessor_fiber r
  refine ⟨hc.1, hc.2.1, hc.2.2, ?_⟩
  intro n hn
  have hf : n ∈ fiber r :=
    (fiber_mem_iff r n).mpr ((mem_modularFiber_iff r n).mp hn).1
  exact ⟨fiber_palindrome_iff r n hf, fiber_orbit_two r n hf,
    first_positive_hit_two r n hf, modular_fiber_mod99_trace r n hn⟩

/-- Every parameter has a positive seed with this full 196-compatible residue
trace and a palindrome at positive first-hit time two. For positive parameters
the initial seed is nonpalindromic as well. This asserts no integer reachability. -/
theorem compatible_first_hit_exists (r : Nat) :
    ∃ n : Nat, 0 < n ∧ (0 < r → ¬ Palindrome n) ∧
      orbit n 2 = fam 5 r ∧
      (0 < (2 : Nat) ∧ Palindrome (orbit n 2) ∧
        ∀ i, 0 < i → i < 2 → ¬ Palindrome (orbit n i)) ∧
      (∀ i, orbit n i % 99 = orbit 196 (7 + i) % 99) := by
  obtain ⟨n, hf, hm⟩ := fiber_mod99_exists r
  have hn : n ∈ modularFiber r :=
    (mem_modularFiber_iff r n).mpr ⟨(fiber_mem_iff r n).mp hf, hm⟩
  exact ⟨n, by omega, fun hr => fiber_nonpalindrome_of_pos r n hr hf,
    fiber_orbit_two r n hf, first_positive_hit_two r n hf,
    modular_fiber_mod99_trace r n hn⟩

#print axioms first_positive_hit_two
#print axioms complete_modular_first_hit_fiber
#print axioms compatible_first_hit_exists

end Agent103.ResidualFiveFirstHit
