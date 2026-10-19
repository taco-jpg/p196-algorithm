import P196.CompleteStreamDecoder.LowValues

/-!
# Finite equality determines the complete original streams

At a common padded width, one additional high term determines the original
fraction exactly. Equal carries give equal numerators; opposite carries
give numerators and denominators related by the same factor of ten. The
published scaling identity therefore recovers every literal high prefix.
Together with finite low-coordinate recovery, this yields a finite and
complete stream equivalence without supplying the actual carry. Fixed
phases may be odd; unknown phases range over the ten even phases.
-/

namespace Agent5.CompleteStreamDecoder

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.BoundedStreamCandidates
open Agent5.PhaseEighteenIsolation Agent5.CompleteExteriorFibers
open Agent5.FiniteExteriorHistories

private theorem actualCarry_le (c : Nat) (B : List Nat)
    (hB : ∀ x ∈ B, x ≤ 18) : actualCarry { c := c, B := B } ≤ 1 :=
  normalize_carry_le B.reverse (if 10 ≤ c then 1 else 0)
    (fun x hx => hB x (List.mem_reverse.mp hx)) (by split <;> decide)

private theorem high_boundary_value (c : Nat) (B : List Nat)
    (hc : c ≤ 18) (hB : ∀ x ∈ B, x ≤ 18) :
    highValue (originalHigh (B.length + 1) { c := c, B := B }) =
      if actualCarry { c := c, B := B } = 0 then
        10 * highValue B + c + c / 9
      else highValue B + c / 9 := by
  let g := actualCarry { c := c, B := B }
  have hg : g ≤ 1 := actualCarry_le c B hB
  have hempty : rhoNum c [] = c := by simp [rhoNum, highValue]
  change highValue (originalHigh (B.length + 1) { c := c, B := B }) =
    if g = 0 then 10 * highValue B + c + c / 9 else highValue B + c / 9
  by_cases hzero : g = 0
  · rw [if_pos hzero]
    have hp : originalHigh (B.length + 1) { c := c, B := B ++ [c] } =
        originalHigh (B.length + 1) { c := c, B := B } := by
      simpa only [originalHigh, actualCarry, List.replicate_one] using
        phase_padding_high_of_le_eighteen c (B.length + 1) B 1 hc
    have hcarry : actualCarry { c := c, B := B ++ [c] } = g := by
      simpa only [actualCarry, g, List.replicate_one] using
        phase_padding_carry_of_le_eighteen c B 1 hc
    rw [← hp]
    change highValue (fractionDigits (B.length + 1) (rhoNum c (B ++ [c]))
      (9 * 10 ^ (B ++ [c]).length *
        10 ^ actualCarry { c := c, B := B ++ [c] })) =
      10 * highValue B + c + c / 9
    rw [hcarry, hzero]
    have h := high_prefix_append_value c 0 (B ++ [c]) [] (by simp)
    simpa only [List.append_nil, List.length_append, List.length_singleton,
      List.length_nil, Nat.add_zero, Nat.pow_zero, Nat.mul_one, hempty,
      highValue_append_single] using h
  · rw [if_neg hzero]
    have hone : g = 1 := by omega
    change highValue (fractionDigits (B.length + 1) (rhoNum c B)
      (9 * 10 ^ B.length * 10 ^ g)) = highValue B + c / 9
    rw [hone]
    have h := high_prefix_append_value c 1 B [] (by omega)
    simpa only [List.append_nil, List.length_nil, Nat.pow_zero, Nat.mul_one,
      hempty] using h

private theorem high_eq_all_of_boundary (c : Nat) (A B : List Nat)
    (hc : c ≤ 18) (hlen : A.length = B.length)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hhi : originalHigh (A.length + 1) { c := c, B := B } =
      originalHigh (A.length + 1) { c := c, B := A }) :
    ∀ n : Nat, originalHigh n { c := c, B := B } =
      originalHigh n { c := c, B := A } := by
  let gA := actualCarry { c := c, B := A }
  let gB := actualCarry { c := c, B := B }
  have hgA : gA ≤ 1 := actualCarry_le c A hA
  have hgB : gB ≤ 1 := actualCarry_le c B hB
  have hga : gA = 0 ∨ gA = 1 := by omega
  have hgb : gB = 0 ∨ gB = 1 := by omega
  have h := congrArg highValue hhi
  have hAreading := high_boundary_value c A hc hA
  have hBreading := high_boundary_value c B hc hB
  rw [← hlen] at hBreading
  rw [hBreading, hAreading] at h
  change (if gB = 0 then 10 * highValue B + c + c / 9 else highValue B + c / 9) =
    (if gA = 0 then 10 * highValue A + c + c / 9 else highValue A + c / 9) at h
  have hrho : 10 ^ gA * rhoNum c B = 10 ^ gB * rhoNum c A := by
    rcases hga with hga | hga <;> rcases hgb with hgb | hgb <;>
      simp [hga, hgb, rhoNum] at h ⊢ <;> omega
  have hden : 10 ^ gA * (9 * 10 ^ A.length * 10 ^ gB) =
      10 ^ gB * (9 * 10 ^ A.length * 10 ^ gA) := by ac_rfl
  intro n
  change fractionDigits n (rhoNum c B) (9 * 10 ^ B.length * 10 ^ gB) =
    fractionDigits n (rhoNum c A) (9 * 10 ^ A.length * 10 ^ gA)
  rw [← hlen]
  calc
    _ = fractionDigits n (10 ^ gA * rhoNum c B)
        (10 ^ gA * (9 * 10 ^ A.length * 10 ^ gB)) :=
      (fractionDigits_scale n (rhoNum c B) (9 * 10 ^ A.length * 10 ^ gB)
        (10 ^ gA) (Nat.pow_pos (by decide))).symm
    _ = fractionDigits n (10 ^ gB * rhoNum c A)
        (10 ^ gB * (9 * 10 ^ A.length * 10 ^ gA)) := by rw [hrho, hden]
    _ = _ := fractionDigits_scale n (rhoNum c A) (9 * 10 ^ A.length * 10 ^ gA)
      (10 ^ gB) (Nat.pow_pos (by decide))

