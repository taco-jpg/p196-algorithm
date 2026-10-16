import LychrelDigitSums

/-!
Three zero pair-sum columns following a positive outer column can occur
only in the first five states of an actual decimal reverse-and-add orbit.
The theorem concerns actual carries and actual changing decimal widths.
It does not imply decimal Lychrel existence or termination of 196.
-/

namespace ZeroExterior

open DecimalDigits FoldedDecimal OverflowCarryNormalization

/-- The displayed four columns are inside the finite word. -/
def ThreeZero (L : Nat) (q : Nat → Nat) : Prop :=
  4 ≤ L ∧ q 1 = 0 ∧ q 2 = 0 ∧ q 3 = 0

theorem threeZero_min_width (L : Nat) (q : Nat → Nat)
    (ha : Admissible L q) (hz : ThreeZero L q) : 5 ≤ L := by
  have hL := hz.1
  have ho := ha.2.1
  have hs := ha.2.2.2.1 0 ha.1
  have hthree := hz.2.2.2
  by_cases he : L = 4
  · subst L
    simp only [Nat.sub_zero, Nat.reduceSub] at hs
    omega
  · omega

/-- Finite local arithmetic: overflow cannot emit three consecutive zeros. -/
theorem overflow_three_zeros_impossible (q a c l u : Nat → Nat)
    (hq : ∀ i, i < 4 → q i ≤ 18)
    (ha : ∀ i, i ≤ 4 → a i ≤ 1)
    (hc : ∀ i, i ≤ 4 → c i ≤ 1)
    (hl : ∀ i, i < 4 → l i ≤ 9)
    (hu : ∀ i, i < 4 → u i ≤ 9)
    (hzero : a 0 = 0) (hover : c 0 = 1)
    (hstep : ∀ i, i < 4 → l i + 10 * a (i + 1) = q i + a i ∧
      u i + 10 * c i = q i + c (i + 1))
    (hz1 : l 1 + u 0 = 0) (hz2 : l 2 + u 1 = 0)
    (hz3 : l 3 + u 2 = 0) : False := by
  have hq0 := hq 0 (by decide)
  have hq1 := hq 1 (by decide)
  have hq2 := hq 2 (by decide)
  have hq3 := hq 3 (by decide)
  have ha1 := ha 1 (by decide)
  have ha2 := ha 2 (by decide)
  have ha3 := ha 3 (by decide)
  have ha4 := ha 4 (by decide)
  have hc1 := hc 1 (by decide)
  have hc2 := hc 2 (by decide)
  have hc3 := hc 3 (by decide)
  have hl0 := hl 0 (by decide)
  have hu0 := hu 0 (by decide)
  have h0 := hstep 0 (by decide)
  have h1 := hstep 1 (by decide)
  have h2 := hstep 2 (by decide)
  have h3 := hstep 3 (by decide)
  simp only [Nat.reduceAdd] at h0 h1 h2 h3
  have hfront : (q 0 = 9 ∧ c 1 = 1 ∧ a 1 = 0) ∨
      (q 0 = 10 ∧ c 1 = 0 ∧ a 1 = 1) := by omega
  rcases hfront with ⟨hqzero, hcone, haone⟩ | ⟨hqzero, hcone, haone⟩
  · have hqone : q 1 = 10 := by omega
    have hatwo : a 2 = 1 := by omega
    have hqtwo : q 2 = 9 := by omega
    have hctwo : c 2 = 0 := by omega
    have hcthree : c 3 = 0 := by omega
    omega
  · have hqone : q 1 = 9 := by omega
    have hctwo : c 2 = 0 := by omega
    omega

