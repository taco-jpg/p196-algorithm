import OddCanonical
import OddCountsPhase

/-!
Exact maxima for complete canonical odd coefficient-word fibers.
The finite list is duplicate-free and its membership is the literal
complete-word predicate from OddCanonical, not an assumed half encoding.
-/
namespace P196.Agent7.OddFibers

open P196.Agent9.InverseFibers

theorem fullOddPreimages_length_le (ss : List Symbol) (v : Fin 10) :
    (fullOddPreimages ss v).length ≤ (oddPreimages ss v 0).length := by
  unfold fullOddPreimages canonicalOddPreimages
  rw [List.length_map]
  exact List.length_filter_le ..

theorem fullOddPreimages_bound (ss : List Symbol) (v : Fin 10) :
    (fullOddPreimages ss v).length ≤ oddMax ss.length :=
  Nat.le_trans (fullOddPreimages_length_le ss v) (odd_preimages_bound ss v)

theorem canonical_leading_eleven (ss : List Symbol) (v : Fin 10) :
    canonicalOddPreimages (11 :: ss) v = oddPreimages (11 :: ss) v 0 := by
  unfold canonicalOddPreimages
  apply List.filter_eq_self.mpr
  intro w hw
  simpa only [decide_eq_true_eq] using
    leading_eleven_odd_positive ss v w.1 w.2 hw

theorem full_leading_eleven_length (ss : List Symbol) (v : Fin 10) :
    (fullOddPreimages (11 :: ss) v).length =
      (oddPreimages (11 :: ss) v 0).length := by
  simp only [fullOddPreimages, List.length_map, canonical_leading_eleven]

theorem fullOddPreimages_center_bound (ss : List Symbol) (v : Fin 10) :
    (fullOddPreimages ss v).length ≤ oddCenterMax ss.length v :=
  Nat.le_trans (fullOddPreimages_length_le ss v) (odd_preimages_exact_center_bound ss v)

/-- Every fixed center has an explicit maximizing canonical target at
positive half-width. The degenerate width-one zero-center case is not
silently treated as positive. -/
theorem full_fixed_center_maximum (n : Nat) (v : Fin 10) :
    (fullOddPreimages (11 :: List.replicate n 9) v).length = oddCenterMax (n+1) v := by
  rw [full_leading_eleven_length]
  exact leading_eleven_exact_center n v

def sharpTargetHalf : Nat → List Symbol
  | 0 => []
  | n+1 => 11 :: List.replicate n 9

theorem sharpTargetHalf_length (m : Nat) : (sharpTargetHalf m).length = m := by
  cases m <;> simp [sharpTargetHalf]

def sharpFamily (m : Nat) : List (List Nat) :=
  fullOddPreimages (sharpTargetHalf m) (sharpCenter m)

theorem sharpFamily_zero : sharpFamily 0 = [[6]] := by decide

theorem sharpFamily_length (m : Nat) : (sharpFamily m).length = oddMax m := by
  cases m with
  | zero => rw [sharpFamily_zero]; rfl
  | succ n =>
    unfold sharpFamily sharpTargetHalf
    rw [full_leading_eleven_length]
    exact explicit_leading_eleven_sharp n

/-- An explicit duplicate-free family of all canonical words in an
attaining fiber. Every word has the same original actual transition. -/
theorem sharpFamily_exact (m : Nat) :
    (sharpFamily m).Nodup ∧ (sharpFamily m).length = oddMax m ∧
      (∀ q, q ∈ sharpFamily m ↔
        CanonicalOddFiber (sharpTargetHalf m) (sharpCenter m) q) := by
  exact ⟨fullOddPreimages_nodup _ _, sharpFamily_length m,
    fullOddPreimages_membership _ _⟩

/-- Uniform sharp maximum over the complete canonical odd-width domain.
Width is exactly 2*m+1; the target is paired from decimal output digits,
so its middle coefficient is twice the prescribed digit. -/
theorem complete_canonical_odd_fiber_maximum (m : Nat) :
    (∀ ss : List Symbol, ∀ v : Fin 10, ss.length = m →
      (fullOddPreimages ss v).length ≤ (fib (m+1)+1)/2) ∧
    (∃ ss : List Symbol, ∃ v : Fin 10, ss.length = m ∧
      (fullOddPreimages ss v).length = (fib (m+1)+1)/2) := by
  constructor
  · intro ss v hlen
    simpa only [hlen, oddMax] using fullOddPreimages_bound ss v
  · exact ⟨sharpTargetHalf m, sharpCenter m, sharpTargetHalf_length m,
      sharpFamily_length m⟩

#print axioms fullOddPreimages_length_le
#print axioms fullOddPreimages_bound
#print axioms canonical_leading_eleven
#print axioms full_leading_eleven_length
#print axioms fullOddPreimages_center_bound
#print axioms full_fixed_center_maximum
#print axioms sharpTargetHalf_length
#print axioms sharpFamily_zero
#print axioms sharpFamily_length
#print axioms sharpFamily_exact
#print axioms complete_canonical_odd_fiber_maximum

end P196.Agent7.OddFibers
