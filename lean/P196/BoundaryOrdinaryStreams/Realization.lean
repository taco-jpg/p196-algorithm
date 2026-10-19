import P196.BoundaryOrdinaryStreams.Definitions

/-!
# Positive ordinary realizations at the two boundary phases

The generic mirrored-word realization theorem supplies the decimal digits.
The positive outer coefficient makes those digits canonical. The only valid
boundary state with no such positive outer coefficient is the empty word at
phase zero; even its one-digit high observation has no ordinary realization.
-/

namespace Agent5.BoundaryOrdinaryStreams

open P196.Agent7.Finite (validOuter)
open Agent115.ExteriorFactorization (entries_le_of_valid)

/-- Every valid boundary exterior except the empty zero-phase state has a
positive ordinary realization with an empty center and the exact protected
width. The existing shape has bands of length `g + 2`, so `g = 0` is allowed. -/
theorem positive_boundary_surrounded_realized (c g : Nat) (B : List Nat)
    (hc : c = 0 ∨ c = 18) (hv : validOuter ⟨c, B⟩ = true)
    (hpos : c ≠ 0 ∨ B ≠ []) :
    ∃ n, 0 < n ∧
      (Agent109.digits n).length = 2 * B.length + 2 * (g + 2) ∧
      Agent109.pairWord n = P196.Agent6.surrounded B c g [] := by
  let X := B ++ List.replicate (g + 2) c
  let q := P196.Agent6.surrounded B c g []
  have hc18 : c ≤ 18 := by omega
  have hB : Agent109.Bounded B := entries_le_of_valid c B hv
  have hX : Agent109.Bounded X := by
    intro x hx
    simp only [X, List.mem_append, List.mem_replicate] at hx
    rcases hx with hx | hx
    · exact hB x hx
    · omega
  have hshape : q = X ++ [] ++ X.reverse := by
    simp only [q, X, P196.Agent6.surrounded, List.reverse_append,
      List.reverse_replicate, List.nil_append, List.append_nil, List.append_assoc]
  have hq : Agent109.Bounded q := by
    rw [hshape]
    intro x hx
    simp only [List.mem_append, List.not_mem_nil, or_false,
      List.mem_reverse] at hx
    rcases hx with hx | hx <;> exact hX x hx
  have hmirror : Agent109.Cert.Mirr q := by
    rw [hshape]
    exact Agent109.Cert.mirr_wrap X [] Agent109.Cert.Mirr.nil
  have hlast : Agent109.LastPos q := by
    intro x hx
    cases hBe : B with
    | nil =>
        have hcpos : 0 < c := by
          rcases hpos with hpos | hpos
          · omega
          · exact False.elim (hpos hBe)
        have hx' : c = x := by
          simpa [q, P196.Agent6.surrounded, hBe, List.getLast?_append,
            List.getLast?_replicate] using hx
        omega
    | cons b tail =>
        have hbpos : 0 < b := by
          have hv' := hv
          rw [hBe] at hv'
          simp only [validOuter, Bool.and_eq_true, decide_eq_true_eq] at hv'
          exact hv'.1.2
        have hlastB : B.reverse.getLast? = some b := by simp [hBe]
        have hlastQ : q.getLast? = some b := by
          simp [q, P196.Agent6.surrounded, List.getLast?_append, hlastB]
        have hx' : b = x := by
          rw [hlastQ] at hx
          exact Option.some.inj hx
        omega
  obtain ⟨D, hD, hdigits, hlastD⟩ := Agent109.Cert.realize q hmirror hq
  have hcanonical : Agent109.Canon D :=
    (Agent109.canon_iff D).mpr ⟨hdigits, hlastD hlast⟩
  have hrep : Agent109.pairWord (Agent109.evalL D) = q := by
    rw [Agent109.pairWord, Agent109.digits_evalL D hcanonical, hD]
  have hlen : (Agent109.digits (Agent109.evalL D)).length =
      2 * B.length + 2 * (g + 2) := by
    have hp := congrArg List.length hrep
    have hpair : (Agent109.pairWord (Agent109.evalL D)).length =
        (Agent109.digits (Agent109.evalL D)).length :=
      Agent109.zipAdd_length _ _ (by simp)
    rw [hpair] at hp
    simp only [q, P196.Agent6.surrounded, List.length_append,
      List.length_replicate, List.length_nil, List.length_reverse] at hp
    omega
  refine ⟨Agent109.evalL D, ?_, hlen, hrep⟩
  apply Nat.pos_of_ne_zero
  intro hzero
  rw [hzero, Agent109.digits_zero, List.length_nil] at hlen
  omega

/-- No ordinary pair word has protected zero bands around an empty exterior,
regardless of its middle word or the size of the protected bands. -/
theorem zero_empty_surrounded_not_realizable (n g : Nat) (W : List Nat) :
    Agent109.pairWord n ≠ P196.Agent6.surrounded [] 0 g W := by
  intro hrep
  have hlast : (Agent109.pairWord n).getLast? = some 0 := by
    rw [hrep]
    simp [P196.Agent6.surrounded, List.getLast?_append,
      List.getLast?_replicate]
  have hpositive := Agent109.lastPos_pairWord n 0 hlast
  omega

/-- The coherent one-digit observation of the empty zero-phase state cannot
be the observation of any ordinary reverse-and-add transition, including zero. -/
theorem zero_empty_observation_not_realizable (n : Nat) :
    Agent5.OrdinaryExteriorHistories.ordinaryObservation 1 n 0 ≠
      coherentObservation 1 ⟨0, []⟩ := by
  intro heq
  have hzero : (coherentObservation 1 ⟨0, []⟩).2.2 = [0] := by rfl
  have hhigh := (congrArg (fun p : Nat × List Nat × List Nat => p.2.2) heq).trans hzero
  change (Agent109.digits (Lychrel196.step n)).reverse.take 1 = [0] at hhigh
  have hlast := ((Agent109.canon_iff _).mp
    (Agent109.canon_digits (Lychrel196.step n))).2
  cases hreverse : (Agent109.digits (Lychrel196.step n)).reverse with
  | nil => simp [hreverse] at hhigh
  | cons a tail =>
      have ha : a = 0 := by simpa [hreverse] using hhigh
      have hword : Agent109.digits (Lychrel196.step n) = tail.reverse ++ [a] := by
        have h := congrArg List.reverse hreverse
        simpa using h
      have hlastA : (Agent109.digits (Lychrel196.step n)).getLast? = some a := by
        rw [hword]
        simp
      have hpositive := hlast a hlastA
      omega

#print axioms positive_boundary_surrounded_realized
#print axioms zero_empty_surrounded_not_realizable
#print axioms zero_empty_observation_not_realizable

end Agent5.BoundaryOrdinaryStreams
