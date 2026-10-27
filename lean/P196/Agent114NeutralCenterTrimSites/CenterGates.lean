import P196.Agent114NeutralCenterTrimSites.HeadCoefficient
import P196.Agent114NeutralCenterTrimSites.CenterSymmetry
import P196.Agent119NeutralCenterCanonicalization.Core
import P196.Agent119NeutralCenterUnpadding.Main

/-!
# Exact center trim gates

This formalizes Agent7's credited center boundary restrictions. The local
overflow gate needs source-head normality. A zero paired stripping depth
implies that head condition only when source symmetry and Hyp are available;
asymmetric accepted sources must not be silently treated as symmetric.
-/

namespace Agent114.NeutralCenterTrimSites

open Agent120.Neutral Agent119.NeutralCenterCanonicalization
  Agent119.NeutralCenterPadding Agent119.NeutralCenterUnpadding

private theorem positive_center_trim_head {b : Nat} {E : Edge}
    (he : edgeOK b E = true) (hv : 0 < E.v) :
    (nextC b E.B E.C).head? = some (b - 1) := by
  rw [(edgeOK_sound he).2.2]
  have hn : E.v ≠ 0 := by omega
  simp [List.head?_append, List.head?_replicate, hn]

/-- A nonneutral source head cannot produce a positive center trim on overflow.
No source symmetry or target-normality premise is needed for this local gate. -/
theorem head_normal_overflow_trim_zero {b : Nat} {E : Edge}
    (he : edgeOK b E = true) (hg : gam b E.B E.C = 1)
    (hn : E.C.head? ≠ some (b - 1)) : E.v = 0 := by
  by_cases hv : E.v = 0
  · exact hv
  · have hp : 0 < E.v := by omega
    exact False.elim (hn ((overflow_head_neutral_iff (edgeOK_sound he).1 hg).1
      (positive_center_trim_head he hp)))

theorem head_normal_positive_trim_nonoverflow {b : Nat} {E : Edge}
    (he : edgeOK b E = true) (hn : E.C.head? ≠ some (b - 1))
    (hv : 0 < E.v) : gam b E.B E.C = 0 := by
  have hgle := (edgeOK_sound he).1.gam_le
  have hgne : gam b E.B E.C ≠ 1 := by
    intro hg
    have hz := head_normal_overflow_trim_zero he hg hn
    omega
  omega

/-- A symmetric valid center with no removable neutral pair has a nonneutral
head. Hyp excludes the exceptional single neutral coefficient. -/
theorem symmetric_core_head_ne {b : Nat} {B C : List Nat}
    (h : Hyp b B C) (hs : C.reverse = C) (hd : depthC b C = 0) :
    C.head? ≠ some (b - 1) := by
  have hcore : coreC b C = C := by
    have hc := decompose b C
    simpa only [hd, padC_zero] using hc.symm
  intro hh
  cases C with
  | nil => simp at hh
  | cons c Q =>
      have hc : c = b - 1 := by simpa using hh
      subst c
      rcases List.eq_nil_or_concat Q with hQ | ⟨D, z, hQ⟩
      · have hn := not_Hyp_neutral_center b B 1
        exact hn (by simpa [hQ] using h)
      · simp only [List.concat_eq_append] at hQ
        have hz : z = b - 1 := by
          have hh' := congrArg List.head? hs
          simpa [hQ] using hh'
        apply core_irreducible b ((b - 1) :: Q)
        refine ⟨D, ?_⟩
        rw [hcore]
        simp [padC, hQ, hz, List.append_assoc]

/-- The exact center head/last coefficient and actual carry entering the last
coefficient. The two alternatives are reversed relative to exterior sites. -/
def CenterTrimSite (b : Nat) (B C : List Nat) : Prop :=
  ∃ P c, C = P ++ [c] ∧ C.head? = some c ∧
    ((e1 b B = 0 ∧ c = (3 * b - 1) / 2 ∧
        (norm b P (e1 b B)).2 = (3 * b - 1) % 2) ∨
     (e1 b B = 1 ∧ c = (b - 2) / 2 ∧
        (norm b P (e1 b B)).2 = (b - 2) % 2))

