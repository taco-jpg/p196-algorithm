import Agent105NumericDecoder9df76b
import Agent105WordFiber9df76b

/-!
Agent #105 / session 9df76b: transport an exact decoded numerical profile
into the finite list of ordinary predecessors at the prescribed source width.
-/

namespace Agent105DecodedFiber9df76b

open DecimalDigits FoldedDecimal Lychrel196 Agent101
open Agent105NumericDecoder9df76b
open Agent105WordFiber9df76b

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
  · apply List.ext_getElem (by simp)
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

/-- All ordinary predecessors at the prescribed source width, computed
by the complete numerical decoder and finite canonical digit splitting. -/
def decodedFiber (e : Nat → Nat) (W L : Nat) : List Nat :=
  match decodeNumerical e W L with
  | some qs => wordFiber qs
  | none => []

/-- Membership has the original numeric step semantics at exactly the
prescribed source width, without a digit-function witness in the result. -/
theorem mem_decodedFiber_decimalWidth
    (Y : Nat) (e : Nat → Nat) (W L n : Nat)
    (htarget : Canonical Y e W) :
    n ∈ decodedFiber e W L ↔ decimalWidth n L ∧ step n = Y := by
  unfold decodedFiber
  cases hdec : decodeNumerical e W L with
  | none =>
    constructor
    · intro hmem
      cases hmem
    · rintro ⟨hw, hs⟩
      obtain ⟨d, hc⟩ := (decimalWidth_iff_canonical n L).mp hw
      have hn : 0 < n := by
        rw [← hc.2.2.2]
        exact value_positive d L hc.1 hc.2.2.1
      have hsome := (decodeNumerical_isSome_iff Y e W L htarget).mpr
        ⟨n, d, hn, hc, hs⟩
      rw [hdec] at hsome
      cases hsome
  | some qs =>
    obtain ⟨hlen, hrev, hb, hv⟩ :=
      decodeNumerical_word_spec Y e W L qs htarget hdec
    simpa only [hlen, hv] using mem_wordFiber qs n hrev hb

/-- Equivalent membership format exposing a positive ordinary integer
and its canonical digits, for direct composition with actual width lemmas. -/
theorem mem_decodedFiber
    (Y : Nat) (e : Nat → Nat) (W L n : Nat)
    (htarget : Canonical Y e W) :
    n ∈ decodedFiber e W L ↔
      0 < n ∧ ∃ d, Canonical n d L ∧ step n = Y := by
  rw [mem_decodedFiber_decimalWidth Y e W L n htarget]
  constructor
  · rintro ⟨hw, hs⟩
    obtain ⟨d, hc⟩ := (decimalWidth_iff_canonical n L).mp hw
    refine ⟨?_, d, hc, hs⟩
    rw [← hc.2.2.2]
    exact value_positive d L hc.1 hc.2.2.1
  · rintro ⟨_, d, hc, hs⟩
    exact ⟨canonical_decimalWidth n d L hc, hs⟩

/-- A decoded fiber never lists an ordinary integer twice. No validity
hypothesis on the target digits or widths is needed for this property. -/
theorem decodedFiber_nodup (e : Nat → Nat) (W L : Nat) :
    (decodedFiber e W L).Nodup := by
  unfold decodedFiber
  cases decodeNumerical e W L with
  | none => exact List.nodup_nil
  | some qs => exact wordFiber_nodup qs

#print axioms decodeNumerical_word_spec
#print axioms mem_decodedFiber_decimalWidth
#print axioms mem_decodedFiber
#print axioms decodedFiber_nodup

end Agent105DecodedFiber9df76b
