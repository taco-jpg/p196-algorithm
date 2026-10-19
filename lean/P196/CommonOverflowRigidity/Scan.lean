import P196.CommonOverflowRigidity.Invariant
import P196.Agent8CommonOverflowDefect.Agent8DefectTransport

/-!
The finite two-layer carry invariant is followed by the actual carries of
bounded symmetric decimal column words. The local relation remains valid through
the whole width, including overlapping reflected positions. At the end of
this full scan, the equal terminal carries exclude every exceptional state.

This module retains an explicit common second terminal carry hypothesis.
The numerical and carry-balance consequences are exposed separately.
-/

set_option autoImplicit false

namespace P196.CommonOverflowRigidity

open DecimalDigits FoldedDecimal
open P196.Agent8.CommonOverflowDefect

/-- Antisymmetry is equivalently equality of the two reflected digit sums. -/
theorem antisymmetric_pair_sum (q s : Nat → Nat) (L : Nat)
    (he : AntisymmetricDefect q s L) (i : Nat) (hi : i < L) :
    output q i + output q (L - 1 - i) =
      output s i + output s (L - 1 - i) := by
  have h := (antisymmetricDefect_iff q s L).mp he i hi
  omega

/-- The original and successor carries, read from both ends at layer i.
The remembered digit supplies the shifted reflection after overflow. -/
def actualState (q s : Nat → Nat) (L i : Nat) : State :=
  ⟨⟨carry q i, carry q (L - i), carry s i, carry s (L - i)⟩,
    ⟨carry (nextColumns q L) i, carry (nextColumns q L) (L + 1 - i),
      carry (nextColumns s L) i, carry (nextColumns s L) (L + 1 - i)⟩,
    extended q L (L - i), extended s L (L - i)⟩

theorem extended_bounded_of_carry_one (q : Nat → Nat) (L : Nat)
    (hc : carry q L = 1) (i : Nat) : extended q L i ≤ 9 := by
  unfold extended
  split
  · exact output_bounded q i
  · omega

theorem next_bounded_overflow (q : Nat → Nat) (L : Nat)
    (hc : carry q L = 1) :
    ∀ i, i < L + 1 → nextColumns q L i ≤ 18 := by
  have hd : ∀ i, i < L + 1 → extended q L i ≤ 9 :=
    fun i _ => extended_bounded_of_carry_one q L hc i
  simpa only [nextColumns, hc, Nat.one_ne_zero, if_false] using
    columnSum_bounded (extended q L) (L + 1) hd

theorem next_symmetric_overflow (q : Nat → Nat) (L : Nat)
    (hc : carry q L = 1) :
    ∀ i, i < L + 1 → nextColumns q L i = nextColumns q L (L + 1 - 1 - i) := by
  simpa only [nextColumns, hc, Nat.one_ne_zero, if_false] using
    columnSum_symmetric (extended q L) (L + 1)

theorem actualState_bounded (q s : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) (hs : ∀ i, i < L → s i ≤ 18)
    (hq1 : carry q L = 1) (hs1 : carry s L = 1)
    (i : Nat) (hi : i ≤ L) : Bounded (actualState q s L i) := by
  have hQ := next_bounded_overflow q L hq1
  have hS := next_bounded_overflow s L hs1
  dsimp only [Bounded, LayerBounded, actualState]
  refine ⟨⟨?_, ?_, ?_, ?_⟩, ⟨?_, ?_, ?_, ?_⟩, ?_, ?_⟩
  · exact carry_bounded q L hq i hi
  · exact carry_bounded q L hq (L - i) (by omega)
  · exact carry_bounded s L hs i hi
  · exact carry_bounded s L hs (L - i) (by omega)
  · exact carry_bounded _ (L + 1) hQ i (by omega)
  · exact carry_bounded _ (L + 1) hQ (L + 1 - i) (by omega)
  · exact carry_bounded _ (L + 1) hS i (by omega)
  · exact carry_bounded _ (L + 1) hS (L + 1 - i) (by omega)
  · exact extended_bounded_of_carry_one q L hq1 (L - i)
  · exact extended_bounded_of_carry_one s L hs1 (L - i)

theorem actualState_zero_diagonal (q s : Nat → Nat) (L : Nat)
    (hq1 : carry q L = 1) (hs1 : carry s L = 1)
    (hc2 : carry (nextColumns q L) (L + 1) =
      carry (nextColumns s L) (L + 1)) :
    Diagonal (actualState q s L 0) := by
  change carry q 0 = carry s 0 ∧ carry q L = carry s L ∧
    carry (nextColumns q L) 0 = carry (nextColumns s L) 0 ∧
    carry (nextColumns q L) (L + 1) = carry (nextColumns s L) (L + 1) ∧
    extended q L L = extended s L L
  exact ⟨rfl, hq1.trans hs1.symm, rfl, hc2, by simp [extended, hq1, hs1]⟩

