import P196.CompleteFiberParity.Integration

/-!
# Numerical uniqueness of accepted odd coefficient profiles

Agent #6: the existing realization and complete decoder transport finite
admissible words to ordinary decimal targets. The cross-width divisibility
theorem makes numerical evaluation injective on all odd profiles, including
profiles of different source widths.
-/

set_option autoImplicit false

namespace OddPredecessorTargetCensus

open DecimalDigits FoldedDecimal Lychrel196 Agent101
open Agent105WordFiber9df76b Agent105NumericDecoder9df76b
open Agent105DecodedFiber9df76b Agent105WidthSupport9df76b
open CompleteFiberParity

/-- An admissible coefficient word evaluates to a positive canonical target
whose exact width is its source width plus its actual terminal carry. -/
theorem admissible_natValue_canonical (qs : List Nat)
    (ha : Admissible qs.length (digitFn qs)) :
    ∃ e, Canonical (natValue qs) e
      (qs.length + carry (digitFn qs) qs.length) := by
  obtain ⟨n, d, _, hn, hr⟩ := valid_word_realizable (digitFn qs) qs.length
    ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2
  have hv : step n = natValue qs := step_eq_word_value n d _ _ hn hr
  have hc := carry_congr_upto (columnSum d qs.length) (digitFn qs) qs.length
    hr qs.length (Nat.le_refl _)
  obtain ⟨e, he⟩ := canonical_step_exists hn
  exact ⟨e, by simpa only [hv, hc] using he⟩

/-- Every admissible finite coefficient word is recovered by the existing
complete decoder from its numerical value at its prescribed source width. -/
theorem admissible_natValue_decode (Y : Nat) (e : Nat → Nat) (W L : Nat)
    (qs : List Nat) (hY : Canonical Y e W) (hlen : qs.length = L)
    (ha : Admissible L (digitFn qs)) (hv : natValue qs = Y) :
    decodeNumerical e W L = some qs := by
  obtain ⟨n, d, hnpos, hn, hr⟩ := valid_word_realizable (digitFn qs) L
    ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2
  apply (decodeNumerical_eq_some_iff Y e W L qs hY).mpr
  refine ⟨hlen, n, d, hnpos, hn, hr, ?_⟩
  have hs := step_eq_word_value n d (digitFn qs) L hn hr
  simpa only [natValue, hlen] using hs.trans (by simpa only [natValue, hlen] using hv)

/-- A successful decode retains admissibility, numerical value, and the
exact terminal carry determined by the target and source widths. -/
theorem decode_admissible_carry (Y : Nat) (e : Nat → Nat) (W L : Nat)
    (qs : List Nat) (hY : Canonical Y e W)
    (hdec : decodeNumerical e W L = some qs) :
    qs.length = L ∧ Admissible L (digitFn qs) ∧ natValue qs = Y ∧
      W = L + carry (digitFn qs) L := by
  obtain ⟨hlen, n, d, _, hn, hr, hs⟩ :=
    (decodeNumerical_eq_some_iff Y e W L qs hY).mp hdec
  have ha := NormalizationBridge.admissible_congr L (columnSum d L)
    (digitFn qs) (NormalizationBridge.canonical_admissible n d L hn) hr
  have hv := (decodeNumerical_word_spec Y e W L qs hY hdec).2.2.2
  have htarget : Canonical (step n) e W := by simpa only [hs] using hY
  have hw := canonical_step_width hn htarget
  have hc := carry_congr_upto (columnSum d L) (digitFn qs) L hr L (Nat.le_refl _)
  exact ⟨hlen, ha, hv, by simpa only [hc] using hw⟩

private theorem decoded_odd_of_profile (e : Nat → Nat) (W L : Nat)
    (qs : List Nat) (hdec : decodeNumerical e W L = some qs)
    (ho : oddProfile (half qs) (center qs) = true) :
    (decodedFiber e W L).length % 2 = 1 := by
  rw [decodedFiber_mod_two]
  simp only [oddDecoded, hdec, ho, if_true]

/-- Numerical evaluation is injective on admissible odd-multiplicity
profiles, without assuming their source widths agree. -/
theorem odd_admissible_natValue_injective (qs rs : List Nat)
    (hq : Admissible qs.length (digitFn qs))
    (hr : Admissible rs.length (digitFn rs))
    (hoq : oddProfile (half qs) (center qs) = true)
    (hor : oddProfile (half rs) (center rs) = true)
    (hv : natValue qs = natValue rs) : qs = rs := by
  obtain ⟨e, hY⟩ := admissible_natValue_canonical qs hq
  let W := qs.length + carry (digitFn qs) qs.length
  have hdq := admissible_natValue_decode (natValue qs) e W qs.length qs hY rfl hq rfl
  have hdr := admissible_natValue_decode (natValue qs) e W rs.length rs hY rfl hr hv.symm
  have hlq := decoded_odd_of_profile e W qs.length qs hdq hoq
  have hlr := decoded_odd_of_profile e W rs.length rs hdr hor
  have hlen : qs.length = rs.length := by
    by_cases heq : qs.length = rs.length
    · exact heq
    · rcases Nat.lt_or_gt_of_ne heq with hlt | hgt
      · exact False.elim (not_both_width_fibers_odd
          (natValue qs) e W qs.length rs.length hY hlt ⟨hlq, hlr⟩)
      · exact False.elim (not_both_width_fibers_odd
          (natValue qs) e W rs.length qs.length hY hgt ⟨hlr, hlq⟩)
  rw [hlen] at hdq
  exact Option.some.inj (hdq.symm.trans hdr)

end OddPredecessorTargetCensus

#print axioms OddPredecessorTargetCensus.admissible_natValue_canonical
#print axioms OddPredecessorTargetCensus.admissible_natValue_decode
#print axioms OddPredecessorTargetCensus.decode_admissible_carry
#print axioms OddPredecessorTargetCensus.odd_admissible_natValue_injective
