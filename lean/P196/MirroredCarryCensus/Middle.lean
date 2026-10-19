import P196.MirroredCarryCensus.Scan
import P196.SymmetricCarryCensus.Enumeration

/-!
Complementing the interval between symmetric internal carry boundaries is
an involution of the original admissible words. The incoming carry is
unchanged. The outgoing carries add to one unless the interval consists
entirely of nines, in which case both retain the incoming carry.
-/

set_option autoImplicit false

namespace MirroredCarryCensus

open DecimalDigits FoldedDecimal SevenColumn.ShortBoundary Agent124.PrefixK
open SymmetricCarryCensus

/-- Complement precisely the half-open interval between the two boundaries. -/
def middleComplement (L j : Nat) (w : List Nat) : List Nat :=
  wordOf (fun i =>
    if j ≤ i ∧ i < L - j then 18 - wordFun w i else wordFun w i) L

/-- The interval between the symmetric boundaries consists entirely of nines. -/
def neutralMiddle (L j : Nat) (w : List Nat) : Bool :=
  (List.range (L - 2 * j)).all (fun k => wordFun w (j + k) == 9)

theorem neutralMiddle_iff (L j : Nat) (w : List Nat) :
    neutralMiddle L j w = true ↔
      ∀ k, k < L - 2 * j → wordFun w (j + k) = 9 := by
  simp only [neutralMiddle, List.all_eq_true, List.mem_range, beq_iff_eq]

theorem middleComplement_length (L j : Nat) (w : List Nat) :
    (middleComplement L j w).length = L := by
  simp [middleComplement, wordOf]

theorem middleComplement_get (L j : Nat) (w : List Nat) (i : Nat)
    (hi : i < L) :
    wordFun (middleComplement L j w) i =
      if j ≤ i ∧ i < L - j then 18 - wordFun w i else wordFun w i := by
  exact wordOf_get
    (fun k => if j ≤ k ∧ k < L - j then 18 - wordFun w k else wordFun w k)
    L i hi

private theorem middle_admissible (L j : Nat) (w : List Nat)
    (hj : 0 < j) (hjj : 2 * j ≤ L)
    (ha : Admissible L (wordFun w)) :
    Admissible L (wordFun (middleComplement L j w)) := by
  rcases ha with ⟨hpos, houter, hbound, hsymm, hcenter⟩
  refine ⟨hpos, ?_, ?_, ?_, ?_⟩
  · rw [middleComplement_get L j w 0 hpos, if_neg (by omega)]
    exact houter
  · intro i hi
    rw [middleComplement_get L j w i hi]
    by_cases hm : j ≤ i ∧ i < L - j
    · rw [if_pos hm]
      omega
    · rw [if_neg hm]
      exact hbound i hi
  · intro i hi
    have hri : L - 1 - i < L := by omega
    rw [middleComplement_get L j w i hi,
      middleComplement_get L j w (L - 1 - i) hri]
    by_cases hm : j ≤ i ∧ i < L - j
    · have hr : j ≤ L - 1 - i ∧ L - 1 - i < L - j := by omega
      simp only [hm, hr, if_true, hsymm i hi]
    · have hr : ¬ (j ≤ L - 1 - i ∧ L - 1 - i < L - j) := by omega
      simp only [hm, hr, if_false, hsymm i hi]
  · intro i hi hfix
    rw [middleComplement_get L j w i hi]
    by_cases hm : j ≤ i ∧ i < L - j
    · rw [if_pos hm]
      have hb := hbound i hi
      have hp := hcenter i hi hfix
      omega
    · rw [if_neg hm]
      exact hcenter i hi hfix

private theorem middle_involutive (L j : Nat) (w : List Nat)
    (hlen : w.length = L) (hb : ∀ i, i < L → wordFun w i ≤ 18) :
    middleComplement L j (middleComplement L j w) = w := by
  change wordOf (fun i =>
    if j ≤ i ∧ i < L - j then 18 - wordFun (middleComplement L j w) i
    else wordFun (middleComplement L j w) i) L = w
  refine Eq.trans ?_ (by simpa only [hlen] using wordOf_wordFun w)
  apply wordOf_congr
  intro i hi
  rw [middleComplement_get L j w i hi]
  by_cases hm : j ≤ i ∧ i < L - j
  · simp only [if_pos hm]
    have hqi := hb i hi
    omega
  · simp only [hm, if_false]

