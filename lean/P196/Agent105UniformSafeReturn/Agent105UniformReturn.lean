import P196.Agent105UniformSafeReturn.Agent105AffineOrbit
import P196.Agent105UniformSafeReturn.Agent105AffineShape
import P196.Agent105UniformSafeReturn.Agent105AffineStability
import P196.Agent105AffineComponents.Agent105ReturnTimeBound

/-!
Agent #105, session 8f1107db019a. Uniform positive safe returns for the original
Agent8 dynamics on a fixed finite affine-run family. The variable-time return
hypothesis is substantive: the theorem neither constructs such returns nor
asserts that any particular starting integer avoids palindromes forever.
-/

namespace Agent105.UniformReturn

open Agent102 Agent105.AffineDynamics Agent105.AffineShape
open Agent105.AffineStability Agent105.TailSelection

/-- The actual next normalized digit output. At a positive time i, this is
normalization after i-1 pair-word steps, not the symmetric pair word itself. -/
def outputWord (w : List Nat) (i : Nat) : List Nat :=
  Agent8.normalize (Agent8.orbit w (i - 1)) 0

/-- Safety includes every positive output through the endpoint t. It makes
no assertion about the initial integer at time zero. -/
def SafeThrough (w : List Nat) (t : Nat) : Prop :=
  ∀ i, 1 ≤ i → i ≤ t → (outputWord w i).reverse ≠ outputWord w i

theorem actual_return_tailStable (Q : Nat → List Nat)
    (hQ : HasAffineRuns Q 18) (s t : Nat) :
    TailStable (fun k => Agent8.orbit (Q k) t = Q (k + s)) :=
  hasAffineRuns_equality_tailStable
    (fun k => Agent8.orbit (Q k) t) (fun k => Q (k + s)) 18 18
    (hasAffineRuns_orbit Q hQ t) (hasAffineRuns_shift Q 18 s hQ)

theorem actual_output_safety_tailStable (Q : Nat → List Nat)
    (hQ : HasAffineRuns Q 18) (i : Nat) :
    TailStable (fun k => (outputWord (Q k) i).reverse ≠ outputWord (Q k) i) :=
  hasAffineRuns_nonpalindrome_tailStable
    (fun k => outputWord (Q k) i) 9
    (hasAffineRuns_normalized_orbit Q hQ (i - 1) 0 (by decide))

/-- A bounded variable-time safe return in the actual dynamics has one
uniform positive time on a whole parameter tail. Stability is proved above,
not included as an unproved arithmetic premise of this theorem. -/
theorem uniform_bounded_safe_return (Q : Nat → List Nat)
    (hQ : HasAffineRuns Q 18) (s B : Nat)
    (hcover : Eventually (fun k => ∃ t, 1 ≤ t ∧ t ≤ B ∧
      Agent8.orbit (Q k) t = Q (k + s) ∧ SafeThrough (Q k) t)) :
    ∃ t, 1 ≤ t ∧ t ≤ B ∧ ∃ K, ∀ k, K ≤ k →
      Agent8.orbit (Q k) t = Q (k + s) ∧ SafeThrough (Q k) t := by
  exact uniform_safe_return_time B
    (Return := fun t k => Agent8.orbit (Q k) t = Q (k + s))
    (Safe := fun i k => (outputWord (Q k) i).reverse ≠ outputWord (Q k) i)
    (fun t _ _ => actual_return_tailStable Q hQ s t)
    (fun i _ _ => actual_output_safety_tailStable Q hQ i) hcover

/-- The written additive-parameter uniform-return theorem for actual words.

Only the original substantive hypotheses remain: a fixed bounded coefficient
run table of positive eventual width slope, a positive parameter shift,
eventual canonicality, and existence of a positive safe return at each large
parameter. Actual affine closure, truth-value stability, equal-head behavior,
the exact width gain, and the common finite time bound are all derived.

The signed affine input lengths include empty and eventually disappearing
runs. A negative intercept is retained; no artificial k=0 width formula is
assumed. CanonicalPair here is the original list predicate and is not silently
identified with ordinary-integer realizability.
-/
theorem uniform_safe_return_wordAt (rs : List RunSpec)
    (hrs : SpecBound rs 18) (s : Nat)
    (hA : 0 < widthSlope rs) (hs : 0 < s)
    (hcanonical : Eventually (fun k => Agent8.CanonicalPair (wordAt rs k)))
    (hreturn : Eventually (fun k => ∃ t, 0 < t ∧
      Agent8.orbit (wordAt rs k) t = wordAt rs (k + s) ∧
      SafeThrough (wordAt rs k) t)) :
    ∃ t, 1 ≤ t ∧ t ≤ 4 * widthSlope rs * s ∧ ∃ K, ∀ k, K ≤ k →
      Agent8.orbit (wordAt rs k) t = wordAt rs (k + s) ∧
      SafeThrough (wordAt rs k) t := by
  obtain ⟨Kc, hc⟩ := hcanonical
  obtain ⟨Kr, hr⟩ := hreturn
  obtain ⟨d, Kw, hw⟩ := wordAt_head_width_eventually rs
  have hcover : Eventually (fun k => ∃ t, 1 ≤ t ∧
      t ≤ 4 * widthSlope rs * s ∧
      Agent8.orbit (wordAt rs k) t = wordAt rs (k + s) ∧
      SafeThrough (wordAt rs k) t) := by
    refine ⟨max Kw (max Kc Kr), ?_⟩
    intro k hk
    have hkw : Kw ≤ k := Nat.le_trans (Nat.le_max_left _ _) hk
    have hkc : Kc ≤ k := Nat.le_trans
      (Nat.le_trans (Nat.le_max_left _ _) (Nat.le_max_right _ _)) hk
    have hkr : Kr ≤ k := Nat.le_trans
      (Nat.le_trans (Nat.le_max_right _ _) (Nat.le_max_right _ _)) hk
    obtain ⟨t, ht, hret, hsafe⟩ := hr k hkr
    have hhead : (wordAt rs (k + s)).headD 0 = (wordAt rs k).headD 0 := by
      rw [(hw (k + s) (by omega)).1, (hw k hkw).1]
    have hwidth := (hw k hkw).2 s
    have hbound := Agent105.ReturnTimeBound.word_family_return_time_bound
      (wordAt rs) k s (widthSlope rs) t hA hs ht (hc k hkc) hret hhead hwidth
    exact ⟨t, hbound.2.1, hbound.2.2, hret, hsafe⟩
  exact uniform_bounded_safe_return (wordAt rs)
    (hasAffineRuns_wordAt rs 18 hrs) s (4 * widthSlope rs * s) hcover

end Agent105.UniformReturn

#print axioms Agent105.UniformReturn.actual_return_tailStable
#print axioms Agent105.UniformReturn.actual_output_safety_tailStable
#print axioms Agent105.UniformReturn.uniform_bounded_safe_return
#print axioms Agent105.UniformReturn.uniform_safe_return_wordAt
