import P196.Agent5ExactDigitStreams.CoordinateOnlyStreams
import P196.Agent5OrdinaryStreamPrefix.ExteriorArithmetic

/-!
Agent #5: the actual one-step raw exterior prefix in literal coordinate digits.

Agent #6's existing `surrounded_raw_exterior` supplies the whole-word carrying
identity. The two Agent #5 stream endpoints supply its literal digit lists,
and Agent #6's coordinate threshold supplies the outgoing carry selector.
The shape hypothesis is retained, including its bands of length `gap + 2`.
-/

namespace Agent5.OrdinaryStreamPrefix

open P196.Agent6 Agent115.ExteriorFactorization Agent5.ExactDigitStreams

/-- The two original Nat normalizers have the same list and final carry.
This is the Agent7/Agent6 adapter; Agent109's adjacent `normalize7_eq` has
`Agent109.norm` as its endpoint. -/
theorem normalize7_eq_norm6 (w : List Nat) (e : Nat) :
    P196.Agent7.Finite.normalize w e = P196.Agent6.norm w e := by
  induction w generalizing e with
  | nil => rfl
  | cons x xs ih =>
    simp [P196.Agent7.Finite.normalize, P196.Agent6.norm, ih]

/-- The eight original stream phases satisfy the ordinary projection domain. -/
theorem nonneutralPhase_nonneutral6 (c : Nat) (hc : nonneutralPhase c) :
    P196.Agent6.Nonneutral c := by
  have hbounds := nonneutralPhase_coordinate_bounds c hc
  refine ⟨?_, hbounds.1, hbounds.2⟩
  simp only [nonneutralPhase, List.mem_cons, List.not_mem_nil, or_false] at hc
  omega

/-- The actual raw pair prefix is the sum of the two literal streams, using
the normalization carry before its coordinate-only replacement. -/
theorem ordinary_raw_prefix_from_normalized_streams
    (D B W : List Nat) (c gap : Nat)
    (hc : nonneutralPhase c)
    (hB : Coefficients B) (hW : Coefficients W)
    (hshape : paired D = surrounded B c gap W) :
    (paired (reverseAddDigits D)).take (B.length + 1) =
      List.zipWith Nat.add
        (adicNumeratorDigits (B.length + 1) (zValue c B - (c : Int)))
        (fractionDigits (B.length + 1) (rhoNum c B)
          (9 * 10 ^ B.length *
            10 ^ (P196.Agent7.Finite.normalize B.reverse
              (if 10 ≤ c then 1 else 0)).2)) := by
  have hlow := adicNumeratorDigits_exterior c B 0 hc hB
  have hhigh := fractionDigits_exterior c B 0 hc hB
  dsimp only at hhigh
  simp only [Nat.add_zero, List.replicate_zero, List.append_nil] at hlow hhigh
  rw [hlow, hhigh]
  unfold reverseAddDigits
  rw [hshape]
  simpa only [normalize7_eq_norm6, lowEnd, carryPhase, digitPhase,
    List.singleton_append] using
    surrounded_raw_exterior B W c gap (nonneutralPhase_nonneutral6 c hc) hB hW

/-- The first complete exterior prefix of the actual one-step pair word is
given by the literal coordinate streams with the exact threshold selector.
Empty and untrimmed exterior words are included. -/
theorem ordinary_raw_prefix_from_streams
    (D B W : List Nat) (c gap : Nat)
    (hc : nonneutralPhase c)
    (hB : Coefficients B) (hW : Coefficients W)
    (hshape : paired D = surrounded B c gap W) :
    (paired (reverseAddDigits D)).take (B.length + 1) =
      List.zipWith Nat.add
        (adicNumeratorDigits (B.length + 1) (zValue c B - (c : Int)))
        (fractionDigits (B.length + 1) (rhoNum c B)
          (9 * 10 ^ B.length *
            10 ^ (if 9 * 10 ^ B.length ≤ rhoNum c B then 1 else 0))) := by
  simpa only [overflow_eq_coordinate_selector c B hc hB] using
    ordinary_raw_prefix_from_normalized_streams D B W c gap hc hB hW hshape

/-- The same actual prefix with Agent #6's exact coordinate quotient. -/
theorem ordinary_raw_prefix_from_streams_quotient
    (D B W : List Nat) (c gap : Nat)
    (hc : nonneutralPhase c)
    (hB : Coefficients B) (hW : Coefficients W)
    (hshape : paired D = surrounded B c gap W) :
    (paired (reverseAddDigits D)).take (B.length + 1) =
      List.zipWith Nat.add
        (adicNumeratorDigits (B.length + 1) (zValue c B - (c : Int)))
        (fractionDigits (B.length + 1) (rhoNum c B)
          (9 * 10 ^ B.length *
            10 ^ (rhoNum c B / (9 * 10 ^ B.length)))) := by
  have hphase := nonneutralPhase_coordinate_bounds c hc
  have hcarry :
      (P196.Agent7.Finite.normalize B.reverse (if 10 ≤ c then 1 else 0)).2 =
        rhoNum c B / (9 * 10 ^ B.length) :=
    Agent6.ExteriorCoordinates.overflow_eq_rho_quotient c B hphase.1 hphase.2
  simpa only [hcarry] using
    ordinary_raw_prefix_from_normalized_streams D B W c gap hc hB hW hshape

#print axioms normalize7_eq_norm6
#print axioms nonneutralPhase_nonneutral6
#print axioms ordinary_raw_prefix_from_normalized_streams
#print axioms ordinary_raw_prefix_from_streams
#print axioms ordinary_raw_prefix_from_streams_quotient

end Agent5.OrdinaryStreamPrefix