private theorem middle_left_carry (L j : Nat) (w : List Nat)
    (hjl : j ≤ L) :
    carry (wordFun (middleComplement L j w)) j = carry (wordFun w) j := by
  apply carry_congr_upto (wordFun (middleComplement L j w)) (wordFun w) j
    ?_ j (Nat.le_refl j)
  intro i hi
  rw [middleComplement_get L j w i (by omega), if_neg (by omega)]

private theorem middle_carry_sum (L j : Nat) (w : List Nat)
    (hjj : 2 * j ≤ L) (ha : Admissible L (wordFun w)) :
    carry (wordFun w) (L - j) +
      carry (wordFun (middleComplement L j w)) (L - j) =
      if neutralMiddle L j w then 2 * carry (wordFun w) j else 1 := by
  have hleft := middle_left_carry L j w (by omega)
  have hc := carry_bounded (wordFun w) L ha.2.2.1 j (by omega)
  have hcomp : ∀ i, i < L - 2 * j →
      wordFun w (j + i) + wordFun (middleComplement L j w) (j + i) = 18 := by
    intro i hi
    have hji : j + i < L := by omega
    have hm : j ≤ j + i ∧ j + i < L - j := by omega
    rw [middleComplement_get L j w (j + i) hji, if_pos hm]
    have hb := ha.2.2.1 (j + i) hji
    omega
  have hsum := complementary_carryIn_sum
    (fun i => wordFun w (j + i))
    (fun i => wordFun (middleComplement L j w) (j + i))
    (carry (wordFun w) j) (L - 2 * j) hc hcomp
  have hend : j + (L - 2 * j) = L - j := by omega
  have hfirst :
      IncomingCarry.carryIn (fun i => wordFun w (j + i))
        (carry (wordFun w) j) (L - 2 * j) = carry (wordFun w) (L - j) := by
    simpa only [hend] using IncomingCarry.carryIn_actual_interval (wordFun w) j
      (L - 2 * j)
  have hsecond :
      IncomingCarry.carryIn (fun i => wordFun (middleComplement L j w) (j + i))
        (carry (wordFun w) j) (L - 2 * j) =
        carry (wordFun (middleComplement L j w)) (L - j) := by
    rw [← hleft]
    simpa only [hend] using IncomingCarry.carryIn_actual_interval
      (wordFun (middleComplement L j w)) j (L - 2 * j)
  rw [hfirst, hsecond] at hsum
  exact hsum

/-- The original enumeration is preserved by the middle involution, with the
exact neutral-interval exception in the symmetric outgoing carry sum. -/
theorem middle_complement_spec (L j : Nat) (w : List Nat)
    (hj : 0 < j) (hjj : 2 * j ≤ L) (hw : w ∈ symWords L) :
    middleComplement L j w ∈ symWords L ∧
      middleComplement L j (middleComplement L j w) = w ∧
      carry (wordFun (middleComplement L j w)) j = carry (wordFun w) j ∧
      carry (wordFun w) (L - j) +
        carry (wordFun (middleComplement L j w)) (L - j) =
        if neutralMiddle L j w then 2 * carry (wordFun w) j else 1 := by
  obtain ⟨hlen, ha⟩ := (mem_symWords_iff L w).mp hw
  refine ⟨(mem_symWords_iff L (middleComplement L j w)).mpr
      ⟨middleComplement_length L j w, middle_admissible L j w hj hjj ha⟩,
    middle_involutive L j w hlen ha.2.2.1,
    middle_left_carry L j w (by omega), middle_carry_sum L j w hjj ha⟩

/-- The middle involution permutes the unchanged original word enumeration. -/
theorem middleComplement_perm (L j : Nat) (hj : 0 < j) (hjj : 2 * j ≤ L) :
    ((symWords L).map (middleComplement L j)).Perm (symWords L) := by
  refine perm_of_nodup_mem_iff _ _ ?_ (symWords_nodup L) ?_
  · apply nodup_map_of_injOn _ _ (symWords_nodup L)
    intro a ha b hb heq
    have h := congrArg (middleComplement L j) heq
    simpa only [(middle_complement_spec L j a hj hjj ha).2.1,
      (middle_complement_spec L j b hj hjj hb).2.1] using h
  · intro w
    constructor
    · intro hw
      obtain ⟨v, hv, rfl⟩ := List.mem_map.mp hw
      exact (middle_complement_spec L j v hj hjj hv).1
    · intro hw
      exact List.mem_map.mpr ⟨middleComplement L j w,
        (middle_complement_spec L j w hj hjj hw).1,
        (middle_complement_spec L j w hj hjj hw).2.1⟩

#print axioms middle_complement_spec
#print axioms middleComplement_perm

end MirroredCarryCensus
