import Agent108WindowDefs
import FamilyStates
import Mathlib.Tactic.Ring

/-!
Agent #108, session b31b8818.  A long-buffer subfamily of the original
Agent13 family from commit 12a32789056f5eec8247166564ac2ef745c3c9d6.
The new work is a literal list/finite-index embedding.  Arithmetic transitions
and finite safety are reused from `Agent13ProductWeights.familyState_spec`.
Physical buffer length is `4*p`; window width is a separate parameter.
-/

namespace Agent108.WindowWeights

/-- Insert `p` old false blocks before, between, and after the chosen bits. -/
def expandBits (p : Nat) (es : List Bool) : List Bool :=
  List.replicate p false ++ es.flatMap (fun e => e :: List.replicate p false)

theorem padded_flatMap_length (p : Nat) (es : List Bool) :
    (es.flatMap (fun e => e :: List.replicate p false)).length = (p+1)*es.length := by
  induction es with
  | nil => simp
  | cons e es ih =>
      simp only [List.flatMap_cons, List.length_append, List.length_cons,
        List.length_replicate, ih, Nat.mul_succ]
      omega

theorem expandBits_length (p : Nat) (es : List Bool) :
    (expandBits p es).length = p+(p+1)*es.length := by
  simp only [expandBits, List.length_append, List.length_replicate, padded_flatMap_length]

theorem padded_flatMap_getElem? (p : Nat) (es : List Bool) (j : Nat) :
    (es.flatMap (fun e => e :: List.replicate p false))[(p+1)*j]? = es[j]? := by
  induction es generalizing j with
  | nil => simp
  | cons e es ih =>
      cases j with
      | zero => simp
      | succ j =>
          rw [List.flatMap_cons, List.getElem?_append_right (by
            simp only [List.length_cons, List.length_replicate, Nat.mul_succ]
            omega)]
          simp only [List.length_cons, List.length_replicate, Nat.mul_succ,
            List.getElem?_cons_succ]
          rw [show (p+1)*j+(p+1)-(p+1) = (p+1)*j by omega]
          exact ih j

/-- Original bits are recovered at exactly the displayed positions, including
the out-of-range case on both sides. -/
theorem expandBits_getElem? (p : Nat) (es : List Bool) (j : Nat) :
    (expandBits p es)[p+(p+1)*j]? = es[j]? := by
  rw [expandBits, List.getElem?_append_right (by simp)]
  simp only [List.length_replicate, Nat.add_sub_cancel_left]
  exact padded_flatMap_getElem? p es j

theorem expandBits_injective (p : Nat) : Function.Injective (expandBits p) := by
  intro es fs h
  apply List.ext_getElem?
  intro j
  have he := congrArg (fun xs : List Bool => xs[p+(p+1)*j]?) h
  simpa only [expandBits_getElem?] using he

theorem blocks_zero_append (es fs : List Bool) :
    blocks 0 (es ++ fs) = blocks 0 es ++ blocks 0 fs := by
  induction es with
  | nil => simp [blocks]
  | cons e es ih => simp [blocks, ih, List.append_assoc]

theorem blocks_zero_replicate_false (p : Nat) :
    blocks 0 (List.replicate p false) = buffer (4*p) := by
  induction p with
  | zero => rfl
  | succ p ih =>
      rw [List.replicate_succ, blocks, ih]
      change List.replicate 4 9 ++ List.replicate (4*p) 9 = List.replicate (4*(p+1)) 9
      rw [← List.replicate_add]
      congr 1
      omega

theorem blocks_zero_padded_flatMap (p : Nat) (es : List Bool) :
    blocks 0 (es.flatMap (fun e => e :: List.replicate p false)) = blocks (4*p) es := by
  induction es with
  | nil => rfl
  | cons e es ih =>
      rw [List.flatMap_cons, blocks_zero_append]
      simp only [blocks, blocks_zero_replicate_false, ih, buffer,
        List.replicate_zero, List.append_nil]

theorem blocks_zero_expandBits (p : Nat) (es : List Bool) :
    blocks 0 (expandBits p es) = buffer (4*p) ++ blocks (4*p) es := by
  rw [expandBits, blocks_zero_append, blocks_zero_replicate_false, blocks_zero_padded_flatMap]

/-- The old unbuffered input at the restricted bit list is literally the
long-buffer input.  This is a list equality, not a carry calculation. -/
theorem inputHalf_expandBits (p k : Nat) (es : List Bool) :
    inputHalf 0 k (expandBits p es) = inputHalf (4*p) k es := by
  simp only [inputHalf, blocks_zero_expandBits, buffer, List.replicate_zero,
    List.append_nil, List.append_assoc]

