import P196.StreamObservationInjectivity.Values

/-!
# Original exterior words from finite separate digit streams

Agent #5. At a fixed nonneutral phase and a shared width n, the first n+1
digits of each original coordinate stream determine every coefficient of a
bounded exterior word. The outgoing high-stream carry is reconstructed from
the observations, rather than assumed equal. Empty, zero-head, and untrimmed
words are included. The conclusion concerns this exterior representation;
it is not injectivity of ordinary reverse-and-add on integers.
-/

namespace Agent5.StreamObservationInjectivity

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- The two finite digit prefixes recover the original bounded exterior word.
No equality of outgoing carries is supplied as a hypothesis. -/
theorem exterior_eq_of_stream_prefixes (c : Nat) (A B : List Nat)
    (hc : nonneutralPhase c)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hlen : A.length = B.length)
    (hlo : adicNumeratorDigits (A.length + 1) (zValue c A - (c : Int)) =
      adicNumeratorDigits (B.length + 1) (zValue c B - (c : Int)))
    (hhi : fractionDigits (A.length + 1) (rhoNum c A)
        (9 * 10 ^ A.length *
          10 ^ (normalize A.reverse (if 10 ≤ c then 1 else 0)).2) =
      fractionDigits (B.length + 1) (rhoNum c B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)) :
    A = B := by
  let k : Nat := if 10 ≤ c then 1 else 0
  let gA := (normalize A.reverse k).2
  let gB := (normalize B.reverse k).2
  have hlow := congrArg lowValue hlo
  rw [low_stream_prefix_value c A hc hA,
    low_stream_prefix_value c B hc hB, hlen] at hlow
  have hV : lowValue A = lowValue B := Nat.add_right_cancel hlow
  have hg : gA = gB := by
    calc
      gA = decodeCarry c
          (adicNumeratorDigits (A.length + 1) (zValue c A - (c : Int)))
          (fractionDigits (A.length + 1) (rhoNum c A)
            (9 * 10 ^ A.length * 10 ^ gA)) :=
        (decodeCarry_correct c A hc hA).symm
      _ = decodeCarry c
          (adicNumeratorDigits (B.length + 1) (zValue c B - (c : Int)))
          (fractionDigits (B.length + 1) (rhoNum c B)
            (9 * 10 ^ B.length * 10 ^ gB)) := by rw [hlo, hhi]
      _ = gB := decodeCarry_correct c B hc hB
  have hhigh := congrArg highValue hhi
  rw [high_stream_prefix_value c A hc hA,
    high_stream_prefix_value c B hc hB] at hhigh
  change (if gA = 0 then 10 * (highValue A + k) + (c - 9 * k)
      else highValue A + k) =
    (if gB = 0 then 10 * (highValue B + k) + (c - 9 * k)
      else highValue B + k) at hhigh
  rw [hg] at hhigh
  have hH : highValue A = highValue B := by
    by_cases hz : gB = 0 <;> simp only [hz, if_true, if_false] at hhigh <;> omega
  exact eq_of_values A B hlen hA hB hV hH

/-- Any common cutoff containing the boundary digit is sufficient. -/
theorem exterior_eq_of_streams_at_cutoff (c cut : Nat) (A B : List Nat)
    (hc : nonneutralPhase c)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hlen : A.length = B.length) (hcut : A.length + 1 ≤ cut)
    (hlo : adicNumeratorDigits cut (zValue c A - (c : Int)) =
      adicNumeratorDigits cut (zValue c B - (c : Int)))
    (hhi : fractionDigits cut (rhoNum c A)
        (9 * 10 ^ A.length *
          10 ^ (normalize A.reverse (if 10 ≤ c then 1 else 0)).2) =
      fractionDigits cut (rhoNum c B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)) :
    A = B := by
  have hsum : A.length + 1 + (cut - (A.length + 1)) = cut :=
    Nat.add_sub_of_le hcut
  have low_take (a : Int) :
      (adicNumeratorDigits cut a).take (A.length + 1) =
        adicNumeratorDigits (A.length + 1) a := by
    simpa only [hsum] using
      adicNumeratorDigits_prefix (A.length + 1) (cut - (A.length + 1)) a
  have high_take (r D : Nat) :
      (fractionDigits cut r D).take (A.length + 1) =
        fractionDigits (A.length + 1) r D := by
    simpa only [hsum] using
      fractionDigits_prefix (A.length + 1) (cut - (A.length + 1)) r D
  apply exterior_eq_of_stream_prefixes c A B hc hA hB hlen
  · have h := congrArg (List.take (A.length + 1)) hlo
    rw [low_take, low_take] at h
    simpa only [hlen] using h
  · have h := congrArg (List.take (A.length + 1)) hhi
    rw [high_take, high_take] at h
    simpa only [hlen] using h

end Agent5.StreamObservationInjectivity
