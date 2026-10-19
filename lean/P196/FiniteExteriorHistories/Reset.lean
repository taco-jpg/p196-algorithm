import P196.FiniteExteriorHistories.Prefix

/-!
# Recovering observations behind a phase coefficient

A nonneutral phase coefficient sends either incoming carry bit to the same
outgoing bit. Consequently, a shared coefficient window that includes one
position beyond the target word fixes the target's high carry and both
original digit windows. The compared word is first padded with its own phase,
so the statement also covers words shorter than the observation window.
-/

namespace Agent5.FiniteExteriorHistories

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

private theorem normalize_append (a b : List Nat) (e : Nat) :
    normalize (a ++ b) e =
      ((normalize a e).1 ++ (normalize b (normalize a e).2).1,
        (normalize b (normalize a e).2).2) := by
  induction a generalizing e with
  | nil => simp [normalize]
  | cons x xs ih => simp [normalize, ih]

private theorem sameObservation_reset_suffix (c d : Nat) (P R : List Nat)
    (hc : nonneutralPhase c) (hd : nonneutralPhase d)
    (hP : ∀ x ∈ P, x ≤ 18) (hR : ∀ x ∈ R, x ≤ 18) :
    sameObservation P.length { c := c, B := P }
      { c := d, B := P ++ c :: R } := by
  let e := (normalize R.reverse (if 10 ≤ d then 1 else 0)).2
  let g := (normalize P.reverse (if 10 ≤ c then 1 else 0)).2
  let X := (normalize P.reverse (if 10 ≤ c then 1 else 0)).1.reverse
  let Y := [(c + e) % 10] ++
    (normalize R.reverse (if 10 ≤ d then 1 else 0)).1.reverse
  have he : e ≤ 1 := normalize_carry_le R.reverse _
    (by intro x hx; exact hR x (List.mem_reverse.mp hx))
    (by split <;> decide)
  have hreset : (c + e) / 10 = (if 10 ≤ c then 1 else 0) :=
    (phase_facts c e hc he).1
  dsimp only [e] at hreset
  have hnorm : normalize (P ++ c :: R).reverse (if 10 ≤ d then 1 else 0) =
      ((normalize R.reverse (if 10 ≤ d then 1 else 0)).1 ++
          ((c + e) % 10 :: (normalize P.reverse (if 10 ≤ c then 1 else 0)).1),
        (normalize P.reverse (if 10 ≤ c then 1 else 0)).2) := by
    rw [List.reverse_append, List.reverse_cons, List.append_assoc,
      List.singleton_append, normalize_append]
    simp only [normalize, e, hreset]
  have hgamma :
      (normalize (P ++ c :: R).reverse (if 10 ≤ d then 1 else 0)).2 = g := by
    rw [hnorm]
  have hreverse :
      (normalize (P ++ c :: R).reverse (if 10 ≤ d then 1 else 0)).1.reverse =
        X ++ Y := by
    rw [hnorm]
    simp only [X, Y, List.reverse_append, List.reverse_cons, List.append_assoc]
  have hX : P.length ≤ X.length := by
    simpa only [X, List.length_reverse, normalize_length] using Nat.le_refl P.length
  have hQ : ∀ x ∈ P ++ c :: R, x ≤ 18 := by
    intro x hx
    rcases List.mem_append.mp hx with hx | hx
    · exact hP x hx
    · rcases List.mem_cons.mp hx with hx | hx
      · subst x
        exact (phase_facts c 0 hc (by decide)).2.2.2.2
      · exact hR x hx
  refine ⟨hgamma, ?_, ?_⟩
  · have hp := adicNumeratorDigits_prefix P.length (c :: R).length
      (zValue d (P ++ c :: R) - (d : Int))
    rw [show P.length + (c :: R).length = (P ++ c :: R).length by simp,
      Agent5.TrimmedStreamObservation.low_prefix_normalized] at hp
    calc
      adicNumeratorDigits P.length (zValue d (P ++ c :: R) - (d : Int)) =
          (normalize P 0).1 := by
        rw [← hp, normalize_append]
        exact (List.take_append_of_le_length (by simp [normalize_length])).trans
          (List.take_of_length_le (by simp [normalize_length]))
      _ = adicNumeratorDigits P.length (zValue c P - (c : Int)) :=
        (Agent5.TrimmedStreamObservation.low_prefix_normalized c P).symm
  · rw [Agent5.UniversalPhasePrefixes.high_prefix_normalized d P.length
        (P ++ c :: R) hd hQ (by simp only [List.length_append, List.length_cons]; omega),
      Agent5.UniversalPhasePrefixes.high_prefix_normalized c P.length P hc hP
        (Nat.le_refl _), hgamma, hreverse]
    change (if g == 0 then X ++ Y else [1] ++ (X ++ Y)).take P.length =
      (if g == 0 then X else [1] ++ X).take P.length
    by_cases hg : g = 0
    · simp only [hg, beq_self_eq_true, if_true]
      exact List.take_append_of_le_length hX
    · have hfalse : (g == 0) = false := by simp [hg]
      simp only [hfalse, Bool.false_eq_true, if_false]
      rw [← List.append_assoc]
      apply List.take_append_of_le_length
      simp only [List.length_append, List.length_singleton]
      omega

