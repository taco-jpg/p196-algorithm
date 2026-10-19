import P196.MirroredCarryCensus.Middle
import P196.SymmetricCarryCensus.Census

/-!
# Exact counts of neutral middle intervals

Inserting an even number of nines in the middle maps the original shorter
symmetric-word enumeration bijectively onto the neutral-middle sublist.
The first observed carry is unchanged, so its existing marginal count
also counts this sublist. An odd center cannot be neutral because it is even.
-/

set_option autoImplicit false

namespace MirroredCarryCensus

open DecimalDigits FoldedDecimal Agent124.PrefixK SevenColumn.ShortBoundary
open SymmetricCarryCensus

/-- Words whose first observed carry is fixed and whose middle is all nine. -/
def neutralCount (L j a : Nat) : Nat :=
  (symWords L).countP (fun w =>
    (carry (wordFun w) j == a) && neutralMiddle L j w)

private def insertNines (j d : Nat) (w : List Nat) : List Nat :=
  wordOf (fun i => if i < j then wordFun w i
    else if i < j + 2 * d then 9 else wordFun w (i - 2 * d)) (2 * (j + d))

private def removeMiddle (j d : Nat) (w : List Nat) : List Nat :=
  wordOf (fun i => if i < j then wordFun w i
    else wordFun w (i + 2 * d)) (2 * j)

private theorem insertNines_get (j d : Nat) (w : List Nat) (i : Nat)
    (hi : i < 2 * (j + d)) :
    wordFun (insertNines j d w) i =
      if i < j then wordFun w i
      else if i < j + 2 * d then 9 else wordFun w (i - 2 * d) := by
  exact wordOf_get _ _ _ hi

private theorem removeMiddle_get (j d : Nat) (w : List Nat) (i : Nat)
    (hi : i < 2 * j) :
    wordFun (removeMiddle j d w) i =
      if i < j then wordFun w i else wordFun w (i + 2 * d) := by
  exact wordOf_get _ _ _ hi

private theorem insertNines_mem (j d : Nat) (w : List Nat) (hj : 0 < j)
    (hw : w ∈ symWords (2 * j)) : insertNines j d w ∈ symWords (2 * (j + d)) := by
  have ha := ((mem_symWords_iff (2 * j) w).mp hw).2
  apply (mem_symWords_iff (2 * (j + d)) _).mpr
  refine ⟨by simp only [insertNines, wordOf_length], by omega, ?_, ?_, ?_, ?_⟩
  · rw [insertNines_get j d w 0 (by omega), if_pos hj]
    exact ha.2.1
  · intro i hi
    rw [insertNines_get j d w i hi]
    by_cases hl : i < j
    · rw [if_pos hl]
      exact ha.2.2.1 i (by omega)
    · rw [if_neg hl]
      by_cases hm : i < j + 2 * d
      · rw [if_pos hm]
        decide
      · rw [if_neg hm]
        exact ha.2.2.1 (i - 2 * d) (by omega)
  · intro i hi
    have hr : 2 * (j + d) - 1 - i < 2 * (j + d) := by omega
    rw [insertNines_get j d w i hi, insertNines_get j d w _ hr]
    by_cases hl : i < j
    · rw [if_pos hl, if_neg (by omega : ¬ 2 * (j + d) - 1 - i < j),
        if_neg (by omega : ¬ 2 * (j + d) - 1 - i < j + 2 * d)]
      rw [show (2 * (j + d) - 1 - i) - 2 * d = 2 * j - 1 - i by omega]
      exact ha.2.2.2.1 i (by omega)
    · rw [if_neg hl]
      by_cases hm : i < j + 2 * d
      · rw [if_pos hm, if_neg (by omega : ¬ 2 * (j + d) - 1 - i < j),
          if_pos (by omega : 2 * (j + d) - 1 - i < j + 2 * d)]
      · rw [if_neg hm, if_pos (by omega : 2 * (j + d) - 1 - i < j)]
        have he : 2 * j - 1 - (i - 2 * d) = 2 * (j + d) - 1 - i := by omega
        simpa only [he] using ha.2.2.2.1 (i - 2 * d) (by omega)
  · intro i hi he
    omega

