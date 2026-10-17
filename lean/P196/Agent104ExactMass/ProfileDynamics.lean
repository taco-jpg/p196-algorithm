import P196.Agent104ExactMass.SharedProfile

namespace DecimalProfile

open DecimalDigits DecimalMass

/-- Binary carries hold everywhere for a bounded half-line profile. -/
theorem carry_le_one (q : Nat → Nat) (hq : ∀ i, q i ≤ 18) (i : Nat) :
    carry q i ≤ 1 := carry_bounded q i (fun j _ => hq j) i (Nat.le_refl _)

theorem reflect_bounded (q : Nat → Nat) (L : Nat) (hq : ∀ i, q i ≤ 18) :
    ∀ i, reflect q L i ≤ 18 := by
  intro i
  simp only [reflect]
  split
  · exact hq _
  · omega

theorem backCarry_bounded (q : Nat → Nat) (L i : Nat)
    (hq : ∀ j, q j ≤ 18) : backCarry q L i ≤ 1 :=
  carry_le_one _ (reflect_bounded q L hq) _

theorem backOutput_bounded (q : Nat → Nat) (L i : Nat) :
    backOutput q L i ≤ 9 := by
  simp only [backOutput]
  split
  · exact output_bounded _ _
  · omega

theorem backCarry_tail (q : Nat → Nat) (L i : Nat) (hi : L ≤ i) :
    backCarry q L i = 0 := by
  simp [backCarry, Nat.sub_eq_zero_of_le hi, carry]

theorem backOutput_tail (q : Nat → Nat) (L i : Nat) (hi : L ≤ i) :
    backOutput q L i = 0 := by simp [backOutput, Nat.not_lt.mpr hi]

theorem back_column_equation (q : Nat → Nat) (L i : Nat) (hi : i < L) :
    backOutput q L i + 10 * backCarry q L i = q i + backCarry q L (i + 1) := by
  have he := column_equation (reflect q L) (L - 1 - i)
  have h₁ : L - 1 - i + 1 = L - i := by omega
  have h₂ : L - (i + 1) = L - 1 - i := by omega
  have h₃ : L - 1 - i < L := by omega
  have h₄ : L - 1 - (L - 1 - i) = i := by omega
  simpa only [backOutput, backCarry, hi, if_true, reflect, h₁, h₂, h₃, h₄] using he

theorem output_at_end (q : Nat → Nat) (L : Nat)
    (hq : ∀ i, q i ≤ 18) (ht : ∀ i, L ≤ i → q i = 0) :
    output q L = carry q L := by
  have hb := carry_le_one q hq L
  simp only [output, ht L (Nat.le_refl _), Nat.zero_add]
  omega

theorem carry_after_end (q : Nat → Nat) (L i : Nat)
    (hq : ∀ j, q j ≤ 18) (ht : ∀ j, L ≤ j → q j = 0) (hi : L < i) :
    carry q i = 0 := by
  cases i with
  | zero => omega
  | succ i =>
    have hb := carry_le_one q hq i
    simp only [carry, ht i (by omega), Nat.zero_add]
    omega

theorem output_after_end (q : Nat → Nat) (L i : Nat)
    (hq : ∀ j, q j ≤ 18) (ht : ∀ j, L ≤ j → q j = 0) (hi : L < i) :
    output q i = 0 := by
  simp [output, ht i (by omega), carry_after_end q L i hq ht hi]

theorem nextLen_bounds (q : Nat → Nat) (L : Nat) :
    L ≤ nextLen q L ∧ nextLen q L ≤ L + 1 := by
  simp only [nextLen]
  split <;> omega

theorem nextLen_of_back_nonzero (q : Nat → Nat) (L : Nat)
    (hc : backCarry q L 0 ≠ 0) : nextLen q L = L + 1 := by
  simp [nextLen, hc]

theorem phi_bounded (q : Nat → Nat) (L i : Nat) : phi q L i ≤ 18 := by
  have hr := output_bounded q i
  have hb := backOutput_bounded q L i
  have hp := backOutput_bounded q L (i - 1)
  simp only [phi]
  split
  · omega
  · split
    · rename_i hi
      subst i
      have h := output_bounded q 0
      omega
    · omega

