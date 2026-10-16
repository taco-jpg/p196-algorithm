import Agent105WidthSupport9df76b

/-!
Exact ordinary-integer constraints on different-width reverse-add collisions.
Agent #105, session 9df76b. Original written source: persist_inverse_notes.txt
sections 1-2, Git blob ecd101823b261fdac15d185fea963d9c9f16c601.
These statements concern a single numerical step, not the pair-word next map.
-/

namespace Agent105CrossWidth9df76b

open Lychrel196 DecimalDigits FoldedDecimal Agent105WidthSupport9df76b

/-- Different input widths force outer pair sums eleven and one, respectively. -/
theorem cross_width_outer
    {n m L K : Nat} {d e : Nat → Nat}
    (hn : Canonical n d L) (hm : Canonical m e K)
    (hLK : L < K) (hstep : step n = step m) :
    columnSum d L 0 = 11 ∧ columnSum e K 0 = 1 := by
  have hL := hn.1
  obtain ⟨hK, hcn, hcm⟩ := cross_width_carries hn hm hLK hstep
  subst K
  let q := columnSum d L
  let r := columnSum e (L + 1)
  have hnout := canonical_next_overflow n d L hn hcn
  have hmout := canonical_next_no_overflow m e (L + 1) hm hcm
  have heq : ∀ i, i < L + 1 → extended q L i = output r i := by
    apply value_injective _ _ (L + 1) hnout.2.1 hmout.2.1
    exact hnout.2.2.2.trans (hstep.trans hmout.2.2.2.symm)
  have hlead : output r L = 1 := by
    have h := heq L (by omega)
    simpa [extended, q, hcn] using h.symm
  have hrpos : 0 < r L := by
    have h := hm.2.2.1
    simp only [Nat.add_sub_cancel] at h
    dsimp [r, columnSum]
    omega
  have hrcol := column_equation r L
  have hrend : carry r (L + 1) = 0 := hcm
  have hrL : r L = 1 := by omega
  have hrsym := columnSum_symmetric e (L + 1) 0 (by omega)
  have hr0 : r 0 = 1 := by
    simpa [r] using hrsym.trans hrL
  have hunitr : output r 0 = 1 := by simp [output, carry, hr0]
  have hunitq : output q 0 = 1 := by
    have h := heq 0 (by omega)
    simpa [extended, hn.1, hunitr] using h
  have hq0b : q 0 ≤ 18 := columnSum_bounded d L hn.2.1 0 hn.1
  have hqsym := columnSum_symmetric d L 0 hn.1
  have hcprev : carry q (L - 1) ≤ 1 :=
    carry_bounded q L (columnSum_bounded d L hn.2.1) (L - 1) (by omega)
  have hlast := column_equation q (L - 1)
  have hlastindex : L - 1 + 1 = L := by omega
  rw [hlastindex] at hlast
  have hqend : carry q L = 1 := hcn
  have hqfirst : q 0 % 10 = 1 := by simpa [output, carry] using hunitq
  have hq0 : q 0 = 11 := by
    change q 0 = q (L - 1 - 0) at hqsym
    simp only [Nat.sub_zero] at hqsym
    omega
  exact ⟨hq0, hr0⟩

/-- Width-one inputs cannot participate as the shorter source. -/
theorem cross_width_short_length
    {n m L K : Nat} {d e : Nat → Nat}
    (hn : Canonical n d L) (hm : Canonical m e K)
    (hLK : L < K) (hstep : step n = step m) : 2 ≤ L := by
  have hq := (cross_width_outer hn hm hLK hstep).1
  by_cases h : 2 ≤ L
  · exact h
  · have hpos := hn.1
    have hL : L = 1 := by omega
    subst L
    simp only [columnSum, reflected, Nat.sub_self, Nat.sub_zero] at hq
    omega