private theorem removeMiddle_mem (j d : Nat) (w : List Nat) (hj : 0 < j)
    (hw : w ∈ symWords (2 * (j + d))) : removeMiddle j d w ∈ symWords (2 * j) := by
  have ha := ((mem_symWords_iff (2 * (j + d)) w).mp hw).2
  apply (mem_symWords_iff (2 * j) _).mpr
  refine ⟨by simp only [removeMiddle, wordOf_length], by omega, ?_, ?_, ?_, ?_⟩
  · rw [removeMiddle_get j d w 0 (by omega), if_pos hj]
    exact ha.2.1
  · intro i hi
    rw [removeMiddle_get j d w i hi]
    by_cases hl : i < j
    · rw [if_pos hl]
      exact ha.2.2.1 i (by omega)
    · rw [if_neg hl]
      exact ha.2.2.1 (i + 2 * d) (by omega)
  · intro i hi
    have hr : 2 * j - 1 - i < 2 * j := by omega
    rw [removeMiddle_get j d w i hi, removeMiddle_get j d w _ hr]
    by_cases hl : i < j
    · rw [if_pos hl, if_neg (by omega : ¬ 2 * j - 1 - i < j)]
      rw [show (2 * j - 1 - i) + 2 * d = 2 * (j + d) - 1 - i by omega]
      exact ha.2.2.2.1 i (by omega)
    · rw [if_neg hl, if_pos (by omega : 2 * j - 1 - i < j)]
      have he : 2 * (j + d) - 1 - (i + 2 * d) = 2 * j - 1 - i := by omega
      simpa only [he] using ha.2.2.2.1 (i + 2 * d) (by omega)
  · intro i hi he
    omega

private theorem insertNines_neutral (j d : Nat) (w : List Nat) :
    neutralMiddle (2 * (j + d)) j (insertNines j d w) = true := by
  apply (neutralMiddle_iff _ _ _).mpr
  intro k hk
  rw [insertNines_get j d w (j + k) (by omega),
    if_neg (by omega : ¬ j + k < j), if_pos (by omega : j + k < j + 2 * d)]

private theorem remove_insert (j d : Nat) (w : List Nat) (hlen : w.length = 2 * j) :
    removeMiddle j d (insertNines j d w) = w := by
  change wordOf (fun i => if i < j then wordFun (insertNines j d w) i
    else wordFun (insertNines j d w) (i + 2 * d)) (2 * j) = w
  calc
    _ = wordOf (wordFun w) (2 * j) := by
      apply wordOf_congr
      intro i hi
      by_cases hl : i < j
      · rw [if_pos hl, insertNines_get j d w i (by omega), if_pos hl]
      · rw [if_neg hl, insertNines_get j d w (i + 2 * d) (by omega),
          if_neg (by omega : ¬ i + 2 * d < j),
          if_neg (by omega : ¬ i + 2 * d < j + 2 * d)]
        simp only [Nat.add_sub_cancel]
    _ = w := by simpa only [hlen] using wordOf_wordFun w

private theorem insert_remove (j d : Nat) (w : List Nat)
    (hlen : w.length = 2 * (j + d))
    (hn : neutralMiddle (2 * (j + d)) j w = true) :
    insertNines j d (removeMiddle j d w) = w := by
  change wordOf (fun i => if i < j then wordFun (removeMiddle j d w) i
    else if i < j + 2 * d then 9
    else wordFun (removeMiddle j d w) (i - 2 * d)) (2 * (j + d)) = w
  calc
    _ = wordOf (wordFun w) (2 * (j + d)) := by
      apply wordOf_congr
      intro i hi
      by_cases hl : i < j
      · rw [if_pos hl, removeMiddle_get j d w i (by omega), if_pos hl]
      · rw [if_neg hl]
        by_cases hm : i < j + 2 * d
        · rw [if_pos hm]
          have h := (neutralMiddle_iff _ _ _).mp hn (i - j) (by omega)
          simpa only [show j + (i - j) = i by omega] using h.symm
        · rw [if_neg hm, removeMiddle_get j d w (i - 2 * d) (by omega),
            if_neg (by omega : ¬ i - 2 * d < j)]
          rw [show (i - 2 * d) + 2 * d = i by omega]
    _ = w := by simpa only [hlen] using wordOf_wordFun w

