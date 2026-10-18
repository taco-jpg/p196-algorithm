import P196.Drafts.Agent108WindowWeightsB31b8818.Trace

namespace Agent13FoldedFamily
open DecimalDigits FoldedDecimal Lychrel196

/-- Reflection retains the complete even width, including internal zero positions. -/
def reflectHalf (H : Nat → Nat) (h i : Nat) : Nat :=
  H (if i < h then i else 2*h-1-i)

def inputWord (e : Nat → Bool) (r k : Nat) : Nat → Nat :=
  reflectHalf (inputHalf e r) (halfWidth r k)

def targetWord (r k : Nat) : Nat → Nat :=
  reflectHalf (targetHalf r) (halfWidth r k)

theorem reflect_low (H : Nat → Nat) (h i : Nat) (hi : i < h) :
    reflectHalf H h i = H i := by simp [reflectHalf,hi]

theorem reflect_symm (H : Nat → Nat) (h i : Nat) (hi : i < 2*h) :
    reflectHalf H h i = reflectHalf H h (2*h-1-i) := by
  have hrev : 2*h-1-(2*h-1-i)=i := by omega
  by_cases hs : i < h
  · simp [reflectHalf, hs, show ¬ 2*h-1-i < h by omega, hrev]
  · simp [reflectHalf, hs, show 2*h-1-i < h by omega]

theorem reflect_admissible (H : Nat → Nat) (h : Nat) (hh : 0 < h)
    (hout : 0 < H 0) (hb : ∀ i, i < h → H i ≤ 18) :
    Admissible (2*h) (reflectHalf H h) := by
  refine ⟨by omega, ?_, ?_, reflect_symm H h, ?_⟩
  · simpa [reflectHalf,hh] using hout
  · intro i hi
    unfold reflectHalf
    split
    · exact hb _ (by omega)
    · exact hb _ (by omega)
  · intro i hi heq
    omega

theorem inputHalf_bounded (e : Nat → Bool) (r i : Nat) : inputHalf e r i ≤ 18 := by
  unfold inputHalf
  split
  · decide
  · split
    · unfold blockDigit; split
      · split <;> decide
      · decide
    · split <;> decide

theorem targetHalf_bounded (r i : Nat) : targetHalf r i ≤ 18 := by
  unfold targetHalf
  split
  · decide
  · split <;> decide

theorem input_admissible (e : Nat → Bool) (r k : Nat) :
    Admissible (2*halfWidth r k) (inputWord e r k) := by
  exact reflect_admissible _ _ (by unfold halfWidth; omega)
    (by simp [inputHalf]) (fun i _ => inputHalf_bounded e r i)

theorem target_admissible (r k : Nat) :
    Admissible (2*halfWidth r k) (targetWord r k) := by
  exact reflect_admissible _ _ (by unfold halfWidth; omega)
    (by simp [targetHalf]) (fun i _ => targetHalf_bounded r i)

/-- The trace closes at the actual even center; no overflow is assumed. -/
theorem actual_trace (e : Nat → Bool) (r k : Nat) (hk : 0 < k) :
    (∀ i, i ≤ halfWidth r k → lowTrace e r i = carry (inputWord e r k) i) ∧
    (∀ i, i ≤ halfWidth r k → highTrace e r i = carry (inputWord e r k) (2*halfWidth r k-i)) ∧
    highTrace e r 0 = carry (inputWord e r k) (2*halfWidth r k) := by
  apply even_folded_trace_sound
  · exact reflect_symm _ _
  · exact (outer_trace e r).1
  · intro i hi
    rw [show inputWord e r k i = inputHalf e r i from reflect_low _ _ _ hi]
    exact (trace_edges e r i).1
  · intro i hi
    rw [show inputWord e r k i = inputHalf e r i from reflect_low _ _ _ hi]
    exact (trace_edges e r i).2.1
  · have h : ¬ halfWidth r k ≤ 4*r+1 := by unfold halfWidth; omega
    have h0 : halfWidth r k ≠ 0 := by unfold halfWidth; omega
    simp [lowTrace, highTrace, h, h0]

theorem binary_family_no_overflow (e : Nat → Bool) (r k : Nat) (hk : 0 < k) :
    carry (inputWord e r k) (2*halfWidth r k) = 0 := by
  exact (actual_trace e r k hk).2.2.symm.trans (outer_trace e r).2.1