/-- A common coefficient window reaching one position beyond the target word
determines the actual high carry and both original digit windows. Only phase
and coefficient bounds are needed; either word may be empty or untrimmed. -/
theorem sameObservation_of_coefficientPrefix (K : Nat) (s q : Outer)
    (hs : nonneutralPhase s.c) (hq : nonneutralPhase q.c)
    (hBs : ∀ x ∈ s.B, x ≤ 18) (hBq : ∀ x ∈ q.B, x ≤ 18)
    (hlen : s.B.length ≤ K)
    (hp : coefficientPrefix (K + 1) q = coefficientPrefix (K + 1) s) :
    sameObservation K s q := by
  let P := s.B ++ List.replicate (K - s.B.length) s.c
  let Q := q.B ++ List.replicate (K + 1) q.c
  let R := Q.drop (K + 1)
  have hPlen : P.length = K := by
    simp only [P, List.length_append, List.length_replicate]
    omega
  have hphase : coefficientPrefix (K + 1) s = P ++ [s.c] := by
    rw [coefficientPrefix_of_length_le (K + 1) s (by omega)]
    have hsub : K + 1 - s.B.length = (K - s.B.length) + 1 := by omega
    simp only [hsub, List.replicate_succ', P, List.append_assoc]
  have hQprefix : Q.take (K + 1) = P ++ [s.c] := hp.trans hphase
  have hQsplit : Q = P ++ s.c :: R := by
    calc
      Q = Q.take (K + 1) ++ Q.drop (K + 1) :=
        (List.take_append_drop (K + 1) Q).symm
      _ = P ++ s.c :: R := by rw [hQprefix]; simp only [R, List.append_assoc,
        List.singleton_append]
  have hP : ∀ x ∈ P, x ≤ 18 := by
    dsimp only [P]
    rw [← coefficientPrefix_of_length_le K s hlen]
    exact coefficientPrefix_bounded K s
      (phase_facts s.c 0 hs (by decide)).2.2.2.2 hBs
  have hQ : ∀ x ∈ Q, x ≤ 18 := by
    intro x hx
    rcases List.mem_append.mp hx with hx | hx
    · exact hBq x hx
    · rw [List.eq_of_mem_replicate hx]
      exact (phase_facts q.c 0 hq (by decide)).2.2.2.2
  have hR : ∀ x ∈ R, x ≤ 18 := by
    intro x hx
    exact hQ x (List.mem_of_mem_drop hx)
  have h := sameObservation_reset_suffix s.c q.c P R hs hq hP hR
  rw [hPlen, ← hQsplit] at h
  rcases h with ⟨hgamma, hlo, hhi⟩
  refine ⟨?_, ?_, ?_⟩
  · simpa only [P, Q,
      Agent5.TrimmedStreamObservation.phase_padding_carry q.c q.B (K + 1) hq,
      Agent5.TrimmedStreamObservation.phase_padding_carry s.c s.B
        (K - s.B.length) hs] using hgamma
  · simpa only [P, Q, Agent5.TrimmedStreamObservation.phase_padding_low] using hlo
  · simpa only [P, Q,
      Agent5.TrimmedStreamObservation.phase_padding_high q.c K q.B (K + 1) hq,
      Agent5.TrimmedStreamObservation.phase_padding_high s.c K s.B
        (K - s.B.length) hs] using hhi

#print axioms sameObservation_of_coefficientPrefix

end Agent5.FiniteExteriorHistories
