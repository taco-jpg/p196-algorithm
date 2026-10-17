import Agent1PeriodicOuterStrip

/-!
Positive outside coefficients for the exact period-four quotient. Normalization
positivity is inherited from Agent8.canonical_step. Whole-period suffix removal
preserves the head of residual ++ period, including an empty residual.
-/

namespace Agent1.Periodic

open Agent8 Agent1.RepeatedBlock

/-- Every positive exponent of a valid tuple is a canonical symmetric pair
word in Agent8's list sense. Odd-center realizability is not inferred from
CanonicalPair; it remains part of the stronger ValidPeriodic input. -/
theorem periodicWord_canonical (B H w : Word) (k : Nat)
    (hv : ValidPeriodic B H w) (hk : 0 < k) :
    CanonicalPair (periodicWord B H w k) := by
  have hhead : (periodicWord B H w k).headD 0 = (B ++ w).headD 0 := by
    cases k with
    | zero => omega
    | succ k =>
      cases B with
      | cons b B => rfl
      | nil =>
        cases w with
        | nil => have := hv.period_length; simp at this
        | cons a w => rfl
  have hpos : 0 < (periodicWord B H w k).headD 0 := by
    rw [hhead]
    exact hv.outside_positive
  have hbr : Bounded B.reverse 18 :=
    fun x hx => hv.outer_bounded x (List.mem_reverse.mp hx)
  have hwr : Bounded w.reverse 18 :=
    fun x hx => hv.period_bounded x (List.mem_reverse.mp hx)
  refine ⟨?_, ?_, ?_, hpos⟩
  · intro he
    simp [he] at hpos
  · simp only [periodicWord, List.reverse_append, List.reverse_reverse,
      pow_reverse, hv.center_symmetric, List.append_assoc]
  · intro x hx
    simp only [periodicWord, List.mem_append] at hx
    rcases hx with (((hx | hx) | hx) | hx) | hx
    · exact hv.outer_bounded x hx
    · exact bounded_pow w k 18 hv.period_bounded x hx
    · exact hv.center_bounded x hx
    · exact bounded_pow w.reverse k 18 hwr x hx
    · exact hbr x hx

/-- The raw outside prefix begins with the positive outside coefficient of
the actual normalized-and-paired exponent-three input. -/
theorem raw_outer_positive (B H w : Word) (hv : ValidPeriodic B H w) :
    0 < (rawOuter B H w).headD 0 := by
  have hc := (canonical_step (periodicWord B H w 3)
    (periodicWord_canonical B H w 3 hv (by omega))).1
  have hp := hc.2.2.2
  cases he : stepWord (periodicWord B H w 3) with
  | nil => simp [he] at hp
  | cons a D => simpa [rawOuter, he] using hp

private theorem outside_append_periods (R w : Word) (n : Nat) :
    (R ++ pow w n ++ w).headD 0 = (R ++ w).headD 0 := by
  cases R with
  | cons a R => rfl
  | nil =>
    cases w with
    | nil =>
      induction n with
      | zero => rfl
      | succ n ih => simpa only [pow, List.nil_append] using ih
    | cons a w =>
      cases n <;> rfl

/-- Whole-period suffix stripping preserves the outside head. The appended
period supplies that head even when all of the outer word is stripped. -/
theorem stripPeriodSuffix_outside (w B : Word) (hw : w ≠ []) :
    ((stripPeriodSuffix w B).1 ++ w).headD 0 = (B ++ w).headD 0 := by
  calc
    ((stripPeriodSuffix w B).1 ++ w).headD 0 =
        ((stripPeriodSuffix w B).1 ++ pow w (stripPeriodSuffix w B).2 ++ w).headD 0 :=
      (outside_append_periods _ _ _).symm
    _ = (B ++ w).headD 0 :=
      congrArg (fun D : Word => (D ++ w).headD 0) (stripPeriodSuffix_spec w B hw).symm

end Agent1.Periodic

#print axioms Agent1.Periodic.periodicWord_canonical
#print axioms Agent1.Periodic.raw_outer_positive
#print axioms Agent1.Periodic.stripPeriodSuffix_outside