theorem targetHalf_expandBits (p k : Nat) (es : List Bool) :
    targetHalf 0 k (expandBits p es).length = targetHalf (4*p) k es.length := by
  have he : (p+(p+1)*es.length)*(0+4)+0+1 = es.length*(4*p+4)+4*p+1 := by ring
  simp only [targetHalf, expandBits_length, he]

/-- The same restricted bit list on the exact finite domain of the old family. -/
def expandFin (p : Nat) {r : Nat} (e : Fin r → Bool) : Fin (p+(p+1)*r) → Bool :=
  fun i => ((expandBits p (List.ofFn e))[i.val]?).getD false

theorem ofFn_expandFin (p : Nat) {r : Nat} (e : Fin r → Bool) :
    List.ofFn (expandFin p e) = expandBits p (List.ofFn e) := by
  apply List.ext_getElem?
  intro i
  have hl : (expandBits p (List.ofFn e)).length = p+(p+1)*r := by
    simp only [expandBits_length, List.length_ofFn]
  by_cases hi : i < p+(p+1)*r
  · have hli : i < (expandBits p (List.ofFn e)).length := by rw [hl]; exact hi
    simp [List.getElem?_ofFn, hi, expandFin, List.getElem?_eq_getElem hli]
  · rw [List.getElem?_ofFn, dif_neg hi, List.getElem?_eq_none (by rw [hl]; omega)]

theorem expandFin_injective (p r : Nat) :
    Function.Injective (expandFin p : (Fin r → Bool) → Fin (p+(p+1)*r) → Bool) := by
  intro e f h
  funext j
  have hidx : p+(p+1)*j.val < p+(p+1)*r :=
    Nat.add_lt_add_left (Nat.mul_lt_mul_of_pos_left j.isLt (by omega)) p
  have he := congrFun h ⟨p+(p+1)*j.val, hidx⟩
  simpa [expandFin, expandBits_getElem?, List.getElem?_ofFn, j.isLt] using he

/-- These are the original canonical finite states, at a restricted bit family. -/
def embeddedState (p k r : Nat) (e : Fin r → Bool) : Agent13ProductWeights.FiniteWord :=
  Agent13ProductWeights.familyState (p+(p+1)*r) k (expandFin p e)

def embeddedTarget (p k r : Nat) : Agent13ProductWeights.FiniteWord :=
  Agent13ProductWeights.targetState (p+(p+1)*r) k

theorem embeddedState_injective (p k r : Nat) : Function.Injective (embeddedState p k r) := by
  exact (Agent13ProductWeights.familyState_injective (p+(p+1)*r) k).comp
    (expandFin_injective p r)

/-- Arithmetic and safety come solely from the original verified API. -/
theorem embeddedState_spec (p k r : Nat) (e : Fin r → Bool) (hk : 0 < k) :
    Agent13ProductWeights.SafeState (embeddedState p k r e) ∧
      Agent13ProductWeights.MapsTo (embeddedState p k r e) (embeddedTarget p k r) := by
  exact Agent13ProductWeights.familyState_spec (p+(p+1)*r) k (expandFin p e) hk

theorem embeddedTarget_safe (p k r : Nat) (hk : 0 < k) :
    Agent13ProductWeights.SafeState (embeddedTarget p k r) := by
  exact Agent13ProductWeights.targetState_safe (p+(p+1)*r) k hk

/-- The half-word used by window potentials; defined on every finite state. -/
def finiteStateHalf (s : Agent13ProductWeights.FiniteWord) : List Nat :=
  (List.range (s.1/2)).map (Agent13ProductWeights.digits s)

theorem embeddedState_width (p k r : Nat) (e : Fin r → Bool) :
    (embeddedState p k r e).1 = 2*Agent13FoldedFamily.halfWidth (p+(p+1)*r) k := rfl

theorem embeddedTarget_width (p k r : Nat) :
    (embeddedTarget p k r).1 = 2*Agent13FoldedFamily.halfWidth (p+(p+1)*r) k := rfl

theorem embedded_width_eq (p k r : Nat) (e : Fin r → Bool) :
    (embeddedState p k r e).1 = (embeddedTarget p k r).1 := rfl

theorem embedding_block_length (e : Bool) : (block e).length = 4 := by
  cases e <;> rfl

theorem embedding_block_getElem? (e : Bool) (j : Nat) (hj : j < 4) :
    (block e)[j]? = some (Agent13FoldedFamily.blockDigit e j) := by
  have hs : j=0 ∨ j=1 ∨ j=2 ∨ j=3 := by omega
  rcases hs with rfl | rfl | rfl | rfl <;> cases e <;> rfl

