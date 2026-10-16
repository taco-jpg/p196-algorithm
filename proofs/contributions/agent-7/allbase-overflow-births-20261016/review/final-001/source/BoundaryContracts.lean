import CanonicalOverflowBirths

/-!
Independent finite boundary contracts for the frozen one-step theorem.
These are review controls, not additional research or novelty claims.
In particular binary 110 -> 1001 is an existing example.
-/

namespace P196.Agent7.AllBaseOverflow.Review

open ResetNormalization PhysicalWidth ReverseAdd ActualBaseBirths
open P196.Agent7.AllBaseOverflow

def binaryTagged : List (Int × Bool) := [(1, true), (2, true), (1, true)]

/-- Consume the literal canonical interface on the existing binary example,
including true reset tags, a zero birth, and both maximal endpoints. -/
theorem canonical_binary_contract :
    actualDigits 2 binaryTagged = [1, 0, 0, 1] ∧
    (actualDigits 2 binaryTagged).length = 4 ∧
    SignedDigitUniqueness.eval 2 (actualDigits 2 binaryTagged) = 9 ∧
    (pairs (actualDigits 2 binaryTagged)).getD 1 0 = 0 ∧
    (pairs (actualDigits 2 binaryTagged)).getD 0 0 = 2 ∧
    (pairs (actualDigits 2 binaryTagged)).getD 3 0 = 2 := by
  have hd : DigitBounds 2 [0, 1, 1] := by
    intro d hd
    simp only [List.mem_cons, List.mem_singleton] at hd
    rcases hd with rfl | rfl | rfl <;> constructor <;> decide
  have h := canonical_reverse_add_overflow_theorem 2 [0, 1, 1] binaryTagged
    (by decide) hd ⟨[0, 1], 1, rfl, by decide⟩ (by decide) (by decide)
  rcases h with ⟨_, _, hlen, hval, _, _, hmax, hinterior⟩
  have hz := (hinterior 1 (by decide) (by decide)).1
  refine ⟨by decide, hlen, hval, hz.mpr (by decide), ?_, ?_⟩
  · exact hmax.1.mpr (by decide)
  · exact hmax.2.mpr (by decide)

/-- Width one is a real canonical overflow with no interior index. -/
theorem canonical_binary_width_one_contract :
    (actualDigits 2 [(2, true)]).length = 2 ∧
    SignedDigitUniqueness.eval 2 (actualDigits 2 [(2, true)]) = 2 ∧
    (pairs (actualDigits 2 [(2, true)])).getD 0 0 = 1 ∧
    (pairs (actualDigits 2 [(2, true)])).getD 1 0 = 1 ∧
    ¬ ∃ i : Nat, 0 < i ∧ i < 1 := by
  have hd : DigitBounds 2 [1] := by
    intro d hd
    simp only [List.mem_singleton] at hd
    subst d
    constructor <;> decide
  have h := canonical_reverse_add_overflow_theorem 2 [1] [(2, true)]
    (by decide) hd ⟨[], 1, rfl, by decide⟩ (by decide) (by decide)
  rcases h with ⟨_, _, hlen, hval, hend, _, _, _⟩
  refine ⟨hlen, hval, hend.1, hend.2, ?_⟩
  omega

/-- Consume the actual maximum iff on a nonneutral inherited binary pair. -/
theorem actual_binary_maximum_contract :
    (pairs (actualDigits 2 [(2, false), (2, false)])).getD 1 0 = 2 := by
  have hb : Bounded 2 [(2, false), (2, false)] := by
    intro p hp
    simp only [List.mem_cons, List.mem_singleton] at hp
    rcases hp with rfl | rfl <;> constructor <;> decide
  apply (actual_overflow_max_iff 2 [(2, false), (2, false)] 1
    (by decide) hb (by decide) (by decide) (by decide) (by decide)).mpr
  exact Or.inl ⟨rfl, rfl⟩

/-- Old-width reflection would assign the wrong value to this center. -/
theorem old_width_mirror_negative_control :
    pairs (actualDigits 2 [(2, false), (2, false)]) = [1, 2, 1] ∧
    (pairs (actualDigits 2 [(2, false), (2, false)])).getD 1 0 ≠
      BaseBirths.localPair 2 2
        (incoming 2 [(2, false), (2, false)] 1)
        (incoming 2 [(2, false), (2, false)] 0) := by
  decide

/-- The actual list erases tags; reset-placed digits may differ. -/
theorem reset_tag_erasure_control :
    actualDigits 3 [(4, false), (2, true), (4, false)] = [1, 0, 2, 1] ∧
    placed 3 0 [(4, false), (2, true), (4, false)] = [1, 3, 1, 1] := by
  decide

/-- Removing the coefficient bound would invalidate the q0=1 endpoint test. -/
theorem endpoint_bound_is_needed_control :
    terminal 2 0 (ordinaryTags [(3, true)]) = 1 ∧
    pairs (actualDigits 2 [(3, true)]) = [2, 2] ∧
    (([(3, true)] : List (Int × Bool)).getD 0 (0, false)).1 ≠ 1 := by
  decide

/-- The endpoint theorem really supports unbounded signed coefficients. -/
theorem signed_unbounded_endpoint_contract :
    ((pairs (actualDigits 3 [(-4, true), (5, true)])).getD 0 0 ≠ 0 ∧
      (pairs (actualDigits 3 [(-4, true), (5, true)])).getD 0 0 ≠ 4) ∧
    ((pairs (actualDigits 3 [(-4, true), (5, true)])).getD 2 0 ≠ 0 ∧
      (pairs (actualDigits 3 [(-4, true), (5, true)])).getD 2 0 ≠ 4) := by
  exact actual_overflow_endpoints_nonextreme 3 [(-4, true), (5, true)]
    (by decide) (by decide)

/-- A neutral neighbor does not by itself imply a new extreme. -/
theorem neutrality_is_not_sufficient_control :
    terminal 2 0 (ordinaryTags [(2, false), (1, false), (2, false)]) = 1 ∧
    (pairs (actualDigits 2 [(2, false), (1, false), (2, false)])).getD 1 0 = 1 := by
  decide

/-- A default zero outside the actual list is not an interior birth. -/
theorem out_of_range_default_control :
    (pairs (actualDigits 2 binaryTagged)).getD 4 0 = 0 ∧
    ¬ (0 < 4 ∧ 4 < binaryTagged.length) := by
  decide

#print axioms canonical_binary_contract
#print axioms canonical_binary_width_one_contract
#print axioms actual_binary_maximum_contract
#print axioms old_width_mirror_negative_control
#print axioms reset_tag_erasure_control
#print axioms endpoint_bound_is_needed_control
#print axioms signed_unbounded_endpoint_contract
#print axioms neutrality_is_not_sufficient_control
#print axioms out_of_range_default_control

end P196.Agent7.AllBaseOverflow.Review
