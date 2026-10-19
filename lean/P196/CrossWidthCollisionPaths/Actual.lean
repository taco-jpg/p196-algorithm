import P196.CrossWidthCollisionPaths.Profiles
import P196.CrossWidthCollisionStates.ActualTrace

/-!
# Actual collisions give valid reflected paths

The finite state trace of an ordinary collision recovers both original
coefficient words on their active prefixes. Its reflection exchanges the
two carry differences, and each self-reflected coefficient is even because
it is twice a source digit.
-/

set_option autoImplicit false

namespace CrossWidthCollisionPaths

open DecimalDigits FoldedDecimal Lychrel196 CrossWidthCollisionStates
open Agent105CrossWidth9df76b

private theorem actual_state_reflection
    (d e : Nat → Nat) (L i : Nat) (hi : 1 ≤ i) (hiL : i ≤ L) :
    stateAt (columnSum d L) (columnSum e (L + 1)) L (L + 1 - i) =
      flip (stateAt (columnSum d L) (columnSum e (L + 1)) L i) := by
  have hfirst : L + 1 - i - 1 = L - i := by omega
  have hlast : L - (L + 1 - i) + 1 = i := by omega
  have hboundary : L + 1 - i = L - i + 1 := by omega
  have hindex : L - 1 - (i - 1) = L - i := by omega
  have hq : columnSum d L (L - i) = columnSum d L (i - 1) := by
    have h := columnSum_symmetric d L (i - 1) (by omega)
    rw [hindex] at h
    exact h.symm
  dsimp only [stateAt, flip]
  rw [hfirst, hlast, hq, hboundary]

/-- The actual state trace reconstructs both source coefficient words.
The equalities concern only the two active source prefixes. -/
theorem actual_trace_words
    {n m L : Nat} {d e : Nat → Nat} {f : Nat → State}
    (hn : Canonical n d L) (hm : Canonical m e (L + 1))
    (hstep : step n = step m)
    (hf : ∀ i, 1 ≤ i → i ≤ L →
      stateAt (columnSum d L) (columnSum e (L + 1)) L i = f i) :
    (∀ i, i < L → columnSum d L i = shortWord f i) ∧
      (∀ i, i < L + 1 → columnSum e (L + 1) i = longWord L f i) := by
  have houter := cross_width_outer hn hm (by omega) hstep
  constructor
  · intro i hi
    have hx := congrArg State.x (hf (i + 1) (by omega) (by omega))
    simpa only [stateAt, shortWord, Nat.add_sub_cancel] using hx
  · intro i hi
    by_cases hi0 : i = 0
    · subst i
      simpa only [longWord, true_or, if_true] using houter.2
    by_cases hiL : i = L
    · subst i
      have hsym : columnSum e (L + 1) 0 = columnSum e (L + 1) L := by
        simpa only [Nat.add_sub_cancel, Nat.sub_zero] using
          columnSum_symmetric e (L + 1) 0 (by omega)
      have hlast : columnSum e (L + 1) L = 1 := hsym.symm.trans houter.2
      simpa only [longWord, or_true, if_true] using hlast
    · have hhigh := cross_width_high_column hn hm (by omega) hstep
        (i := i) (by omega) (by omega)
      rw [hf i (by omega) (by omega),
        hf (i + 1) (by omega) (by omega)] at hhigh
      simp only [longWord, hi0, hiL, or_self, if_false]
      omega

/-- Every actual collision trace is a closed reflected path with the
center parity required for ordinary source coefficient words. -/
theorem actual_trace_valid
    {n m L : Nat} {d e : Nat → Nat} {f : Nat → State}
    (hn : Canonical n d L) (hm : Canonical m e (L + 1))
    (hstep : step n = step m)
    (hf : ∀ i, 1 ≤ i → i ≤ L →
      stateAt (columnSum d L) (columnSum e (L + 1)) L i = f i) :
    Valid L f := by
  have hL := cross_width_short_length hn hm (by omega) hstep
  obtain ⟨hfirst, hlast, hedge⟩ :=
    cross_width_state_closed_walk hn hm (by omega) hstep
  have hclosed : Closed L f := by
    refine ⟨hL, ?_, ?_, ?_, ?_⟩
    · exact (hf 1 (by omega) (by omega)).symm.trans hfirst
    · exact (hf L (by omega) (by omega)).symm.trans hlast
    · intro i hi hiL
      have h := hedge i hi hiL
      rw [hf i hi (by omega), hf (i + 1) (by omega) (by omega)] at h
      exact h
    · intro i hi hiL
      have h := actual_state_reflection d e L i hi hiL
      rw [hf (L + 1 - i) (by omega) (by omega), hf i hi hiL] at h
      exact h
  obtain ⟨hshort, hlong⟩ := actual_trace_words hn hm hstep hf
  refine { toClosed := hclosed, short_center := ?_, long_center := ?_ }
  · intro i hi hcenter
    rw [← hshort i hi]
    have hmirror : L - 1 - i = i := hcenter.symm
    simp only [columnSum, reflected, hmirror]
    omega
  · intro i hi hcenter
    rw [← hlong i hi]
    have hmirror : L + 1 - 1 - i = i := by omega
    simp only [columnSum, reflected, hmirror]
    omega

end CrossWidthCollisionPaths

#print axioms CrossWidthCollisionPaths.actual_trace_words
#print axioms CrossWidthCollisionPaths.actual_trace_valid
