import P196.Agent1PeriodicWidthProjection.Agent1PeriodicWidth
import P196.Agent1PeriodicGuard.Agent1PeriodicNumeric

/-!
Ordinary decimal-width residues under the original canonical digit predicate.
The successor wrapper retains the complete in-range column-sum realization.
These wrappers give width equalities only; they do not assert a small-exponent
whole-word quotient formula or supply a freely chosen integer realization.
-/

namespace Agent1.Periodic

open Agent8

/-- A canonical input with the displayed width has the interface residue.
No copy-count positivity or column-sum realization is needed for input width. -/
theorem periodic_decimalLength_mod_eight (B H w : Word) (k n : Nat)
    (d : Nat → Nat) (hlen : w.length = 4)
    (hcan : DecimalDigits.Canonical n d (periodicWord B H w k).length) :
    DecimalQuantitativeMass.decimalLength n % 8 = widthResidue B H := by
  rw [DecimalQuantitativeMass.decimalLength_of_canonical n d _ hcan]
  exact periodicWord_length_mod_eight B H w k hlen

/-- The actual ordinary successor width has the quotient interface residue
for every positive copy count with the original full realization premises. -/
theorem periodic_actual_step_decimalLength_mod_eight (B H w : Word)
    (k : Nat) (hk : 0 < k) (n : Nat) (d : Nat → Nat)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hcan : DecimalDigits.Canonical n d (periodicWord B H w k).length)
    (hrep : ∀ i, i < (periodicWord B H w k).length →
      DecimalDigits.columnSum d (periodicWord B H w k).length i =
        ((periodicWord B H w k)[i]?).getD 0)
    (hlen : w.length = 4) :
    DecimalQuantitativeMass.decimalLength (Lychrel196.step n) % 8 =
      widthResidue (quotientOuter B H w) (quotientCenter B H w) := by
  rw [periodic_actual_step_decimalLength B H w k hk n d hB hH hw hcan hrep]
  unfold widthResidue
  rw [quotient_width_mod_eight B H w hB hH hw hlen]
  unfold rawGamma
  rw [hlen]
  omega

end Agent1.Periodic

#print axioms Agent1.Periodic.periodic_decimalLength_mod_eight
#print axioms Agent1.Periodic.periodic_actual_step_decimalLength_mod_eight
