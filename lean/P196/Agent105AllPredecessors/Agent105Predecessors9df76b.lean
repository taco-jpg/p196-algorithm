import P196.Agent105AllPredecessors.Agent105DecodedFiber9df76b

/-!
Agent #105 / session 9df76b: the complete ordinary positive predecessor list.
The two branches enumerate exactly the two possible canonical source widths.
Digit splitting, finite symmetric-list decomposition, and numerical decoding
are imported unchanged from the credited preceding modules.
-/

namespace Agent105Predecessors9df76b

open DecimalDigits Lychrel196 Agent101 Agent105DecodedFiber9df76b

/-- All positive one-step predecessors of a canonical target digit function. -/
def predecessors (e : Nat → Nat) (W : Nat) : List Nat :=
  decodedFiber e W W ++ decodedFiber e W (W - 1)

/-- Membership covers every positive ordinary integer, without a source-width premise. -/
theorem mem_predecessors (Y : Nat) (e : Nat → Nat) (W n : Nat)
    (htarget : Canonical Y e W) :
    n ∈ predecessors e W ↔ 0 < n ∧ step n = Y := by
  change n ∈ decodedFiber e W W ++ decodedFiber e W (W - 1) ↔ _
  constructor
  · intro hm
    rcases List.mem_append.mp hm with hm | hm
    · rcases (mem_decodedFiber Y e W W n htarget).mp hm with ⟨hp, d, hd, hs⟩
      exact ⟨hp, hs⟩
    · rcases (mem_decodedFiber Y e W (W - 1) n htarget).mp hm with ⟨hp, d, hd, hs⟩
      exact ⟨hp, hs⟩
  · rintro ⟨hp, hs⟩
    obtain ⟨d, L, hd⟩ := canonical_exists n hp
    have ht : Canonical (step n) e W := by simpa only [hs] using htarget
    rcases Agent105WidthSupport9df76b.step_width_cases hd ht with ⟨hw, hc⟩ | ⟨hw, hc⟩
    · apply List.mem_append.mpr
      left
      apply (mem_decodedFiber Y e W W n htarget).mpr
      exact ⟨hp, d, by simpa only [hw] using hd, hs⟩
    · have hshort : W - 1 = L := by omega
      apply List.mem_append.mpr
      right
      apply (mem_decodedFiber Y e W (W - 1) n htarget).mpr
      exact ⟨hp, d, by simpa only [hshort] using hd, hs⟩

/-- Each branch is duplicate free; a positive integer cannot have both source widths. -/
theorem predecessors_nodup (Y : Nat) (e : Nat → Nat) (W : Nat)
    (htarget : Canonical Y e W) : (predecessors e W).Nodup := by
  change List.Pairwise (fun a b : Nat => a ≠ b)
    (decodedFiber e W W ++ decodedFiber e W (W - 1))
  apply List.pairwise_append.mpr
  refine ⟨decodedFiber_nodup e W W, decodedFiber_nodup e W (W - 1), ?_⟩
  intro a ha b hb hab
  subst b
  have hleft := (mem_decodedFiber_decimalWidth Y e W W a htarget).mp ha
  have hright := (mem_decodedFiber_decimalWidth Y e W (W - 1) a htarget).mp hb
  have heq := decimalWidth_unique a W (W - 1) hleft.1 hright.1
  have hpos := htarget.1
  omega

#print axioms predecessors
#print axioms mem_predecessors
#print axioms predecessors_nodup

end Agent105Predecessors9df76b
