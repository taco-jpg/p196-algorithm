import Agent1PeriodicGuardFacts

/-!
Exact complete-block suffix removal for the periodic whole-word quotient.
The remaining word keeps its original order. The recursive fuel is bounded
by input length, and the specification proves that this fuel suffices for
maximal removal of every nonempty block. No digit arithmetic is redefined.
-/

namespace Agent1.Periodic

open Agent8 Agent1.RepeatedBlock

/-- One iteration removes exactly one final copy of `w`. The empty block is
never removed. Fuel makes the executable recursion structurally terminating. -/
def stripPeriodSuffixAux (w : Word) : Nat → Word → Word × Nat
  | 0, B => (B, 0)
  | fuel + 1, B =>
      if w ≠ [] ∧ w.length ≤ B.length ∧ B.drop (B.length - w.length) = w then
        let r := stripPeriodSuffixAux w fuel (B.take (B.length - w.length))
        (r.1, r.2 + 1)
      else (B, 0)

/-- The exact maximal whole-block suffix removal used by the periodic quotient.
Input length is sufficient fuel even for a one-letter block. -/
def stripPeriodSuffix (w B : Word) : Word × Nat :=
  stripPeriodSuffixAux w B.length B

/-- Sufficient fuel yields both exact reconstruction and a fully stripped
remainder. This rules out interpreting a fuel-limited run as maximal. -/
theorem stripPeriodSuffixAux_spec (w : Word) (fuel : Nat) (B : Word)
    (hw : w ≠ []) (hFuel : B.length ≤ fuel) :
    B = (stripPeriodSuffixAux w fuel B).1 ++
          pow w (stripPeriodSuffixAux w fuel B).2 ∧
      ¬ ∃ D, (stripPeriodSuffixAux w fuel B).1 = D ++ w := by
  have hwpos : 0 < w.length := List.length_pos_iff.mpr hw
  induction fuel generalizing B with
  | zero =>
    have hB : B = [] := List.length_eq_zero_iff.mp (by omega)
    subst B
    constructor
    · rfl
    · rintro ⟨D, hD⟩
      have hl := congrArg List.length hD
      simp only [stripPeriodSuffixAux, List.length_nil, List.length_append] at hl
      omega
  | succ fuel ih =>
    rw [stripPeriodSuffixAux]
    split
    · rename_i h
      have hshort : (B.take (B.length - w.length)).length ≤ fuel := by
        rw [List.length_take_of_le (Nat.sub_le _ _)]
        omega
      obtain ⟨he, hm⟩ := ih (B.take (B.length - w.length)) hshort
      have hsplit : B = B.take (B.length - w.length) ++ w := by
        simpa only [h.2.2] using (List.take_append_drop (B.length - w.length) B).symm
      constructor
      · change B = (stripPeriodSuffixAux w fuel (B.take (B.length - w.length))).1 ++
            pow w ((stripPeriodSuffixAux w fuel (B.take (B.length - w.length))).2 + 1)
        rw [pow_succ_right, ← List.append_assoc, ← he]
        exact hsplit
      · exact hm
    · rename_i h
      constructor
      · simp [pow]
      · rintro ⟨D, hD⟩
        change B = D ++ w at hD
        apply h
        refine ⟨hw, ?_, ?_⟩
        · simp [hD]
        · simp [hD, List.drop_left]

/-- The reported count reconstructs the input exactly. -/
theorem stripPeriodSuffix_spec (w B : Word) (hw : w ≠ []) :
    B = (stripPeriodSuffix w B).1 ++ pow w (stripPeriodSuffix w B).2 :=
  (stripPeriodSuffixAux_spec w B.length B hw (Nat.le_refl _)).1

/-- No complete final copy of the nonempty block remains. -/
theorem stripPeriodSuffix_maximal (w B : Word) (hw : w ≠ []) :
    ¬ ∃ D, (stripPeriodSuffix w B).1 = D ++ w :=
  (stripPeriodSuffixAux_spec w B.length B hw (Nat.le_refl _)).2

/-- Empty blocks are explicitly left untouched and counted zero times. -/
theorem stripPeriodSuffix_empty_block (B : Word) :
    stripPeriodSuffix [] B = (B, 0) := by
  unfold stripPeriodSuffix
  cases B.length <;> simp [stripPeriodSuffixAux]

/-- Exact finite length accounting for the removed copies. -/
theorem stripPeriodSuffix_length (w B : Word) (hw : w ≠ []) :
    B.length = (stripPeriodSuffix w B).1.length +
      (stripPeriodSuffix w B).2 * w.length := by
  have h := congrArg List.length (stripPeriodSuffix_spec w B hw)
  simpa only [List.length_append, pow_length] using h

/-- Every retained coefficient was already in the input. -/
theorem stripPeriodSuffix_bounded (w B : Word) (bound : Nat)
    (hw : w ≠ []) (hB : Bounded B bound) :
    Bounded (stripPeriodSuffix w B).1 bound := by
  intro x hx
  apply hB x
  rw [stripPeriodSuffix_spec w B hw]
  exact List.mem_append_left _ hx

end Agent1.Periodic

#print axioms Agent1.Periodic.stripPeriodSuffixAux_spec
#print axioms Agent1.Periodic.stripPeriodSuffix_spec
#print axioms Agent1.Periodic.stripPeriodSuffix_maximal
#print axioms Agent1.Periodic.stripPeriodSuffix_empty_block
#print axioms Agent1.Periodic.stripPeriodSuffix_length
#print axioms Agent1.Periodic.stripPeriodSuffix_bounded