theorem nextColumns_symm_no_overflow (q : Nat → Nat) (L i : Nat) (hi : i < L)
    (hc : carry q L = 0) : nextColumns q L i = nextColumns q L (L-1-i) := by
  have hh : L-1-(L-1-i)=i := by omega
  simp only [nextColumns,hc,if_true,columnSum,reflected,hh]
  exact Nat.add_comm _ _

theorem binary_family_half_transition (e : Nat → Bool) (r k i : Nat)
    (hk : 0 < k) (hi : i < halfWidth r k) :
    nextColumns (inputWord e r k) (2*halfWidth r k) i = targetHalf r i := by
  have ht := actual_trace e r k hk
  have hc := binary_family_no_overflow e r k hk
  rw [folded_emission_no_overflow (inputWord e r k) (2*halfWidth r k) i
    (by omega) (fun j hj => reflect_symm (inputHalf e r) (halfWidth r k) j hj) hc]
  rw [show inputWord e r k i = inputHalf e r i from reflect_low _ _ _ hi,
    ← ht.1 i (by omega)]
  have hr : 2*halfWidth r k-1-i = 2*halfWidth r k-(i+1) := by omega
  rw [hr, ← ht.2.1 (i+1) (by omega)]
  exact (trace_edges e r i).2.2

/-- Equality on every column, not only on the exterior prefix. -/
theorem binary_family_transition (e : Nat → Bool) (r k : Nat) (hk : 0 < k) :
    nextWidth (inputWord e r k) (2*halfWidth r k) = 2*halfWidth r k ∧
    ∀ i, i < 2*halfWidth r k →
      nextColumns (inputWord e r k) (2*halfWidth r k) i = targetWord r k i := by
  have hc := binary_family_no_overflow e r k hk
  refine ⟨by simp [nextWidth,hc], ?_⟩
  intro i hi
  by_cases hl : i < halfWidth r k
  · rw [binary_family_half_transition e r k i hk hl]
    exact (reflect_low _ _ _ hl).symm
  · have hr : 2*halfWidth r k-1-i < halfWidth r k := by omega
    rw [nextColumns_symm_no_overflow _ _ _ hi hc,
      binary_family_half_transition e r k _ hk hr]
    simp [targetWord,reflectHalf,hl]

/-- Every canonical realization of the displayed input follows this exact edge. -/
theorem binary_family_actual_step (e : Nat → Bool) (r k n : Nat) (d : Nat → Nat)
    (hk : 0 < k) (hcan : Canonical n d (2*halfWidth r k))
    (hrep : ∀ i, i < 2*halfWidth r k → columnSum d (2*halfWidth r k) i = inputWord e r k i) :
    step n = value (inputWord e r k) (2*halfWidth r k) ∧
    ∃ d', Canonical (step n) d' (2*halfWidth r k) ∧
      ∀ i, i < 2*halfWidth r k → columnSum d' (2*halfWidth r k) i = targetWord r k i := by
  refine ⟨step_eq_word_value n d _ _ hcan hrep, ?_⟩
  obtain ⟨d',hd',hr⟩ := representation_next n d _ _ hcan hrep
  have ht := binary_family_transition e r k hk
  rw [ht.1] at hd' hr
  exact ⟨d',hd',fun i hi => (hr i hi).trans (ht.2 i hi)⟩

/-- The symbolic family has ordinary positive decimal realizations. -/
theorem binary_family_realization (e : Nat → Bool) (r k : Nat) (hk : 0 < k) :
    ∃ n d, 0 < n ∧ Canonical n d (2*halfWidth r k) ∧
      (∀ i, i < 2*halfWidth r k → columnSum d (2*halfWidth r k) i = inputWord e r k i) ∧
      step n = value (inputWord e r k) (2*halfWidth r k) ∧
      ∃ d', Canonical (step n) d' (2*halfWidth r k) ∧
        ∀ i, i < 2*halfWidth r k → columnSum d' (2*halfWidth r k) i = targetWord r k i := by
  have h := input_admissible e r k
  obtain ⟨n,d,hn,hcan,hrep⟩ := valid_word_realizable _ _ h.1 h.2.1 h.2.2.1 h.2.2.2.1 h.2.2.2.2
  exact ⟨n,d,hn,hcan,hrep,binary_family_actual_step e r k n d hk hcan hrep⟩

end Agent13FoldedFamily
