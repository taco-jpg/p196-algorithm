import P196.CompleteExteriorFibers.Definitions

/-!
# Recovering an even phase from its low tail

The published low-stream formula already covers the eight interior phases.
At phases zero and eighteen, the same finite scan leaves a constant tail
of zeros or nines. These ten eventual digits are distinct, so a common low
prefix reaching beyond both boundary digits determines the phase alone.
The proof uses the original stream and normalization, including empty,
untrimmed, and zero-head coefficient words.
-/

namespace Agent5.CompleteExteriorFibers

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- The phase-tail entrance formula extends to both even boundary phases.
The interior cases are the published nonneutral-phase theorem. -/
theorem adicNumeratorDigits_even_phase (c e q : Nat)
    (hc : c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (he : e ≤ 1) :
    adicNumeratorDigits (q + 1) (9 * (e : Int) - (c : Int)) =
      (c + e - 10 * (if 10 ≤ c then 1 else 0)) ::
        List.replicate q (c - 9 * (if 10 ≤ c then 1 else 0)) := by
  by_cases hinterior : nonneutralPhase c
  · exact adicNumeratorDigits_phase c e q hinterior he
  have hboundary : c = 0 ∨ c = 18 := by
    simp only [List.mem_cons, List.mem_nil_iff, or_false] at hc
    simp only [nonneutralPhase, List.mem_cons, List.mem_nil_iff, or_false] at hinterior
    omega
  have hecases : e = 0 ∨ e = 1 := by omega
  have hzero := adicNumeratorDigits_constant q 0 (by decide)
  have hnine := adicNumeratorDigits_constant q 9 (by decide)
  change adicNumeratorDigits q 0 = List.replicate q 0 at hzero
  change adicNumeratorDigits q (-9) = List.replicate q 9 at hnine
  rcases hboundary with rfl | rfl <;>
    rcases hecases with rfl | rfl <;>
    simp [adicNumeratorDigits, hzero, hnine]

/-- After the coefficient scan and its boundary digit, the original low
stream repeats the phase's eventual digit at all ten even phases. -/
theorem low_prefix_even_phase (c : Nat) (B : List Nat) (q : Nat)
    (hc : c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hB : ∀ x ∈ B, x ≤ 18) :
    adicNumeratorDigits (B.length + 1 + q) (zValue c B - (c : Int)) =
      (normalize B 0).1 ++
        [c + (normalize B 0).2 - 10 * (if 10 ≤ c then 1 else 0)] ++
        List.replicate q (c - 9 * (if 10 ≤ c then 1 else 0)) := by
  by_cases hinterior : nonneutralPhase c
  · exact adicNumeratorDigits_exterior c B q hinterior hB
  have hscan := adicNumeratorDigits_normalize B 0 (q + 1) (c : Int)
  simp only [Nat.add_zero] at hscan
  rw [adicNumeratorDigits_even_phase c (normalize B 0).2 q hc
    (normalize_carry_le B 0 hB (by decide))] at hscan
  have hz : zValue c B - (c : Int) =
      9 * (lowValue B : Int) - (c : Int) * 10 ^ B.length := by
    simp only [zValue, Int.mul_sub, Int.mul_one]
    omega
  rw [hz, show B.length + 1 + q = B.length + (q + 1) by omega]
  simpa only [List.append_assoc, List.singleton_append] using hscan

private theorem low_prefix_last_phase (c cut : Nat) (B : List Nat)
    (hc : c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hB : ∀ x ∈ B, x ≤ 18) (hcut : B.length + 2 ≤ cut) :
    (adicNumeratorDigits cut (zValue c B - (c : Int))).getLast? =
      some (c - 9 * (if 10 ≤ c then 1 else 0)) := by
  let q := cut - (B.length + 1)
  have hq : q ≠ 0 := by dsimp [q]; omega
  have hlen : B.length + 1 + q = cut := by dsimp [q]; omega
  have hformula := low_prefix_even_phase c B q hc hB
  rw [hlen] at hformula
  rw [hformula]
  simp [List.getLast?_append, List.getLast?_cons, List.getLast?_replicate, hq]

/-- A low prefix extending past both coefficient boundaries determines
the phase among all ten even phases, without high-stream or carry data. -/
theorem phase_eq_of_low_prefix (c d cut : Nat) (A B : List Nat)
    (hc : c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hd : d ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hcut : max A.length B.length + 2 ≤ cut)
    (hlo : adicNumeratorDigits cut (zValue c A - (c : Int)) =
      adicNumeratorDigits cut (zValue d B - (d : Int))) : c = d := by
  have hAcut : A.length + 2 ≤ cut := by
    have := Nat.le_max_left A.length B.length
    omega
  have hBcut : B.length + 2 ≤ cut := by
    have := Nat.le_max_right A.length B.length
    omega
  have hlast := congrArg List.getLast? hlo
  rw [low_prefix_last_phase c cut A hc hA hAcut,
    low_prefix_last_phase d cut B hd hB hBcut] at hlast
  have htail := Option.some.inj hlast
  simp only [List.mem_cons, List.mem_nil_iff, or_false] at hc hd
  split at htail <;> split at htail <;> omega

#print axioms adicNumeratorDigits_even_phase
#print axioms low_prefix_even_phase
#print axioms phase_eq_of_low_prefix

end Agent5.CompleteExteriorFibers