/-- One genuine symmetric column pair satisfies the local folded relation. -/
theorem local_of_actual (q s : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i = q (L - 1 - i))
    (hs : ∀ i, i < L → s i = s (L - 1 - i))
    (he : AntisymmetricDefect q s L) (i : Nat) (hi : i < L) :
    Local ⟨carry q i, carry q (L - i), carry s i, carry s (L - i)⟩
      (q i) (s i) (carry q (L - 1 - i)) (carry s (L - 1 - i)) := by
  have hqi := hq i hi
  have hsi := hs i hi
  have hind : L - 1 - i + 1 = L - i := by omega
  have hpair := antisymmetric_pair_sum q s L he i hi
  dsimp only [Local]
  refine ⟨?_, ?_, ?_⟩
  · calc
      (q i + carry q (L - 1 - i)) / 10 =
          (q (L - 1 - i) + carry q (L - 1 - i)) / 10 := by rw [hqi]
      _ = carry q (L - 1 - i + 1) := rfl
      _ = carry q (L - i) := by rw [hind]
  · calc
      (s i + carry s (L - 1 - i)) / 10 =
          (s (L - 1 - i) + carry s (L - 1 - i)) / 10 := by rw [hsi]
      _ = carry s (L - 1 - i + 1) := rfl
      _ = carry s (L - i) := by rw [hind]
  · simpa only [output, ← hqi, ← hsi] using hpair

/-- Overflow changes the reflected partner to the remembered high digit. -/
theorem nextColumns_low_overflow (q : Nat → Nat) (L : Nat)
    (hc : carry q L = 1) (i : Nat) (hi : i < L) :
    nextColumns q L i = output q i + extended q L (L - i) := by
  simp only [nextColumns, hc, Nat.one_ne_zero, if_false, columnSum,
    reflected, Nat.add_sub_cancel, extended, if_pos hi]

theorem actual_transition (q s : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i = q (L - 1 - i))
    (hs : ∀ i, i < L → s i = s (L - 1 - i))
    (hq1 : carry q L = 1) (hs1 : carry s L = 1)
    (he1 : AntisymmetricDefect q s L)
    (he2 : AntisymmetricDefect (nextColumns q L) (nextColumns s L) (L + 1))
    (i : Nat) (hi : i < L) :
    Transition (actualState q s L i) (q i) (s i)
      (carry q (L - 1 - i)) (carry s (L - 1 - i))
      (carry (nextColumns q L) (L - i))
      (carry (nextColumns s L) (L - i)) := by
  have hQ := next_symmetric_overflow q L hq1
  have hS := next_symmetric_overflow s L hs1
  unfold Transition
  dsimp only [actualState]
  constructor
  · exact local_of_actual q s L hq hs he1 i hi
  · change Local _ (output q i + extended q L (L - i))
      (output s i + extended s L (L - i)) _ _
    rw [← nextColumns_low_overflow q L hq1 i hi,
      ← nextColumns_low_overflow s L hs1 i hi]
    simpa only [Nat.add_sub_cancel] using
      local_of_actual (nextColumns q L) (nextColumns s L) (L + 1)
        hQ hS he2 i (by omega)

theorem actual_advance (q s : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i = q (L - 1 - i))
    (hs : ∀ i, i < L → s i = s (L - 1 - i))
    (hq1 : carry q L = 1) (hs1 : carry s L = 1)
    (i : Nat) (hi : i < L) :
    advance (actualState q s L i) (q i) (s i)
      (carry q (L - 1 - i)) (carry s (L - 1 - i))
      (carry (nextColumns q L) (L - i))
      (carry (nextColumns s L) (L - i)) = actualState q s L (i + 1) := by
  have hqi := hq i hi
  have hsi := hs i hi
  have hreflect : L - 1 - i = L - (i + 1) := by omega
  have hnextReflect : L - i = L + 1 - (i + 1) := by omega
  have hmirror : L - 1 - i < L := by omega
  have hA : (q i + carry q i) % 10 + extended q L (L - i) =
      nextColumns q L i := (nextColumns_low_overflow q L hq1 i hi).symm
  have hB : (s i + carry s i) % 10 + extended s L (L - i) =
      nextColumns s L i := (nextColumns_low_overflow s L hs1 i hi).symm
  have hpq : (q i + carry q (L - 1 - i)) % 10 =
      extended q L (L - (i + 1)) := by
    rw [← hreflect]
    simp only [extended, if_pos hmirror, output, ← hqi]
  have hps : (s i + carry s (L - 1 - i)) % 10 =
      extended s L (L - (i + 1)) := by
    rw [← hreflect]
    simp only [extended, if_pos hmirror, output, ← hsi]
  simp only [advance, advanceLayer, actualState, State.mk.injEq, Layer.mk.injEq]
  rw [hA, hB]
  exact ⟨⟨rfl, by rw [hreflect], rfl, by rw [hreflect]⟩,
    ⟨rfl, by rw [hnextReflect], rfl, by rw [hnextReflect]⟩, hpq, hps⟩

