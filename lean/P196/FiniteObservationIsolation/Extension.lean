import P196.FiniteObservationIsolation.FractionPrefixes
import P196.PhaseEighteenIsolation.Padding
import P196.UniversalPhasePrefixes.Extension

/-!
# Deep extensions of the zero phase

The existing universal word at phase zero adds zeros and a final one. Its
actual carry agrees with the target at every natural alternative phase.
A sufficiently deep final one also preserves both literal observations
through phase eighteen, without any coefficient bound on the target word.
-/

namespace Agent5.FiniteObservationIsolation

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.FiniteExteriorHistories
open Agent5.UniversalPhasePrefixes

/-- The terminal one transfers every natural phase's incoming carry to
zero, preserving the target's actual outgoing carry. -/
theorem zero_extension_carry (d : Nat) (B : List Nat) (m : Nat) :
    (normalize (universalWord 0 B m).reverse
      (if 10 ≤ d then 1 else 0)).2 = (normalize B.reverse 0).2 := by
  have hr : (1 + (if 10 ≤ d then 1 else 0)) / 10 =
      (if 10 ≤ (0 : Nat) then 1 else 0) := by
    split <;> decide
  change (normalize ((B ++ List.replicate m 0) ++ [1]).reverse
    (if 10 ≤ d then 1 else 0)).2 = _
  rw [relay_high_carry 0 d (B ++ List.replicate m 0) 1 hr]
  exact Agent5.PhaseEighteenIsolation.phase_padding_carry_of_le_eighteen
    0 B m (by decide)

/-- All low observations preceding the final one agree with the zero-phase
target, at every natural alternative phase and without coefficient bounds. -/
theorem zero_extension_low (d cut m : Nat) (B : List Nat)
    (hcut : cut ≤ B.length + m) :
    adicNumeratorDigits cut (zValue d (universalWord 0 B m) - (d : Int)) =
      adicNumeratorDigits cut (zValue 0 B - (0 : Int)) := by
  have hlen : cut ≤ (B ++ List.replicate m 0).length := by simpa using hcut
  change adicNumeratorDigits cut
    (zValue d ((B ++ List.replicate m 0) ++ [1]) - (d : Int)) = _
  rw [Agent5.StreamNonisolation.append_low_prefix d cut
    (B ++ List.replicate m 0) 1 hlen]
  rw [low_prefix_phase_independent d 0 cut (B ++ List.replicate m 0) hlen]
  exact Agent5.TrimmedStreamObservation.phase_padding_low 0 cut B m

private theorem zero_extension_numerator (d : Nat) (B : List Nat) (m : Nat) :
    rhoNum d (universalWord 0 B m) =
      (9 * 10 ^ (m + 1)) * highValue B + (9 + d) := by
  have hpad := rhoNum_append_replicate 0 B m
  simp only [rhoNum, Nat.add_zero] at hpad
  change 9 * highValue ((B ++ List.replicate m 0) ++ [1]) + d = _
  rw [highValue_append_single]
  calc
    9 * (10 * highValue (B ++ List.replicate m 0) + 1) + d =
        10 * (9 * highValue (B ++ List.replicate m 0)) + (9 + d) := by omega
    _ = 10 * (10 ^ m * (9 * highValue B)) + (9 + d) := by rw [hpad]
    _ = (9 * 10 ^ (m + 1)) * highValue B + (9 + d) := by
      rw [Nat.pow_succ]
      ac_rfl

/-- A deep terminal one preserves the original high prefix at every phase
at most eighteen. Each denominator uses its own word width and actual
outgoing carry; arbitrary target coefficients and improper fractions are
allowed. -/
theorem zero_extension_high (d cut m : Nat) (B : List Nat)
    (hd : d ≤ 18) (hcut : cut ≤ m) :
    fractionDigits cut (rhoNum d (universalWord 0 B m))
        (9 * 10 ^ (universalWord 0 B m).length *
          10 ^ (normalize (universalWord 0 B m).reverse
            (if 10 ≤ d then 1 else 0)).2) =
      fractionDigits cut (rhoNum 0 B)
        (9 * 10 ^ B.length * 10 ^ (normalize B.reverse 0).2) := by
  let g := (normalize B.reverse 0).2
  have hD : 0 < 10 ^ B.length * 10 ^ g :=
    Nat.mul_pos (Nat.pow_pos (by decide)) (Nat.pow_pos (by decide))
  have hscale : 0 < 9 * 10 ^ (m + 1) :=
    Nat.mul_pos (by decide) (Nat.pow_pos (by decide))
  have htail : 10 ^ cut * (9 + d) < 9 * 10 ^ (m + 1) := by
    have hp : 10 ^ cut ≤ 10 ^ m := Nat.pow_le_pow_right (by decide) hcut
    have hm : 0 < 10 ^ m := Nat.pow_pos (by decide)
    calc
      10 ^ cut * (9 + d) ≤ 10 ^ m * 27 :=
        Nat.mul_le_mul hp (by omega)
      _ < 10 ^ m * 90 := Nat.mul_lt_mul_of_pos_left (by decide) hm
      _ = 9 * 10 ^ (m + 1) := by
        rw [Nat.pow_succ]
        change 10 ^ m * (9 * 10) = 9 * (10 ^ m * 10)
        ac_rfl
  have hden : 9 * 10 ^ (B.length + m + 1) * 10 ^ g =
      (9 * 10 ^ (m + 1)) * (10 ^ B.length * 10 ^ g) := by
    rw [show B.length + m + 1 = B.length + (m + 1) from Nat.add_assoc ..,
      Nat.pow_add]
    ac_rfl
  rw [zero_extension_carry, universalWord_length, zero_extension_numerator]
  change fractionDigits cut
    ((9 * 10 ^ (m + 1)) * highValue B + (9 + d))
    (9 * 10 ^ (B.length + m + 1) * 10 ^ g) = _
  rw [hden, fractionDigits_add_small_tail cut (highValue B)
    (10 ^ B.length * 10 ^ g) (9 * 10 ^ (m + 1)) (9 + d) hD hscale htail]
  simpa only [rhoNum, Nat.add_zero, Nat.mul_assoc] using
    (fractionDigits_scale cut (highValue B) (10 ^ B.length * 10 ^ g)
      9 (by decide)).symm

/-- Both original prefixes and the actual carry of a zero-phase word are
unchanged by this deep extension at any alternative phase at most eighteen. -/
theorem zero_extension_sameObservation (d cut m : Nat) (B : List Nat)
    (hd : d ≤ 18) (hcut : cut ≤ m) :
    sameObservation cut { c := 0, B := B }
      { c := d, B := universalWord 0 B m } := by
  exact ⟨zero_extension_carry d B m,
    zero_extension_low d cut m B (by omega),
    zero_extension_high d cut m B hd hcut⟩

#print axioms zero_extension_carry
#print axioms zero_extension_low
#print axioms zero_extension_high
#print axioms zero_extension_sameObservation

end Agent5.FiniteObservationIsolation