/-- Without overflow, those three zeros force the same predecessor zeros. -/
theorem no_overflow_three_zeros_rigidity (q a c l u : Nat → Nat)
    (hq : ∀ i, i < 4 → q i ≤ 18)
    (ha : ∀ i, i ≤ 4 → a i ≤ 1)
    (hc : ∀ i, i ≤ 4 → c i ≤ 1)
    (hl : ∀ i, i < 4 → l i ≤ 9)
    (hu : ∀ i, i < 4 → u i ≤ 9)
    (hzero : a 0 = 0) (hover : c 0 = 0)
    (hstep : ∀ i, i < 4 → l i + 10 * a (i + 1) = q i + a i ∧
      u i + 10 * c i = q i + c (i + 1))
    (hz1 : l 1 + u 1 = 0) (hz2 : l 2 + u 2 = 0)
    (hz3 : l 3 + u 3 = 0) :
    q 1 = 0 ∧ q 2 = 0 ∧ q 3 = 0 ∧ c 1 = 0 ∧ q 0 ≤ 9 := by
  have hq0 := hq 0 (by decide)
  have hq1 := hq 1 (by decide)
  have hq2 := hq 2 (by decide)
  have hq3 := hq 3 (by decide)
  have ha1 := ha 1 (by decide)
  have ha2 := ha 2 (by decide)
  have ha3 := ha 3 (by decide)
  have ha4 := ha 4 (by decide)
  have hc1 := hc 1 (by decide)
  have hc2 := hc 2 (by decide)
  have hc3 := hc 3 (by decide)
  have hc4 := hc 4 (by decide)
  have hl0 := hl 0 (by decide)
  have hu0 := hu 0 (by decide)
  have h0 := hstep 0 (by decide)
  have h1 := hstep 1 (by decide)
  have h2 := hstep 2 (by decide)
  have h3 := hstep 3 (by decide)
  simp only [Nat.reduceAdd] at h0 h1 h2 h3
  have hfront : q 0 ≤ 9 ∧ a 1 = 0 := by omega
  have hqone : q 1 = 0 := by
    have hcase : q 1 = 0 ∨ q 1 = 10 := by omega
    rcases hcase with hz | ht
    · exact hz
    · have hatwo : a 2 = 1 := by omega
      have hqtwo : q 2 = 9 := by omega
      have hctwo : c 2 = 0 := by omega
      have hcthree : c 3 = 1 := by omega
      omega
  have hcone : c 1 = 0 := by omega
  have hatwo : a 2 = 0 := by omega
  have hctwo : c 2 = 0 := by omega
  have hqtwo : q 2 = 0 := by omega
  have hathree : a 3 = 0 := by omega
  have hcthree : c 3 = 0 := by omega
  have hqthree : q 3 = 0 := by omega
  exact ⟨hqone, hqtwo, hqthree, hcone, hfront.1⟩

