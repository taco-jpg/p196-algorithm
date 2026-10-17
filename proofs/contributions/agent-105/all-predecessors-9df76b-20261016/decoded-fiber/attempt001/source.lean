import Agent105NumericDecoder9df76b

/-!
Agent #105 / session 9df76b: transport an exact decoded numerical profile
into the finite list of ordinary predecessors at the prescribed source width.
-/

namespace Agent105DecodedFiber9df76b

open DecimalDigits FoldedDecimal Lychrel196 Agent101
open Agent105NumericDecoder9df76b

/-- A successful canonical-target decode is a finite symmetric bounded
coefficient word whose ordinary positional value is exactly the target. -/
theorem decodeNumerical_word_spec
    (Y : Nat) (e : Nat → Nat) (W L : Nat) (qs : List Nat)
    (htarget : Canonical Y e W)
    (hdec : decodeNumerical e W L = some qs) :
    qs.length = L ∧ qs.reverse = qs ∧
      (∀ s ∈ qs, s ≤ 18) ∧ natValue qs = Y := by
  obtain ⟨hlen, n, d, _, hc, hprofile, hstep⟩ :=
    (decodeNumerical_eq_some_iff Y e W L qs htarget).mp hdec
  refine ⟨hlen, ?_, ?_, ?_⟩
  · apply List.ext_getElem (List.length_reverse qs)
    intro i hi hj
    have hs := columnSum_symmetric d L i (by omega)
    rw [hprofile i (by omega), hprofile (L - 1 - i) (by omega)] at hs
    rw [← hlen] at hs
    rw [digitFn_getElem qs i hj,
      digitFn_getElem qs (qs.length - 1 - i) (by omega)] at hs
    simpa only [List.getElem_reverse] using hs.symm
  · intro s hs
    obtain ⟨i, hi, rfl⟩ := List.mem_iff_getElem.mp hs
    have hb := columnSum_bounded d L hc.2.1 i (by omega)
    rw [hprofile i (by omega), digitFn_getElem qs i hi] at hb
    exact hb
  · have hv : step n = natValue qs := by
      unfold natValue
      rw [hlen]
      exact step_eq_word_value n d (digitFn qs) L hc hprofile
    exact hv.symm.trans hstep

#print axioms decodeNumerical_word_spec

end Agent105DecodedFiber9df76b
