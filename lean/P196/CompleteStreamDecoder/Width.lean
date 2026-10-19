import P196.CompleteStreamDecoder.LowValues
import P196.CompleteExteriorFibers.Fibers

/-!
# Width of a complete-stream competitor

The published interior classification already gives exact word equality.
At either boundary, equality of the complete low streams gives equality
of a positional invariant. Terminal trimming bounds the width represented
by that invariant, allowing at most one extra coefficient. The argument
uses the original complete streams and does not bound the widths of states
that agree only through a supplied finite cutoff.
-/

namespace Agent5.CompleteStreamDecoder

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.CompleteExteriorFibers

private theorem bounded_low_value (B : List Nat)
    (hB : ∀ x ∈ B, x ≤ 18) :
    lowValue B + 2 ≤ 2 * 10 ^ B.length := by
  simpa only [highValue_reverse, List.length_reverse] using
    highValue_lt B.reverse
      (fun x hx => hB x (List.mem_reverse.mp hx))

private theorem zero_length_le (A B : List Nat)
    (hB : ∀ x ∈ B, x ≤ 18)
    (ht : A.getLast? ≠ some 0)
    (hz : zValue 0 A = zValue 0 B) :
    A.length ≤ B.length + 1 := by
  have hvalue : lowValue A = lowValue B := by
    simp only [zValue, Int.natCast_zero, Int.zero_mul, Int.sub_zero] at hz
    omega
  rcases List.eq_nil_or_concat A with hnil | ⟨U, x, hA⟩
  · subst A
    simp
  · rw [List.concat_eq_append] at hA
    subst A
    apply Nat.le_of_not_lt
    intro hlength
    have hlen : (U ++ [x]).length = U.length + 1 := by simp
    have hUlen : B.length + 1 ≤ U.length := by omega
    have hxne : x ≠ 0 := by
      intro hx
      apply ht
      simp [hx]
    have hx : 1 ≤ x := by omega
    have hlast : 10 ^ U.length ≤ 10 ^ U.length * x := by
      simpa only [Nat.mul_one] using Nat.mul_le_mul_left (10 ^ U.length) hx
    have hpower : 10 ^ B.length * 10 ≤ 10 ^ U.length := by
      simpa only [Nat.pow_succ] using
        Nat.pow_le_pow_right (by decide : 0 < 10) hUlen
    have hpositive : 0 < 10 ^ B.length := Nat.pow_pos (by decide)
    have hbound := bounded_low_value B hB
    rw [lowValue_append_single] at hvalue
    omega

private theorem eighteen_length_le (A B : List Nat)
    (hA : ∀ x ∈ A, x ≤ 18)
    (ht : A.getLast? ≠ some 18)
    (hz : zValue 18 A = zValue 18 B) :
    A.length ≤ B.length + 1 := by
  have hbalance : lowValue A + 2 * 10 ^ B.length =
      lowValue B + 2 * 10 ^ A.length := by
    change 9 * (lowValue A : Int) - 18 * ((10 : Int) ^ A.length - 1) =
      9 * (lowValue B : Int) - 18 * ((10 : Int) ^ B.length - 1) at hz
    have hpow (n : Nat) : (10 : Int) ^ n = (10 ^ n : Nat) :=
      (Int.natCast_pow 10 n).symm
    rw [hpow, hpow] at hz
    omega
  rcases List.eq_nil_or_concat A with hnil | ⟨U, x, hAeq⟩
  · subst A
    simp
  · rw [List.concat_eq_append] at hAeq
    subst A
    apply Nat.le_of_not_lt
    intro hlength
    have hlen : (U ++ [x]).length = U.length + 1 := by simp
    have hUlen : B.length + 1 ≤ U.length := by omega
    have hU : ∀ y ∈ U, y ≤ 18 := by
      intro y hy
      exact hA y (List.mem_append.mpr (Or.inl hy))
    have hx18 : x ≤ 18 := hA x (by simp)
    have hxne : x ≠ 18 := by
      intro hx
      apply ht
      simp [hx]
    have hx : x ≤ 17 := by omega
    have hlast : 10 ^ U.length * x ≤ 17 * 10 ^ U.length := by
      calc
        10 ^ U.length * x ≤ 10 ^ U.length * 17 :=
          Nat.mul_le_mul_left (10 ^ U.length) hx
        _ = 17 * 10 ^ U.length := Nat.mul_comm _ _
    have hbound := bounded_low_value U hU
    have hpower : 10 ^ B.length * 10 ≤ 10 ^ U.length := by
      simpa only [Nat.pow_succ] using
        Nat.pow_le_pow_right (by decide : 0 < 10) hUlen
    have hpositive : 0 < 10 ^ B.length := Nat.pow_pos (by decide)
    rw [lowValue_append_single, hlen, Nat.pow_succ] at hbalance
    omega

/-- A valid competitor with the same two complete original streams has
at most one more coefficient than the target, among the ten even phases.
Neither a competing-width bound nor equality of the actual carries is
supplied. Empty words are included. -/
theorem complete_competitor_length_le (s q : Outer)
    (hsTen : s.c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hqTen : q.c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hvs : validOuter s = true) (hvq : validOuter q = true)
    (hstreams : sameStreams s q) :
    q.B.length ≤ s.B.length + 1 := by
  rcases s with ⟨c, S⟩
  rcases q with ⟨d, Q⟩
  have hS := entries_le_of_valid c S hvs
  have hQ := entries_le_of_valid d Q hvq
  have hphase := phase_eq_of_complete_streams c d S Q hsTen hqTen hS hQ hstreams
  subst d
  have hc : c ≤ 18 := by
    simp only [List.mem_cons, List.mem_nil_iff, or_false] at hsTen
    omega
  have hz := zValue_eq_of_low_prefix c (max Q.length S.length + 2)
    Q S hc hQ hS (Nat.le_refl _) (hstreams _).1
  by_cases hcZero : c = 0
  · subst c
    exact zero_length_le Q S hS (last_ne_of_valid 0 Q hvq) hz
  by_cases hcEighteen : c = 18
  · subst c
    exact eighteen_length_le Q S hQ (last_ne_of_valid 18 Q hvq) hz
  have hcInterior : nonneutralPhase c := by
    simp only [List.mem_cons, List.mem_nil_iff, or_false] at hsTen
    simp only [nonneutralPhase, List.mem_cons, List.mem_nil_iff, or_false]
    omega
  have hword := (interior_complete_fiber_singleton
    c c S Q hcInterior hqTen hvs hvq hstreams).2
  change Q.length ≤ S.length + 1
  rw [← hword]
  omega

#print axioms complete_competitor_length_le

end Agent5.CompleteStreamDecoder