/-- The actual successor prefix forces no overflow, the same predecessor
zeros, and exact doubling of the positive outer coefficient. -/
theorem next_threeZero_predecessor (q : Nat → Nat) (L : Nat)
    (hadm : Admissible L q)
    (hz : ThreeZero (nextWidth q L) (nextColumns q L)) :
    carry q L = 0 ∧ ThreeZero L q ∧ nextColumns q L 0 = 2 * q 0 := by
  have hn := NormalizationBridge.admissible_next q L hadm
  have hnextL := threeZero_min_width _ _ hn hz
  have hwidth : nextWidth q L ≤ L + 1 := by
    simp only [nextWidth]
    split <;> omega
  have hL : 4 ≤ L := by omega
  let a := carry q
  let c := fun i => carry q (L - i)
  let l := output q
  let u := fun i => (q i + c (i + 1)) % 10
  have hq : ∀ i, i < 4 → q i ≤ 18 := fun i hi => hadm.2.2.1 i (by omega)
  have ha : ∀ i, i ≤ 4 → a i ≤ 1 := by
    intro i hi
    exact carry_bounded q L hadm.2.2.1 i (by omega)
  have hc : ∀ i, i ≤ 4 → c i ≤ 1 := by
    intro i _
    exact carry_bounded q L hadm.2.2.1 (L - i) (by omega)
  have hl : ∀ i, i < 4 → l i ≤ 9 := fun i _ => output_bounded q i
  have hu : ∀ i, i < 4 → u i ≤ 9 := by
    intro i _
    dsimp only [u]
    omega
  have ha0 : a 0 = 0 := rfl
  have hstep : ∀ i, i < 4 → l i + 10 * a (i + 1) = q i + a i ∧
      u i + 10 * c i = q i + c (i + 1) := by
    intro i hi
    refine ⟨column_equation q i, ?_⟩
    have hh := (folded_carry_transition q L i (by omega) hadm.2.2.2.1).2
    have hind : L - 1 - i = L - (i + 1) := by omega
    rw [hind] at hh
    change c i = (q i + c (i + 1)) / 10 at hh
    rw [hh]
    exact Nat.mod_add_div _ _
  by_cases hover : carry q L = 0
  · have hc0 : c 0 = 0 := by simpa only [c, Nat.sub_zero] using hover
    have hem : ∀ i, i < 4 → nextColumns q L i = l i + u i := by
      intro i hi
      have he := folded_emission_no_overflow q L i (by omega) hadm.2.2.2.1 hover
      have hind : L - 1 - i = L - (i + 1) := by omega
      simpa only [l, u, c, output, hind] using he
    have hz1 : l 1 + u 1 = 0 := (hem 1 (by decide)).symm.trans hz.2.1
    have hz2 : l 2 + u 2 = 0 := (hem 2 (by decide)).symm.trans hz.2.2.1
    have hz3 : l 3 + u 3 = 0 := (hem 3 (by decide)).symm.trans hz.2.2.2
    obtain ⟨hq1, hq2, hq3, hc1, _⟩ :=
      no_overflow_three_zeros_rigidity q a c l u hq ha hc hl hu ha0 hc0 hstep hz1 hz2 hz3
    refine ⟨hover, ⟨hL, hq1, hq2, hq3⟩, ?_⟩
    have he := hem 0 (by decide)
    have hs := hstep 0 (by decide)
    simp only [Nat.reduceAdd] at hs
    have hla : a 1 = 0 := by
      have hzero := ha0
      change carry q 1 = 0
      have hb := no_overflow_three_zeros_rigidity q a c l u hq ha hc hl hu ha0 hc0
        hstep hz1 hz2 hz3
      simp only [carry]
      omega
    omega
  · have hcL := carry_bounded q L hadm.2.2.1 L (Nat.le_refl L)
    have hoverone : carry q L = 1 := by omega
    have hc0 : c 0 = 1 := by simpa only [c, Nat.sub_zero] using hoverone
    have hdelay : ∀ j, j < 4 → extended q L (L - (j + 1)) = u j := by
      intro j hj
      have he := folded_delay_update q L j (by omega) hadm.2.2.2.1
      have hind : L - 1 - j = L - (j + 1) := by omega
      simpa only [u, c, hind] using he
    have hem : ∀ i, 0 < i → i < 4 → nextColumns q L i = l i + u (i - 1) := by
      intro i hi0 hi
      have he := folded_emission_overflow q L i (by omega) hoverone
      have hd := hdelay (i - 1) (by omega)
      have hind : i - 1 + 1 = i := by omega
      rw [hind] at hd
      simpa only [l, output, hd] using he
    have hz1 : l 1 + u 0 = 0 := by
      have he := hem 1 (by decide) (by decide)
      simpa using he.symm.trans hz.2.1
    have hz2 : l 2 + u 1 = 0 := by
      have he := hem 2 (by decide) (by decide)
      simpa using he.symm.trans hz.2.2.1
    have hz3 : l 3 + u 2 = 0 := by
      have he := hem 3 (by decide) (by decide)
      simpa using he.symm.trans hz.2.2.2
    exact False.elim (overflow_three_zeros_impossible q a c l u hq ha hc hl hu ha0
      hc0 hstep hz1 hz2 hz3)

