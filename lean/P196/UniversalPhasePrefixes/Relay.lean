import P196.StreamNonisolation.Append

/-!
# Finite original prefixes under a change of phase

Low observations through a word's width are independent of its phase. For
high observations, an appended coefficient can transfer the new phase's
incoming carry to the old one. The normalized prefix then proves equality
of the original fractional streams, each with its own width and actual
outgoing carry in the denominator.
-/

namespace Agent5.UniversalPhasePrefixes

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- Through the original word width, the low stream is independent of the
phase, without phase restrictions or coefficient bounds. -/
theorem low_prefix_phase_independent (c d cut : Nat) (P : List Nat)
    (hcut : cut ≤ P.length) :
    adicNumeratorDigits cut (zValue c P - (c : Int)) =
      adicNumeratorDigits cut (zValue d P - (d : Int)) := by
  have hfull := (Agent5.TrimmedStreamObservation.low_prefix_normalized c P).trans
    (Agent5.TrimmedStreamObservation.low_prefix_normalized d P).symm
  have hsum : cut + (P.length - cut) = P.length := Nat.add_sub_of_le hcut
  have hpc := adicNumeratorDigits_prefix cut (P.length - cut)
    (zValue c P - (c : Int))
  have hpd := adicNumeratorDigits_prefix cut (P.length - cut)
    (zValue d P - (d : Int))
  rw [hsum] at hpc hpd
  exact hpc.symm.trans ((congrArg (List.take cut) hfull).trans hpd)

/-- An appended coefficient that transfers the incoming carry from the new
phase to the old one preserves the actual outgoing carry. No coefficient
bound or nonneutral phase assumption is required. -/
theorem relay_high_carry (c d : Nat) (P : List Nat) (e : Nat)
    (hrelay : (e + (if 10 ≤ d then 1 else 0)) / 10 =
      (if 10 ≤ c then 1 else 0)) :
    (normalize (P ++ [e]).reverse (if 10 ≤ d then 1 else 0)).2 =
      (normalize P.reverse (if 10 ≤ c then 1 else 0)).2 := by
  rw [List.reverse_append, show [e].reverse = [e] from rfl,
    List.singleton_append]
  simp only [normalize, hrelay]

/-- The high stream through the word width is the corresponding prefix of
its reversed normalization, with a leading one exactly in the overflow
branch. The original phase-tail digit is beyond this cutoff. -/
theorem high_prefix_normalized (c cut : Nat) (P : List Nat)
    (hc : nonneutralPhase c) (hP : ∀ x ∈ P, x ≤ 18)
    (hcut : cut ≤ P.length) :
    fractionDigits cut (rhoNum c P)
        (9 * 10 ^ P.length *
          10 ^ (normalize P.reverse (if 10 ≤ c then 1 else 0)).2) =
      (if (normalize P.reverse (if 10 ≤ c then 1 else 0)).2 == 0 then
        (normalize P.reverse (if 10 ≤ c then 1 else 0)).1.reverse
       else [1] ++ (normalize P.reverse (if 10 ≤ c then 1 else 0)).1.reverse).take cut := by
  let k : Nat := if 10 ≤ c then 1 else 0
  let g : Nat := (normalize P.reverse k).2
  let X : List Nat := (normalize P.reverse k).1.reverse
  let t : Nat := c - 9 * k
  change fractionDigits cut (rhoNum c P) (9 * 10 ^ P.length * 10 ^ g) =
    (if g == 0 then X else [1] ++ X).take cut
  have hf := fractionDigits_exterior c P 0 hc hP
  simp only [Nat.add_zero, List.replicate_zero, List.append_nil] at hf
  change fractionDigits (P.length + 1) (rhoNum c P)
      (9 * 10 ^ P.length * 10 ^ g) =
    (if g == 0 then X ++ [t] else [1] ++ X) at hf
  have hsum : cut + (P.length + 1 - cut) = P.length + 1 := by omega
  have hp := fractionDigits_prefix cut (P.length + 1 - cut) (rhoNum c P)
    (9 * 10 ^ P.length * 10 ^ g)
  rw [hsum] at hp
  rw [← hp, hf]
  by_cases hg : g = 0
  · simp only [hg, beq_self_eq_true, if_true]
    apply List.take_append_of_le_length
    simpa only [X, List.length_reverse, normalize_length] using hcut
  · simp [hg]

/-- A coefficient that transfers the phase carry preserves the original
high observations through the old word width when the phase changes.
Both streams retain their own original numerator, width, and actual carry. -/
theorem relay_high_prefix (c d cut : Nat) (P : List Nat) (e : Nat)
    (hc : nonneutralPhase c) (hd : nonneutralPhase d)
    (hP : ∀ x ∈ P, x ≤ 18) (he : e ≤ 18)
    (hrelay : (e + (if 10 ≤ d then 1 else 0)) / 10 =
      (if 10 ≤ c then 1 else 0))
    (hcut : cut ≤ P.length) :
    fractionDigits cut (rhoNum d (P ++ [e]))
        (9 * 10 ^ (P ++ [e]).length *
          10 ^ (normalize (P ++ [e]).reverse (if 10 ≤ d then 1 else 0)).2) =
      fractionDigits cut (rhoNum c P)
        (9 * 10 ^ P.length *
          10 ^ (normalize P.reverse (if 10 ≤ c then 1 else 0)).2) := by
  have hPe : ∀ x ∈ P ++ [e], x ≤ 18 := by
    intro x hx
    rcases List.mem_append.mp hx with hx | hx
    · exact hP x hx
    · have hxe : x = e := List.mem_singleton.mp hx
      simpa only [hxe] using he
  have hcut' : cut ≤ (P ++ [e]).length := by
    simp only [List.length_append, List.length_singleton]
    omega
  rw [high_prefix_normalized d cut (P ++ [e]) hd hPe hcut',
    high_prefix_normalized c cut P hc hP hcut,
    relay_high_carry c d P e hrelay]
  have hnorm :
      (normalize (P ++ [e]).reverse (if 10 ≤ d then 1 else 0)).1.reverse =
        (normalize P.reverse (if 10 ≤ c then 1 else 0)).1.reverse ++
          [(e + (if 10 ≤ d then 1 else 0)) % 10] := by
    simp only [List.reverse_append, List.reverse_cons, List.reverse_nil,
      List.nil_append, List.singleton_append, normalize, hrelay]
  rw [hnorm]
  have hcutX : cut ≤
      ((normalize P.reverse (if 10 ≤ c then 1 else 0)).1.reverse).length := by
    simpa only [List.length_reverse, normalize_length] using hcut
  by_cases hg : (normalize P.reverse (if 10 ≤ c then 1 else 0)).2 = 0
  · simp only [hg, beq_self_eq_true, if_true]
    exact List.take_append_of_le_length hcutX
  · have hfalse :
        ((normalize P.reverse (if 10 ≤ c then 1 else 0)).2 == 0) = false := by
      simp [hg]
    simp only [hfalse, Bool.false_eq_true, if_false]
    rw [← List.append_assoc]
    apply List.take_append_of_le_length
    simp only [List.length_append, List.length_singleton]
    omega

#print axioms low_prefix_phase_independent
#print axioms relay_high_carry
#print axioms high_prefix_normalized
#print axioms relay_high_prefix

end Agent5.UniversalPhasePrefixes
