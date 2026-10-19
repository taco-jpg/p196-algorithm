import P196.OrdinaryExteriorHistories.Numeric

/-!
# Widths and separation of ordinary realizations

The existing realization theorem supplies the integer. Its exact template
length makes positivity and the common decimal width explicit. With a fixed
exterior and positive band length, the first band coefficient distinguishes
the phase, so ordinary realizations of different phases are different seeds.
-/

namespace Agent5.OrdinaryExteriorHistories

private theorem pairWord_length (n : Nat) :
    (Agent109.pairWord n).length = (Agent109.digits n).length :=
  Agent109.zipAdd_length _ _ (by simp)

/-- The ordinary decimal width grows by exactly the whole terminal carry.
This includes zero, whose digit word is empty. -/
theorem digits_step_length (n : Nat) :
    (Agent109.digits (Lychrel196.step n)).length =
      (Agent109.digits n).length +
        (Agent109.norm (Agent109.pairWord n) 0).2 := by
  rw [digits_step_eq_normalize, Agent109.normalize_eq_norm,
    List.length_append, Agent109.norm_length, pairWord_length]
  have hcarry := Agent109.norm_carry_le (Agent109.pairWord n) 0
    (Agent109.bounded_pair_digits n) (by decide)
  rcases (by omega : (Agent109.norm (Agent109.pairWord n) 0).2 = 0 ∨
      (Agent109.norm (Agent109.pairWord n) 0).2 = 1) with h | h <;>
    simp [h, Agent109.carryWord]

/-- Empty inner words and equal band lengths give this exact initial
decimal width, for any ordinary realization of the template. -/
theorem digits_length_of_template (n c : Nat) (B : List Nat) (g : Nat)
    (hrep : Agent109.pairWord n = Agent109.template c B [] [] g g) :
    (Agent109.digits n).length = 2 * B.length + 4 * g := by
  have hlen := congrArg List.length hrep
  rw [pairWord_length] at hlen
  simp only [Agent109.template, List.length_append, List.length_replicate,
    List.length_nil, List.length_reverse] at hlen
  omega

/-- The existing admissible-template realization can be chosen positive,
with an explicit width independent of the phase. -/
theorem positive_template_realized (c : Nat) (B : List Nat) (g : Nat)
    (hc : Agent109.Phase c) (hg : 0 < g)
    (hB : Agent109.Bounded B)
    (hhead : ∀ b, B.head? = some b → 0 < b) :
    ∃ n, 0 < n ∧
      (Agent109.digits n).length = 2 * B.length + 4 * g ∧
      Agent109.pairWord n = Agent109.template c B [] [] g g := by
  obtain ⟨n, hn⟩ := Agent109.Cert.template_realized c B [] [] g g hc hg hB
    (by simp [Agent109.Bounded]) (by simp [Agent109.Bounded])
    Agent109.Cert.Mirr.nil hhead
  have hlen := digits_length_of_template n c B g hn
  refine ⟨n, ?_, hlen, hn⟩
  by_cases hnzero : n = 0
  · rw [hnzero, Agent109.digits_zero, List.length_nil] at hlen
    omega
  · exact Nat.pos_of_ne_zero hnzero

/-- A common exterior and positive common outer band determine the phase
of a template from its full pair word, without any coefficient bounds. -/
theorem template_phase_injective (c d : Nat) (B : List Nat) (g h : Nat)
    (hg : 0 < g)
    (heq : Agent109.template c B [] [] g h =
      Agent109.template d B [] [] g h) : c = d := by
  obtain ⟨r, hr⟩ : ∃ r, g = r + 1 := ⟨g - 1, by omega⟩
  rw [hr] at heq
  simp only [Agent109.template, List.append_assoc] at heq
  have htail := List.append_cancel_left heq
  simp only [List.replicate_succ, List.cons_append] at htail
  exact (List.cons.inj htail).1

/-- Different template phases with the same exterior and positive band
give different ordinary integers. No injectivity of pairWord is assumed. -/
theorem distinct_phase_seeds (n m c d : Nat) (B : List Nat) (g h : Nat)
    (hg : 0 < g) (hcd : c ≠ d)
    (hn : Agent109.pairWord n = Agent109.template c B [] [] g h)
    (hm : Agent109.pairWord m = Agent109.template d B [] [] g h) : n ≠ m := by
  intro hnm
  apply hcd
  exact template_phase_injective c d B g h hg
    (hn.symm.trans ((congrArg Agent109.pairWord hnm).trans hm))

#print axioms digits_step_length
#print axioms digits_length_of_template
#print axioms positive_template_realized
#print axioms template_phase_injective
#print axioms distinct_phase_seeds

end Agent5.OrdinaryExteriorHistories