/-- Every earlier state has the same zero exterior; no preceding update
overflows, the width is unchanged, and the outer symbol doubles each time. -/
theorem iterPairs_threeZero_history (q : Nat → Nat) (L t : Nat)
    (ha : Admissible L q)
    (hz : ThreeZero (iterPairs q L t).1 (iterPairs q L t).2) :
    (∀ s, s ≤ t → ThreeZero (iterPairs q L s).1 (iterPairs q L s).2) ∧
      (∀ s, s < t → carry (iterPairs q L s).2 (iterPairs q L s).1 = 0) ∧
      (iterPairs q L t).1 = L ∧
      (iterPairs q L t).2 0 = 2 ^ t * q 0 := by
  induction t with
  | zero =>
      refine ⟨?_, ?_, rfl, ?_⟩
      · intro s hs
        have he : s = 0 := by omega
        simpa only [he] using hz
      · intro s hs
        omega
      · simp [iterPairs]
  | succ t ih =>
      have hp := next_threeZero_predecessor (iterPairs q L t).2 (iterPairs q L t).1
        (CarryHistory.iterPairs_admissible q L t ha) hz
      obtain ⟨hall, hcarry, hwidth, houter⟩ := ih hp.2.1
      refine ⟨?_, ?_, ?_, ?_⟩
      · intro s hs
        by_cases hst : s ≤ t
        · exact hall s hst
        · have he : s = t + 1 := by omega
          simpa only [he] using hz
      · intro s hs
        by_cases hst : s < t
        · exact hcarry s hst
        · have he : s = t := by omega
          simpa only [he] using hp.1
      · change nextWidth (iterPairs q L t).2 (iterPairs q L t).1 = L
        rw [nextWidth, if_pos hp.1]
        exact hwidth
      · change nextColumns (iterPairs q L t).2 (iterPairs q L t).1 0 = _
        rw [hp.2.2, houter, Nat.pow_succ]
        simp [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]

/-- The all-time bound follows from positivity and the digit-pair ceiling18. -/
theorem iterPairs_threeZero_time_bound (q : Nat → Nat) (L t : Nat)
    (ha : Admissible L q)
    (hz : ThreeZero (iterPairs q L t).1 (iterPairs q L t).2) : t ≤ 4 := by
  have hh := (iterPairs_threeZero_history q L t ha hz).2.2.2
  have hat := CarryHistory.iterPairs_admissible q L t ha
  have hb := hat.2.2.1 0 hat.1
  have hpos : 1 ≤ q 0 := ha.2.1
  have hmul := Nat.mul_le_mul_left (2 ^ t) hpos
  simp only [Nat.mul_one] at hmul
  have hpow : 2 ^ t ≤ 18 := by omega
  by_cases ht : t ≤ 4
  · exact ht
  · have hfive : 5 ≤ t := by omega
    have hlarge := Nat.pow_le_pow_right (by decide : 0 < 2) hfive
    have hvalue : 2 ^ 5 = 32 := by decide
    rw [hvalue] at hlarge
    omega

/-- Any canonical representation of an arbitrary positive numeric orbit
state with the displayed prefix obeys the same bound. -/
theorem numeric_threeZero_time_bound (n t W : Nat) (e : Nat → Nat)
    (hn : 0 < n) (hc : Canonical (Lychrel196.orbit n t) e W)
    (hz : ThreeZero W (columnSum e W)) : t ≤ 4 := by
  obtain ⟨d, L, hd⟩ := canonical_exists n hn
  let q := columnSum d L
  have ha : Admissible L q := NormalizationBridge.canonical_admissible n d L hd
  obtain ⟨f, hf, hrep⟩ := iterPairs_representation n d q L t hd (fun _ _ => rfl)
  have hW : W = (iterPairs q L t).1 :=
    (DecimalQuantitativeMass.decimalLength_of_canonical _ e W hc).symm.trans
      (DecimalQuantitativeMass.decimalLength_of_canonical _ f _ hf)
  subst W
  have heq : ∀ i, i < (iterPairs q L t).1 → e i = f i :=
    value_injective e f _ hc.2.1 hf.2.1 (hc.2.2.2.trans hf.2.2.2.symm)
  have hcol : ∀ i, i < (iterPairs q L t).1 →
      columnSum e (iterPairs q L t).1 i = (iterPairs q L t).2 i := by
    intro i hi
    rw [← hrep i hi]
    have hm : (iterPairs q L t).1 - 1 - i < (iterPairs q L t).1 := by omega
    simp only [columnSum, reflected, heq i hi, heq _ hm]
  apply iterPairs_threeZero_time_bound q L t ha
  refine ⟨hz.1, ?_, ?_, ?_⟩
  · rw [← hcol 1 (by have h := hz.1; omega)]
    exact hz.2.1
  · rw [← hcol 2 (by have h := hz.1; omega)]
    exact hz.2.2.1
  · rw [← hcol 3 (by have h := hz.1; omega)]
    exact hz.2.2.2

end ZeroExterior
