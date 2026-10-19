import P196.BoundaryOrdinaryStreams.Definitions

/-!
# Actual normalization between two boundary bands

The published band normalizer already includes phases zero and eighteen.
Two uses of that theorem isolate the exterior scans from an arbitrary
bounded middle, retaining the actual terminal carry. This is a surrounding
band identity and does not require complementary inner bands or a supplied
quotient trajectory.
-/

namespace Agent5.BoundaryOrdinaryStreams

/-- Two boundary bands expose both normalized exterior ends and their
calculated terminal carry, independently of the bounded middle word. -/
theorem boundary_surrounded_normalization (c g : Nat) (B W : List Nat)
    (hc : c = 0 ∨ c = 18)
    (hB : Agent109.Bounded B) (hW : Agent109.Bounded W) :
    let k := Agent109.kOf c
    let t := Agent109.tOf c
    let left := Agent109.norm B 0
    let middle := Agent109.norm W k
    let right := Agent109.norm B.reverse k
    Agent109.norm (P196.Agent6.surrounded B c g W) 0 =
      (left.1 ++ [c + left.2 - 10 * k] ++ List.replicate (g + 1) t ++
        middle.1 ++ [c + middle.2 - 10 * k] ++ List.replicate (g + 1) t ++
        right.1, right.2) := by
  have hc18 : c ≤ 18 := by rcases hc with rfl | rfl <;> decide
  have hc9 : c ≠ 9 := by rcases hc with rfl | rfl <;> decide
  have hk : Agent109.kOf c ≤ 1 := by
    unfold Agent109.kOf
    split <;> decide
  have hb := Agent109.norm_carry_le B 0 hB (by decide)
  have hw := Agent109.norm_carry_le W (Agent109.kOf c) hW hk
  dsimp only
  simp only [P196.Agent6.surrounded, Agent109.norm_append]
  rw [Agent109.norm_band c (g + 1) (Agent109.norm B 0).2 hc18 hc9 hb,
    Agent109.norm_band c (g + 1) (Agent109.norm W (Agent109.kOf c)).2 hc18 hc9 hw]
  simp only [List.append_assoc, List.singleton_append]

#print axioms boundary_surrounded_normalization

end Agent5.BoundaryOrdinaryStreams