theorem blocks_zero_length (es : List Bool) : (blocks 0 es).length = 4*es.length := by
  induction es with
  | nil => rfl
  | cons e es ih =>
      simp only [blocks, buffer, List.length_append, List.length_replicate,
        embedding_block_length, List.length_cons, ih, Nat.mul_succ]
      omega

theorem blocks_zero_getElem? (es : List Bool) (i : Nat) (hi : i < 4*es.length) :
    (blocks 0 es)[i]? =
      some (Agent13FoldedFamily.blockDigit ((es[i/4]?).getD false) (i%4)) := by
  induction es generalizing i with
  | nil => simp at hi
  | cons e es ih =>
      simp only [blocks, buffer, List.replicate_zero, List.append_nil]
      by_cases hi4 : i < 4
      · rw [List.getElem?_append_left (by rw [embedding_block_length]; exact hi4),
          embedding_block_getElem? e i hi4]
        simp [Nat.div_eq_of_lt hi4, Nat.mod_eq_of_lt hi4]
      · rw [List.getElem?_append_right (by rw [embedding_block_length]; omega),
          embedding_block_length]
        have hit : i-4 < 4*es.length := by
          simp only [List.length_cons, Nat.mul_succ] at hi
          omega
        rw [ih (i-4) hit]
        have hd : i/4 = (i-4)/4+1 := by omega
        have hm : (i-4)%4 = i%4 := by omega
        simp only [hd, List.getElem?_cons_succ, hm]

def bitsFromList (es : List Bool) (i : Nat) : Bool := (es[i]?).getD false

theorem extendBits_eq_bitsFromList {r : Nat} (e : Fin r → Bool) :
    Agent13ProductWeights.extendBits e = bitsFromList (List.ofFn e) := by
  funext i
  by_cases hi : i < r <;>
    simp [Agent13ProductWeights.extendBits, bitsFromList, List.getElem?_ofFn, hi]

theorem inputHalf_zero_shape (k : Nat) (es : List Bool) :
    inputHalf 0 k es = 5 :: (blocks 0 es ++ 14 :: List.replicate k 18) := by
  simp [inputHalf, buffer, List.append_assoc]

theorem targetHalf_zero_shape (r k : Nat) :
    targetHalf 0 k r = 11 :: (List.replicate (4*r+1) 9 ++ List.replicate k 18) := by
  simp [targetHalf, Nat.mul_comm]

theorem inputHalf_zero_length (k : Nat) (es : List Bool) :
    (inputHalf 0 k es).length = Agent13FoldedFamily.halfWidth es.length k := by
  simp only [inputHalf_zero_shape, List.length_cons, List.length_append,
    blocks_zero_length, List.length_replicate, Agent13FoldedFamily.halfWidth]
  omega

theorem targetHalf_zero_length (r k : Nat) :
    (targetHalf 0 k r).length = Agent13FoldedFamily.halfWidth r k := by
  simp only [targetHalf_zero_shape, List.length_cons, List.length_append,
    List.length_replicate, Agent13FoldedFamily.halfWidth]
  omega

/-- Pointwise bridge to Agent13's original coefficient function on its full
half-width.  Only the four literal block entries and list indexing are used. -/
theorem inputHalf_zero_getElem? (k : Nat) (es : List Bool) (i : Nat)
    (hi : i < Agent13FoldedFamily.halfWidth es.length k) :
    (inputHalf 0 k es)[i]? =
      some (Agent13FoldedFamily.inputHalf (bitsFromList es) es.length i) := by
  cases i with
  | zero => simp [inputHalf_zero_shape, Agent13FoldedFamily.inputHalf]
  | succ i =>
      rw [inputHalf_zero_shape, List.getElem?_cons_succ]
      simp only [Agent13FoldedFamily.inputHalf, Nat.succ_ne_zero, if_false, Nat.add_sub_cancel]
      by_cases hb : i < 4*es.length
      · rw [if_pos (show i+1 < 4*es.length+1 by omega),
          List.getElem?_append_left (by rw [blocks_zero_length]; exact hb)]
        exact blocks_zero_getElem? es i hb
      · rw [if_neg (show ¬ i+1 < 4*es.length+1 by omega),
          List.getElem?_append_right (by rw [blocks_zero_length]; omega), blocks_zero_length]
        by_cases he : i = 4*es.length
        · subst i
          simp
        · rw [if_neg (show i+1 ≠ 4*es.length+1 by omega)]
          have hj : i-4*es.length = (i-4*es.length-1)+1 := by omega
          rw [hj, List.getElem?_cons_succ]
          apply List.getElem?_replicate_of_lt
          change i+1 < 4*es.length+k+2 at hi
          omega