theorem phi_outer_no_overflow (q : Nat → Nat) (L : Nat)
    (hv : Valid L q) (hc : backCarry q L 0 = 0) :
    phi q L 0 = 2 * q 0 + backCarry q L 1 := by
  have hb := back_column_equation q L 0 hv.1
  simp only [Nat.zero_add] at hb
  have hu := backOutput_bounded q L 0
  have hq : q 0 < 10 := by omega
  have hr : output q 0 = q 0 := by simp [output, carry, Nat.mod_eq_of_lt hq]
  simp only [phi, hc, if_true, hr]
  omega

theorem phi_anchor (q : Nat → Nat) (L : Nat) (hv : Valid L q) :
    0 < phi q L 0 := by
  by_cases hc : backCarry q L 0 = 0
  · rw [phi_outer_no_overflow q L hv hc]
    have hp := hv.2.1
    omega
  · simp only [phi, hc, if_false, if_true]
    omega

theorem phi_terminal (q : Nat → Nat) (L : Nat) (hv : Valid L q) :
    0 < phi q L (nextLen q L - 1) := by
  have hL := hv.1
  have hq := hv.2.2.1
  have ht := hv.2.2.2.1
  have hp := hv.2.2.2.2
  have hlast : L - 1 + 1 = L := by omega
  have hf := column_equation q (L - 1)
  rw [hlast] at hf
  have hb := back_column_equation q L (L - 1) (by omega)
  rw [hlast, backCarry_tail q L L (by omega)] at hb
  have hd := output_bounded q (L - 1)
  have he := output_at_end q L hq ht
  by_cases hc : backCarry q L 0 = 0
  · by_cases hf0 : carry q L = 0
    · have hn : nextLen q L = L := by simp [nextLen, hf0, hc]
      rw [hn]
      simp only [phi, hc, if_true]
      omega
    · have hn : nextLen q L = L + 1 := by simp [nextLen, hf0]
      rw [hn, Nat.add_sub_cancel]
      simp only [phi, hc, if_true]
      omega
  · rw [nextLen_of_back_nonzero q L hc, Nat.add_sub_cancel]
    simp only [phi, hc, if_false, Nat.ne_of_gt hL, he]
    omega

theorem phi_tail (q : Nat → Nat) (L : Nat) (hv : Valid L q) :
    ∀ i, nextLen q L ≤ i → phi q L i = 0 := by
  intro i hi
  have hq := hv.2.2.1
  have ht := hv.2.2.2.1
  have hLi := Nat.le_trans (nextLen_bounds q L).1 hi
  by_cases hc : backCarry q L 0 = 0
  · have hu := backOutput_tail q L i hLi
    have hr : output q i = 0 := by
      by_cases he : i = L
      · subst i
        have hf0 : carry q L = 0 := by
          apply Classical.byContradiction
          intro hn
          have hh : nextLen q L = L + 1 := by simp [nextLen, hn]
          omega
        rw [output_at_end q L hq ht, hf0]
      · exact output_after_end q L i hq ht (by omega)
    simp [phi, hc, hu, hr]
  · have hni := nextLen_of_back_nonzero q L hc
    have hip : L ≤ i - 1 := by omega
    have hi0 : i ≠ 0 := by omega
    have hr := output_after_end q L i hq ht (by omega)
    have hu := backOutput_tail q L (i - 1) hip
    simp [phi, hc, hi0, hr, hu]

theorem step_valid (s : State) (hv : Valid s.1 s.2) :
    Valid (step s).1 (step s).2 := by
  change Valid (nextLen s.2 s.1) (phi s.2 s.1)
  refine ⟨?_, phi_anchor _ _ hv, phi_bounded _ _, phi_tail _ _ hv, phi_terminal _ _ hv⟩
  have hh := nextLen_bounds s.2 s.1
  have hp := hv.1
  omega

theorem iter_valid (s : State) (t : Nat) (hv : Valid s.1 s.2) :
    Valid (iter s t).1 (iter s t).2 := by
  induction t with
  | zero => exact hv
  | succ t ih => exact step_valid _ ih

open DecimalWidthGrowth

private theorem finite_no_back_overflow :
    ∀ a ∈ List.range 19, ∀ b ∈ [0,1], 0<a → a+b<10 →
      lowerPotential (2*a+b)+1 ≤ lowerPotential a := by decide

private theorem finite_back_overflow :
    ∀ a ∈ List.range 19, ∀ b ∈ [0,1], 0<a → 10≤a+b →
      lowerPotential (a+1-10*(a/10))+1 ≤ lowerPotential a+4 := by decide

