import Lychrel196Research
import MassCriterion

/-!
# A bound on zero gaps is preserved by actual decimal reverse-and-add

The update here is `FoldedDecimal.nextColumns`, including its actual final
carry and width. No orbit hypothesis or finite search is used.
-/

namespace DecimalZeroGap

open DecimalDigits FoldedDecimal DecimalMass

/-- Every nonempty interval of zero coefficients has length at most `K`. -/
def ZeroBound (q : Nat → Nat) (L K : Nat) : Prop :=
  ∀ a k, 0 < k → a + k ≤ L →
    (∀ i, a ≤ i → i < a + k → q i = 0) → k ≤ K

/-- The input word itself always supplies an initial zero-gap bound. -/
theorem zeroBound_length (q : Nat → Nat) (L : Nat) : ZeroBound q L L := by
  intro a k _ hk _
  omega

/-- Reflection of the actual carries, indexed at column boundaries. -/
def backCarry (q : Nat → Nat) (L i : Nat) : Nat := carry q (L - i)

/-- Reflection of the actual output digits. -/
def backOutput (q : Nat → Nat) (L i : Nat) : Nat := output q (L - 1 - i)

theorem back_column_equation (q : Nat → Nat) (L i : Nat)
    (hs : ∀ j, j < L → q j = q (L - 1 - j)) (hi : i < L) :
    backOutput q L i + 10 * backCarry q L i = q i + backCarry q L (i + 1) := by
  have he := column_equation q (L - 1 - i)
  have h₁ : L - 1 - i + 1 = L - i := by omega
  have h₂ : L - (i + 1) = L - 1 - i := by omega
  simpa only [backOutput, backCarry, h₁, h₂, ← hs i hi] using he

theorem backCarry_bounded (q : Nat → Nat) (L i : Nat)
    (hq : ∀ j, j < L → q j ≤ 18) : backCarry q L i ≤ 1 := by
  exact carry_bounded q L hq (L - i) (by omega)

/-- Simultaneous zero digits interchange the two binary carry states. -/
theorem simultaneous_zero_carries (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi : i < L)
    (hr : output q i = 0) (hu : backOutput q L i = 0) :
    carry q (i + 1) = backCarry q L i ∧
      carry q i = backCarry q L (i + 1) := by
  have hf := column_equation q i
  have hb := back_column_equation q L i ha.2.2.2.1 hi
  have hci := carry_bounded q L ha.2.2.1 i (by omega)
  have hcn := carry_bounded q L ha.2.2.1 (i + 1) (by omega)
  have hbi := backCarry_bounded q L i ha.2.2.1
  have hbn := backCarry_bounded q L (i + 1) ha.2.2.1
  omega

/-- Two adjacent simultaneous zero digits have identical old coefficients,
which must be zero or nine. An isolated simultaneous zero is insufficient. -/
theorem adjacent_zero_columns (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi : i + 1 < L)
    (hr : output q i = 0) (hu : backOutput q L i = 0)
    (hrn : output q (i + 1) = 0) (hun : backOutput q L (i + 1) = 0) :
    q i = q (i + 1) ∧ (q i = 0 ∨ q i = 9) := by
  have h₁ := simultaneous_zero_carries q L i ha (by omega) hr hu
  have h₂ := simultaneous_zero_carries q L (i + 1) ha hi hrn hun
  have he₁ := column_equation q i
  have he₂ := column_equation q (i + 1)
  have hci := carry_bounded q L ha.2.2.1 i (by omega)
  have hcn := carry_bounded q L ha.2.2.1 (i + 1) (by omega)
  omega

/-- A simultaneous zero interval of length at least two is entirely zero
or entirely nine in the old pair-sum word. -/
theorem simultaneous_zero_interval (q : Nat → Nat) (L a k : Nat)
    (ha : Admissible L q) (hk : 2 ≤ k) (hbound : a + k ≤ L)
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


theorem wordSum_mono_length (q : Nat → Nat) (a b : Nat) (hab : a ≤ b) :
    wordSum q a ≤ wordSum q b := by
  induction b generalizing a with
  | zero =>
    have ha : a = 0 := by omega
    subst a
    exact Nat.le_refl _
  | succ b ih =>
    by_cases h : a ≤ b
    · have he := ih a h
      simp only [wordSum]
      omega
    · have he : a = b + 1 := by omega
      subst a
      exact Nat.le_refl _

/-- Every interval of positive coefficients costs at least its length. -/
theorem interval_length_le_mass (q : Nat → Nat) (L a k : Nat)
    (hbound : a + k ≤ L)
    (hpos : ∀ i, a ≤ i → i < a + k → 0 < q i) :
    k ≤ wordSum q L := by
  have hp : k ≤ wordSum q (a + k) := by
    induction k with
    | zero => omega
    | succ k ih =>
      have hb : a + k ≤ L := by omega
      have hi := ih hb (fun i hia hik => hpos i hia (by omega))
      have hlast := hpos (a + k) (by omega) (by omega)
      simpa only [Nat.add_assoc, wordSum] using (by omega : k + 1 ≤ wordSum q (a + k) + q (a + k))
  exact Nat.le_trans hp (wordSum_mono_length q (a + k) L hbound)

