import P196.Agent105UniformIntegerReturn.Agent105UniformReturnPlain
import P196.Agent105UniformIntegerReturn.Agent105IntegerSafety
import P196.Agent105UniformIntegerReturn.IntegerEndpoints

/-!
Agent #105, session 8f1107db019a. Ordinary-natural-number versions of the
affine-family uniform-return theorem. Existence assumptions explicitly give
positive integer realizations; the conclusion retains realizability and works
for every ordinary integer with the same pair word. Original Lychrel196 and
Agent109 compatibility theorems are used without modifying their definitions.
-/

namespace Agent105.UniformReturn

open Agent102 Agent105.AffineDynamics Agent105.AffineShape
open Agent105.TailSelection

theorem safeThrough_iff_integer (n : Nat) (w : List Nat) (t : Nat)
    (hrep : Agent109.pairWord n = w) :
    SafeThrough w t ↔
      ∀ i, 1 ≤ i → i ≤ t → ¬ Lychrel196.Palindrome (Lychrel196.orbit n i) := by
  constructor
  · intro h i hi hit
    exact (Agent105.IntegerSafety.nonpalindrome_orbit_positive_iff_of_pairWord
      n i w hi hrep).mpr (h i hi hit)
  · intro h i hi hit
    exact (Agent105.IntegerSafety.nonpalindrome_orbit_positive_iff_of_pairWord
      n i w hi hrep).mp (h i hi hit)

/-- Variable positive return times for actual positive integer realizations
imply a uniform time for all sufficiently large parameters and all realizations.
The return is a pair-word return, not equality of arbitrary chosen integers. -/
theorem uniform_integer_return (rs : List RunSpec) (hrs : SpecBound rs 18)
    (s : Nat) (hA : 0 < widthSlope rs) (hs : 0 < s)
    (hcover : Eventually (fun k => ∃ n t : Nat, n ≠ 0 ∧ 0 < t ∧
      Agent109.pairWord n = wordAt rs k ∧
      Agent109.pairWord (Lychrel196.orbit n t) = wordAt rs (k + s))) :
    ∃ t, 1 ≤ t ∧ t ≤ 4 * widthSlope rs * s ∧ ∃ K, ∀ k, K ≤ k →
      (∃ n, n ≠ 0 ∧ Agent109.pairWord n = wordAt rs k) ∧
      ∀ n, Agent109.pairWord n = wordAt rs k →
        Agent109.pairWord (Lychrel196.orbit n t) = wordAt rs (k + s) := by
  obtain ⟨K0, h0⟩ := hcover
  have hc : Eventually (fun k => Agent8.CanonicalPair (wordAt rs k)) := by
    refine ⟨K0, ?_⟩
    intro k hk
    obtain ⟨n, t, hn, ht, hrep, hret⟩ := h0 k hk
    rw [← hrep]
    exact Agent109.Endpoints.pairWord_canonical n hn
  have hr : Eventually (fun k => ∃ t, 0 < t ∧
      Agent8.orbit (wordAt rs k) t = wordAt rs (k + s)) := by
    refine ⟨K0, ?_⟩
    intro k hk
    obtain ⟨n, t, hn, ht, hrep, hret⟩ := h0 k hk
    rw [Agent109.Compat.pairWord_orbit, hrep] at hret
    exact ⟨t, ht, hret⟩
  obtain ⟨t, ht, hbound, Kt, htail⟩ := uniform_return_wordAt rs hrs s hA hs hc hr
  refine ⟨t, ht, hbound, max K0 Kt, ?_⟩
  intro k hk
  have hk0 : K0 ≤ k := Nat.le_trans (Nat.le_max_left _ _) hk
  have hkt : Kt ≤ k := Nat.le_trans (Nat.le_max_right _ _) hk
  obtain ⟨n0, t0, hn0, ht0, hrep0, hret0⟩ := h0 k hk0
  refine ⟨⟨n0, hn0, hrep0⟩, ?_⟩
  intro n hrep
  rw [Agent109.Compat.pairWord_orbit, hrep]
  exact htail k hkt

/-- The safe version preserves every actual positive output, including the
return endpoint. Existence of positive realizations is retained in the result,
so the universal statement about all realizations is not left vacuous. -/
theorem uniform_integer_safe_return (rs : List RunSpec) (hrs : SpecBound rs 18)
    (s : Nat) (hA : 0 < widthSlope rs) (hs : 0 < s)
    (hcover : Eventually (fun k => ∃ n t : Nat, n ≠ 0 ∧ 0 < t ∧
      Agent109.pairWord n = wordAt rs k ∧
      Agent109.pairWord (Lychrel196.orbit n t) = wordAt rs (k + s) ∧
      ∀ i, 1 ≤ i → i ≤ t → ¬ Lychrel196.Palindrome (Lychrel196.orbit n i))) :
    ∃ t, 1 ≤ t ∧ t ≤ 4 * widthSlope rs * s ∧ ∃ K, ∀ k, K ≤ k →
      (∃ n, n ≠ 0 ∧ Agent109.pairWord n = wordAt rs k) ∧
      ∀ n, Agent109.pairWord n = wordAt rs k →
        Agent109.pairWord (Lychrel196.orbit n t) = wordAt rs (k + s) ∧
        ∀ i, 1 ≤ i → i ≤ t → ¬ Lychrel196.Palindrome (Lychrel196.orbit n i) := by
  obtain ⟨K0, h0⟩ := hcover
  have hc : Eventually (fun k => Agent8.CanonicalPair (wordAt rs k)) := by
    refine ⟨K0, ?_⟩
    intro k hk
    obtain ⟨n, t, hn, ht, hrep, hret, hsafe⟩ := h0 k hk
    rw [← hrep]
    exact Agent109.Endpoints.pairWord_canonical n hn
  have hr : Eventually (fun k => ∃ t, 0 < t ∧
      Agent8.orbit (wordAt rs k) t = wordAt rs (k + s) ∧
      SafeThrough (wordAt rs k) t) := by
    refine ⟨K0, ?_⟩
    intro k hk
    obtain ⟨n, t, hn, ht, hrep, hret, hsafe⟩ := h0 k hk
    rw [Agent109.Compat.pairWord_orbit, hrep] at hret
    exact ⟨t, ht, hret, (safeThrough_iff_integer n (wordAt rs k) t hrep).mpr hsafe⟩
  obtain ⟨t, ht, hbound, Kt, htail⟩ := uniform_safe_return_wordAt rs hrs s hA hs hc hr
  refine ⟨t, ht, hbound, max K0 Kt, ?_⟩
  intro k hk
  have hk0 : K0 ≤ k := Nat.le_trans (Nat.le_max_left _ _) hk
  have hkt : Kt ≤ k := Nat.le_trans (Nat.le_max_right _ _) hk
  obtain ⟨n0, t0, hn0, ht0, hrep0, hret0, hsafe0⟩ := h0 k hk0
  refine ⟨⟨n0, hn0, hrep0⟩, ?_⟩
  intro n hrep
  obtain ⟨hret, hsafe⟩ := htail k hkt
  constructor
  · rw [Agent109.Compat.pairWord_orbit, hrep]
    exact hret
  · exact (safeThrough_iff_integer n (wordAt rs k) t hrep).mp hsafe

end Agent105.UniformReturn

#print axioms Agent105.UniformReturn.safeThrough_iff_integer
#print axioms Agent105.UniformReturn.uniform_integer_return
#print axioms Agent105.UniformReturn.uniform_integer_safe_return
