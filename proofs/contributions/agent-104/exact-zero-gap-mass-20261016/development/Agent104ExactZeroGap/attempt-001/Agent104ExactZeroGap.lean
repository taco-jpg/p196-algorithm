import LychrelDigitSums

/-!
# Exact mass-sensitive zero-gap transport for actual decimal addition

Agent #104, 2026-10-16. This formalizes the retained nine-mass estimates in
`continuation/sparse_orbits_theorem.md`, sections 3--5. The original
`DecimalZeroGap` carry and interval lemmas are reused without modification.
The update is the original `FoldedDecimal.nextColumns`, with its real final
carry and changing width. No palindrome avoidance is assumed or concluded.
-/

namespace Agent104.ExactZeroGap

open DecimalDigits FoldedDecimal DecimalMass DecimalZeroGap

/-- An interval consisting of nines costs nine units of mass per column. -/
theorem interval_nine_mass (q : Nat → Nat) (L a k : Nat)
    (hbound : a + k ≤ L)
    (hnine : ∀ i, a ≤ i → i < a + k → q i = 9) :
    9 * k ≤ wordSum q L := by
  have hp : 9 * k ≤ wordSum q (a + k) := by
    induction k with
    | zero => omega
    | succ k ih =>
      have hb : a + k ≤ L := by omega
      have hi := ih hb (fun i hia hik => hnine i hia (by omega))
      have hlast := hnine (a + k) (by omega) (by omega)
      simpa only [Nat.add_assoc, wordSum, hlast] using
        (by omega : 9 * (k + 1) ≤ wordSum q (a + k) + 9)
  exact Nat.le_trans hp (wordSum_mono_length q (a + k) L hbound)

/-- Without overflow the only long new zero intervals come from one old
zero interval or one all-nine interval. Isolated columns cost the explicit 1. -/
theorem zeroBound_next_nooverflow_exact (q : Nat → Nat) (L M K : Nat)
    (ha : Admissible L q) (hm : wordSum q L ≤ M)
    (hz : ZeroBound q L K) (hc : carry q L = 0) :
    ZeroBound (nextColumns q L) (nextWidth q L) (max K (max 1 (M / 9))) := by
  intro a k hk hbound hzero
  have hcapK : K ≤ max K (max 1 (M / 9)) := Nat.le_max_left _ _
  have hcap1 : 1 ≤ max K (max 1 (M / 9)) :=
    Nat.le_trans (Nat.le_max_left _ _) (Nat.le_max_right _ _)
  have hcapM : M / 9 ≤ max K (max 1 (M / 9)) :=
    Nat.le_trans (Nat.le_max_right _ _) (Nat.le_max_right _ _)
  by_cases hs : k ≤ 1
  · omega
  have hb : a + k ≤ L := by simpa only [nextWidth, hc, if_true] using hbound
  have hboth : ∀ i, a ≤ i → i < a + k →
      output q i = 0 ∧ backOutput q L i = 0 := by
    intro i hia hik
    exact next_zero_no_overflow q L i hc (hzero i hia hik)
  rcases simultaneous_zero_interval q L a k ha (by omega) hb hboth with ho | hn
  · have hold := hz a k hk hb ho
    omega
  · have hmass := interval_nine_mass q L a k hb hn
    omega

/-- Overflow shortens old zero gaps by at least one. New long gaps created
from nines have an overlap core one column shorter than the output gap. -/
theorem zeroBound_next_overflow_exact (q : Nat → Nat) (L M K : Nat)
    (ha : Admissible L q) (hm : wordSum q L ≤ M)
    (hz : ZeroBound q L K) (hc : carry q L = 1) :
    ZeroBound (nextColumns q L) (nextWidth q L)
      (max (K - 1) (max 2 (M / 9 + 1))) := by
  intro a k hk hbound hzero
  have hcapK : K - 1 ≤ max (K - 1) (max 2 (M / 9 + 1)) := Nat.le_max_left _ _
  have hcap2 : 2 ≤ max (K - 1) (max 2 (M / 9 + 1)) :=
    Nat.le_trans (Nat.le_max_left _ _) (Nat.le_max_right _ _)
  have hcapM : M / 9 + 1 ≤ max (K - 1) (max 2 (M / 9 + 1)) :=
    Nat.le_trans (Nat.le_max_right _ _) (Nat.le_max_right _ _)
  by_cases hs : k ≤ 2
  · omega
  have hb : a + k ≤ L + 1 := by
    simpa only [nextWidth, hc, Nat.one_ne_zero, if_false] using hbound
  have hout : ∀ i, a ≤ i → i < a + k →
      0 < i ∧ i < L ∧ output q i = 0 ∧ backOutput q L (i - 1) = 0 := by
    intro i hia hik
    exact next_zero_overflow q L i ha.1 hc (by omega) (hzero i hia hik)
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
  · have hmass := interval_nine_mass q L a (k - 1) (by omega) hn
    omega

/-- The common budget needs only the quotient of the mass by nine. -/
theorem zeroBound_next_preserved (q : Nat → Nat) (L M K : Nat)
    (ha : Admissible L q) (hm : wordSum q L ≤ M)
    (hz : ZeroBound q L K) (hsmall : 2 ≤ K) (hquot : M / 9 + 1 ≤ K) :
    ZeroBound (nextColumns q L) (nextWidth q L) K := by
  by_cases hc : carry q L = 0
  · have hh := zeroBound_next_nooverflow_exact q L M K ha hm hz hc
    intro a k hk hb hz'
    have ht := hh a k hk hb hz'
    have hmax : max K (max 1 (M / 9)) ≤ K := by omega
    omega
  · have hcb := carry_bounded q L ha.2.2.1 L (by omega)
    have hc1 : carry q L = 1 := by omega
    have hh := zeroBound_next_overflow_exact q L M K ha hm hz hc1
    intro a k hk hb hz'
    have ht := hh a k hk hb hz'
    have hmax : max (K - 1) (max 2 (M / 9 + 1)) ≤ K := by omega
    omega

#print axioms interval_nine_mass
#print axioms zeroBound_next_nooverflow_exact
#print axioms zeroBound_next_overflow_exact
#print axioms zeroBound_next_preserved

end Agent104.ExactZeroGap
