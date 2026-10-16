import Agent108WindowWeights
import Mathlib.Tactic.Ring

namespace Agent108.WindowWeights

def blockProduct (b : Nat) (psi : List Nat → ℝ) (e : Bool) : ℝ :=
  windowProduct b psi (localBlock b e)

theorem blockProduct_pos {b : Nat} {psi : List Nat → ℝ}
    (hpsi : PositivePotential b psi) (e : Bool) : 0 < blockProduct b psi e := by
  apply windowProduct_pos hpsi
  intro x hx
  cases e <;> simp [localBlock, block, buffer] at hx <;> omega

theorem blockProduct_false (b : Nat) (psi : List Nat → ℝ) :
    blockProduct b psi false = psi (buffer (b+1)) ^ (b+4) := by
  change windowProduct b psi
    (List.replicate b 9 ++ List.replicate 4 9 ++ List.replicate b 9) = _
  rw [← List.replicate_add, ← List.replicate_add, windowProduct_replicate]
  congr 1
  omega

theorem prefix_buffer_product (b c a : Nat) (psi : List Nat → ℝ) :
    windowProduct b psi ([a] ++ buffer (b+c)) =
      psi ([a] ++ buffer b) * psi (buffer (b+1)) ^ c := by
  have he : [a] ++ buffer (b+c) = ([a] ++ buffer b) ++ buffer c := by
    simp [buffer, List.replicate_add, List.append_assoc]
  rw [he, windowProduct_overlap b psi [a] (buffer b) (buffer c)
    (by simp [buffer])]
  rw [windowProduct_single b psi ([a] ++ buffer b) (by simp [buffer])]
  have hn : buffer b ++ buffer c = buffer (b+c) := by
    simp [buffer, List.replicate_add]
  rw [hn]
  simp [buffer, windowProduct_replicate]

theorem block_buffer_product (b c : Nat) (psi : List Nat → ℝ) (e : Bool) :
    windowProduct b psi (buffer b ++ block e ++ buffer (b+c)) =
      blockProduct b psi e * psi (buffer (b+1)) ^ c := by
  have he : buffer b ++ block e ++ buffer (b+c) =
      (buffer b ++ block e) ++ buffer b ++ buffer c := by
    simp [buffer, List.replicate_add, List.append_assoc]
  rw [he, windowProduct_overlap b psi (buffer b ++ block e) (buffer b) (buffer c)
    (by simp [buffer])]
  change blockProduct b psi e * windowProduct b psi (buffer b ++ buffer c) = _
  have hn : buffer b ++ buffer c = buffer (b+c) := by
    simp [buffer, List.replicate_add]
  rw [hn]
  simp [buffer, windowProduct_replicate]

theorem blocks_buffer_product (b c k a : Nat) (psi : List Nat → ℝ)
    (es : List Bool) :
    windowProduct b psi
      (buffer b ++ blocks (b+c) es ++ [a] ++ List.replicate k 18) =
      psi (buffer (b+1)) ^ (c*es.length) *
        (es.map (blockProduct b psi)).prod * windowProduct b psi (endpoint b k a) := by
  have hpad : (buffer b).length = b := by simp [buffer]
  have hB : buffer (b+c) = buffer c ++ buffer b := by
    simp [buffer, ← List.replicate_add, Nat.add_comm]
  induction es with
  | nil => simp [blocks, endpoint]
  | cons e es ih =>
      have he : buffer b ++ blocks (b+c) (e :: es) ++ [a] ++ List.replicate k 18 =
          (buffer b ++ block e ++ buffer c) ++ buffer b ++
            (blocks (b+c) es ++ [a] ++ List.replicate k 18) := by
        simp [blocks, hB, List.append_assoc]
      rw [he, windowProduct_overlap b psi (buffer b ++ block e ++ buffer c)
        (buffer b) (blocks (b+c) es ++ [a] ++ List.replicate k 18) hpad]
      have hf : windowProduct b psi ((buffer b ++ block e ++ buffer c) ++ buffer b) =
          blockProduct b psi e * psi (buffer (b+1)) ^ c := by
        rw [show (buffer b ++ block e ++ buffer c) ++ buffer b =
          buffer b ++ block e ++ buffer (b+c) by simp [hB, List.append_assoc]]
        exact block_buffer_product b c psi e
      rw [hf]
      have ht : windowProduct b psi
          (buffer b ++ (blocks (b+c) es ++ [a] ++ List.replicate k 18)) =
          psi (buffer (b+1)) ^ (c*es.length) *
            (es.map (blockProduct b psi)).prod * windowProduct b psi (endpoint b k a) := by
        simpa only [List.append_assoc] using ih
      rw [ht]
      simp only [List.length_cons, List.map_cons, List.prod_cons]
      rw [show c * (es.length+1) = c + c*es.length by ring, pow_add]
      ring

