import AdicDigits
import FractionDigits

/-!
Agent #5: assembly of literal coordinate streams for the original exterior map.
The constant tail contributes precisely the new band coefficient, so extending
an already complete stream prefix does not change its trimmed exterior word.
-/

namespace Agent5.ExactDigitStreams

open P196.Agent7.Finite Agent115.ExteriorFactorization

theorem strip_zip_append_replicate (a b : List Nat) (t q : Nat)
    (hlen : a.length = b.length) :
    stripSuffix (2 * t)
      (List.zipWith (fun x y => x + y)
        (a ++ List.replicate q t) (b ++ List.replicate q t)) =
    stripSuffix (2 * t) (List.zipWith (fun x y => x + y) a b) := by
  induction q with
  | zero => simp
  | succ q ih =>
    rw [List.replicate_succ', ← List.append_assoc, ← List.append_assoc]
    rw [strip_zip_append _ _ t t (2 * t)
      (by simp [hlen]) (by omega)]
    exact ih

/-- The original exterior update is the sum of the two literal coordinate
streams, after discarding the new constant band. Every tail length is allowed. -/
theorem outerNext_from_streams (c : Nat) (B : List Nat) (q : Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) :
    outerNext { c := c, B := B } =
      { c := bulkPhase c,
        B := stripSuffix (bulkPhase c)
          (List.zipWith (fun x y => x + y)
            (adicNumeratorDigits (B.length + 1 + q) (zValue c B - (c : Int)))
            (fractionDigits (B.length + 1 + q) (rhoNum c B)
              (9 * 10 ^ B.length *
                10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2))) } := by
  have hlen :
      ((normalize B 0).1 ++
        [c + (normalize B 0).2 - 10 * (if 10 ≤ c then 1 else 0)]).length =
      (if (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 == 0 then
        (normalize B.reverse (if 10 ≤ c then 1 else 0)).1.reverse ++
          [c - 9 * (if 10 ≤ c then 1 else 0)]
       else [1] ++ (normalize B.reverse (if 10 ≤ c then 1 else 0)).1.reverse).length := by
    by_cases hg : (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 = 0 <;>
      simp [hg, normalize_length, Nat.add_comm]
  rw [adicNumeratorDigits_exterior c B q hc hB,
    fractionDigits_exterior c B q hc hB]
  unfold bulkPhase
  rw [strip_zip_append_replicate _ _ _ _ hlen]
  rfl

/-- Any cutoff containing the boundary digit gives exactly the same original
exterior successor. No canonicality, positive-head, or nonempty-word premise
is imposed. -/
theorem outerNext_from_streams_of_cutoff (c : Nat) (B : List Nat) (cut : Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18)
    (hcut : B.length + 1 ≤ cut) :
    outerNext { c := c, B := B } =
      { c := bulkPhase c,
        B := stripSuffix (bulkPhase c)
          (List.zipWith (fun x y => x + y)
            (adicNumeratorDigits cut (zValue c B - (c : Int)))
            (fractionDigits cut (rhoNum c B)
              (9 * 10 ^ B.length *
                10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2))) } := by
  have hlen : B.length + 1 + (cut - (B.length + 1)) = cut := by omega
  simpa only [hlen] using outerNext_from_streams c B (cut - (B.length + 1)) hc hB

#print axioms strip_zip_append_replicate
#print axioms outerNext_from_streams
#print axioms outerNext_from_streams_of_cutoff

end Agent5.ExactDigitStreams
