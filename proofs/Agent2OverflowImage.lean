import Agent2OverflowActual
import Agent2OverflowLocal
import Agent2OverflowSharp

/-!
Exact image of the all-width overflow sharp family under Agent8.stepWord.
All carries below are the actual prefix carries of Agent8.normalize.
-/

namespace P196.Agent2.OverflowFibers

set_option maxRecDepth 10000
set_option maxHeartbeats 4000000

theorem five_fourteen_bounds (q : List Nat)
    (hq : ∀ x ∈ q, x = 5 ∨ x = 14) : ∀ x ∈ q, x ≤ 18 := by
  intro x hx
  rcases hq x hx with rfl | rfl <;> decide

theorem five_fourteen_getElemBang (q : List Nat) (i : Nat)
    (hq : ∀ x ∈ q, x = 5 ∨ x = 14) (hi : i < q.length) :
    q[i]! = 5 ∨ q[i]! = 14 := by
  apply hq
  rw [getElemBang_eq q i hi]
  exact List.getElem_mem hi

/-- A five/fourteen coefficient fixes the outgoing carry independently of
the preceding actual binary carry. -/
theorem five_fourteen_carryAt (q : List Nat) (e i : Nat)
    (he : e ≤ 1) (hq : ∀ x ∈ q, x = 5 ∨ x = 14)
    (hi : i < q.length) :
    carryAt q e (i + 1) = q[i]! / 10 := by
  rw [carryAt_succ q e i hi]
  have hb := carryAt_bound q e i he (five_fourteen_bounds q hq)
  rcases five_fourteen_getElemBang q i hq hi with hx | hx <;> rw [hx] <;> omega

/-- Positive symmetric words in the family end in fourteen, so they really
overflow; this is derived from the normalizer rather than assumed. -/
theorem five_fourteen_overflow (q : List Nat) (hpos : 0 < q.length)
    (hsym : q.reverse = q) (hq : ∀ x ∈ q, x = 5 ∨ x = 14)
    (hhead : q[0]! = 14) : carryAt q 0 q.length = 1 := by
  have hc := five_fourteen_carryAt q 0 (q.length - 1) (by decide) hq (by omega)
  have hl : q.length - 1 + 1 = q.length := by omega
  have hs := symmetric_getElemBang q hsym 0 hpos
  simp only [Nat.sub_zero] at hs
  rw [hl, hs, hhead] at hc
  exact hc

theorem image_zipAdd_length (q r : List Nat) (hlen : q.length = r.length) :
    (Agent8.zipAdd q r).length = q.length := by
  induction q generalizing r with
  | nil => simp [Agent8.zipAdd]
  | cons x xs ih =>
    cases r with
    | nil => simp at hlen
    | cons y ys =>
      simp only [Agent8.zipAdd, List.length_cons]
      rw [ih ys (by simpa using hlen)]

theorem image_pair_length (q : List Nat) : (Agent8.pair q).length = q.length := by
  exact image_zipAdd_length q q.reverse (by simp)

theorem overflow_step_length (q : List Nat) (hc : carryAt q 0 q.length = 1) :
    (Agent8.stepWord q).length = q.length + 1 := by
  simp [Agent8.stepWord, image_pair_length, normalize_length, hc]

theorem overflow_step_last (q : List Nat) (hpos : 0 < q.length)
    (hc : carryAt q 0 q.length = 1) :
    (Agent8.stepWord q)[q.length]! = 1 + q[0]! % 10 := by
  have hn : (Agent8.normalize q 0).length = q.length + 1 := by
    simp [normalize_length, hc]
  unfold Agent8.stepWord
  rw [pair_getElemBang _ q.length (by omega), hn]
  simp only [Nat.add_sub_cancel, Nat.sub_self]
  rw [normalize_final_getElemBang, hc, normalize_getElemBang q 0 0 hpos]
  simp

/-- Every actual interior target coefficient equals ten, including positions
whose reflected source intervals overlap. -/
theorem five_fourteen_step_inner (q : List Nat) (i : Nat)
    (hsym : q.reverse = q) (hq : ∀ x ∈ q, x = 5 ∨ x = 14)
    (hc : carryAt q 0 q.length = 1) (h0 : 0 < i) (hi : i < q.length) :
    (Agent8.stepWord q)[i]! = 10 := by
  rw [overflow_step_inner q i h0 hi hc]
  have hlow := five_fourteen_carryAt q 0 (i - 1) (by decide) hq (by omega)
  have hhigh := five_fourteen_carryAt q 0 (q.length - i - 1)
    (by decide) hq (by omega)
  have hil : i - 1 + 1 = i := by omega
  have hir : q.length - i - 1 + 1 = q.length - i := by omega
  rw [hil] at hlow
  rw [hir] at hhigh
  have hs1 := symmetric_getElemBang q hsym (i - 1) (by omega)
  have hs2 := symmetric_getElemBang q hsym i hi
  have hi1 : q.length - 1 - (i - 1) = q.length - i := by omega
  have hi2 : q.length - 1 - i = q.length - i - 1 := by omega
  rw [hi1] at hs1
  rw [hi2] at hs2
  rw [hlow, hhigh, hs1, hs2]
  rcases five_fourteen_getElemBang q i hq hi with hx | hx <;>
    rcases five_fourteen_getElemBang q (i - 1) hq (by omega) with hp | hp <;>
    rw [hx, hp] <;> decide