/-- At any fixed natural phase at most eighteen, equality of sufficiently
long original prefixes is equivalent to equality at every cutoff. Neither
validity nor equality of the separately calculated carries is assumed. -/
theorem same_phase_streams_iff_prefixes (c cut : Nat) (A B : List Nat)
    (hc : c ≤ 18)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hcut : max A.length B.length + 2 ≤ cut) :
    sameStreams { c := c, B := A } { c := c, B := B } ↔
      originalLow cut { c := c, B := B } = originalLow cut { c := c, B := A } ∧
      originalHigh cut { c := c, B := B } = originalHigh cut { c := c, B := A } := by
  constructor
  · intro h
    exact h cut
  · rintro ⟨hlo, hhi⟩
    have hz := zValue_eq_of_low_prefix c cut A B hc hA hB hcut hlo.symm
    let M := max A.length B.length + 1
    let X := A ++ List.replicate (M - A.length) c
    let Y := B ++ List.replicate (M - B.length) c
    have hAM : A.length ≤ M := by
      have := Nat.le_max_left A.length B.length
      omega
    have hBM : B.length ≤ M := by
      have := Nat.le_max_right A.length B.length
      omega
    have hXlen : X.length = M := by
      simp only [X, List.length_append, List.length_replicate]
      exact Nat.add_sub_of_le hAM
    have hYlen : Y.length = M := by
      simp only [Y, List.length_append, List.length_replicate]
      exact Nat.add_sub_of_le hBM
    have hX : ∀ x ∈ X, x ≤ 18 := by
      have h := coefficientPrefix_bounded M { c := c, B := A } hc hA
      rw [coefficientPrefix_of_length_le M { c := c, B := A } hAM] at h
      exact h
    have hY : ∀ x ∈ Y, x ≤ 18 := by
      have h := coefficientPrefix_bounded M { c := c, B := B } hc hB
      rw [coefficientPrefix_of_length_le M { c := c, B := B } hBM] at h
      exact h
    have hpA (n : Nat) : originalHigh n { c := c, B := X } =
        originalHigh n { c := c, B := A } :=
      phase_padding_high_of_le_eighteen c n A (M - A.length) hc
    have hpB (n : Nat) : originalHigh n { c := c, B := Y } =
        originalHigh n { c := c, B := B } :=
      phase_padding_high_of_le_eighteen c n B (M - B.length) hc
    have hpadded := (hpB cut).trans (hhi.trans (hpA cut).symm)
    have hprefix : originalHigh (M + 1) { c := c, B := Y } =
        originalHigh (M + 1) { c := c, B := X } := by
      have h := congrArg (List.take (M + 1)) hpadded
      change (fractionDigits cut (rhoNum c Y)
        (9 * 10 ^ Y.length * 10 ^ actualCarry { c := c, B := Y })).take (M + 1) =
        (fractionDigits cut (rhoNum c X)
          (9 * 10 ^ X.length * 10 ^ actualCarry { c := c, B := X })).take (M + 1) at h
      rw [show cut = (M + 1) + (cut - (M + 1)) by omega] at h
      simpa only [fractionDigits_prefix] using h
    have hall := high_eq_all_of_boundary c X Y hc (hXlen.trans hYlen.symm) hX hY
      (by simpa only [hXlen] using hprefix)
    intro n
    constructor
    · change originalLow n { c := c, B := B } = originalLow n { c := c, B := A }
      simp only [originalLow, hz]
    · change originalHigh n { c := c, B := B } = originalHigh n { c := c, B := A }
      exact (hpB n).symm.trans ((hall n).trans (hpA n))

/-- Among the ten even phases, the same finite and complete equivalence
holds without a known phase, actual carry, or canonical-word assumption. -/
theorem same_streams_iff_prefixes (cut : Nat) (s q : Outer)
    (hsTen : s.c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hqTen : q.c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hS : ∀ x ∈ s.B, x ≤ 18) (hQ : ∀ x ∈ q.B, x ≤ 18)
    (hcut : max s.B.length q.B.length + 2 ≤ cut) :
    sameStreams s q ↔ originalLow cut q = originalLow cut s ∧
      originalHigh cut q = originalHigh cut s := by
  constructor
  · intro h
    exact h cut
  · rintro ⟨hlo, hhi⟩
    rcases s with ⟨c, A⟩
    rcases q with ⟨d, B⟩
    have hphase := phase_eq_of_low_prefix c d cut A B hsTen hqTen hS hQ hcut hlo.symm
    subst d
    have hc : c ≤ 18 := by
      simp only [List.mem_cons, List.mem_nil_iff, or_false] at hsTen
      omega
    exact (same_phase_streams_iff_prefixes c cut A B hc hS hQ hcut).mpr ⟨hlo, hhi⟩

#print axioms same_phase_streams_iff_prefixes
#print axioms same_streams_iff_prefixes

end Agent5.CompleteStreamDecoder