private theorem insertNines_carry (j d : Nat) (w : List Nat) :
    carry (wordFun (insertNines j d w)) j = carry (wordFun w) j := by
  apply carry_congr_upto _ _ j _ j (Nat.le_refl j)
  intro i hi
  rw [insertNines_get j d w i (by omega), if_pos hi]

private theorem neutral_image_perm (j d : Nat) (hj : 0 < j) :
    ((symWords (2 * j)).map (insertNines j d)).Perm
      ((symWords (2 * (j + d))).filter (neutralMiddle (2 * (j + d)) j)) := by
  refine perm_of_nodup_mem_iff _ _ ?_ ?_ ?_
  · apply nodup_map_of_injOn _ _ (symWords_nodup (2 * j))
    intro a ha b hb heq
    have h := congrArg (removeMiddle j d) heq
    have hla := ((mem_symWords_iff (2 * j) a).mp ha).1
    have hlb := ((mem_symWords_iff (2 * j) b).mp hb).1
    simpa only [remove_insert j d a hla, remove_insert j d b hlb] using h
  · exact List.Pairwise.filter _ (symWords_nodup (2 * (j + d)))
  · intro w
    simp only [List.mem_filter]
    constructor
    · intro hw
      obtain ⟨v, hv, rfl⟩ := List.mem_map.mp hw
      exact ⟨insertNines_mem j d v hj hv, insertNines_neutral j d v⟩
    · rintro ⟨hw, hn⟩
      refine List.mem_map.mpr ⟨removeMiddle j d w, removeMiddle_mem j d w hj hw, ?_⟩
      exact insert_remove j d w ((mem_symWords_iff _ _).mp hw).1 hn

/-- At even width, a neutral middle has the same carry census as the shorter word. -/
theorem neutral_count_even (m j a : Nat) (hj : 0 < j) (hjm : j ≤ m) (ha : a ≤ 1) :
    neutralCount (2 * m) j a = 9 * 19 ^ (j - 1) := by
  have hm : j + (m - j) = m := by omega
  have hc := (neutral_image_perm j (m - j) hj).countP_eq
    (fun w => carry (wordFun w) j == a)
  simp only [List.countP_map, List.countP_filter, Function.comp_def,
    insertNines_carry, hm] at hc
  have hs : (symWords (2 * j)).countP (fun w => carry (wordFun w) j == a) =
      9 * 19 ^ (j - 1) := by
    have h := internal_carry_count (2 * j) j a hj (by omega) ha
    have hd : (2 * j) / 2 = j := by omega
    have he : (2 * j) % 2 = 0 := by omega
    simpa only [hd, he, if_true, Nat.mul_one] using h
  simpa only [neutralCount] using hc.symm.trans hs

/-- At odd width, the even center prevents a neutral middle. -/
theorem neutral_count_odd (m j a : Nat) (_hj : 0 < j) (hjm : j ≤ m) (_ha : a ≤ 1) :
    neutralCount (2 * m + 1) j a = 0 := by
  unfold neutralCount
  apply List.countP_eq_zero.mpr
  intro w hw h
  simp only [Bool.and_eq_true] at h
  have hn := (neutralMiddle_iff (2 * m + 1) j w).mp h.2 (m - j) (by omega)
  rw [show j + (m - j) = m by omega] at hn
  have hadm := ((mem_symWords_iff (2 * m + 1) w).mp hw).2
  have heven := hadm.2.2.2.2 m (by omega) (by omega)
  omega

#print axioms neutral_count_even
#print axioms neutral_count_odd

end MirroredCarryCensus
