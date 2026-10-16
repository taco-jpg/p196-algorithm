import OddCounts

/-
Agent #7. Fixed-center strengthening of the frozen OddCounts checkpoint.
Status before successful compilation: proof-development draft.
This file does not modify the frozen checkpoint being published by parent.
-/
namespace P196.Agent7.OddFibers

open P196.Agent9.InverseFibers

set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

theorem oddEndpoint_monotone (v : Fin 10) (a b : Counts) (h : countLe a b) :
    oddEndpoint v a ≤ oddEndpoint v b := by
  simp only [countLe] at h
  unfold oddEndpoint
  split <;> omega

theorem one_class_endpoint_bound : ∀ i : Fin 5, ∀ v : Fin 10,
    oddEndpoint v (classAdvance i initial) ≤ oddEndpoint v (nineRun 1) := by
  decide

theorem two_class_endpoint_bound : ∀ i j : Fin 5, ∀ v : Fin 10,
    oddEndpoint v (classAdvance j (classAdvance i initial)) ≤
      oddEndpoint v (nineRun 2) := by
  decide

theorem three_class_endpoint_bound : ∀ i j k : Fin 5, ∀ v : Fin 10,
    oddEndpoint v (classAdvance k (classAdvance j (classAdvance i initial))) ≤
      oddEndpoint v (nineRun 3) := by
  decide

/-- The all-nine target maximizes the inverse count separately for every
fixed middle digit, including the small and empty half-width cases. -/
theorem odd_count_fixed_center_bound (ss : List Symbol) (v : Fin 10) :
    oddInverseCount ss v ≤ oddInverseCount (List.replicate ss.length 9) v := by
  change oddEndpoint v (run ss initial) ≤ oddEndpoint v (nineRun ss.length)
  cases ss with
  | nil => exact Nat.le_refl _
  | cons s ss =>
    cases ss with
    | nil =>
      simpa [run, advance_eq_class] using one_class_endpoint_bound (symbolClass s) v
    | cons t ss =>
      cases ss with
      | nil =>
        simpa [run, advance_eq_class] using two_class_endpoint_bound (symbolClass s) (symbolClass t) v
      | cons u ss =>
        cases ss with
        | nil =>
          simpa [run, advance_eq_class] using three_class_endpoint_bound (symbolClass s) (symbolClass t) (symbolClass u) v
        | cons w ss =>
          have h := oddEndpoint_monotone v _ _ (long_run_dominated s t u w ss)
          simpa only [List.length_cons, Nat.add_assoc] using h

theorem odd_preimages_fixed_center_bound (ss : List Symbol) (v : Fin 10) :
    (oddPreimages ss v 0).length ≤
      (oddPreimages (List.replicate ss.length 9) v 0).length := by
  rw [odd_preimages_length, odd_preimages_length]
  exact odd_count_fixed_center_bound ss v

/-- At positive half-width, the canonical-positive leading-eleven family
attains the maximum for each fixed center digit, even when that maximum is zero. -/
theorem leading_eleven_fixed_center_maximum (n : Nat) (v : Fin 10) :
    ∀ ss : List Symbol, ss.length = n+1 →
      (oddPreimages ss v 0).length ≤
        (oddPreimages (11 :: List.replicate n 9) v 0).length := by
  intro ss hs
  rw [odd_preimages_length, odd_preimages_length, leading_eleven_odd_count]
  have h := odd_count_fixed_center_bound ss v
  rw [hs] at h
  exact h

#print axioms oddEndpoint_monotone
#print axioms one_class_endpoint_bound
#print axioms two_class_endpoint_bound
#print axioms three_class_endpoint_bound
#print axioms odd_count_fixed_center_bound
#print axioms odd_preimages_fixed_center_bound
#print axioms leading_eleven_fixed_center_maximum

end P196.Agent7.OddFibers
