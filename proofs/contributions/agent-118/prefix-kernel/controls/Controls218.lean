import Rank218
import PrefixChecksBase

/-!
# Positive controls for the 218 instance (Agent #118)

Not part of the endpoint's import graph. These kernel-checked facts show that the
218 statements are not vacuous and that the new short premise is needed:

* the target family is nonempty: 10700 -> 11401 -> 21812, a palindrome beginning
  with 218 reached at time 2 (found by the fresh-context review);
* Agent #104's earlier premise "no exact short image lies in the tree" is false
  for this certificate (the short source [1,0,14,0,1] maps onto the ranked short
  target [2,1,8,1,2]);
* the certificate's initial bound 33 is attained, so 33 cannot be lowered with
  this tree (index 9988 is the word 2,1,8,9,9,8,8).
-/

namespace Agent118.Controls218

open Lychrel196 DecimalDigits SevenColumn.Certificate SevenColumn.ShortBoundary
open Agent118.PrefixKernel Agent118.Cert218

set_option maxRecDepth 100000

theorem witness_orbit : orbit 10700 2 = 21812 := by decide

theorem witness_family : PalindromeStarts3 2 1 8 21812 := by
  refine ⟨by decide, fun i => (21812 / 10 ^ i) % 10, 5, ?_, by decide, by decide, by decide, by decide⟩
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i _
  show 21812 / 10 ^ i % 10 ≤ 9
  omega

/-- The ancestry theorem `ancestry_bound34` has a nonempty hypothesis set. -/
theorem family_reached : ∃ A P t, 0 < A ∧ PalindromeStarts3 2 1 8 P ∧ orbit A t = P :=
  ⟨10700, 21812, 2, by decide, witness_family, witness_orbit⟩

theorem short_edge_image : lookup ranks (nextWord [1,0,14,0,1]) = some 1 := by decide +kernel

theorem short_edge_source : lookup ranks [1,0,14,0,1] = some 0 := by decide +kernel

theorem short_source_mem : [1,0,14,0,1] ∈ shortWords := by decide +kernel

/-- Agent #104's 739 short premise fails for the 218 tree. -/
theorem old_short_premise_fails :
    ¬ ∀ s ∈ shortWords, lookup ranks (nextWord s) = none := by
  intro h
  have := h _ short_source_mem
  rw [short_edge_image] at this
  contradiction

theorem bound33_attained : lookup ranks (targetInitialWord 2 1 8 9988) = some 33 := by
  decide +kernel

theorem bound32_fails : checkInitial ranks 32 (targetInitialWord 2 1 8 9988) = false := by
  decide +kernel

#print axioms witness_family
#print axioms family_reached
#print axioms old_short_premise_fails
#print axioms bound33_attained
#print axioms bound32_fails

end Agent118.Controls218
