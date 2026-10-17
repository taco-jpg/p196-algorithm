import P196.Foundations.Agent1PeriodicOuter
import P196.Agent2SaturatedProfile.SaturationTheorem

/-!
The actual three-coefficient prefix of the original maximal period-four
quotient, interpreted in the existing Agent4 prefix model. The control is
inputThree of the exponent-three word: it enters the last three columns,
not just the last column. The proof reuses canonical prefix semantics and
the exact quotient transition, including empty stored exterior/center blocks.
No abstract path realization or new saturation classification is asserted.
-/
namespace Agent1.Periodic
open Agent8 Agent1.RepeatedBlock

private def prefixOfTriple (q : Agent8.Triple3) : P196.Agent4.Saturation.Prefix :=
  ⟨q.1, q.2.1, q.2.2⟩

/-- Three physical coefficients, borrowing from the period when B is short. -/
def physicalPrefix (B w : Word) : P196.Agent4.Saturation.Prefix :=
  prefixOfTriple (Agent8.firstThree (B ++ w))

private theorem firstThree_append_of_length (A R : Word) (hA : 3 ≤ A.length) :
    Agent8.firstThree (A ++ R) = Agent8.firstThree A := by
  cases A with
  | nil => simp at hA
  | cons a A =>
      cases A with
      | nil => simp at hA
      | cons b A =>
          cases A with
          | nil => simp at hA
          | cons c A => rfl

/-- A positive period copy supplies the entire physical prefix, independent
of the exponent and center. Length four covers empty/short exterior blocks. -/
theorem firstThree_periodicWord (B H w : Word) (k : Nat)
    (hlen : w.length = 4) (hk : 1 ≤ k) :
    Agent8.firstThree (periodicWord B H w k) = Agent8.firstThree (B ++ w) := by
  cases k with
  | zero => omega
  | succ k =>
      have hlen' : 3 ≤ (B ++ w).length := by
        simp only [List.length_append, hlen]
        omega
      simpa only [periodicWord, pow, List.append_assoc] using
        firstThree_append_of_length (B ++ w)
          (pow w k ++ H ++ pow w.reverse (k+1) ++ B.reverse) hlen'

/-- The first physical prefix coordinate is the existing outside coefficient. -/
theorem physicalPrefix_a (B w : Word) (hlen : w.length = 4) :
    (physicalPrefix B w).a = outside B w := by
  have hlen' : 3 ≤ (B ++ w).length := by
    simp only [List.length_append, hlen]
    omega
  unfold physicalPrefix prefixOfTriple outside
  generalize B ++ w = A at hlen' ⊢
  cases A with
  | nil => simp at hlen'
  | cons a A =>
      cases A with
      | nil => simp at hlen'
      | cons b A =>
          cases A with
          | nil => simp at hlen'
          | cons c A => rfl

private theorem prefixOfTriple_advance (q : Agent8.Triple3) (e : Nat) :
    P196.Agent4.Saturation.advance (prefixOfTriple q) e =
      (prefixOfTriple (Agent8.prefixNext q e), Agent8.prefixOverflow q e) := by
  rcases q with ⟨a, b, c⟩
  dsimp only [P196.Agent4.Saturation.advance, prefixOfTriple,
    Agent8.prefixNext, Agent8.prefixOverflow]
  split <;> simp_all

/-- Original full validity makes the physical prefix valid in the existing
three-column saturation model. -/
theorem physicalPrefix_valid (B H w : Word) (hv : ValidPeriodic B H w) :
    P196.Agent4.Saturation.Valid (physicalPrefix B w) := by
  have hcan := periodicWord_canonical B H w 3 hv (by decide)
  have hlen : 3 ≤ (periodicWord B H w 3).length := by
    rw [periodicWord_length, hv.period_length]
    omega
  have hp := Agent8.firstThree_valid (periodicWord B H w 3) hcan hlen
  rw [firstThree_periodicWord B H w 3 hv.period_length (by decide)] at hp
  exact hp

/-- The actual inputThree bit drives exactly the original prefix advance,
with the physical quotient prefix and actual raw overflow as output. -/
theorem physicalPrefix_step (B H w : Word) (hv : ValidPeriodic B H w) :
    P196.Agent4.Saturation.Valid (physicalPrefix B w) ∧
      Agent8.inputThree (periodicWord B H w 3) ≤ 1 ∧
      P196.Agent4.Saturation.advance (physicalPrefix B w)
        (Agent8.inputThree (periodicWord B H w 3)) =
        (physicalPrefix (quotientOuter B H w) (rawPeriod B H w), rawGamma B H w) := by
  have hcan := periodicWord_canonical B H w 3 hv (by decide)
  have hlen : 6 ≤ (periodicWord B H w 3).length := by
    rw [periodicWord_length, hv.period_length]
    omega
  have hs := Agent8.prefix_step_of_canonical (periodicWord B H w 3) hcan hlen
  have hin := firstThree_periodicWord B H w 3 hv.period_length (by decide)
  have htransition := valid_quotient_transition B H w 3 hv (by decide)
  have hout : Agent8.firstThree (Agent8.stepWord (periodicWord B H w 3)) =
      Agent8.firstThree (quotientOuter B H w ++ rawPeriod B H w) := by
    rw [htransition.2.2]
    exact firstThree_periodicWord _ _ _ _ htransition.1.period_length htransition.2.1
  have hgamma : Agent8.prefixOverflow (Agent8.firstThree (periodicWord B H w 3))
      (Agent8.inputThree (periodicWord B H w 3)) = rawGamma B H w :=
    hs.2.2.trans (Agent8.terminalCarry_eq_actual_overflow (periodicWord B H w 3) hcan).symm
  refine ⟨physicalPrefix_valid B H w hv, hs.2.1, ?_⟩
  unfold physicalPrefix
  rw [prefixOfTriple_advance, ← hin, ← hs.1, hout, hgamma]

end Agent1.Periodic

#print axioms Agent1.Periodic.firstThree_periodicWord
#print axioms Agent1.Periodic.physicalPrefix_a
#print axioms Agent1.Periodic.physicalPrefix_valid
#print axioms Agent1.Periodic.physicalPrefix_step
