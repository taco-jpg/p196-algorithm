import P196.OrbitPowerResidues.Arithmetic

/-!
The ordinary orbit of 196 has three initial modulo-99 residues before it
enters the existing six-phase table. The table agrees with absolute time
from time three onward, although its imported theorem starts at time six.
Only the three missing finite cases and the phase index are supplied here.

Every displayed residue differs from one. Consequently exponent zero must
be treated separately from the positive-exponent root-count formula.
-/

set_option autoImplicit false

namespace P196.AllTimePowerResidues

open Lychrel196 Agent423.TemporalResidues

/-- The first three residues; its use as an orbit formula requires k < 3. -/
def initialResidue (k : Nat) : Nat :=
  if k = 0 then 97 else if k = 1 then 95 else 91

/-- The exact residues of the ordinary orbit at times zero, one, and two. -/
theorem orbit_residue_of_lt_three (k : Nat) (hk : k < 3) :
    orbit 196 k % 99 = initialResidue k := by
  have h : k = 0 ∨ k = 1 ∨ k = 2 := by omega
  rcases h with rfl | rfl | rfl <;> decide +kernel

/-- The existing phase function uses the absolute time from time three onward. -/
theorem orbit_residue_of_three_le (k : Nat) (hk : 3 ≤ k) :
    orbit 196 k % 99 = phase196 k := by
  by_cases hsix : 6 ≤ k
  · have hindex : 6 + (k - 6) = k := by omega
    have hmod : (k - 6) % 6 = k % 6 := by omega
    simpa only [hindex, phase196, hmod] using orbit196_mod99_table (k - 6)
  · have h : k = 3 ∨ k = 4 ∨ k = 5 := by omega
    rcases h with rfl | rfl | rfl <;> decide +kernel

/-- No time of the ordinary orbit has the residue of a zeroth power. -/
theorem orbit_residue_ne_one (k : Nat) : orbit 196 k % 99 ≠ 1 := by
  by_cases hk : k < 3
  · rw [orbit_residue_of_lt_three k hk]
    have h : k = 0 ∨ k = 1 ∨ k = 2 := by omega
    rcases h with rfl | rfl | rfl <;> decide +kernel
  · rw [orbit_residue_of_three_le k (by omega)]
    have h : ∀ r : Fin 6, phase196 r.val ≠ 1 := by decide +kernel
    simpa only [phase196, Nat.mod_mod] using
      h ⟨k % 6, Nat.mod_lt _ (by decide)⟩

end P196.AllTimePowerResidues
