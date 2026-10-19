import P196.SymmetricCarryCensus.Enumeration

/-!
An involution of the original admissible symmetric words complements every
strictly internal carry. Both outer coefficients are subtracted from 19;
all interior coefficients are subtracted from 18. An odd center remains
even. The final carry is outside the stated range.
-/

set_option autoImplicit false

namespace SymmetricCarryCensus

open DecimalDigits FoldedDecimal SevenColumn.ShortBoundary Agent124.PrefixK

/-- Complement both outer coefficients around 19 and the interior around 18. -/
def complementWord (w : List Nat) : List Nat :=
  (List.range w.length).map fun i =>
    if i = 0 ∨ i + 1 = w.length then 19 - wordFun w i
    else 18 - wordFun w i

private theorem complementWord_length (w : List Nat) :
    (complementWord w).length = w.length := by
  simp [complementWord]

private theorem complementWord_get (w : List Nat) (i : Nat)
    (hi : i < w.length) :
    wordFun (complementWord w) i =
      if i = 0 ∨ i + 1 = w.length then 19 - wordFun w i
      else 18 - wordFun w i := by
  exact wordOf_get
    (fun k => if k = 0 ∨ k + 1 = w.length then 19 - wordFun w k
      else 18 - wordFun w k) w.length i hi

private theorem complement_admissible (L : Nat) (w : List Nat)
    (hL : 2 ≤ L) (hlen : w.length = L)
    (ha : Admissible L (wordFun w)) :
    Admissible L (wordFun (complementWord w)) := by
  rcases ha with ⟨hpos, houter, hbound, hsymm, hcenter⟩
  have hget : ∀ i, i < L →
      wordFun (complementWord w) i =
        if i = 0 ∨ i + 1 = L then 19 - wordFun w i
        else 18 - wordFun w i := by
    intro i hi
    simpa only [hlen] using complementWord_get w i (by omega)
  refine ⟨hpos, ?_, ?_, ?_, ?_⟩
  · rw [hget 0 hpos, if_pos (Or.inl rfl)]
    have hb := hbound 0 hpos
    omega
  · intro i hi
    rw [hget i hi]
    by_cases he : i = 0 ∨ i + 1 = L
    · rw [if_pos he]
      have hqi : 0 < wordFun w i := by
        rcases he with he | he
        · subst i
          exact houter
        · have hz : L - 1 - i = 0 := by omega
          have hs := hsymm i hi
          rw [hz] at hs
          omega
      omega
    · rw [if_neg he]
      omega
  · intro i hi
    have hri : L - 1 - i < L := by omega
    rw [hget i hi, hget (L - 1 - i) hri]
    by_cases he : i = 0 ∨ i + 1 = L
    · have hr : L - 1 - i = 0 ∨ (L - 1 - i) + 1 = L := by omega
      simp only [he, hr, if_true, hsymm i hi]
    · have hr : ¬ (L - 1 - i = 0 ∨ (L - 1 - i) + 1 = L) := by omega
      simp only [he, hr, if_false, hsymm i hi]
  · intro i hi hc
    have he : ¬ (i = 0 ∨ i + 1 = L) := by omega
    rw [hget i hi, if_neg he]
    have hb := hbound i hi
    have hp := hcenter i hi hc
    omega

private theorem complement_involutive (w : List Nat)
    (hb : ∀ i, i < w.length → wordFun w i ≤ 18) :
    complementWord (complementWord w) = w := by
  change wordOf (fun i =>
    if i = 0 ∨ i + 1 = (complementWord w).length then
      19 - wordFun (complementWord w) i
    else 18 - wordFun (complementWord w) i)
    (complementWord w).length = w
  simp only [complementWord_length]
  refine Eq.trans ?_ (wordOf_wordFun w)
  apply wordOf_congr
  intro i hi
  rw [complementWord_get w i hi]
  have hqi := hb i hi
  by_cases he : i = 0 ∨ i + 1 = w.length
  · simp only [he, if_true]
    omega
  · simp only [he, if_false]
    omega

private theorem complement_carries (L : Nat) (w : List Nat)
    (hlen : w.length = L) (ha : Admissible L (wordFun w)) :
    ∀ j, 0 < j → j < L →
      carry (wordFun w) j + carry (wordFun (complementWord w)) j = 1 := by
  intro j
  induction j with
  | zero =>
    intro hj _
    omega
  | succ j ih =>
    intro _ hjL
    by_cases hj : j = 0
    · subst j
      have hp := ha.2.1
      have hb := ha.2.2.1 0 (by omega)
      have hget : wordFun (complementWord w) 0 = 19 - wordFun w 0 := by
        simpa using complementWord_get w 0 (by omega)
      simp only [carry, Nat.add_zero]
      rw [hget]
      omega
    · have hprev := ih (by omega) (by omega)
      have he : ¬ (j = 0 ∨ j + 1 = w.length) := by omega
      have hget := complementWord_get w j (by omega)
      rw [if_neg he] at hget
      have hb := ha.2.2.1 j (by omega)
      have hsum : wordFun w j + wordFun (complementWord w) j = 18 := by omega
      exact (AstraLanguages.complementary_column
        (wordFun w j) (wordFun (complementWord w) j)
        (carry (wordFun w) j) (carry (wordFun (complementWord w)) j)
        hsum hprev).1

/-- At width at least two, the complement preserves the original enumeration,
is an involution, and swaps every strictly internal carry. -/
theorem complement_spec (L : Nat) (w : List Nat) (hL : 2 ≤ L)
    (hw : w ∈ symWords L) :
    complementWord w ∈ symWords L ∧
      complementWord (complementWord w) = w ∧
      ∀ j, 0 < j → j < L →
        carry (wordFun w) j + carry (wordFun (complementWord w)) j = 1 := by
  obtain ⟨hlen, ha⟩ := (mem_symWords_iff L w).mp hw
  refine ⟨(mem_symWords_iff L (complementWord w)).mpr
    ⟨(complementWord_length w).trans hlen,
      complement_admissible L w hL hlen ha⟩,
    complement_involutive w (fun i hi => ha.2.2.1 i (by omega)),
    complement_carries L w hlen ha⟩

#print axioms complement_spec

end SymmetricCarryCensus