/-- Positive center trim at a symmetric source with nonneutral head forces
one of the exact all-base terminal carry/coefficient sites. -/
theorem symmetric_positive_trim_site {b : Nat} {E : Edge}
    (he : edgeOK b E = true) (hs : E.C.reverse = E.C)
    (hn : E.C.head? ≠ some (b - 1)) (hv : 0 < E.v) :
    CenterTrimSite b E.B E.C := by
  have h := (edgeOK_sound he).1
  have hg := head_normal_positive_trim_nonoverflow he hn hv
  have hh := positive_center_trim_head he hv
  rcases List.eq_nil_or_concat E.C with hnil | ⟨P, c, hC⟩
  · have hf := h.flip
    simp [e2, hnil] at hf
  · simp only [List.concat_eq_append] at hC
    have hhead : (P ++ [c]).head? = some c := by
      have hp := congrArg List.head? hs
      simpa [hC] using hp.symm
    have hc : c ≠ b - 1 := by
      intro heq
      apply hn
      simpa [hC, heq] using hhead
    have hP : ∀ x ∈ P, x ≤ 2 * (b - 1) := by
      intro x hx
      exact h.boundC x (by rw [hC]; exact List.mem_append_left _ hx)
    have ht : (norm b P (e1 b E.B)).2 ≤ 1 :=
      norm_carry_le_one b (by have := h.base; omega) P (e1 b E.B) hP h.e1_le
    have h' : Hyp b E.B (P ++ [c]) := by simpa [hC] using h
    have hg' : gam b E.B (P ++ [c]) = 0 := by simpa [hC] using hg
    have hh' : (nextC b E.B (P ++ [c])).head? = some (b - 1) := by
      simpa [hC] using hh
    obtain ⟨he0, hc0⟩ | ⟨he1, hc1⟩ :=
      nooverflow_head_thresholds h' hhead hc hg' hh'
    · exact ⟨P, c, hC, by simpa [hC] using hhead,
        Or.inl ⟨he0, by omega, by omega⟩⟩
    · exact ⟨P, c, hC, by simpa [hC] using hhead,
        Or.inr ⟨he1, by omega, by omega⟩⟩

/-- In base ten, a symmetric positive-trim source uses head/last 14 and last
incoming carry 1 when e1=0, or head/last 4 and carry 0 when e1=1. -/
theorem decimal_positive_center_trim_site {E : Edge}
    (he : edgeOK 10 E = true) (hs : E.C.reverse = E.C)
    (hn : E.C.head? ≠ some 9) (hv : 0 < E.v) :
    (∃ P, E.C = P ++ [14] ∧ E.C.head? = some 14 ∧ e1 10 E.B = 0 ∧
      (norm 10 P (e1 10 E.B)).2 = 1) ∨
    (∃ P, E.C = P ++ [4] ∧ E.C.head? = some 4 ∧ e1 10 E.B = 1 ∧
      (norm 10 P (e1 10 E.B)).2 = 0) := by
  obtain ⟨P, c, hC, hh, ht⟩ := symmetric_positive_trim_site he hs hn hv
  rcases ht with ⟨he0, hc, ht⟩ | ⟨he1, hc, ht⟩
  · change c = 14 at hc
    change (norm 10 P (e1 10 E.B)).2 = 1 at ht
    exact Or.inl ⟨P, by simpa [hc] using hC, by simpa [hc] using hh, he0, ht⟩
  · change c = 4 at hc
    change (norm 10 P (e1 10 E.B)).2 = 0 at ht
    exact Or.inr ⟨P, by simpa [hc] using hC, by simpa [hc] using hh, he1, ht⟩

end Agent114.NeutralCenterTrimSites

#print axioms Agent114.NeutralCenterTrimSites.head_normal_overflow_trim_zero
#print axioms Agent114.NeutralCenterTrimSites.head_normal_positive_trim_nonoverflow
#print axioms Agent114.NeutralCenterTrimSites.symmetric_core_head_ne
#print axioms Agent114.NeutralCenterTrimSites.symmetric_positive_trim_site
#print axioms Agent114.NeutralCenterTrimSites.decimal_positive_center_trim_site
