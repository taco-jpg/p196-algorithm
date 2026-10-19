import P196.FiniteExteriorHistories.Prefix
import P196.Agent5ExactDigitStreams.CoordinateStreams
import P196.Agent6CoordinateDynamics.CoordinateCycle

/-!
# Evolution of finite exterior coefficient windows

Every coefficient window of the original successor is the pointwise sum of
the corresponding two original coordinate prefixes. Extending the stripped
word by its new phase is essential at cutoffs that meet the removed suffix.

The remaining statements provide the phase, coefficient, and width bounds
needed to iterate this identity. They do not require a positive first
coefficient or a trimmed input word.
-/

namespace Agent5.FiniteExteriorHistories

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent6.ExteriorCoordinates

/-- At every cutoff, the phase-extended successor coefficients are the sums
of the original low and high observations at that same cutoff. -/
theorem coefficientPrefix_outerNext (cut : Nat) (s : Outer)
    (hc : nonneutralPhase s.c) (hB : ∀ x ∈ s.B, x ≤ 18) :
    coefficientPrefix cut (outerNext s) =
      List.zipWith (fun x y => x + y)
        (adicNumeratorDigits cut (zValue s.c s.B - (s.c : Int)))
        (fractionDigits cut (rhoNum s.c s.B)
          (9 * 10 ^ s.B.length *
            10 ^ (normalize s.B.reverse (if 10 ≤ s.c then 1 else 0)).2)) := by
  rcases s with ⟨c, B⟩
  rw [outerNext_from_streams c B cut hc hB,
    coefficientPrefix_stripSuffix]
  rw [coefficientPrefix_of_le cut _ (by
    simp only [List.length_zipWith, adicNumeratorDigits_length,
      fractionDigits_length, Nat.min_self]
    omega)]
  rw [List.take_zipWith]
  have hcut : B.length + 1 + cut = cut + (B.length + 1) := Nat.add_comm _ _
  rw [hcut, adicNumeratorDigits_prefix, fractionDigits_prefix]

private theorem zip_add_bounded18 (L R : List Nat)
    (hL : ∀ x ∈ L, x ≤ 9) (hR : ∀ x ∈ R, x < 10) :
    ∀ x ∈ List.zipWith (fun a b => a + b) L R, x ≤ 18 := by
  induction L generalizing R with
  | nil => simp
  | cons a L ih =>
    cases R with
    | nil => simp
    | cons b R =>
      intro x hx
      simp only [List.zipWith_cons_cons, List.mem_cons] at hx
      rcases hx with rfl | hx
      · have ha := hL a List.mem_cons_self
        have hb := hR b List.mem_cons_self
        omega
      · exact ih R (fun y hy => hL y (List.mem_cons_of_mem a hy))
          (fun y hy => hR y (List.mem_cons_of_mem b hy)) x hx

/-- The original exterior update preserves the eight nonneutral phases. -/
theorem outerNext_nonneutral (s : Outer) (hc : nonneutralPhase s.c) :
    nonneutralPhase (outerNext s).c := by
  rcases s with ⟨c, B⟩
  change nonneutralPhase (bulkPhase c)
  unfold nonneutralPhase at hc ⊢
  simp only [List.mem_cons, List.mem_nil_iff, or_false] at hc
  rcases hc with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> decide

/-- Summing the two decimal streams preserves the coefficient bound 18. -/
theorem outerNext_bounded (s : Outer) (hc : nonneutralPhase s.c)
    (hB : ∀ x ∈ s.B, x ≤ 18) :
    ∀ x ∈ (outerNext s).B, x ≤ 18 := by
  have hfull := coefficientPrefix_outerNext (outerNext s).B.length s hc hB
  rw [coefficientPrefix_of_le _ _ (Nat.le_refl _), List.take_length] at hfull
  intro x hx
  rw [hfull] at hx
  exact zip_add_bounded18 _ _
    (adicNumeratorDigits_bounded _ _)
    (fractionDigits_exterior_digits_lt_ten s.c s.B _ hc hB) x hx

/-- One original exterior step adds at most one coefficient before trimming.
This width bound holds for arbitrary phases and arbitrary coefficients. -/
theorem outerNext_length_le (s : Outer) :
    (outerNext s).B.length ≤ s.B.length + 1 := by
  rcases s with ⟨c, B⟩
  change (stripSuffix (2 * (c - 9 * (if 10 ≤ c then 1 else 0)))
    (rawSucc c B)).length ≤ B.length + 1
  obtain ⟨m, hm⟩ := stripSuffix_spec
    (2 * (c - 9 * (if 10 ≤ c then 1 else 0))) (rawSucc c B)
  have hlen := congrArg List.length hm
  simp only [List.length_append, List.length_replicate, rawSucc_length] at hlen
  omega

/-- Every finite iterate remains at a nonneutral phase. -/
theorem outerIter_nonneutral (s : Outer) (t : Nat)
    (hc : nonneutralPhase s.c) :
    nonneutralPhase (outerIter t s).c := by
  induction t with
  | zero => exact hc
  | succ t ih => exact outerNext_nonneutral (outerIter t s) ih

/-- Every finite iterate retains the coefficient bound 18. -/
theorem outerIter_bounded (s : Outer) (t : Nat)
    (hc : nonneutralPhase s.c) (hB : ∀ x ∈ s.B, x ≤ 18) :
    ∀ x ∈ (outerIter t s).B, x ≤ 18 := by
  induction t with
  | zero => exact hB
  | succ t ih =>
    exact outerNext_bounded (outerIter t s) (outerIter_nonneutral s t hc) ih

/-- The core width increases by at most the number of elapsed steps, without
any phase, coefficient, or canonicality assumptions. -/
theorem outerIter_length_le (s : Outer) (t : Nat) :
    (outerIter t s).B.length ≤ s.B.length + t := by
  induction t with
  | zero => simp only [outerIter_zero, Nat.add_zero, Nat.le_refl]
  | succ t ih =>
    have hstep := outerNext_length_le (outerIter t s)
    change (outerNext (outerIter t s)).B.length ≤ s.B.length + (t + 1)
    omega

#print axioms coefficientPrefix_outerNext
#print axioms outerNext_nonneutral
#print axioms outerNext_bounded
#print axioms outerNext_length_le
#print axioms outerIter_nonneutral
#print axioms outerIter_bounded
#print axioms outerIter_length_le

end Agent5.FiniteExteriorHistories