theorem targetHalf_zero_getElem? (r k i : Nat)
    (hi : i < Agent13FoldedFamily.halfWidth r k) :
    (targetHalf 0 k r)[i]? = some (Agent13FoldedFamily.targetHalf r i) := by
  cases i with
  | zero => simp [targetHalf_zero_shape, Agent13FoldedFamily.targetHalf]
  | succ i =>
      rw [targetHalf_zero_shape, List.getElem?_cons_succ]
      simp only [Agent13FoldedFamily.targetHalf, Nat.succ_ne_zero, if_false]
      by_cases hb : i < 4*r+1
      · rw [if_pos (show i+1 ≤ 4*r+1 by omega),
          List.getElem?_append_left (by simpa using hb), List.getElem?_replicate_of_lt hb]
      · rw [if_neg (show ¬ i+1 ≤ 4*r+1 by omega),
          List.getElem?_append_right (by simp; omega)]
        simp only [List.length_replicate]
        apply List.getElem?_replicate_of_lt
        change i+1 < 4*r+k+2 at hi
        omega

theorem embedding_range_map {α : Type} (xs : List α) (f : Nat → α)
    (h : ∀ i, i < xs.length → xs[i]? = some (f i)) :
    (List.range xs.length).map f = xs := by
  apply List.ext_getElem?
  intro i
  by_cases hi : i < xs.length
  · rw [List.getElem?_map, List.getElem?_range hi]
    exact (h i hi).symm
  · rw [List.getElem?_eq_none (by simp; omega), List.getElem?_eq_none (by omega)]

/-- Exact correspondence between the original finite family state and the
literal complete source half-word, on every one of its coordinates. -/
theorem familyState_half (r k : Nat) (e : Fin r → Bool) :
    finiteStateHalf (Agent13ProductWeights.familyState r k e) =
      inputHalf 0 k (List.ofFn e) := by
  unfold finiteStateHalf
  change (List.range ((2*Agent13FoldedFamily.halfWidth r k)/2)).map
      (Agent13ProductWeights.digits (Agent13ProductWeights.familyState r k e)) = _
  have hl : (inputHalf 0 k (List.ofFn e)).length = Agent13FoldedFamily.halfWidth r k := by
    rw [inputHalf_zero_length, List.length_ofFn]
  rw [show (2*Agent13FoldedFamily.halfWidth r k)/2 =
    Agent13FoldedFamily.halfWidth r k by omega, ← hl]
  apply embedding_range_map
  intro i hi
  have hi' : i < Agent13FoldedFamily.halfWidth r k := by rwa [hl] at hi
  rw [inputHalf_zero_getElem? k (List.ofFn e) i (by
    simpa only [List.length_ofFn] using hi'), List.length_ofFn,
    ← extendBits_eq_bitsFromList e]
  apply congrArg some
  symm
  rw [Agent13ProductWeights.familyState,
    Agent13ProductWeights.digits_encodeWord _ _ _ i (by omega)]
  exact Agent13FoldedFamily.reflect_low _ _ _ hi'

theorem targetState_half (r k : Nat) :
    finiteStateHalf (Agent13ProductWeights.targetState r k) = targetHalf 0 k r := by
  unfold finiteStateHalf
  change (List.range ((2*Agent13FoldedFamily.halfWidth r k)/2)).map
      (Agent13ProductWeights.digits (Agent13ProductWeights.targetState r k)) = _
  have hl : (targetHalf 0 k r).length = Agent13FoldedFamily.halfWidth r k :=
    targetHalf_zero_length r k
  rw [show (2*Agent13FoldedFamily.halfWidth r k)/2 =
    Agent13FoldedFamily.halfWidth r k by omega, ← hl]
  apply embedding_range_map
  intro i hi
  have hi' : i < Agent13FoldedFamily.halfWidth r k := by rwa [hl] at hi
  rw [targetHalf_zero_getElem? r k i hi']
  apply congrArg some
  symm
  rw [Agent13ProductWeights.targetState,
    Agent13ProductWeights.digits_encodeWord _ _ _ i (by omega)]
  exact Agent13FoldedFamily.reflect_low _ _ _ hi'

theorem embeddedState_half (p k r : Nat) (e : Fin r → Bool) :
    finiteStateHalf (embeddedState p k r e) = inputHalf (4*p) k (List.ofFn e) := by
  rw [embeddedState, familyState_half, ofFn_expandFin, inputHalf_expandBits]

theorem embeddedTarget_half (p k r : Nat) :
    finiteStateHalf (embeddedTarget p k r) = targetHalf (4*p) k r := by
  rw [embeddedTarget, targetState_half]
  have h := targetHalf_expandBits p k (List.ofFn (fun _ : Fin r => false))
  simpa only [expandBits_length, List.length_ofFn] using h

end Agent108.WindowWeights