theorem constant_middle_getElemBang (m i : Nat) (hi : i < m + 2) :
    (5 :: (List.replicate m 10 ++ [5]))[i]! =
      if i = 0 ∨ i = m + 1 then 5 else 10 := by
  cases i with
  | zero => simp
  | succ i =>
    rw [List.getElem!_cons_succ]
    by_cases him : i < m
    · rw [List.getElem!_eq_getElem?_getD,
        List.getElem?_append_left (by simpa using him), List.getElem?_replicate]
      simp [him, show i + 1 ≠ m + 1 from by omega]
    · have hieq : i = m := by omega
      subst i
      simp [List.getElem!_eq_getElem?_getD, List.getElem?_append_right]

/-- The exact entire target word, for every positive symmetric input width.
No carry or independent transition premise appears in the conclusion. -/
theorem five_fourteen_step_image (q : List Nat) (hpos : 0 < q.length)
    (hsym : q.reverse = q) (hq : ∀ x ∈ q, x = 5 ∨ x = 14)
    (hhead : q[0]! = 14) :
    Agent8.stepWord q = 5 :: (List.replicate (q.length - 1) 10 ++ [5]) := by
  have hc := five_fourteen_overflow q hpos hsym hq hhead
  have hn := overflow_step_length q hc
  apply List.ext_getElem (by simp only [List.length_cons, List.length_append,
    List.length_replicate, List.length_nil]; omega)
  intro i hi hj
  rw [← getElemBang_eq _ i hi, ← getElemBang_eq _ i hj]
  rw [constant_middle_getElemBang (q.length - 1) i (by omega)]
  have hlen : q.length - 1 + 1 = q.length := by omega
  rw [hlen]
  by_cases hi0 : i = 0
  · subst i
    rw [overflow_step_outer q hpos hc, hhead]
    simp
  · by_cases hil : i = q.length
    · subst i
      rw [overflow_step_last q hpos hc, hhead]
      simp
    · rw [five_fourteen_step_inner q i hsym hq hc (by omega) (by omega)]
      simp [hi0, hil]

/-- The odd-width construction uses fourteen at the unique center. -/
theorem sharpWord_center (bs : List Bool) :
    (sharpWord true bs)[bs.length + 1]! = 14 := by
  simp only [sharpWord, Bool.true_eq, ↓reduceIte, List.append_assoc,
    List.getElem!_cons_succ]
  rw [List.getElem!_eq_getElem?_getD,
    List.getElem?_append_right (by simp)]
  simp

/-- All canonical whole-word premises are derived for the sharp family. -/
theorem sharpWord_canonical (odd : Bool) (bs : List Bool) :
    Canonical (sharpWord odd bs) := by
  refine ⟨sharpWord_symmetric odd bs,
    five_fourteen_bounds _ (sharpWord_coefficients odd bs),
    sharpWord_positive odd bs, ?_⟩
  intro hodd
  have hl := sharpWord_length odd bs
  cases odd with
  | false =>
    simp only [Bool.false_eq_true, ↓reduceIte] at hl
    omega
  | true =>
    simp only [Bool.true_eq, ↓reduceIte] at hl
    have hc : (sharpWord true bs).length / 2 = bs.length + 1 := by omega
    rw [hc, sharpWord_center]

theorem sharpWord_overflow (odd : Bool) (bs : List Bool) :
    carryAt (sharpWord odd bs) 0 (sharpWord odd bs).length = 1 := by
  apply five_fourteen_overflow
  · simp [sharpWord]
  · exact sharpWord_symmetric odd bs
  · exact sharpWord_coefficients odd bs
  · simp [sharpWord]

/-- The family has one literal target under the original Agent8 transition,
for either parity and every number of independently chosen mirrored pairs. -/
theorem sharpWord_step (odd : Bool) (bs : List Bool) :
    Agent8.stepWord (sharpWord odd bs) =
      sharpTarget (2 * bs.length + (if odd then 1 else 0)) := by
  rw [five_fourteen_step_image (sharpWord odd bs)
    (by simp [sharpWord]) (sharpWord_symmetric odd bs)
    (sharpWord_coefficients odd bs) (by simp [sharpWord])]
  have hlen : (sharpWord odd bs).length - 1 =
      2 * bs.length + (if odd then 1 else 0) + 1 := by
    rw [sharpWord_length]
    omega
  rw [hlen]
  rfl

theorem sharpWord_actualOverflowFiber (odd : Bool) (bs : List Bool) :
    ActualOverflowFiber (2 * bs.length + 2 + (if odd then 1 else 0))
      (sharpTarget (2 * bs.length + (if odd then 1 else 0)))
      (sharpWord odd bs) := by
  exact ⟨sharpWord_length odd bs, sharpWord_canonical odd bs,
    sharpWord_overflow odd bs, sharpWord_step odd bs⟩

#print axioms five_fourteen_carryAt
#print axioms five_fourteen_overflow
#print axioms overflow_step_length
#print axioms five_fourteen_step_inner
#print axioms five_fourteen_step_image
#print axioms sharpWord_center
#print axioms sharpWord_canonical
#print axioms sharpWord_overflow
#print axioms sharpWord_step
#print axioms sharpWord_actualOverflowFiber

end P196.Agent2.OverflowFibers