theorem assembledHalf_product (b c k a z : Nat) (psi : List Nat → ℝ)
    (es : List Bool) :
    windowProduct b psi
      ([a] ++ buffer (b+c) ++ blocks (b+c) es ++ [z] ++ List.replicate k 18) =
      psi ([a] ++ buffer b) * psi (buffer (b+1)) ^ (c*(es.length+1)) *
        (es.map (blockProduct b psi)).prod * windowProduct b psi (endpoint b k z) := by
  have hpad : (buffer b).length = b := by simp [buffer]
  have hB : buffer (b+c) = buffer c ++ buffer b := by
    simp [buffer, ← List.replicate_add, Nat.add_comm]
  have he : [a] ++ buffer (b+c) ++ blocks (b+c) es ++ [z] ++ List.replicate k 18 =
      ([a] ++ buffer c) ++ buffer b ++
        (blocks (b+c) es ++ [z] ++ List.replicate k 18) := by
    simp [hB, List.append_assoc]
  rw [he, windowProduct_overlap b psi ([a] ++ buffer c) (buffer b)
    (blocks (b+c) es ++ [z] ++ List.replicate k 18) hpad]
  have hf : windowProduct b psi (([a] ++ buffer c) ++ buffer b) =
      psi ([a] ++ buffer b) * psi (buffer (b+1)) ^ c := by
    rw [show ([a] ++ buffer c) ++ buffer b = [a] ++ buffer (b+c) by
      simp [hB, List.append_assoc]]
    exact prefix_buffer_product b c a psi
  rw [hf]
  have ht := blocks_buffer_product b c k z psi es
  simp only [List.append_assoc] at ht
  rw [ht]
  rw [show c * (es.length+1) = c + c*es.length by ring, pow_add]
  ring

theorem inputHalf_product (b c k : Nat) (psi : List Nat → ℝ) (es : List Bool) :
    windowProduct b psi (inputHalf (b+c) k es) =
      psi ([5] ++ buffer b) * psi (buffer (b+1)) ^ (c*(es.length+1)) *
        (es.map (blockProduct b psi)).prod * windowProduct b psi (endpoint b k 14) := by
  exact assembledHalf_product b c k 5 14 psi es

theorem targetHalf_product (b c k r : Nat) (psi : List Nat → ℝ) :
    windowProduct b psi (targetHalf (b+c) k r) =
      psi ([11] ++ buffer b) * psi (buffer (b+1)) ^ (r*(b+c+4)+c) *
        windowProduct b psi (endpoint b k 9) := by
  let N := r*(b+c+4)+c
  have hrep : List.replicate (r*(b+c+4)+(b+c)+1) 9 = buffer (b+N) ++ [9] := by
    change List.replicate (r*(b+c+4)+(b+c)+1) 9 =
      List.replicate (b+N) 9 ++ List.replicate 1 9
    rw [← List.replicate_add]
    congr 1
    dsimp [N]
    omega
  have he : targetHalf (b+c) k r =
      [11] ++ buffer (b+N) ++ blocks (b+N) [] ++ [9] ++ List.replicate k 18 := by
    simp only [targetHalf, hrep, blocks, List.append_nil, List.append_assoc]
  rw [he, assembledHalf_product b N k 11 9 psi []]
  simp [N]

end Agent108.WindowWeights