theorem lower_potential_step (q : Nat → Nat) (L : Nat) (hv : Valid L q) :
    lowerPotential (phi q L 0)+1+4*L ≤
      lowerPotential (q 0)+4*nextLen q L := by
  have hp := hv.2.1
  have hq := hv.2.2.1 0
  have hb := backCarry_bounded q L 1 hv.2.2.1
  have hc := backCarry_bounded q L 0 hv.2.2.1
  have he := back_column_equation q L 0 hv.1
  simp only [Nat.zero_add] at he
  have hu := backOutput_bounded q L 0
  have hmem : q 0 ∈ List.range 19 := by simp; omega
  have hbmem : backCarry q L 1 ∈ [0,1] := by simp; omega
  by_cases hzero : backCarry q L 0 = 0
  · have hsmall : q 0 + backCarry q L 1 < 10 := by omega
    have hpstep := finite_no_back_overflow (q 0) hmem (backCarry q L 1) hbmem hp hsmall
    rw [phi_outer_no_overflow q L hv hzero]
    have hn := (nextLen_bounds q L).1
    omega
  · have hlarge : 10 ≤ q 0 + backCarry q L 1 := by omega
    have hpstep := finite_back_overflow (q 0) hmem (backCarry q L 1) hbmem hp hlarge
    have houter : phi q L 0 = q 0 + 1 - 10 * (q 0 / 10) := by
      simp only [phi, hzero, if_false, if_true, output, carry, Nat.add_zero]
      have hdiv := Nat.mod_add_div (q 0) 10
      omega
    rw [houter, nextLen_of_back_nonzero q L hzero]
    omega

theorem iter_width_clock (s : State) (t : Nat) (hv : Valid s.1 s.2) :
    t + 4 * s.1 ≤ 4 * (iter s t).1 + 4 := by
  have hpot : ∀ k,
      lowerPotential ((iter s k).2 0) + k + 4 * s.1 ≤
        lowerPotential (s.2 0) + 4 * (iter s k).1 := by
    intro k
    induction k with
    | zero => simp [iter]
    | succ k ih =>
      have hs := lower_potential_step (iter s k).2 (iter s k).1 (iter_valid s k hv)
      change lowerPotential (phi (iter s k).2 (iter s k).1 0) + (k+1) + 4*s.1 ≤
        lowerPotential (s.2 0) + 4 * nextLen (iter s k).2 (iter s k).1
      omega
  have hh := hpot t
  have hb := lowerPotential_bounded (s.2 0)
  omega

/-- Simultaneous zero digits interchange the two binary carry states. -/
theorem simultaneous_zero_carries (q : Nat → Nat) (L i : Nat)
    (ha : Valid L q) (hi : i < L)
    (hr : output q i = 0) (hu : backOutput q L i = 0) :
    carry q (i + 1) = backCarry q L i ∧
      carry q i = backCarry q L (i + 1) := by
  have hf := column_equation q i
  have hb := back_column_equation q L i hi
  have hci := carry_bounded q L (fun j _ => ha.2.2.1 j) i (by omega)
  have hcn := carry_bounded q L (fun j _ => ha.2.2.1 j) (i + 1) (by omega)
  have hbi := backCarry_bounded q L i ha.2.2.1
  have hbn := backCarry_bounded q L (i + 1) ha.2.2.1
  omega

/-- Two adjacent simultaneous zero digits have identical old coefficients,
which must be zero or nine. An isolated simultaneous zero is insufficient. -/
theorem adjacent_zero_columns (q : Nat → Nat) (L i : Nat)
    (ha : Valid L q) (hi : i + 1 < L)
    (hr : output q i = 0) (hu : backOutput q L i = 0)
    (hrn : output q (i + 1) = 0) (hun : backOutput q L (i + 1) = 0) :
    q i = q (i + 1) ∧ (q i = 0 ∨ q i = 9) := by
  have h₁ := simultaneous_zero_carries q L i ha (by omega) hr hu
  have h₂ := simultaneous_zero_carries q L (i + 1) ha hi hrn hun
  have he₁ := column_equation q i
  have he₂ := column_equation q (i + 1)
  have hci := carry_bounded q L (fun j _ => ha.2.2.1 j) i (by omega)
  have hcn := carry_bounded q L (fun j _ => ha.2.2.1 j) (i + 1) (by omega)
  omega

