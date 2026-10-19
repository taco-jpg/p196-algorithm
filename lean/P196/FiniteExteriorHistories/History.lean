import P196.FiniteExteriorHistories.Evolution
import P196.FiniteExteriorHistories.Reset

/-!
# Simultaneous all-phase finite exterior histories

One step consumes one position of a protected coefficient window. The
target word can grow by one position in the same step, so a buffer of
twice the time horizon supplies a phase-reset coefficient throughout the
induction. This is a sufficient finite buffer, not an optimality claim.

The explicit alternative word is chosen before the alternative phase and
the time. The original transition and original observations are retained.
-/

namespace Agent5.FiniteExteriorHistories

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent6.ExteriorCoordinates
open Agent5.UniversalPhasePrefixes

/-- Agreement through one more spatial position propagates for one step
when the target successor has a phase coefficient in that last position. -/
theorem sameObservation_step (K : Nat) (s q : Outer)
    (hs : nonneutralPhase s.c) (hq : nonneutralPhase q.c)
    (hBs : ∀ x ∈ s.B, x ≤ 18) (hBq : ∀ x ∈ q.B, x ≤ 18)
    (hlen : (outerNext s).B.length ≤ K)
    (hobs : sameObservation (K + 1) s q) :
    sameObservation K (outerNext s) (outerNext q) := by
  apply sameObservation_of_coefficientPrefix K (outerNext s) (outerNext q)
    (outerNext_nonneutral s hs) (outerNext_nonneutral q hq)
    (outerNext_bounded s hs hBs) (outerNext_bounded q hq hBq) hlen
  rw [coefficientPrefix_outerNext _ q hq hBq,
    coefficientPrefix_outerNext _ s hs hBs, hobs.2.1, hobs.2.2]

/-- An initial observation window with two positions per elapsed step
protects the original observations at the remaining spatial radius. -/
theorem sameObservation_outerIter (N t : Nat) (s q : Outer)
    (hs : nonneutralPhase s.c) (hq : nonneutralPhase q.c)
    (hBs : ∀ x ∈ s.B, x ≤ 18) (hBq : ∀ x ∈ q.B, x ≤ 18)
    (hN : s.B.length + 2 * t ≤ N)
    (hobs : sameObservation N s q) :
    sameObservation (N - t) (outerIter t s) (outerIter t q) := by
  revert hN
  induction t with
  | zero =>
      intro _
      simpa only [Nat.sub_zero, outerIter_zero] using hobs
  | succ t ih =>
      intro hN
      have hprev : s.B.length + 2 * t ≤ N := by omega
      have hp := ih hprev
      have hradius : N - t = (N - (t + 1)) + 1 := by omega
      rw [hradius] at hp
      apply sameObservation_step (N - (t + 1))
        (outerIter t s) (outerIter t q)
        (outerIter_nonneutral s t hs) (outerIter_nonneutral q t hq)
        (outerIter_bounded s t hs hBs) (outerIter_bounded q t hq hBq) _ hp
      have hwidth := outerIter_length_le s (t + 1)
      change (outerIter (t + 1) s).B.length ≤ N - (t + 1)
      omega

private theorem universalWord_bounded (c : Nat) (B : List Nat) (m : Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) :
    ∀ x ∈ universalWord c B m, x ≤ 18 := by
  have hc18 : c ≤ 18 := (phase_facts c 0 hc (by decide)).2.2.2.2
  have he18 : relayLetter c ≤ 18 := by
    by_cases h : 10 ≤ c <;> simp [relayLetter, h]
  intro x hx
  change x ∈ (B ++ List.replicate m c) ++ [relayLetter c] at hx
  rcases List.mem_append.mp hx with hx | hx
  · rcases List.mem_append.mp hx with hx | hx
    · exact hB x hx
    · simpa only [List.eq_of_mem_replicate hx] using hc18
  · simpa only [List.mem_singleton.mp hx] using he18

/-- One explicit word reproduces every observation through the prescribed
time horizon at each alternative nonneutral phase. No head or trimming
condition is imposed on the bounded target word. -/
theorem universalWord_same_history
    (c d cut T m : Nat) (B : List Nat)
    (hc : nonneutralPhase c) (hd : nonneutralPhase d)
    (hB : ∀ x ∈ B, x ≤ 18)
    (hm : 2 * T ≤ m)
    (hcut : cut + T ≤ B.length + m) :
    ∀ t, t ≤ T →
      sameObservation cut
        (outerIter t { c := c, B := B })
        (outerIter t { c := d, B := universalWord c B m }) := by
  have hinitial : sameObservation (B.length + m)
      { c := c, B := B } { c := d, B := universalWord c B m } :=
    universalWord_same_prefixes c d (B.length + m) m B hc hd hB (Nat.le_refl _)
  intro t ht
  have hprotected := sameObservation_outerIter (B.length + m) t
    { c := c, B := B } { c := d, B := universalWord c B m }
    hc hd hB (universalWord_bounded c B m hc hB)
    (by dsimp only; omega) hinitial
  exact sameObservation_take cut (B.length + m - t) _ _ (by omega) hprotected

/-- For every target and finite time horizon, one arbitrarily wide valid
canonical word reproduces the actual high carry and both original finite
prefixes at all eight initial nonneutral phases and every observed time. -/
theorem arbitrarily_wide_all_phase_same_history
    (c cut T W : Nat) (B : List Nat)
    (hc : nonneutralPhase c)
    (hv : validOuter { c := c, B := B } = true) :
    ∃ A : List Nat,
      max B.length W < A.length ∧
      ∀ d, nonneutralPhase d →
        validOuter { c := d, B := A } = true ∧
        stripSuffix d A = A ∧
        ∀ t, t ≤ T →
          sameObservation cut
            (outerIter t { c := c, B := B })
            (outerIter t { c := d, B := A }) := by
  refine ⟨universalWord c B (max cut W + 2 * T), ?_, ?_⟩
  · rw [universalWord_length]
    have := Nat.le_max_right cut W
    omega
  · intro d hd
    refine ⟨universalWord_valid c d B _ hc hd hv,
      universalWord_canonical c d B _ hd, ?_⟩
    apply universalWord_same_history c d cut T (max cut W + 2 * T) B
      hc hd (entries_le_of_valid c B hv)
    · omega
    · have := Nat.le_max_left cut W
      omega

#print axioms sameObservation_step
#print axioms sameObservation_outerIter
#print axioms universalWord_same_history
#print axioms arbitrarily_wide_all_phase_same_history

end Agent5.FiniteExteriorHistories
