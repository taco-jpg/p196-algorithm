import Agent105WidthSupport9df76b

/-!
Agent #105 / session 9df76b. Exact ordinary-number target semantics used by
the complete numerical inverse decoder. These interfaces reuse the original
canonical realization and actual carry semantics; they impose no canonicality
condition on the low-width payload after an overflow digit is removed.
-/

namespace Agent105DecoderTarget9df76b

open DecimalDigits FoldedDecimal Lychrel196 Agent105WidthSupport9df76b

def PayloadSpec (e : Nat → Nat) (L h : Nat) (q : Nat → Nat) : Prop :=
  Admissible L q ∧ (∀ i, i < L → output q i = e i) ∧ carry q L = h

def WidthChoice (e : Nat → Nat) (W L h : Nat) : Prop :=
  (W = L ∧ h = 0) ∨ (W = L + 1 ∧ h = 1 ∧ e L = 1)

theorem payload_congr (e : Nat → Nat) (L h : Nat) (q r : Nat → Nat)
    (hp : PayloadSpec e L h q) (he : ∀ i, i < L → q i = r i) :
    PayloadSpec e L h r := by
  refine ⟨admissible_congr L q r hp.1 he, ?_, ?_⟩
  · intro i hi
    exact (output_congr_upto q r L he i hi).symm.trans (hp.2.1 i hi)
  · exact (carry_congr_upto q r L he L (Nat.le_refl L)).symm.trans hp.2.2

/-- An accepted physical payload gives an actual positive predecessor,
with every in-range pair coefficient retained in the witness. -/
theorem realize_payload (Y : Nat) (e : Nat → Nat) (W L h : Nat)
    (q : Nat → Nat) (htarget : Canonical Y e W)
    (hw : WidthChoice e W L h) (hp : PayloadSpec e L h q) :
    ∃ n d, 0 < n ∧ Canonical n d L ∧
      (∀ i, i < L → columnSum d L i = q i) ∧ step n = Y := by
  obtain ⟨n, d, hn, hc, hr⟩ := valid_word_realizable q L
    hp.1.1 hp.1.2.1 hp.1.2.2.1 hp.1.2.2.2.1 hp.1.2.2.2.2
  refine ⟨n, d, hn, hc, hr, ?_⟩
  rw [step_eq_word_value n d q L hc hr, ← value_output]
  rw [value_congr (output q) e L hp.2.1, hp.2.2]
  rcases hw with ⟨hW, hz⟩ | ⟨hW, ho, htop⟩
  · rw [hz, Nat.zero_mul, Nat.add_zero]
    simpa only [hW] using htarget.2.2.2
  · rw [ho, Nat.one_mul]
    simpa only [hW, value, htop, Nat.one_mul] using htarget.2.2.2

/-- Every actual predecessor supplies exactly the matching physical
payload and the correct no-overflow/overflow width branch. -/
theorem canonical_predecessor_payload
    (Y n : Nat) (e d : Nat → Nat) (W L : Nat)
    (htarget : Canonical Y e W) (hn : Canonical n d L)
    (hstep : step n = Y) :
    ∃ h, WidthChoice e W L h ∧ PayloadSpec e L h (columnSum d L) := by
  have hs : Canonical (step n) e W := by simpa only [hstep] using htarget
  rcases step_width_cases hn hs with ⟨hW, hc⟩ | ⟨hW, hc⟩
  · have he : Canonical (step n) e L := by simpa only [hW] using hs
    have heq := canonical_digits_unique (canonical_next_no_overflow n d L hn hc) he
    exact ⟨0, Or.inl ⟨hW, rfl⟩, canonical_admissible n d L hn, heq, hc⟩
  · have he : Canonical (step n) e (L + 1) := by simpa only [hW] using hs
    have heq := canonical_digits_unique (canonical_next_overflow n d L hn hc) he
    have htop : e L = 1 := by
      have ht := heq L (by omega)
      simpa only [extended, Nat.lt_irrefl, if_false, hc] using ht.symm
    refine ⟨1, Or.inr ⟨hW, rfl, htop⟩, canonical_admissible n d L hn, ?_, hc⟩
    intro i hi
    simpa only [extended, hi, if_true] using heq i (by omega)

/-- The exact fixed-width numerical existence problem is equivalent to
a finite admissible physical payload. List conversion preserves only the
actual finite coefficients and places no conditions on irrelevant tails. -/
theorem positive_predecessor_iff_finite_payload
    (Y : Nat) (e : Nat → Nat) (W L : Nat) (htarget : Canonical Y e W) :
    (∃ n d, 0 < n ∧ Canonical n d L ∧ step n = Y) ↔
      ∃ h qs, WidthChoice e W L h ∧ qs.length = L ∧
        PayloadSpec e L h (Agent101.digitFn qs) := by
  constructor
  · rintro ⟨n, d, _, hn, hstep⟩
    obtain ⟨h, hw, hp⟩ := canonical_predecessor_payload Y n e d W L htarget hn hstep
    let qs := List.ofFn (fun i : Fin L => columnSum d L i)
    have hlen : qs.length = L := List.length_ofFn
    have heq : ∀ i, i < L → columnSum d L i = Agent101.digitFn qs i := by
      intro i hi
      simp [Agent101.digitFn, qs, List.getElem?_ofFn, hi]
    exact ⟨h, qs, hw, hlen, payload_congr e L h _ _ hp heq⟩
  · rintro ⟨h, qs, hw, _, hp⟩
    obtain ⟨n, d, hn, hc, _, hs⟩ := realize_payload Y e W L h
      (Agent101.digitFn qs) htarget hw hp
    exact ⟨n, d, hn, hc, hs⟩

#print axioms payload_congr
#print axioms realize_payload
#print axioms canonical_predecessor_payload
#print axioms positive_predecessor_iff_finite_payload

end Agent105DecoderTarget9df76b