/-- A simultaneous zero interval of length at least two is entirely zero
or entirely nine in the old pair-sum word. -/
theorem simultaneous_zero_interval (q : Nat → Nat) (L a k : Nat)
    (ha : Valid L q) (hk : 2 ≤ k) (hbound : a + k ≤ L)
    (hz : ∀ i, a ≤ i → i < a + k → output q i = 0 ∧ backOutput q L i = 0) :
    (∀ i, a ≤ i → i < a + k → q i = 0) ∨
      (∀ i, a ≤ i → i < a + k → q i = 9) := by
  have hadj : ∀ i, a ≤ i → i + 1 < a + k →
      q i = q (i + 1) ∧ (q i = 0 ∨ q i = 9) := by
    intro i hia hik
    have h₁ := hz i hia (by omega)
    have h₂ := hz (i + 1) (by omega) hik
    exact adjacent_zero_columns q L i ha (by omega) h₁.1 h₁.2 h₂.1 h₂.2
  have heq : ∀ j, j < k → q (a + j) = q a := by
    intro j
    induction j with
    | zero => intro _; simp
    | succ j ih =>
      intro hj
      have he := (hadj (a + j) (by omega) (by omega)).1
      have hp := ih (by omega)
      simpa only [Nat.add_assoc] using he.symm.trans hp
  rcases (hadj a (by omega) (by omega)).2 with hzero | hnine
  · left
    intro i hia hik
    have he := heq (i - a) (by omega)
    have hind : a + (i - a) = i := by omega
    rw [hind] at he
    exact he.trans hzero
  · right
    intro i hia hik
    have he := heq (i - a) (by omega)
    have hind : a + (i - a) = i := by omega
    rw [hind] at he
    exact he.trans hnine



/-- A zero input column with two zero output digits has four zero carries. -/
theorem zero_column_carries (q : Nat → Nat) (L i : Nat)
    (ha : Valid L q) (hi : i < L)
    (hq : q i = 0) (hr : output q i = 0) (hu : backOutput q L i = 0) :
    carry q i = 0 ∧ carry q (i + 1) = 0 ∧
      backCarry q L i = 0 ∧ backCarry q L (i + 1) = 0 := by
  have hs := simultaneous_zero_carries q L i ha hi hr hu
  have he := column_equation q i
  have hb := carry_bounded q L (fun j _ => ha.2.2.1 j) i (by omega)
  omega

/-- In the overflowing alignment, an all-zero core extends by one old
zero column at each end. This prevents merging unrelated old gaps. -/
theorem zero_core_extends (q : Nat → Nat) (L a k : Nat)
    (ha : Valid L q) (ha0 : 0 < a) (hk : 0 < k) (hbound : a + k < L)
    (hcore : ∀ i, a ≤ i → i < a + k → q i = 0)
    (hz : ∀ i, a ≤ i → i < a + k → output q i = 0 ∧ backOutput q L i = 0)
    (hleft : backOutput q L (a - 1) = 0) (hright : output q (a + k) = 0) :
    ∀ i, a - 1 ≤ i → i < a + k + 1 → q i = 0 := by
  have hca := zero_column_carries q L a ha (by omega)
    (hcore a (by omega) (by omega))
    (hz a (by omega) (by omega)).1 (hz a (by omega) (by omega)).2
  have hcb := zero_column_carries q L (a + k - 1) ha (by omega)
    (hcore (a + k - 1) (by omega) (by omega))
    (hz (a + k - 1) (by omega) (by omega)).1
    (hz (a + k - 1) (by omega) (by omega)).2
  have hlind : a - 1 + 1 = a := by omega
  have hrind : a + k - 1 + 1 = a + k := by omega
  rw [hrind] at hcb
  have hql : q (a - 1) = 0 := by
    have hf := column_equation q (a - 1)
    have hb := back_column_equation q L (a - 1) (by omega)
    have hd := output_bounded q (a - 1)
    rw [hlind] at hf hb
    omega
  have hqr : q (a + k) = 0 := by
    have hf := column_equation q (a + k)
    have hb := back_column_equation q L (a + k) hbound
    have hd : backOutput q L (a + k) ≤ 9 := backOutput_bounded q L (a + k)
    omega
  intro i hia hik
  by_cases hi₁ : i = a - 1
  · exact hi₁ ▸ hql
  by_cases hi₂ : i = a + k
  · exact hi₂ ▸ hqr
  exact hcore i (by omega) (by omega)



