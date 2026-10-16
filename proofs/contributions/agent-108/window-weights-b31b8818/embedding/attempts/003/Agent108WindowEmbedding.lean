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

end Agent108.WindowWeights
