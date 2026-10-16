import Agent101ProfileExtraction

/-!
Agent #105: executable projections of Agent #101's finite coefficientWord.
Symmetric-list decomposition is consumed from Agent101ProfileExtraction,
published at 9bf1b2c35129500da39388727e17523f55fae80e; it is not reproved here.
The integer enumeration and its duplicate freedom are the original
Agent101.numericFiber results. The optional center retains its coefficient.
-/

namespace Agent105WordFiber9df76b

open Agent101

def half (qs : List Nat) : List Nat :=
  qs.take (qs.length / 2)

def center (qs : List Nat) : Option Nat :=
  if qs.length % 2 = 0 then none else qs[qs.length / 2]?

def wordFiber (qs : List Nat) : List Nat :=
  Agent101.numericFiber (half qs) (center qs)

/-- The executable low half projects the original coefficientWord half. -/
theorem half_coefficientWord (h : List Nat) (c : Option Nat) :
    half (coefficientWord h c) = h := by
  unfold half
  rw [← coefficientWord_half_length h c]
  unfold coefficientWord
  rw [List.append_assoc, List.take_append_of_le_length (Nat.le_refl _)]
  exact List.take_length

/-- The executable center projects the original optional coefficient. -/
theorem center_coefficientWord (h : List Nat) (c : Option Nat) :
    center (coefficientWord h c) = c := by
  unfold center
  rw [← coefficientWord_half_length h c]
  cases c with
  | none =>
    have heven : (coefficientWord h none).length % 2 = 0 := by
      simp [length_coefficientWord]
    exact if_pos heven
  | some s =>
    have hodd : (coefficientWord h (some s)).length % 2 ≠ 0 := by
      rw [length_coefficientWord]
      simp only [Option.toList_some, List.length_cons, List.length_nil]
      omega
    rw [if_neg hodd]
    simp only [coefficientWord, Option.toList_some, List.append_assoc]
    rw [List.getElem?_append_right (Nat.le_refl _)]
    simp

/-- Consume Agent #101's symmetric decomposition, then compute its projections. -/
theorem coefficientWord_roundtrip (qs : List Nat) (hrev : qs.reverse = qs) :
    coefficientWord (half qs) (center qs) = qs := by
  obtain ⟨h, c, rfl⟩ := exists_coefficientWord_of_reverse qs hrev
  rw [half_coefficientWord, center_coefficientWord]

/-- Complete ordinary-integer membership at this finite coefficient width. -/
theorem mem_wordFiber (qs : List Nat) (n : Nat)
    (hrev : qs.reverse = qs) (hb : ∀ s ∈ qs, s ≤ 18) :
    n ∈ wordFiber qs ↔ decimalWidth n qs.length ∧
      Lychrel196.step n = natValue qs := by
  have hr := coefficientWord_roundtrip qs hrev
  have hbound : ∀ s ∈ coefficientWord (half qs) (center qs), s ≤ 18 := by
    simpa only [hr] using hb
  simpa only [wordFiber, hr] using
    Agent101.mem_numericFiber (half qs) (center qs) n hbound

/-- Duplicate freedom is inherited even for a nonsymmetric or invalid input. -/
theorem wordFiber_nodup (qs : List Nat) : (wordFiber qs).Nodup :=
  Agent101.numericFiber_nodup (half qs) (center qs)

#print axioms half
#print axioms center
#print axioms wordFiber
#print axioms half_coefficientWord
#print axioms center_coefficientWord
#print axioms coefficientWord_roundtrip
#print axioms mem_wordFiber
#print axioms wordFiber_nodup

end Agent105WordFiber9df76b
