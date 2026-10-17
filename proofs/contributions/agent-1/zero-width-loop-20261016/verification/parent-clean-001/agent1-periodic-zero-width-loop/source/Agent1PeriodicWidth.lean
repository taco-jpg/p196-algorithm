import Agent1PeriodicQuotient

/-!
The interface-width residue for period-four words and the actual maximal
quotient. These are consequences of the existing exact length and signed
width-balance theorems; no new carry or numeric-orbit hypothesis is used.
-/

namespace Agent1.Periodic

open Agent8 Agent1.RepeatedBlock

/-- The finite exterior-and-center width, reduced modulo eight. -/
def widthResidue (B H : Word) : Nat := (2 * B.length + H.length) % 8

theorem widthResidue_lt (B H : Word) : widthResidue B H < 8 := by
  exact Nat.mod_lt _ (by decide)

/-- Every complete pair of period-four bands contributes a multiple of eight,
including exponent zero and coefficient lists without validity assumptions. -/
theorem periodicWord_length_mod_eight (B H w : Word) (k : Nat)
    (hlen : w.length = 4) :
    (periodicWord B H w k).length % 8 = (2 * B.length + H.length) % 8 := by
  rw [periodicWord_length, hlen]
  omega

/-- Maximal stripping changes the interface residue by the actual terminal
carry. Only the original coefficient bounds and period length are needed. -/
theorem quotient_width_mod_eight (B H w : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hlen : w.length = 4) :
    (2 * (quotientOuter B H w).length + (quotientCenter B H w).length) % 8 =
      (2 * B.length + H.length + rawGamma B H w) % 8 := by
  have h := quotient_width_balance B H w hB hH hw hlen
  omega

/-- The quotient update on the eight possible interface-width residues. -/
theorem quotient_widthResidue (B H w : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hlen : w.length = 4) :
    widthResidue (quotientOuter B H w) (quotientCenter B H w) =
      (widthResidue B H + rawGamma B H w) % 8 := by
  unfold widthResidue
  rw [quotient_width_mod_eight B H w hB hH hw hlen]
  simp only [Nat.add_mod, Nat.mod_mod]

end Agent1.Periodic

#print axioms Agent1.Periodic.widthResidue_lt
#print axioms Agent1.Periodic.periodicWord_length_mod_eight
#print axioms Agent1.Periodic.quotient_width_mod_eight
#print axioms Agent1.Periodic.quotient_widthResidue
