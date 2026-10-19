import P196.CompleteExteriorFibers.Fibers
import P196.CompleteExteriorFibers.BoundaryFamily

/-!
# Complete streams do not always determine the omitted carry

At either even boundary phase, every word width at least three admits two
distinct valid words with the same complete streams. Consequently even a
decoder chosen knowing the phase and exact width cannot recover all valid
words from those streams without additional information.
-/

namespace Agent5.CompleteExteriorFibers

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- No decoder of both complete original streams recovers every valid
word of a fixed width at least three at phase zero or eighteen. The
decoder may be chosen separately for the known phase and exact width. -/
theorem no_boundary_complete_decoder (c n : Nat)
    (hc : c = 0 ∨ c = 18) (hn : 3 ≤ n) :
    ¬ ∃ D : (Nat → List Nat) → (Nat → List Nat) → List Nat,
      ∀ B : List Nat,
        B.length = n → validOuter { c := c, B := B } = true →
        D (fun cut => adicNumeratorDigits cut (zValue c B - (c : Int)))
            (fun cut => fractionDigits cut (rhoNum c B)
              (9 * 10 ^ B.length *
                10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)) = B := by
  rintro ⟨D, hD⟩
  obtain ⟨A, B, hAlen, hBlen, hvA, hvB, hne, _, _, hstreams⟩ :=
    boundary_double_fiber c (n - 3) hc
  have hDA := hD A (show A.length = n by omega) hvA
  have hDB := hD B (show B.length = n by omega) hvB
  have hlo := funext (fun cut => (hstreams cut).1)
  have hhi := funext (fun cut => (hstreams cut).2)
  rw [hlo, hhi] at hDB
  exact hne (hDA.symm.trans hDB)

#print axioms no_boundary_complete_decoder

end Agent5.CompleteExteriorFibers
