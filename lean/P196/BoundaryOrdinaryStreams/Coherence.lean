import P196.BoundaryOrdinaryStreams.Definitions

/-!
# Consistent prefixes of the boundary high scan

Any complete high window may be used for a shorter observation that fits
inside it. The corrected readout therefore has exact requested length and
is compatible with taking further prefixes. No validity or positive-head
assumption is needed for these identities on bounded coefficient words.
-/

namespace Agent5.BoundaryOrdinaryStreams

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.BoundedStreamCandidates Agent5.OriginalStreamSuccessor

/-- A complete corrected window gives the same shorter high observation
as the definition using an extended complete window. -/
theorem complete_high_window_take (c cut q : Nat) (B : List Nat)
    (hc : c = 0 ∨ c = 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hcut : cut ≤ B.length + 1 + q) :
    (correctedHigh c (B.length + 1 + q)
      (originalHigh (B.length + 1 + q) { c := c, B := B })).take cut =
      coherentHigh cut { c := c, B := B } := by
  dsimp only [coherentHigh]
  rw [boundary_high_reconstruction c q B hc hB,
    boundary_high_reconstruction c cut B hc hB]
  let k := if 10 ≤ c then 1 else 0
  let t := c - 9 * k
  let W := if (normalize B.reverse k).2 == 0 then
      (normalize B.reverse k).1.reverse ++ [t]
    else [1] ++ (normalize B.reverse k).1.reverse
  change (W ++ List.replicate q t).take cut =
    (W ++ List.replicate cut t).take cut
  have hlen : W.length = B.length + 1 := by
    dsimp only [W]
    split <;> simp [normalize_length]
  have hq : cut - W.length ≤ q := by omega
  simp only [List.take_append_eq_append_take, List.take_replicate,
    Nat.min_eq_left hq, Nat.min_eq_left (Nat.sub_le cut W.length)]

/-- Boundary high observations are coherent under a second prefix cut. -/
theorem coherentHigh_prefix (c cut extra : Nat) (B : List Nat)
    (hc : c = 0 ∨ c = 18) (hB : ∀ x ∈ B, x ≤ 18) :
    (coherentHigh (cut + extra) { c := c, B := B }).take cut =
      coherentHigh cut { c := c, B := B } := by
  dsimp only [coherentHigh]
  rw [List.take_take, Nat.min_eq_left (Nat.le_add_right cut extra)]
  exact complete_high_window_take c cut (cut + extra) B hc hB (by omega)

/-- The coherent high observation has exactly the requested length. -/
theorem coherentHigh_length (c cut : Nat) (B : List Nat)
    (hc : c = 0 ∨ c = 18) (hB : ∀ x ∈ B, x ≤ 18) :
    (coherentHigh cut { c := c, B := B }).length = cut := by
  dsimp only [coherentHigh]
  rw [boundary_high_reconstruction c cut B hc hB]
  split <;> simp [normalize_length, Nat.min_eq_left (by omega :
    cut ≤ B.length + 1 + cut)]

#print axioms complete_high_window_take
#print axioms coherentHigh_prefix
#print axioms coherentHigh_length

end Agent5.BoundaryOrdinaryStreams
