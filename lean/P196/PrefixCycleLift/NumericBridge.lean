import P196.PrefixCycleLift.Checker
import P196.Agent105InverseBoundaries.Agent105WidthSupport9df76b

/-!
# Ordinary integer semantics of a one-column prefix lift

The source and target are canonical representations of actual consecutive
reverse-and-add integers. Their widths may differ. Canonical uniqueness
transports the exact pair-word update to the caller's target digit function.
-/

namespace PrefixCycleLift

open SevenColumnProjection DecimalDigits FoldedDecimal
open Agent105WidthSupport9df76b

/-- Consecutive ordinary integers have an admitted finite-prefix edge. -/
theorem canonical_step_prefix_admitted
    {n L W : Nat} {d e : Nat → Nat} (k : Nat)
    (hd : Canonical n d L) (he : Canonical (Lychrel196.step n) e W)
    (hk : k ≤ L) :
    ForwardAdmitted (wordPrefix (columnSum d L) k)
      (wordPrefix (columnSum e W) k) := by
  let q : Nat → Nat := columnSum d L
  obtain ⟨f, hf, hrep⟩ := representation_next n d q L hd
    (fun _ _ => rfl)
  have hW : W = nextWidth q L := canonical_width_unique he hf
  have hLW : L ≤ nextWidth q L := by
    unfold nextWidth
    split <;> omega
  have hdigits : ∀ i, i < nextWidth q L → e i = f i := by
    rw [hW] at he
    exact canonical_digits_unique he hf
  have hprefix : wordPrefix (nextColumns q L) k =
      wordPrefix (columnSum e W) k := by
    rw [wordPrefix_eq_range_map, wordPrefix_eq_range_map]
    apply List.map_congr_left
    intro i hi
    have hik : i < k := List.mem_range.mp hi
    have hiW : i < nextWidth q L := by omega
    rw [← hrep i hiW, hW]
    simp only [columnSum, reflected]
    rw [hdigits i hiW, hdigits (nextWidth q L - 1 - i) (by omega)]
  have hactual := actual_forward_admitted q L k
    (NormalizationBridge.canonical_admissible n d L hd) hk
  rw [hprefix] at hactual
  exact hactual

/-- The additional coefficient and boundary carry come from an actual
ordinary reverse-and-add step, including possible overflow. -/
theorem canonical_step_lift
    {n L W : Nat} {d e : Nat → Nat} (k : Nat)
    (hd : Canonical n d L) (he : Canonical (Lychrel196.step n) e W)
    (hk : k + 1 ≤ L) :
    ForwardAdmitted
      (wordPrefix (columnSum d L) k ++ [columnSum d L k])
      (wordPrefix (columnSum e W) k ++ [columnSum e W k]) := by
  have h := canonical_step_prefix_admitted (k + 1) hd he hk
  rw [wordPrefix_succ, wordPrefix_succ] at h
  exact h

end PrefixCycleLift
