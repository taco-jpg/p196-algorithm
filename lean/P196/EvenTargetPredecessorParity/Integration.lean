import P196.EvenTargetPredecessorParity.ProfilePalindrome
import P196.EvenTargetPredecessorParity.OutputShape
import P196.CompleteFiberParity.Integration

/-!
# A closed form for complete predecessor parity at every even target

Agent #6: odd multiplicity in a decoded width is equivalent to a
palindromic predecessor and a condition on the target's leading digit.
The palindromic predecessor must be half the target. Combining the two
complete source-width fibers eliminates decoding from the final criterion.
-/

set_option autoImplicit false

namespace EvenTargetPredecessorParity

open DecimalDigits Lychrel196 Agent101
open Agent105WordFiber9df76b Agent105NumericDecoder9df76b
open Agent105DecodedFiber9df76b Agent105Predecessors9df76b
open CompleteFiberParity

/-- At any source width of an even canonical target, the profile test is
odd exactly when the palindromic half-target is present and the target is
a singleton or has leading digit one. -/
theorem even_target_odd_decoded_iff
    (Y : Nat) (e : Nat → Nat) (W L : Nat)
    (hY : Canonical Y e W) (heven : Y % 2 = 0) :
    oddDecoded e W L = true ↔
      (Y / 2 ∈ decodedFiber e W L) ∧ Palindrome (Y / 2) ∧
      (W = 1 ∨ e (W - 1) = 1) := by
  cases hdec : decodeNumerical e W L with
  | none => simp [oddDecoded, decodedFiber, hdec]
  | some qs =>
      obtain ⟨hlen, n, d, _, hn, hprofile, hstep⟩ :=
        (decodeNumerical_eq_some_iff Y e W L qs hY).mp hdec
      have hqpos : 0 < qs.length := by have hL := hn.1; omega
      have hqeven : digitFn qs 0 % 2 = 0 := by
        rw [← hprofile 0 hn.1]
        exact even_predecessor_outer n Y L d hn hstep heven
      have hgate : (qs.length = 1 ∨ 10 ≤ digitFn qs 0) ↔
          (W = 1 ∨ e (W - 1) = 1) := by
        rw [hlen, ← hprofile 0 hn.1]
        exact even_predecessor_outer_iff n Y L W d e hn hY hstep heven
      have hpalMember : (∃ m, m ∈ wordFiber qs ∧ Palindrome m) ↔
          (Y / 2 ∈ wordFiber qs) ∧ Palindrome (Y / 2) := by
        constructor
        · rintro ⟨m, hm, hpal⟩
          have hmdec : m ∈ decodedFiber e W L := by
            simpa only [decodedFiber, hdec] using hm
          obtain ⟨_, _, _, hmstep⟩ := (mem_decodedFiber Y e W L m hY).mp hmdec
          have hfixed : reverse10 m = m := hpal
          have hdouble : m + m = Y := by
            simpa only [step, hfixed] using hmstep
          have hhalf : m = Y / 2 := by omega
          simpa only [hhalf] using And.intro hm hpal
        · rintro ⟨hm, hpal⟩
          exact ⟨Y / 2, hm, hpal⟩
      simp only [oddDecoded, decodedFiber, hdec]
      rw [oddWordProfile_iff_palindrome qs hqpos hqeven, hpalMember, hgate]
      simp only [and_assoc]

/-- An even canonical target has an odd complete positive predecessor
count exactly when its half is a palindrome and it is a singleton or
has leading digit one. -/
theorem even_target_predecessor_odd_iff
    (Y : Nat) (e : Nat → Nat) (W : Nat)
    (hY : Canonical Y e W) (heven : Y % 2 = 0) :
    (predecessors e W).length % 2 = 1 ↔
      Palindrome (Y / 2) ∧ (W = 1 ∨ e (W - 1) = 1) := by
  rw [complete_predecessor_odd_iff Y e W hY,
    even_target_odd_decoded_iff Y e W W hY heven,
    even_target_odd_decoded_iff Y e W (W - 1) hY heven]
  constructor
  · rintro (h | h)
    · exact h.2
    · exact h.2
  · rintro ⟨hpal, hgate⟩
    have hpositive : 0 < Y := by
      rw [← hY.2.2.2]
      exact value_positive e W hY.1 hY.2.2.1
    have hhalfpos : 0 < Y / 2 := by omega
    have hdouble : Y / 2 + Y / 2 = Y := by omega
    have hfixed : reverse10 (Y / 2) = Y / 2 := hpal
    have hstep : step (Y / 2) = Y := by
      simpa only [step, hfixed] using hdouble
    have hm := (mem_predecessors Y e W (Y / 2) hY).mpr ⟨hhalfpos, hstep⟩
    change Y / 2 ∈ decodedFiber e W W ++ decodedFiber e W (W - 1) at hm
    rcases List.mem_append.mp hm with hm | hm
    · exact Or.inl ⟨hm, hpal, hgate⟩
    · exact Or.inr ⟨hm, hpal, hgate⟩

/-- The exact complete predecessor parity, expressed only through the
even target's half, canonical width and leading digit. -/
theorem even_target_predecessor_parity
    (Y : Nat) (e : Nat → Nat) (W : Nat)
    (hY : Canonical Y e W) (heven : Y % 2 = 0) :
    (predecessors e W).length % 2 =
      if Palindrome (Y / 2) ∧ (W = 1 ∨ e (W - 1) = 1) then 1 else 0 := by
  have hiff := even_target_predecessor_odd_iff Y e W hY heven
  split
  · rename_i h
    exact hiff.mpr h
  · rename_i h
    have hnot : (predecessors e W).length % 2 ≠ 1 := by
      intro ho
      exact h (hiff.mp ho)
    omega

/-- The closed form is independent of enumeration order and applies to
every duplicate-free list of all positive ordinary predecessors. -/
theorem ordinary_complete_even_target_parity
    (Y : Nat) (e : Nat → Nat) (W : Nat)
    (hY : Canonical Y e W) (heven : Y % 2 = 0)
    (ns : List Nat) (hnd : ns.Nodup)
    (hcomplete : ∀ n, n ∈ ns ↔ 0 < n ∧ step n = Y) :
    ns.length % 2 =
      if Palindrome (Y / 2) ∧ (W = 1 ∨ e (W - 1) = 1) then 1 else 0 := by
  have hsame : ns.length % 2 = (predecessors e W).length % 2 := by
    rw [ordinary_complete_predecessor_parity Y e W hY ns hnd hcomplete,
      complete_predecessor_parity Y e W hY]
  rw [hsame]
  exact even_target_predecessor_parity Y e W hY heven

#print axioms even_target_odd_decoded_iff
#print axioms even_target_predecessor_odd_iff
#print axioms even_target_predecessor_parity
#print axioms ordinary_complete_even_target_parity

end EvenTargetPredecessorParity
