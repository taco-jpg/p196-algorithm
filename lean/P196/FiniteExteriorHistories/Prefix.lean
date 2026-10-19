import P196.UniversalPhasePrefixes.Extension
import P196.Agent6CoordinateDynamics.ExteriorUpdateLaw

/-!
# Finite coefficient windows and original observations

The coefficient window extends the finite word by its own constant phase.
It is unchanged by removing or appending that phase suffix. The observation
predicate only packages the two original coordinate prefixes and the actual
outgoing high normalization carry; it introduces no replacement dynamics.
-/

namespace Agent5.FiniteExteriorHistories

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- The first `cut` coefficients of the word with its constant phase tail. -/
def coefficientPrefix (cut : Nat) (s : Outer) : List Nat :=
  (s.B ++ List.replicate cut s.c).take cut

/-- Equality of the actual high carry and both original coordinate prefixes.
The compared state `q` retains its own phase, width, and denominator. -/
def sameObservation (cut : Nat) (s q : Outer) : Prop :=
  (normalize q.B.reverse (if 10 ≤ q.c then 1 else 0)).2 =
    (normalize s.B.reverse (if 10 ≤ s.c then 1 else 0)).2 ∧
  adicNumeratorDigits cut (zValue q.c q.B - (q.c : Int)) =
    adicNumeratorDigits cut (zValue s.c s.B - (s.c : Int)) ∧
  fractionDigits cut (rhoNum q.c q.B)
      (9 * 10 ^ q.B.length *
        10 ^ (normalize q.B.reverse (if 10 ≤ q.c then 1 else 0)).2) =
    fractionDigits cut (rhoNum s.c s.B)
      (9 * 10 ^ s.B.length *
        10 ^ (normalize s.B.reverse (if 10 ≤ s.c then 1 else 0)).2)

@[simp] theorem coefficientPrefix_length (cut : Nat) (s : Outer) :
    (coefficientPrefix cut s).length = cut := by
  simp [coefficientPrefix, Nat.min_eq_left (show cut ≤ s.B.length + cut by omega)]

theorem coefficientPrefix_of_le (cut : Nat) (s : Outer)
    (hcut : cut ≤ s.B.length) :
    coefficientPrefix cut s = s.B.take cut := by
  exact List.take_append_of_le_length hcut

theorem coefficientPrefix_of_length_le (cut : Nat) (s : Outer)
    (hlen : s.B.length ≤ cut) :
    coefficientPrefix cut s =
      s.B ++ List.replicate (cut - s.B.length) s.c := by
  simp only [coefficientPrefix, List.take_append_eq_append_take,
    List.take_of_length_le hlen, List.take_replicate,
    Nat.min_eq_left (Nat.sub_le cut s.B.length)]

/-- Taking a shorter coefficient window agrees with constructing it directly. -/
theorem coefficientPrefix_take (small big : Nat) (s : Outer)
    (h : small ≤ big) :
    (coefficientPrefix big s).take small = coefficientPrefix small s := by
  unfold coefficientPrefix
  rw [List.take_take, Nat.min_eq_left h]
  simp only [List.take_append_eq_append_take, List.take_replicate,
    Nat.min_eq_left (show small - s.B.length ≤ big by omega),
    Nat.min_eq_left (Nat.sub_le small s.B.length)]

/-- Appending the current phase does not change any coefficient window. -/
theorem coefficientPrefix_append_phase (cut c : Nat) (B : List Nat) (m : Nat) :
    coefficientPrefix cut { c := c, B := B ++ List.replicate m c } =
      coefficientPrefix cut { c := c, B := B } := by
  change ((B ++ List.replicate m c) ++ List.replicate cut c).take cut =
    (B ++ List.replicate cut c).take cut
  rw [List.append_assoc, List.replicate_append_replicate]
  simp only [List.take_append_eq_append_take, List.take_replicate,
    Nat.min_eq_left (show cut - B.length ≤ m + cut by omega),
    Nat.min_eq_left (Nat.sub_le cut B.length)]

/-- Maximal phase-suffix removal preserves every coefficient window. -/
theorem coefficientPrefix_stripSuffix (cut c : Nat) (w : List Nat) :
    coefficientPrefix cut { c := c, B := stripSuffix c w } =
      coefficientPrefix cut { c := c, B := w } := by
  obtain ⟨m, hm⟩ := stripSuffix_spec c w
  calc
    coefficientPrefix cut { c := c, B := stripSuffix c w } =
        coefficientPrefix cut
          { c := c, B := stripSuffix c w ++ List.replicate m c } :=
      (coefficientPrefix_append_phase cut c (stripSuffix c w) m).symm
    _ = coefficientPrefix cut { c := c, B := w } := by rw [hm]

theorem coefficientPrefix_bounded (cut : Nat) (s : Outer)
    (hc : s.c ≤ 18) (hB : ∀ x ∈ s.B, x ≤ 18) :
    ∀ x ∈ coefficientPrefix cut s, x ≤ 18 := by
  intro x hx
  have hx' : x ∈ s.B ++ List.replicate cut s.c := List.mem_of_mem_take hx
  rcases List.mem_append.mp hx' with hx' | hx'
  · exact hB x hx'
  · simpa only [List.eq_of_mem_replicate hx'] using hc

/-- Agreement at a larger spatial cutoff includes every smaller cutoff. -/
theorem sameObservation_take (small big : Nat) (s q : Outer)
    (h : small ≤ big) (hs : sameObservation big s q) :
    sameObservation small s q := by
  have hsum : small + (big - small) = big := Nat.add_sub_of_le h
  refine ⟨hs.1, ?_, ?_⟩
  · have hlo := congrArg (List.take small) hs.2.1
    rw [← hsum, adicNumeratorDigits_prefix, adicNumeratorDigits_prefix] at hlo
    exact hlo
  · have hhi := congrArg (List.take small) hs.2.2
    rw [← hsum, fractionDigits_prefix, fractionDigits_prefix] at hhi
    exact hhi

#print axioms coefficientPrefix_stripSuffix
#print axioms sameObservation_take

end Agent5.FiniteExteriorHistories