/-- At least one of two adjacent input widths is even. -/
theorem cross_width_output_dvd_eleven
    {n m L K : Nat} {d e : Nat → Nat}
    (hn : Canonical n d L) (hm : Canonical m e K)
    (hLK : L < K) (hstep : step n = step m) : 11 ∣ step n := by
  have hK := (cross_width_carries hn hm hLK hstep).1
  by_cases hL : L % 2 = 0
  · exact AstraModular.even_width_step_dvd11 n d L hn hL
  · have hKeven : K % 2 = 0 := by omega
    rw [hstep]
    exact AstraModular.even_width_step_dvd11 m e K hm hKeven

/-- Any canonical representation of the common output has leading and units
digits one. The representation's width is the longer input width. -/
theorem cross_width_target_digits
    {n m L K W : Nat} {d e f : Nat → Nat}
    (hn : Canonical n d L) (hm : Canonical m e K)
    (hLK : L < K) (hstep : step n = step m)
    (hf : Canonical (step n) f W) :
    W = K ∧ f 0 = 1 ∧ f (W - 1) = 1 := by
  obtain ⟨hK, hcn, _⟩ := cross_width_carries hn hm hLK hstep
  have hq := (cross_width_outer hn hm hLK hstep).1
  have hnout := canonical_next_overflow n d L hn hcn
  have hW := canonical_width_unique hf hnout
  subst W
  have heq := canonical_digits_unique hf hnout
  refine ⟨hK.symm, ?_, ?_⟩
  · have h := heq 0 (by omega)
    simpa [extended, hn.1, output, carry, hq] using h
  · have h := heq L (by omega)
    simpa [extended, hcn] using h

/-- A numerical step value confines all positive source widths to adjacent
integers. A difference of two or more widths is impossible. -/
theorem equal_step_widths_close
    {n m L K : Nat} {d e : Nat → Nat}
    (hn : Canonical n d L) (hm : Canonical m e K)
    (hstep : step n = step m) : L ≤ K + 1 ∧ K ≤ L + 1 := by
  rcases Nat.lt_trichotomy L K with hlt | heq | hgt
  · have h := (cross_width_carries hn hm hlt hstep).1
    omega
  · omega
  · have h := (cross_width_carries hm hn hgt hstep.symm).1
    omega

/-- Among any three canonical positive digit lists giving the same numerical
output, two have exactly the same finite pair-sum list. This is the all-width
at-most-two-profile statement for the numerical map, not for `stepWord`. -/
theorem three_preimages_share_pair_profile
    (a b c : List Nat)
    (ha : Agent101.canonicalDigits a)
    (hb : Agent101.canonicalDigits b)
    (hc : Agent101.canonicalDigits c)
    (hab : step (Agent101.natValue a) = step (Agent101.natValue b))
    (hac : step (Agent101.natValue a) = step (Agent101.natValue c)) :
    Agent101.digitPairSums a = Agent101.digitPairSums b ∨
    Agent101.digitPairSums a = Agent101.digitPairSums c ∨
    Agent101.digitPairSums b = Agent101.digitPairSums c := by
  have hca := (Agent101.canonicalDigits_iff a).mp ha
  have hcb := (Agent101.canonicalDigits_iff b).mp hb
  have hcc := (Agent101.canonicalDigits_iff c).mp hc
  have habw := equal_step_widths_close hca hcb hab
  have hacw := equal_step_widths_close hca hcc hac
  have hbc := hab.symm.trans hac
  have hbcw := equal_step_widths_close hcb hcc hbc
  by_cases hlab : a.length = b.length
  · exact Or.inl ((Agent101.same_width_step_eq_iff_digitPairSums a b ha hb hlab).mp hab)
  by_cases hlac : a.length = c.length
  · exact Or.inr (Or.inl
      ((Agent101.same_width_step_eq_iff_digitPairSums a c ha hc hlac).mp hac))
  have hlbc : b.length = c.length := by omega
  exact Or.inr (Or.inr
    ((Agent101.same_width_step_eq_iff_digitPairSums b c hb hc hlbc).mp hbc))

#print axioms cross_width_outer
#print axioms cross_width_short_length
#print axioms cross_width_output_dvd_eleven
#print axioms cross_width_target_digits
#print axioms equal_step_widths_close
#print axioms three_preimages_share_pair_profile

end Agent105CrossWidth9df76b
