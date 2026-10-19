import P196.FiniteObservationIsolation.Classification

/-!
# Equality of both complete original exterior streams

This predicate omits the separately observed high carry. Each high stream
still uses its own original numerator, word width, and actual calculated
carry in its denominator. Equality means equality at every finite cutoff.
-/

namespace Agent5.CompleteExteriorFibers

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- Equality of the two original streams at every cutoff, without requiring
the two actual high carries to be equal. -/
def sameStreams (s q : Outer) : Prop :=
  ∀ cut : Nat,
    adicNumeratorDigits cut (zValue q.c q.B - (q.c : Int)) =
      adicNumeratorDigits cut (zValue s.c s.B - (s.c : Int)) ∧
    fractionDigits cut (rhoNum q.c q.B)
        (9 * 10 ^ q.B.length *
          10 ^ (normalize q.B.reverse (if 10 ≤ q.c then 1 else 0)).2) =
      fractionDigits cut (rhoNum s.c s.B)
        (9 * 10 ^ s.B.length *
          10 ^ (normalize s.B.reverse (if 10 ≤ s.c then 1 else 0)).2)

end Agent5.CompleteExteriorFibers
