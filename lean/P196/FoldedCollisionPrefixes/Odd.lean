import P196.FoldedCollisionPrefixes.Prefixes

/-!
# Odd-width reflected collision prefixes

An odd shorter width has one central state. Its two carry coordinates
agree, and its coefficient is even. These conditions complete the finite
walk to a valid reflected trace. Extraction and reflection are inverse
on the full active interval.
-/

set_option autoImplicit false

namespace FoldedCollisionPrefixes

open CrossWidthCollisionStates CrossWidthCollisionPaths

private theorem oddTrace_reflection
    (k : Nat) (p : Prefix (k + 1))
    (ht : OddTerminal (prefixAt p (k + 1)))
    {i : Nat} (hi : 1 ≤ i) (hiL : i ≤ 2 * k + 3) :
    oddTrace k p (2 * k + 3 + 1 - i) = flip (oddTrace k p i) := by
  by_cases hleft : i < k + 2
  · have hcurrent : i ≤ k + 2 := by omega
    have hmirror : ¬ (2 * k + 3 + 1 - i ≤ k + 2) := by omega
    have hindex : 2 * k + 3 - (2 * k + 3 + 1 - i) = i - 1 := by omega
    simp only [oddTrace, if_pos hcurrent, if_neg hmirror, hindex]
  by_cases hcenter : i = k + 2
  · subst i
    have hmirror : 2 * k + 3 + 1 - (k + 2) = k + 2 := by omega
    have hmiddle : k + 2 = (k + 1) + 1 := by omega
    rw [hmirror, hmiddle, oddTrace_prefix k p (by omega)]
    exact (oddTerminal_flip ht).symm
  · have hcurrent : ¬ (i ≤ k + 2) := by omega
    have hmirror : 2 * k + 3 + 1 - i ≤ k + 2 := by omega
    have hindex : 2 * k + 3 + 1 - i - 1 = 2 * k + 3 - i := by omega
    simp only [oddTrace, if_neg hcurrent, if_pos hmirror, hindex,
      flip_involution]

private theorem oddTrace_left_edge
    {k : Nat} {p : Prefix (k + 1)} (hw : Walk (k + 1) p)
    {i : Nat} (hi : 1 ≤ i) (hiL : i < k + 2) :
    Edge (oddTrace k p i) (oddTrace k p (i + 1)) := by
  have hindex : i - 1 + 1 = i := by omega
  have hcurrent := oddTrace_prefix k p (i := i - 1) (by omega)
  have hnext := oddTrace_prefix k p (i := i) (by omega)
  rw [hindex] at hcurrent
  rw [hcurrent, hnext]
  simpa only [hindex] using hw.2 (i - 1) (by omega)

private theorem oddTrace_closed
    {k : Nat} {p : Prefix (k + 1)} (h : OddAccepted k p) :
    Closed (2 * k + 3) (oddTrace k p) := by
  obtain ⟨hw, ht⟩ := h
  refine ⟨by omega, ?_, ?_, ?_, ?_⟩
  · exact (oddTrace_prefix k p (i := 0) (by omega)).trans hw.1
  · have hlast : ¬ (2 * k + 3 ≤ k + 2) := by omega
    simp only [oddTrace, if_neg hlast, Nat.sub_self, hw.1, flip_initial]
  · intro i hi hiL
    by_cases hleft : i < k + 2
    · exact oddTrace_left_edge hw hi hleft
    · let j := 2 * k + 3 - i
      have hj : 1 ≤ j := by dsimp only [j]; omega
      have hjL : j < k + 2 := by dsimp only [j]; omega
      have hedge := oddTrace_left_edge hw hj hjL
      have hcurrent := oddTrace_reflection k p ht (i := j + 1)
        (by omega) (by dsimp only [j]; omega)
      have hnext := oddTrace_reflection k p ht (i := j) hj
        (by dsimp only [j]; omega)
      have hcurrentIndex : 2 * k + 3 + 1 - (j + 1) = i := by
        dsimp only [j]
        omega
      have hnextIndex : 2 * k + 3 + 1 - j = i + 1 := by
        dsimp only [j]
        omega
      rw [hcurrentIndex] at hcurrent
      rw [hnextIndex] at hnext
      rw [hcurrent, hnext]
      exact (edge_flip_iff _ _).mp hedge
  · intro i hi hiL
    exact oddTrace_reflection k p ht hi hiL

/-- Extracting the independent half of an odd-width valid trace gives
an accepted finite prefix, including the even self-reflected center. -/
theorem oddAccepted_take
    {k : Nat} {f : Nat → State} (h : Valid (2 * k + 3) f) :
    OddAccepted k (takePrefix (k + 1) f) := by
  constructor
  · constructor
    · rw [prefixAt_take (k + 1) f (i := 0) (by omega)]
      exact h.toClosed.first
    · intro i hi
      rw [prefixAt_take (k + 1) f (i := i) (by omega),
        prefixAt_take (k + 1) f (i := i + 1) (by omega)]
      exact h.toClosed.edge (i + 1) (by omega) (by omega)
  · unfold OddTerminal
    rw [prefixAt_take (k + 1) f (i := k + 1) (Nat.le_refl _)]
    have hmiddle : (k + 1) + 1 = k + 2 := by omega
    rw [hmiddle]
    constructor
    · have href := h.toClosed.reflection (k + 2) (by omega) (by omega)
      have hmirror : 2 * k + 3 + 1 - (k + 2) = k + 2 := by omega
      simpa only [hmirror, CrossWidthCollisionPaths.flip] using congrArg State.u href
    · have hc := h.short_center (k + 1) (by omega) (by omega)
      simpa only [shortWord, hmiddle] using hc

/-- Odd prefix acceptance is exactly validity of its reflected trace
at the specified shorter source width 2*k+3. -/
theorem odd_valid_iff (k : Nat) (p : Prefix (k + 1)) :
    OddAccepted k p ↔ Valid (2 * k + 3) (oddTrace k p) := by
  constructor
  · intro h
    refine { toClosed := oddTrace_closed h, short_center := ?_, long_center := ?_ }
    · intro i hi hcenter
      have hmiddle : i = k + 1 := by omega
      subst i
      change (oddTrace k p ((k + 1) + 1)).x % 2 = 0
      rw [oddTrace_prefix k p (Nat.le_refl _)]
      exact h.2.2
    · intro i hi hcenter
      omega
  · intro h
    have hp := oddAccepted_take h
    simpa only [takePrefix_oddTrace] using hp

/-- Reflecting the extracted half recovers every state of an odd-width
closed trace on the full active interval. -/
theorem oddTrace_take
    {k : Nat} {f : Nat → State} (h : Closed (2 * k + 3) f) :
    ∀ i, 1 ≤ i → i ≤ 2 * k + 3 →
      oddTrace k (takePrefix (k + 1) f) i = f i := by
  intro i hi hiL
  by_cases hleft : i ≤ k + 2
  · rw [oddTrace, if_pos hleft,
      prefixAt_take (k + 1) f (i := i - 1) (by omega)]
    congr 1
    omega
  · rw [oddTrace, if_neg hleft,
      prefixAt_take (k + 1) f (i := 2 * k + 3 - i) (by omega)]
    have href := h.reflection i hi hiL
    have hindex : 2 * k + 3 + 1 - i = (2 * k + 3 - i) + 1 := by omega
    rw [hindex] at href
    rw [href, flip_involution]

end FoldedCollisionPrefixes

#print axioms FoldedCollisionPrefixes.odd_valid_iff
#print axioms FoldedCollisionPrefixes.oddTrace_take
#print axioms FoldedCollisionPrefixes.oddAccepted_take
