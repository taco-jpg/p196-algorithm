import P196.OddTargetPredecessorParity.Definitions
import P196.Agent101NonpalindromicFibers.Agent101PalindromeFibers
import P196.Drafts.Agent103ResidualFiveFibers.ResidualFiveResidues

/-!
# Increasing the outer coefficient of an odd profile

Agent #6: the existing odd-multiplicity test for an odd outer coefficient
selects the five values one, three, five, seven and nine. Increasing that
coefficient in both mirrored positions gives an even profile with an
actual palindromic member. The positional change is exactly one at each
end of the original coefficient word.
-/

set_option autoImplicit false

namespace OddTargetPredecessorParity

open Agent101 Lychrel196 CompleteFiberParity
open Agent103.ResidualFiveResidues

/-- An odd outer profile has odd multiplicity exactly when increasing its
outer coefficient by one gives a palindromic member and the original
outer coefficient is at most nine. Invalid profiles remain covered. -/
theorem oddProfile_iff_shifted_palindrome (s : Nat) (h : List Nat) (c : Option Nat)
    (hodd : s % 2 = 1) :
    oddProfile (s :: h) c = true ↔
      (∃ p, p ∈ numericFiber ((s + 1) :: h) c ∧ Palindrome p) ∧
      s ≤ 9 := by
  constructor
  · intro ho
    have ht :
        ((s ≤ 9 ∧ s % 2 = 1) ∨
          (10 ≤ s ∧ s ≤ 18 ∧ s % 2 = 0)) ∧
        centerCount c = 1 ∧
        (∀ t ∈ h, t ≤ 18 ∧ t % 2 = 0) := by
      simpa only [oddProfile, Bool.and_eq_true, decide_eq_true_eq,
        List.all_eq_true, and_assoc] using ho
    have hs : s ≤ 9 := by omega
    have hm : profileCount (s :: h) c % 2 = 1 := by
      simpa [ho] using profileCount_mod_two (s :: h) c
    have hp : 0 < profileCount (s :: h) c := by omega
    have hrest : 0 < centerCount c * natProduct (h.map (pairCount false)) := by
      apply Nat.pos_of_mul_pos_left (a := pairCount true s)
      simpa only [profileCount, Nat.mul_assoc] using hp
    have houter : 0 < pairCount true (s + 1) := by
      have h18 : s + 1 ≤ 18 := by omega
      by_cases h9 : s + 1 ≤ 9 <;> simp [pairCount, h9, h18] <;> omega
    have hshift : 0 < profileCount ((s + 1) :: h) c := by
      simpa only [profileCount, Nat.mul_assoc] using Nat.mul_pos houter hrest
    have hhalf : ∀ t ∈ (s + 1) :: h, t % 2 = 0 := by
      rw [List.forall_mem_cons]
      exact ⟨by omega, fun t hmem => (ht.2.2 t hmem).2⟩
    have hcenter : ∀ t ∈ c.toList, t % 2 = 0 := by
      cases c with
      | none => simp
      | some t =>
          have hcount := ht.2.1
          simp only [centerCount] at hcount
          split at hcount
          · rename_i hvalid
            simpa only [Option.toList_some, List.forall_mem_singleton] using hvalid.2
          · omega
    have hall : ∀ t ∈ coefficientWord ((s + 1) :: h) c, t % 2 = 0 := by
      simp only [coefficientWord, List.forall_mem_append, List.mem_reverse, and_assoc]
      exact ⟨hhalf, hcenter, hhalf⟩
    exact ⟨(palindrome_numericFiber_exists_iff ((s + 1) :: h) c).mpr
      ⟨hshift, hall⟩, hs⟩
  · rintro ⟨⟨p, hp, hpal⟩, hs⟩
    have hall := ((palindrome_mem_numericFiber_iff ((s + 1) :: h) c p).mp
      ⟨hp, hpal⟩).2.1
    obtain ⟨ds, hds, hprofile, _⟩ :=
      (mem_numericFiber_digits ((s + 1) :: h) c p).mp hp
    have hb : ∀ t ∈ coefficientWord ((s + 1) :: h) c, t ≤ 18 := by
      rw [← hprofile]
      exact digitPairSums_bounded ds hds.1
    have hcenter : centerCount c = 1 := by
      cases c with
      | none => rfl
      | some t =>
          have hmem : t ∈ coefficientWord ((s + 1) :: h) (some t) := by
            simp [coefficientWord]
          simp [centerCount, hb t hmem, hall t hmem]
    simp only [oddProfile, Bool.and_eq_true, decide_eq_true_eq,
      List.all_eq_true, and_assoc]
    refine ⟨Or.inl ⟨hs, hodd⟩, hcenter, ?_⟩
    intro t ht
    have hmem : t ∈ coefficientWord ((s + 1) :: h) c := by
      simp [coefficientWord, ht]
    exact ⟨hb t hmem, hall t hmem⟩

/-- Increasing both mirrored outer coefficients adds exactly one at each
end of the unchanged-width positional word. No digit bounds are required. -/
theorem coefficientWord_outer_shift (s : Nat) (h : List Nat) (c : Option Nat) :
    natValue (coefficientWord ((s + 1) :: h) c) =
      natValue (coefficientWord (s :: h) c) +
        10 ^ ((coefficientWord (s :: h) c).length - 1) + 1 := by
  simp only [coefficientWord_cons, natValue_wrap, length_wrapDigits]
  rw [show (coefficientWord h c).length + 2 - 1 =
    (coefficientWord h c).length + 1 by omega]
  simp only [Nat.add_mul, Nat.one_mul]
  omega

end OddTargetPredecessorParity

#print axioms OddTargetPredecessorParity.oddProfile_iff_shifted_palindrome
#print axioms OddTargetPredecessorParity.coefficientWord_outer_shift
