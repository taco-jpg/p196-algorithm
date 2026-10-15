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

end ZeroExterior
