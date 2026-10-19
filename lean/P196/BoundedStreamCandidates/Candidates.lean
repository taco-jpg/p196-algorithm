import P196.BoundedStreamCandidates.Phase
import P196.BoundedStreamCandidates.Recovery

/-!
# Exact enumeration of the finite compatible-state set

The actual carry chooses a successful reconstruction branch for every
compatible state. Conversely, each retained branch has passed the original
finite observation checks. Testing exactly two carries bounds the list
length, and checking the actual carry prevents repeated states.
-/

namespace Agent5.BoundedStreamCandidates

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

private theorem checkedGuess_sound (N g : Nat) (low high : List Nat)
    (s : Outer) (h : checkedGuess N low high g = some s) :
    boundedPrefixMatch N low high s ∧ actualCarry s = g := by
  unfold checkedGuess at h
  dsimp only at h
  split at h
  · rename_i hgood
    have hs := Option.some.inj h
    cases hs
    exact hgood
  · cases h

private theorem checkedGuess_complete (N : Nat) (low high : List Nat)
    (s : Outer) (hs : boundedPrefixMatch N low high s) :
    checkedGuess N low high (actualCarry s) = some s := by
  rcases s with ⟨c, B⟩
  have hs0 := hs
  rcases hs with ⟨hc, hv, hw, hlo, hhi⟩
  have hcBound : c ≤ 18 := by
    simp only [List.mem_cons, List.mem_nil_iff, or_false] at hc
    omega
  have hphase : phaseFromLow low = c := by
    rw [← hlo]
    exact phaseFromLow_correct N c B hc (entries_le_of_valid c B hv) hw
  have hword : candidateAtCarry N (phaseFromLow low)
      (actualCarry { c := c, B := B }) low high = { c := c, B := B } := by
    rw [hphase, ← hlo, ← hhi]
    exact candidateAtCarry_correct N c B hcBound hv hw
  simp [checkedGuess, hword, hs0]

/-- The output list contains exactly the valid ten-phase states of width
at most N whose two original prefixes equal the entire supplied lists. -/
theorem mem_decodeCandidates (N : Nat) (low high : List Nat) (s : Outer) :
    s ∈ decodeCandidates N low high ↔ boundedPrefixMatch N low high s := by
  rw [decodeCandidates, List.mem_filterMap]
  constructor
  · rintro ⟨g, _, hg⟩
    exact (checkedGuess_sound N g low high s hg).1
  · intro hs
    have hcarry : actualCarry s ≤ 1 := by
      apply normalize_carry_le s.B.reverse _
        (fun x hx => entries_le_of_valid s.c s.B hs.2.1 x (List.mem_reverse.mp hx))
      split <;> decide
    refine ⟨actualCarry s, ?_, checkedGuess_complete N low high s hs⟩
    simp only [List.mem_cons, List.mem_nil_iff, or_false]
    omega

/-- Every input, including malformed lists, yields at most two candidates. -/
theorem decodeCandidates_length (N : Nat) (low high : List Nat) :
    (decodeCandidates N low high).length ≤ 2 := by
  exact List.length_filterMap_le (checkedGuess N low high) [0, 1]

/-- The two retained guesses cannot name the same state, because their
checks certify different actual carries. This holds on arbitrary inputs. -/
theorem decodeCandidates_nodup (N : Nat) (low high : List Nat) :
    (decodeCandidates N low high).Nodup := by
  cases hzero : checkedGuess N low high 0 with
  | none =>
      cases hone : checkedGuess N low high 1 <;>
        simp [decodeCandidates, List.filterMap_cons, hzero, hone]
  | some a =>
      cases hone : checkedGuess N low high 1 with
      | none => simp [decodeCandidates, List.filterMap_cons, hzero, hone]
      | some b =>
          have ha := (checkedGuess_sound N 0 low high a hzero).2
          have hb := (checkedGuess_sound N 1 low high b hone).2
          have hne : a ≠ b := by
            intro h
            rw [h] at ha
            omega
          simp [decodeCandidates, List.filterMap_cons, hzero, hone, hne]

#print axioms mem_decodeCandidates
#print axioms decodeCandidates_length
#print axioms decodeCandidates_nodup

end Agent5.BoundedStreamCandidates