/-- Without overflow a new zero is precisely a simultaneous old output zero. -/
theorem next_zero_no_overflow (q : Nat → Nat) (L i : Nat)
    (hc : carry q L = 0) (hz : nextColumns q L i = 0) :
    output q i = 0 ∧ backOutput q L i = 0 := by
  simpa only [nextColumns, hc, if_true, columnSum, reflected, backOutput,
    Nat.add_eq_zero_iff] using hz

/-- Every zero in an overflowing next word is strictly internal; its two
vanishing output digits have the one-column shifted alignment. -/
theorem next_zero_overflow (q : Nat → Nat) (L i : Nat)
    (hL : 0 < L) (hc : carry q L = 1) (hi : i < L + 1)
    (hz : nextColumns q L i = 0) :
    0 < i ∧ i < L ∧ output q i = 0 ∧ backOutput q L (i - 1) = 0 := by
  have hzero : i ≠ 0 := by
    intro he
    subst i
    simp [nextColumns, hc, columnSum, reflected, extended, hL] at hz
  have hlast : i ≠ L := by
    intro he
    subst i
    simp [nextColumns, hc, columnSum, reflected, extended, hL] at hz
  have hil : i < L := by omega
  have hmir : L - i < L := by omega
  have hind : L - 1 - (i - 1) = L - i := by omega
  simp only [nextColumns, hc, Nat.one_ne_zero, if_false, columnSum,
    reflected, Nat.add_sub_cancel, extended, hil, hmir, if_true] at hz
  refine ⟨by omega, hil, by omega, ?_⟩
  simp only [backOutput, hind]
  omega

/-- A zero input column with two zero output digits has four zero carries. -/
theorem zero_column_carries (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi : i < L)
    (hq : q i = 0) (hr : output q i = 0) (hu : backOutput q L i = 0) :
    carry q i = 0 ∧ carry q (i + 1) = 0 ∧
      backCarry q L i = 0 ∧ backCarry q L (i + 1) = 0 := by
  have hs := simultaneous_zero_carries q L i ha hi hr hu
  have he := column_equation q i
  have hb := carry_bounded q L ha.2.2.1 i (by omega)
  omega

/-- In the overflowing alignment, an all-zero core extends by one old
zero column at each end. This prevents merging unrelated old gaps. -/
theorem zero_core_extends (q : Nat → Nat) (L a k : Nat)
    (ha : Admissible L q) (ha0 : 0 < a) (hk : 0 < k) (hbound : a + k < L)
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
    have hb := back_column_equation q L (a - 1) ha.2.2.2.1 (by omega)
    have hd := output_bounded q (a - 1)
    rw [hlind] at hf hb
    omega
  have hqr : q (a + k) = 0 := by
    have hf := column_equation q (a + k)
    have hb := back_column_equation q L (a + k) ha.2.2.2.1 hbound
    have hd : backOutput q L (a + k) ≤ 9 := output_bounded q _
    omega
  intro i hia hik
  by_cases hi₁ : i = a - 1
  · exact hi₁ ▸ hql
  by_cases hi₂ : i = a + k
  · exact hi₂ ▸ hqr
  exact hcore i (by omega) (by omega)


/-- A uniform input mass bound and an initial zero-gap bound propagate
through the actual overflow-dependent pair-sum update. The deliberately
coarse condition `M + 2 ≤ K` handles every short-run exception. -/
theorem zeroBound_next (q : Nat → Nat) (L M K : Nat)
    (ha : Admissible L q) (hm : wordSum q L ≤ M)
    (hz : ZeroBound q L K) (hK : M + 2 ≤ K) :
    ZeroBound (nextColumns q L) (nextWidth q L) K := by
  intro a k hk hbound hzero
  by_cases hshort : k ≤ K
  · exact hshort
  have hlong : 3 ≤ k := by omega
  by_cases hc : carry q L = 0
  · have hb : a + k ≤ L := by simpa only [nextWidth, hc, if_true] using hbound
    have hboth : ∀ i, a ≤ i → i < a + k →
        output q i = 0 ∧ backOutput q L i = 0 := by
      intro i hia hik
      exact next_zero_no_overflow q L i hc (hzero i hia hik)
    rcases simultaneous_zero_interval q L a k ha (by omega) hb hboth with ho | hn
    · exact hz a k hk hb ho
    · have hmass := interval_length_le_mass q L a k hb
        (fun i hia hik => by rw [hn i hia hik]; decide)
      omega
  · have hcb := carry_bounded q L ha.2.2.1 L (by omega)
    have hc1 : carry q L = 1 := by omega
    have hb : a + k ≤ L + 1 := by
      simpa only [nextWidth, hc, if_false] using hbound
    have hout : ∀ i, a ≤ i → i < a + k →
        0 < i ∧ i < L ∧ output q i = 0 ∧ backOutput q L (i - 1) = 0 := by
      intro i hia hik
      exact next_zero_overflow q L i ha.1 hc1 (by omega) (hzero i hia hik)
    have hfirst := hout a (by omega) (by omega)
    have hlast := hout (a + k - 1) (by omega) (by omega)
    have ha0 : 0 < a := hfirst.1
    have hbk : a + k ≤ L := by omega
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
    · have hmass := interval_length_le_mass q L a (k - 1) (by omega)
        (fun i hia hik => by rw [hn i hia hik]; decide)
      omega

#print axioms simultaneous_zero_interval
#print axioms zero_core_extends
#print axioms zeroBound_next

end DecimalZeroGap