/-- Either every digit already scanned agrees and the state is diagonal,
or the scan has entered the closed exceptional set. The bound is the full
width L; no assumption that the reflected positions are distinct is used. -/
theorem scan_prefix (q s : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) (hs : ∀ i, i < L → s i ≤ 18)
    (hqs : ∀ i, i < L → q i = q (L - 1 - i))
    (hss : ∀ i, i < L → s i = s (L - 1 - i))
    (hq1 : carry q L = 1) (hs1 : carry s L = 1)
    (he1 : AntisymmetricDefect q s L)
    (hc2 : carry (nextColumns q L) (L + 1) =
      carry (nextColumns s L) (L + 1))
    (he2 : AntisymmetricDefect (nextColumns q L) (nextColumns s L) (L + 1)) :
    ∀ k, k ≤ L →
      ((∀ i, i < k → output q i = output s i) ∧ Diagonal (actualState q s L k)) ∨
        Bad (actualState q s L k) := by
  have hQ := next_bounded_overflow q L hq1
  have hS := next_bounded_overflow s L hs1
  intro k
  induction k with
  | zero =>
    intro _
    exact Or.inl ⟨by intro i hi; omega,
      actualState_zero_diagonal q s L hq1 hs1 hc2⟩
  | succ k ih =>
    intro hk
    have hkL : k < L := by omega
    have hbound := actualState_bounded q s L hq hs hq1 hs1 k (by omega)
    have ha := hq k hkL
    have hb := hs k hkL
    have hrq := carry_bounded q L hq (L - 1 - k) (by omega)
    have hrs := carry_bounded s L hs (L - 1 - k) (by omega)
    have htq := carry_bounded (nextColumns q L) (L + 1)
      hQ (L - k) (by omega)
    have hts := carry_bounded (nextColumns s L) (L + 1)
      hS (L - k) (by omega)
    have htrans := actual_transition q s L hqs hss hq1 hs1 he1 he2 k hkL
    have hadv := actual_advance q s L hqs hss hq1 hs1 k hkL
    rcases ih (by omega) with ⟨hprefix, hdiag⟩ | hbad
    · have hstep := diagonal_step (actualState q s L k) (q k) (s k)
        (carry q (L - 1 - k)) (carry s (L - 1 - k))
        (carry (nextColumns q L) (L - k))
        (carry (nextColumns s L) (L - k))
        hbound hdiag ha hb hrq hrs htq hts htrans
      rw [hadv] at hstep
      rcases hstep with ⟨hdiag', hdigit⟩ | hbad'
      · left
        refine ⟨?_, hdiag'⟩
        intro i hi
        by_cases hik : i < k
        · exact hprefix i hik
        · have hieq : i = k := by omega
          subst i
          simpa only [actualState, output] using hdigit
      · exact Or.inr hbad'
    · right
      have hstep := bad_step (actualState q s L k) (q k) (s k)
        (carry q (L - 1 - k)) (carry s (L - 1 - k))
        (carry (nextColumns q L) (L - k))
        (carry (nextColumns s L) (L - k))
        hbound hbad ha hb hrq hrs htq hts htrans
      simpa only [hadv] using hstep

/-- Two antisymmetric normalized defects, after common first overflow and
with equal second terminal carries, force every first normalized digit to
agree. The full-width scan supplies its own exact terminal condition. -/
theorem repeated_antisymmetry_outputs_of_carry_eq (q s : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) (hs : ∀ i, i < L → s i ≤ 18)
    (hqs : ∀ i, i < L → q i = q (L - 1 - i))
    (hss : ∀ i, i < L → s i = s (L - 1 - i))
    (hq1 : carry q L = 1) (hs1 : carry s L = 1)
    (he1 : AntisymmetricDefect q s L)
    (hc2 : carry (nextColumns q L) (L + 1) =
      carry (nextColumns s L) (L + 1))
    (he2 : AntisymmetricDefect (nextColumns q L) (nextColumns s L) (L + 1)) :
    ∀ i, i < L → output q i = output s i := by
  rcases scan_prefix q s L hq hs hqs hss hq1 hs1 he1 hc2 he2 L (Nat.le_refl L) with
    ⟨hprefix, _⟩ | hbad
  · exact hprefix
  · have hne := bad_low_ne (actualState q s L L) hbad
    have heq : (actualState q s L L).first.qLow =
        (actualState q s L L).first.sLow := hq1.trans hs1.symm
    exact False.elim (hne heq)

end P196.CommonOverflowRigidity
