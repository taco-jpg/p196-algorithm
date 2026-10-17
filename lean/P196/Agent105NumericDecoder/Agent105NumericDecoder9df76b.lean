import P196.Agent105NumericDecoder.Agent105DecoderTarget9df76b
import P196.Agent105NumericDecoder.Agent105DecoderScan9df76b

/-!
Executable complete numerical-target inversion at a prescribed source width.
Agent #105 / session 9df76b. The canonical target supplies the decimal-digit
domain used by the scan specification; a stripped overflow payload itself
need not be a canonical numeral.
-/

namespace Agent105NumericDecoder9df76b

open DecimalDigits FoldedDecimal Lychrel196 Agent101
open Agent105DecoderTarget9df76b Agent105DecoderScan9df76b

/-- Decode the only physically possible carry at the prescribed source
width, checking the additional leading digit in the overflow branch. -/
def decodeNumerical (e : Nat → Nat) (W L : Nat) : Option (List Nat) :=
  if W = L then decodeAtWidth e L 0
  else if W = L + 1 ∧ e L = 1 then decodeAtWidth e L 1
  else none

theorem decodeNumerical_eq_some_iff_payload
    (Y : Nat) (e : Nat → Nat) (W L : Nat) (qs : List Nat)
    (htarget : Canonical Y e W) :
    decodeNumerical e W L = some qs ↔
      ∃ h, WidthChoice e W L h ∧ qs.length = L ∧
        PayloadSpec e L h (digitFn qs) := by
  unfold decodeNumerical
  by_cases hzero : W = L
  · rw [if_pos hzero]
    have he : ∀ i, i < L → e i ≤ 9 := by
      intro i hi
      exact htarget.2.1 i (by omega)
    constructor
    · intro hdec
      have hp := (decodeAtWidth_eq_some_iff e L 0 qs he).mp hdec
      exact ⟨0, Or.inl ⟨hzero, rfl⟩, hp⟩
    · rintro ⟨h, hw, hlen, hp⟩
      have hh : h = 0 := by
        rcases hw with ⟨_, hz⟩ | ⟨hW, _, _⟩
        · exact hz
        · omega
      subst h
      exact (decodeAtWidth_eq_some_iff e L 0 qs he).mpr ⟨hlen, hp⟩
  · rw [if_neg hzero]
    by_cases hover : W = L + 1 ∧ e L = 1
    · rw [if_pos hover]
      have he : ∀ i, i < L → e i ≤ 9 := by
        intro i hi
        exact htarget.2.1 i (by omega)
      constructor
      · intro hdec
        have hp := (decodeAtWidth_eq_some_iff e L 1 qs he).mp hdec
        exact ⟨1, Or.inr ⟨hover.1, rfl, hover.2⟩, hp⟩
      · rintro ⟨h, hw, hlen, hp⟩
        have hh : h = 1 := by
          rcases hw with ⟨hW, _⟩ | ⟨_, hh, _⟩
          · exact False.elim (hzero hW)
          · exact hh
        subst h
        exact (decodeAtWidth_eq_some_iff e L 1 qs he).mpr ⟨hlen, hp⟩
    · rw [if_neg hover]
      constructor
      · intro h
        cases h
      · rintro ⟨h, hw, _, _⟩
        rcases hw with ⟨hW, _⟩ | ⟨hW, _, ht⟩
        · exact False.elim (hzero hW)
        · exact False.elim (hover ⟨hW, ht⟩)

/-- Exact returned-profile semantics, including a positive ordinary
integer witness and every finite pair coefficient. -/
theorem decodeNumerical_eq_some_iff
    (Y : Nat) (e : Nat → Nat) (W L : Nat) (qs : List Nat)
    (htarget : Canonical Y e W) :
    decodeNumerical e W L = some qs ↔
      qs.length = L ∧ ∃ n d, 0 < n ∧ Canonical n d L ∧
        (∀ i, i < L → columnSum d L i = digitFn qs i) ∧ step n = Y := by
  rw [decodeNumerical_eq_some_iff_payload Y e W L qs htarget]
  constructor
  · rintro ⟨h, hw, hlen, hp⟩
    exact ⟨hlen, realize_payload Y e W L h (digitFn qs) htarget hw hp⟩
  · rintro ⟨hlen, n, d, _, hn, hr, hs⟩
    obtain ⟨h, hw, hp⟩ := canonical_predecessor_payload Y n e d W L htarget hn hs
    exact ⟨h, hw, hlen, payload_congr e L h _ _ hp hr⟩

/-- The executable fixed-width acceptance test is equivalent to the
existence of an actual positive canonical reverse-add predecessor. -/
theorem decodeNumerical_isSome_iff
    (Y : Nat) (e : Nat → Nat) (W L : Nat) (htarget : Canonical Y e W) :
    (decodeNumerical e W L).isSome = true ↔
      ∃ n d, 0 < n ∧ Canonical n d L ∧ step n = Y := by
  rw [positive_predecessor_iff_finite_payload Y e W L htarget]
  constructor
  · intro hsuccess
    cases hd : decodeNumerical e W L with
    | none => simp only [hd, Option.isSome_none] at hsuccess; cases hsuccess
    | some qs =>
      obtain ⟨h, hw, hlen, hp⟩ :=
        (decodeNumerical_eq_some_iff_payload Y e W L qs htarget).mp hd
      exact ⟨h, qs, hw, hlen, hp⟩
  · rintro ⟨h, qs, hw, hlen, hp⟩
    rw [(decodeNumerical_eq_some_iff_payload Y e W L qs htarget).mpr
      ⟨h, hw, hlen, hp⟩]
    rfl

#print axioms decodeNumerical_eq_some_iff_payload
#print axioms decodeNumerical_eq_some_iff
#print axioms decodeNumerical_isSome_iff

end Agent105NumericDecoder9df76b
