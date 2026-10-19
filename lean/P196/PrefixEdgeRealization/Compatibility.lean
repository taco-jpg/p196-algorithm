import P196.Agent117RemainingCycles.PrefixCycle

/-!
# Exact compatibility of the two prefix descriptions

The executable inverse already contains every valid forward prefix edge.
Here the inverse equations recover a terminal carry bit and the two
deterministic scans, giving the converse. No full-word realization or
temporal composition is used in this module.
-/

set_option autoImplicit false

namespace PrefixEdgeRealization

open SevenColumn SevenColumnProjection

private theorem noOverflow_scans {p s : List Nat} {x y : Nat}
    (h : NoOverflow p s x y) :
    y < 2 → ∃ e, e < 2 ∧ (highDigits s e).1 = y ∧
      p = List.zipWith (· + ·) (lowDigits s x) (highDigits s e).2 := by
  induction h with
  | nil x y =>
      intro hy
      exact ⟨y, hy, rfl, rfl⟩
  | @cons p s v a x y z ha hz hy hv tail ih =>
      intro _
      obtain ⟨e, he, hh, hp⟩ := ih hz
      refine ⟨e, he, ?_, ?_⟩
      · simpa only [Agent117.highDigits_cons, hh] using hy
      · simp only [Agent117.lowDigits_cons, Agent117.highDigits_cons,
          List.zipWith_cons_cons]
        rw [hh, ← hp, hv]

private theorem overflowTail_scans {p s : List Nat} {prev x y : Nat}
    (h : OverflowTail p s prev x y) :
    ∃ e, e < 2 ∧ carry prev (highDigits s e).1 = y ∧
      p = List.zipWith (· + ·) (lowDigits s x)
        (lowDigit prev (highDigits s e).1 :: (highDigits s e).2) := by
  induction h with
  | @nil prev x y terminal =>
      obtain ⟨e, he, hh⟩ := terminal
      exact ⟨e, he, hh, rfl⟩
  | @cons p s v a prev x y z ha hz hy hv tail ih =>
      obtain ⟨e, he, hh, hp⟩ := ih
      refine ⟨e, he, ?_, ?_⟩
      · simpa only [Agent117.highDigits_cons, hh] using hy
      · simp only [Agent117.lowDigits_cons, Agent117.highDigits_cons,
          List.zipWith_cons_cons]
        rw [hh, ← hp, hv]

/-- Every complete inverse edge has one of the two forward carry labels. -/
theorem longCompatible_forwardAdmitted {p s : List Nat}
    (h : LongCompatible p s) : ForwardAdmitted s p := by
  cases h with
  | @noOverflow p s a positive equations =>
      obtain ⟨e, he, hh, hp⟩ := noOverflow_scans equations (by decide)
      refine ⟨e, by omega, ?_⟩
      simp only [forwardPrefix, hh, if_true]
      exact hp.symm
  | @overflow p s v a positive ha outer equations =>
      obtain ⟨e, he, hh, hp⟩ := overflowTail_scans equations
      refine ⟨e, by omega, ?_⟩
      simp only [forwardPrefix, Agent117.highDigits_cons,
        Agent117.lowDigits_cons, hh, Nat.one_ne_zero, if_false,
        List.zipWith_cons_cons]
      rw [← hp]
      exact congrArg (fun z => z :: p) ((Nat.add_comm _ _).trans outer.symm)

/-- Exact equivalence on all lists; source validity is explicit and also
excludes the empty list. The existing forward-to-inverse proof is reused. -/
theorem mem_prefixPredecessors_iff_forwardAdmitted (s p : List Nat) :
    s ∈ prefixPredecessors p ↔
      (∀ a ∈ s, a < 19) ∧ 0 < s.headD 0 ∧ ForwardAdmitted s p := by
  constructor
  · intro h
    have hc := SevenColumn.mem_prefixPredecessors_iff.mp h
    exact ⟨hc.source_lt19, hc.positive_exterior,
      longCompatible_forwardAdmitted hc⟩
  · rintro ⟨hs, hpos, hf⟩
    exact Agent117.forwardAdmitted_mem_prefixPredecessors hs hpos hf

/-- Membership of a proposed source in the full executable inverse can
be checked by the existing forward checker at its two possible carry bits. -/
theorem mem_prefixPredecessors_iff_edgeOK (s p : List Nat) :
    s ∈ prefixPredecessors p ↔
      (Agent117.edgeOK p s 0 || Agent117.edgeOK p s 1) = true := by
  constructor
  · intro h
    obtain ⟨hs, hpos, e, he, hf⟩ :=
      (mem_prefixPredecessors_iff_forwardAdmitted s p).mp h
    have hok : Agent117.edgeOK p s e = true := by
      simp only [Agent117.edgeOK, Bool.and_eq_true, decide_eq_true_eq,
        List.all_eq_true, beq_iff_eq]
      exact ⟨⟨⟨by omega, hs⟩, hpos⟩, hf⟩
    have hbit : e = 0 ∨ e = 1 := by omega
    rcases hbit with rfl | rfl <;> simp [hok]
  · intro h
    simp only [Bool.or_eq_true] at h
    rcases h with h | h
    · exact Agent117.edgeOK_sound h
    · exact Agent117.edgeOK_sound h

#print axioms longCompatible_forwardAdmitted
#print axioms mem_prefixPredecessors_iff_forwardAdmitted
#print axioms mem_prefixPredecessors_iff_edgeOK

end PrefixEdgeRealization
