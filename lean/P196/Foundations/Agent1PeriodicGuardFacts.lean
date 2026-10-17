import P196.Foundations.Agent1PeriodicGuard

/-!
Exact sizes, symmetry, and coefficient bounds of the literal raw output slices.
These are one-transition facts. They do not assert safety, a stripped return,
or preservation of the full canonical valid-state predicate.
-/

namespace Agent1.Periodic

open Agent8 Agent1.RepeatedBlock

/-- Exact sizes of the three slices taken from the exponent-three output. -/
theorem raw_block_lengths (B H w : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hlen : w.length = 4) :
    (rawOuter B H w).length = B.length + 4 ∧
    (rawPeriod B H w).length = 4 ∧
    (rawCenter B H w).length = H.length + 8 + rawGamma B H w := by
  obtain ⟨hO, hW, hM⟩ := raw_blocks_eq_zipper B H w hB hH hw hlen
  rw [hO, hW, hM]
  obtain ⟨hA, hU, hC, hV, hZ⟩ := scan_block_lengths B H w hB hH hw
  have hg : rawGamma B H w ≤ 4 := by
    have := scan_carry_le_one B H w hB hH hw
    change rawGamma B H w ≤ 1 at this
    omega
  exact zipper_block_lengths (leftGuardDigits B w) (leftPeriodDigits B w)
    (centerGuardDigits B H w) (rightPeriodDigits B H w) (rightGuardDigits B H w)
    B.length H.length (rawGamma B H w)
    (by simpa only [hlen] using hA) (hU.trans hlen)
    (by simpa only [hlen] using hC) (hV.trans hlen) hZ hg

/-- The raw center is symmetric even if the original center is not. -/
theorem raw_center_symmetric (B H w : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hlen : w.length = 4) :
    (rawCenter B H w).reverse = rawCenter B H w := by
  rw [(raw_blocks_eq_zipper B H w hB hH hw hlen).2.2]
  exact pair_symmetric _

/-- Every coefficient in all three literal raw slices lies in the decimal
pair-sum range. This does not require symmetry or a positive exterior. -/
theorem raw_blocks_bounded (B H w : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18) :
    Bounded (rawOuter B H w) 18 ∧ Bounded (rawPeriod B H w) 18 ∧
      Bounded (rawCenter B H w) 18 := by
  have hbr : Bounded B.reverse 18 := fun x hx => hB x (List.mem_reverse.mp hx)
  have hwr : Bounded w.reverse 18 := fun x hx => hw x (List.mem_reverse.mp hx)
  have hwhole : Bounded (periodicWord B H w 3) 18 := by
    intro x hx
    simp only [periodicWord, List.mem_append] at hx
    rcases hx with (((hx | hx) | hx) | hx) | hx
    · exact hB x hx
    · exact bounded_pow w 3 18 hw x hx
    · exact hH x hx
    · exact bounded_pow w.reverse 3 18 hwr x hx
    · exact hbr x hx
  have hout : Bounded (stepWord (periodicWord B H w 3)) 18 :=
    pair_bounded _ (normalized_digits_bounded _ 0 hwhole (by omega))
  constructor
  · intro x hx
    exact hout x (List.mem_of_mem_take hx)
  constructor
  · intro x hx
    exact hout x (List.mem_of_mem_drop (List.mem_of_mem_take hx))
  · intro x hx
    exact hout x (List.mem_of_mem_drop (List.mem_of_mem_take hx))

end Agent1.Periodic

#print axioms Agent1.Periodic.raw_block_lengths
#print axioms Agent1.Periodic.raw_center_symmetric
#print axioms Agent1.Periodic.raw_blocks_bounded
