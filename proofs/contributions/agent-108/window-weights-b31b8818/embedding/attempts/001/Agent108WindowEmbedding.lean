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
  rw [expandBits, List.getElem?_append_right (by simp; omega)]
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
      change (block e ++ blocks 0 (List.replicate p false)) ++
        blocks 0 (es.flatMap (fun e => e :: List.replicate p false)) =
        block e ++ buffer (4*p) ++ blocks (4*p) es
      rw [blocks_zero_replicate_false, ih]

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

end Agent108.WindowWeights
