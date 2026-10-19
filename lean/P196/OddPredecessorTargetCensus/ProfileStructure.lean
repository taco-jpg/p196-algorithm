import P196.OddPredecessorTargetCensus.EvenWords
import P196.CompleteFiberParity.ProfileParity
import P196.Agent105AllPredecessors.Agent105WordFiber9df76b
import P196.Agent105NumericDecoder.Agent105DecoderScan9df76b

/-!
# Structural conditions for accepted coefficient words

Agent #6: relate the existing finite-word admissibility and multiplicity
test to symmetric lists with bounded even interiors. Zero inner entries
remain valid, including a zero center surrounded by an outer pair.
-/

set_option autoImplicit false

namespace OddPredecessorTargetCensus

open FoldedDecimal Agent101 CompleteFiberParity
open Agent105WordFiber9df76b Agent105DecoderScan9df76b

/-- Admissibility of the finite digit function implies list symmetry. -/
theorem reverse_of_admissible (qs : List Nat)
    (ha : Admissible qs.length (digitFn qs)) : qs.reverse = qs := by
  apply List.ext_getElem (by simp)
  intro i hi hj
  have hs := ha.2.2.2.1 i hj
  rw [digitFn_getElem qs i hj,
    digitFn_getElem qs (qs.length - 1 - i) (by omega)] at hs
  simpa only [List.getElem_reverse] using hs.symm

/-- For a symmetric interior, odd multiplicity is exactly the outer-pair
condition together with bounded even entries throughout the interior. -/
theorem oddProfile_wrap_iff (s : Nat) (xs : List Nat)
    (hrev : xs.reverse = xs) :
    oddProfile (half (wrapDigits s s xs))
      (center (wrapDigits s s xs)) = true ↔
      ((s ≤ 9 ∧ s % 2 = 1) ∨ (10 ≤ s ∧ s ≤ 18 ∧ s % 2 = 0)) ∧
      ∀ t ∈ xs, t ≤ 18 ∧ t % 2 = 0 := by
  obtain ⟨h, c, rfl⟩ := exists_coefficientWord_of_reverse xs hrev
  rw [← coefficientWord_cons, half_coefficientWord, center_coefficientWord]
  simp only [oddProfile, Bool.and_eq_true, decide_eq_true_eq,
    List.all_eq_true, and_assoc]
  constructor
  · rintro ⟨hs, hc, hh⟩
    have hcenter : ∀ t ∈ c.toList, t ≤ 18 ∧ t % 2 = 0 := by
      cases c with
      | none => simp
      | some t =>
        have ht : t ≤ 18 ∧ t % 2 = 0 := by
          by_cases ht : t ≤ 18 ∧ t % 2 = 0
          · exact ht
          · simp [centerCount, ht] at hc
        simpa using ht
    refine ⟨hs, ?_⟩
    intro t ht
    simp only [coefficientWord, List.mem_append, List.mem_reverse,
      or_assoc] at ht
    rcases ht with ht | ht | ht
    · exact hh t ht
    · exact hcenter t ht
    · exact hh t ht
  · rintro ⟨hs, hall⟩
    refine ⟨hs, ?_, ?_⟩
    · cases c with
      | none => rfl
      | some t =>
        have ht := hall t (by simp [coefficientWord])
        simp only [centerCount, if_pos ht]
    · intro t ht
      exact hall t (by simp [coefficientWord, ht])

/-- A positive bounded outer coefficient around a symmetric bounded even
interior satisfies every existing finite-word admissibility condition. -/
theorem admissible_wrap (s : Nat) (xs : List Nat)
    (hrev : xs.reverse = xs) (hs : 0 < s ∧ s ≤ 18)
    (he : ∀ t ∈ xs, t ≤ 18 ∧ t % 2 = 0) :
    Admissible (wrapDigits s s xs).length
      (digitFn (wrapDigits s s xs)) := by
  have hconditions := wrap_word_conditions s xs hs.2
    (bounded_digitFn xs 18 (fun t ht => (he t ht).1))
    (digitFn_symmetric_of_reverse xs hrev)
    (fun i hi _ => by
      rw [digitFn_getElem xs i hi]
      exact (he _ (List.getElem_mem hi)).2)
  rw [Admissible, length_wrapDigits, digitFn_wrap_zero]
  exact ⟨by omega, hs.1, hconditions⟩

end OddPredecessorTargetCensus

#print axioms OddPredecessorTargetCensus.reverse_of_admissible
#print axioms OddPredecessorTargetCensus.oddProfile_wrap_iff
#print axioms OddPredecessorTargetCensus.admissible_wrap