/-- A zero in the new exact support cannot lie beyond the old support. -/
theorem phi_zero_index (q : Nat → Nat) (L i : Nat) (hv : Valid L q)
    (hi : i < nextLen q L) (hz : phi q L i = 0) : i < L := by
  have hn := nextLen_bounds q L
  by_cases h : i < L
  · exact h
  · have he : i = L := by omega
    have hlen : nextLen q L = L + 1 := by omega
    have hp := phi_terminal q L hv
    subst i
    rw [hlen, Nat.add_sub_cancel, hz] at hp
    omega

theorem phi_zero_no_overflow (q : Nat → Nat) (L i : Nat)
    (hc : backCarry q L 0 = 0) (hz : phi q L i = 0) :
    output q i = 0 ∧ backOutput q L i = 0 := by
  simpa only [phi, hc, if_true, Nat.add_eq_zero_iff] using hz

theorem phi_zero_overflow (q : Nat → Nat) (L i : Nat)
    (hv : Valid L q) (hc : backCarry q L 0 ≠ 0) (hi : i < nextLen q L)
    (hz : phi q L i = 0) :
    0 < i ∧ i < L ∧ output q i = 0 ∧ backOutput q L (i - 1) = 0 := by
  have hil := phi_zero_index q L i hv hi hz
  have hi0 : i ≠ 0 := by
    intro he
    subst i
    have hp := phi_anchor q L hv
    omega
  simp only [phi, hc, if_false, hi0] at hz
  exact ⟨by omega, hil, by omega, by omega⟩

/-- The old zero-gap mechanism needs no symmetry. -/
theorem zeroBound_phi (q : Nat → Nat) (L M K : Nat)
    (ha : Valid L q) (hm : wordSum q L ≤ M)
    (hz : DecimalZeroGap.ZeroBound q L K) (hK : M + 2 ≤ K) :
    DecimalZeroGap.ZeroBound (phi q L) (nextLen q L) K := by
  intro a k hk hbound hzero
  by_cases hshort : k ≤ K
  · exact hshort
  have hlong : 3 ≤ k := by omega
  have hlast := phi_zero_index q L (a+k-1) ha (by omega)
    (hzero (a+k-1) (by omega) (by omega))
  have hb : a + k ≤ L := by omega
  by_cases hc : backCarry q L 0 = 0
  · have hboth : ∀ i, a ≤ i → i < a + k →
        output q i = 0 ∧ backOutput q L i = 0 := by
      intro i hia hik
      exact phi_zero_no_overflow q L i hc (hzero i hia hik)
    rcases simultaneous_zero_interval q L a k ha (by omega) hb hboth with ho | hn
    · exact hz a k hk hb ho
    · have hmass := DecimalZeroGap.interval_length_le_mass q L a k hb
        (fun i hia hik => by rw [hn i hia hik]; decide)
      omega
  · have hout : ∀ i, a ≤ i → i < a + k →
        0 < i ∧ i < L ∧ output q i = 0 ∧ backOutput q L (i - 1) = 0 := by
      intro i hia hik
      exact phi_zero_overflow q L i ha hc (by omega) (hzero i hia hik)
    have hfirst := hout a (by omega) (by omega)
    have ha0 : 0 < a := hfirst.1
    have hcore : ∀ i, a ≤ i → i < a + (k - 1) →
        output q i = 0 ∧ backOutput q L i = 0 := by
      intro i hia hik
      have hr := (hout i hia (by omega)).2.2.1
      have hu := (hout (i + 1) (by omega) (by omega)).2.2.2
      exact ⟨hr, by simpa only [Nat.add_sub_cancel] using hu⟩
    rcases simultaneous_zero_interval q L a (k - 1) ha (by omega) (by omega) hcore
      with ho | hn
    · have hright : output q (a + (k - 1)) = 0 :=
        (hout (a + (k - 1)) (by omega) (by omega)).2.2.1
      have hext := zero_core_extends q L a (k - 1) ha ha0 (by omega)
        (by omega) ho hcore hfirst.2.2.2 hright
      have hold : k + 1 ≤ K := hz (a - 1) (k + 1) (by omega) (by omega)
        (fun i hia hik => hext i hia (by omega))
      omega
    · have hmass := DecimalZeroGap.interval_length_le_mass q L a (k - 1) (by omega)
        (fun i hia hik => by rw [hn i hia hik]; decide)
      omega

#print axioms step_valid
#print axioms iter_width_clock
#print axioms zeroBound_phi

end DecimalProfile
