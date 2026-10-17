import P196.Agent101ProtectedFamily.FiniteHorizonOverflow
import P196.Agent101ProtectedFamily.NormalizedSafety

/-!
The unconditional aggregate for the protected overflow family.

The counted objects are coefficient words. For each such word we also use
the unchanged decimal normalization to produce a positive ordinary integer,
and prove its reverse-add orbit avoids palindromes at every time `0, ..., k`.
The words, widths, and integers may depend on the prescribed finite horizon.
-/

namespace P196.Agent3.OverflowHorizon

open Agent8

/-- The actual normalized digit list has decimal digits and ends in carry one. -/
theorem inputWord_normalized_digits (xs : List Bool) (k : Nat) :
    Bounded (normalize (inputWord xs k) 0) 9 ∧
      ∃ init last, normalize (inputWord xs k) 0 = init ++ [last] ∧ 0 < last := by
  refine ⟨normalized_digits_bounded _ 0 (inputWord_bounded xs k) (by decide), ?_⟩
  refine ⟨fixedDigits (inputWord xs k) 0, 1, ?_, by decide⟩
  rw [normalize_decompose, inputWord_final_carry]
  rfl

/-- Every actual normalized family output is a positive ordinary integer
whose decimal reverse-add orbit avoids palindromes through time `k`. -/
theorem inputWord_normalized_safe (xs : List Bool) (k : Nat) (hk : 0 < k) :
    0 < digitValue (normalize (inputWord xs k) 0) ∧
      ∀ t, t ≤ k → ¬ Lychrel196.Palindrome
        (Lychrel196.orbit (digitValue (normalize (inputWord xs k) 0)) t) := by
  obtain ⟨hb, hp⟩ := inputWord_normalized_digits xs k
  exact normalized_target_safe_prefix _ xs.length k hk hb hp (inputWord_step xs k hk)

/-- All normalized outputs have the same next ordinary reverse-add value. -/
theorem inputWord_common_next_value (xs : List Bool) (k : Nat) (hk : 0 < k) :
    Lychrel196.step (digitValue (normalize (inputWord xs k) 0)) =
      DecimalDigits.value (targetColumn xs.length k) (target xs.length k).length := by
  obtain ⟨hb, hp⟩ := inputWord_normalized_digits xs k
  exact normalized_target_step_value _ xs.length k hb hp (inputWord_step xs k hk)

/-- Exact counted overflow family, actual common image, and unconditional
ordinary-integer finite safety. No infinite-time seed is asserted. -/
theorem finite_horizon_overflow_family (m k : Nat) (hk : 0 < k) :
    (familyWords m k).length = 2 ^ m ∧
    (familyWords m k).Nodup ∧
    ∀ w ∈ familyWords m k,
      CanonicalPair w ∧
      w.length = 2 * (m + k + 1) ∧
      w.length % 2 = 0 ∧
      terminalCarry w 0 = 1 ∧
      stepWord w = target m k ∧
      0 < digitValue (normalize w 0) ∧
      (∀ t, t ≤ k → ¬ Lychrel196.Palindrome
        (Lychrel196.orbit (digitValue (normalize w 0)) t)) ∧
      Lychrel196.step (digitValue (normalize w 0)) =
        DecimalDigits.value (targetColumn m k) (target m k).length := by
  refine ⟨familyWords_length m k, familyWords_nodup m k, ?_⟩
  intro w hw
  obtain ⟨xs, hlen, rfl⟩ := (mem_familyWords_iff w m k).mp hw
  obtain ⟨hp, hs⟩ := inputWord_normalized_safe xs k hk
  refine ⟨inputWord_canonical xs k, ?_, inputWord_even_width xs k,
    inputWord_final_carry xs k, ?_, hp, hs, ?_⟩
  · rw [inputWord_length, hlen]
  · simpa only [hlen] using inputWord_step xs k hk
  · simpa only [hlen] using inputWord_common_next_value xs k hk

end P196.Agent3.OverflowHorizon
