import P196.CompleteFiberParity.ProfileParity
import P196.Agent101NonpalindromicFibers.Agent101PalindromeFibers
import P196.Agent105AllPredecessors.Agent105WordFiber9df76b

/-!
# Odd even-outer profiles and palindromic predecessors

Agent #6: an even outer coefficient removes the odd small-outer cases
from the existing multiplicity test. The remaining even coefficients
are exactly the existing condition for a palindromic member of the
complete profile fiber. Empty and single-digit profiles retain their
original positivity convention.
-/

set_option autoImplicit false

namespace EvenTargetPredecessorParity

open Agent101 Lychrel196 CompleteFiberParity Agent105WordFiber9df76b

private theorem center_even_of_count_one (c : Option Nat)
    (hc : centerCount c = 1) :
    ∀ s ∈ c.toList, s % 2 = 0 := by
  cases c with
  | none => simp
  | some s =>
      have hs : s ≤ 18 ∧ s % 2 = 0 := by
        by_cases hs : s ≤ 18 ∧ s % 2 = 0
        · exact hs
        · simp [centerCount, hs] at hc
      simpa using hs.2

/-- With an even outer coefficient, odd multiplicity means that the
complete profile has a palindromic member and either has no outer pair
or has outer coefficient at least ten. No realizability premise is needed. -/
theorem oddProfile_iff_palindrome (h : List Nat) (c : Option Nat)
    (heven : h.headD 0 % 2 = 0) :
    oddProfile h c = true ↔
      (∃ n, n ∈ numericFiber h c ∧ Palindrome n) ∧
      (h = [] ∨ 10 ≤ h.headD 0) := by
  cases h with
  | nil =>
      rw [palindrome_numericFiber_exists_iff]
      cases c with
      | none => simp [oddProfile, profileCount]
      | some s =>
          by_cases hs : 0 < s <;>
            by_cases hc : s ≤ 18 ∧ s % 2 = 0 <;>
            simp [oddProfile, profileCount, centerCount, coefficientWord, hs, hc] <;>
            omega
  | cons s h =>
      change s % 2 = 0 at heven
      constructor
      · intro ho
        have hm : profileCount (s :: h) c % 2 = 1 := by
          simpa [ho] using profileCount_mod_two (s :: h) c
        have hp : 0 < profileCount (s :: h) c := by omega
        have ht :
            ((s ≤ 9 ∧ s % 2 = 1) ∨
              (10 ≤ s ∧ s ≤ 18 ∧ s % 2 = 0)) ∧
            centerCount c = 1 ∧
            (∀ t ∈ h, t ≤ 18 ∧ t % 2 = 0) := by
          simpa only [oddProfile, Bool.and_eq_true, decide_eq_true_eq,
            List.all_eq_true, and_assoc] using ho
        have hlarge : 10 ≤ s := by omega
        have hh : ∀ t ∈ s :: h, t % 2 = 0 := by
          intro t htmem
          rcases List.mem_cons.mp htmem with rfl | htmem
          · exact heven
          · exact (ht.2.2 t htmem).2
        have hc := center_even_of_count_one c ht.2.1
        have hall : ∀ t ∈ coefficientWord (s :: h) c, t % 2 = 0 := by
          intro t htmem
          simp only [coefficientWord, List.mem_append, List.mem_reverse,
            or_assoc] at htmem
          rcases htmem with htmem | htmem | htmem
          · exact hh t htmem
          · exact hc t htmem
          · exact hh t htmem
        exact ⟨(palindrome_numericFiber_exists_iff (s :: h) c).mpr ⟨hp, hall⟩,
          Or.inr hlarge⟩
      · rintro ⟨⟨n, hn, hpal⟩, hlarge⟩
        have hlarge' : 10 ≤ s := by simpa using hlarge
        have hpall := (palindrome_mem_numericFiber_iff (s :: h) c n).mp ⟨hn, hpal⟩
        have hp := hpall.1
        have hall := hpall.2.1
        obtain ⟨ds, hds, hprofile, _⟩ := (mem_numericFiber_digits (s :: h) c n).mp hn
        have hb : ∀ t ∈ coefficientWord (s :: h) c, t ≤ 18 := by
          rw [← hprofile]
          exact digitPairSums_bounded ds hds.1
        have hs : s ≤ 18 := hb s (by simp [coefficientWord])
        have hc : centerCount c = 1 := by
          have hle := centerCount_le c
          have hne : centerCount c ≠ 0 := by
            intro hz
            simp [profileCount, hz] at hp
          omega
        simp only [oddProfile, Bool.and_eq_true, decide_eq_true_eq,
          List.all_eq_true, and_assoc]
        refine ⟨Or.inr ⟨hlarge', hs, heven⟩, hc, ?_⟩
        intro t ht
        have hmem : t ∈ coefficientWord (s :: h) c := by
          simp [coefficientWord, ht]
        exact ⟨hb t hmem, hall t hmem⟩

/-- The same criterion for the existing executable half/center projection.
Symmetry of the supplied word is unnecessary: this statement concerns its
projected profile fiber, including invalid profiles and the singleton case. -/
theorem oddWordProfile_iff_palindrome (qs : List Nat)
    (hlen : 0 < qs.length) (heven : digitFn qs 0 % 2 = 0) :
    oddProfile (half qs) (center qs) = true ↔
      (∃ n, n ∈ wordFiber qs ∧ Palindrome n) ∧
      (qs.length = 1 ∨ 10 ≤ digitFn qs 0) := by
  by_cases hsingle : qs.length = 1
  · have hhalf : half qs = [] := by simp [half, hsingle]
    simpa [wordFiber, hhalf, hsingle] using
      oddProfile_iff_palindrome [] (center qs) (by simp)
  · have hhalf : half qs ≠ [] ∧ (half qs).headD 0 = digitFn qs 0 := by
      cases qs with
      | nil => simp at hlen
      | cons s qs =>
          have htake : 0 < (s :: qs).length / 2 := by
            simp only [List.length_cons] at hlen hsingle ⊢
            omega
          simp only [half, List.take_cons htake, List.headD_cons]
          constructor
          · simp
          · rfl
    have heven' : (half qs).headD 0 % 2 = 0 := by
      rw [hhalf.2]
      exact heven
    simpa only [wordFiber, hhalf.1, hhalf.2, hsingle, false_or] using
      oddProfile_iff_palindrome (half qs) (center qs) heven'

end EvenTargetPredecessorParity

#print axioms EvenTargetPredecessorParity.oddProfile_iff_palindrome
#print axioms EvenTargetPredecessorParity.oddWordProfile_iff_palindrome
