import CertificateCarryBudget
import PrefixModel

namespace Agent110.CertificatePrefix

open Agent109 Agent109.Cert
open P196.Agent4.Saturation (Prefix advance)

/-- The first three exterior coefficients, continued by the constant band. -/
def padPrefix (B : Word) (c : Nat) : Prefix :=
  ⟨B.getD 0 c, B.getD 1 c, B.getD 2 c⟩

def statePrefix (s : State) : Prefix := padPrefix s.B s.c

theorem prefix_a (s : State) : (statePrefix s).a = CarryBudget.exterior s := by
  cases he : s.B <;> simp [statePrefix, padPrefix, CarryBudget.exterior, he]

theorem getD_bounded (B : Word) (c i : Nat) (hB : Bounded B) (hc : c ≤ 18) :
    B.getD i c ≤ 18 := by
  induction B generalizing i with
  | nil => simpa using hc
  | cons a as ih =>
    cases i with
    | zero => simpa using hB a (by simp)
    | succ i =>
      apply ih
      intro x hx; exact hB x (by simp [hx])

theorem prefix_bounds (s : State) (hc : Phase s.c) (hB : Bounded s.B) :
    (statePrefix s).a ≤ 18 ∧ (statePrefix s).b ≤ 18 ∧ (statePrefix s).c ≤ 18 := by
  have hc18 : s.c ≤ 18 := by have := hc.2.1; omega
  exact ⟨getD_bounded _ _ _ hB hc18, getD_bounded _ _ _ hB hc18,
    getD_bounded _ _ _ hB hc18⟩

theorem getD_replicate_default (c j i : Nat) : (List.replicate j c).getD i c = c := by
  induction j generalizing i with
  | zero => simp
  | succ j ih =>
    cases i with
    | zero => simp [List.replicate_succ]
    | succ i => simpa only [List.replicate_succ] using ih i

theorem getD_append_replicate (B : Word) (c j i : Nat) :
    (B ++ List.replicate j c).getD i c = B.getD i c := by
  induction B generalizing i with
  | nil => exact getD_replicate_default c j i
  | cons a as ih =>
    cases i with
    | zero => rfl
    | succ i => exact ih i

/-- Arbitrary suffix trimming leaves the band-padded prefix unchanged. -/
theorem padPrefix_trim (B : Word) (c j : Nat) :
    padPrefix (B ++ List.replicate j c) c = padPrefix B c := by
  unfold padPrefix
  rw [getD_append_replicate, getD_append_replicate, getD_append_replicate]

theorem band_arithmetic (c e : Nat) (hc : Phase c) (he : e ≤ 1) :
    (c + e) / 10 = kOf c ∧ (c + e) % 10 = c + e - 10 * kOf c := by
  unfold Phase at hc
  unfold kOf
  split <;> omega

theorem raw_prefix_empty (c : Nat) (A C : Word) (hc : Phase c) :
    advance (padPrefix [] c) (kOf c) =
      (padPrefix (Br c [] A C) (tOf c + tOf c), (data c [] A C).γ) := by
  have hc1 := hc.1
  have hc2 := hc.2.1
  have hc9 := hc.2.2
  by_cases hk : 10 ≤ c
  · have hcdiv : c / 10 = 1 := by omega
    have hcadd : (c + 1) / 10 = 1 := by omega
    simp [padPrefix, advance, Br, data, norm, kOf, hk, tOf, u0,
      zipAdd, hcdiv, hcadd]
    omega
  · have hcdiv : c / 10 = 0 := by omega
    simp [padPrefix, advance, Br, data, norm, kOf, hk, tOf, u0,
      zipAdd, hcdiv]
    omega

theorem raw_prefix_single (c a : Nat) (A C : Word) (hc : Phase c) (ha : a ≤ 18) :
    advance (padPrefix [a] c) (kOf c) =
      (padPrefix (Br c [a] A C) (tOf c + tOf c), (data c [a] A C).γ) := by
  have hk : kOf c ≤ 1 := by unfold kOf; split <;> omega
  have hband := band_arithmetic c (kOf c) hc hk
  have hband0 := band_arithmetic c (a / 10) hc (by omega)
  simp only [padPrefix, advance, Br, data, norm, List.reverse_cons,
    List.reverse_nil, List.nil_append, List.cons_append, List.append_nil,
    Nat.add_zero, hband.1, hband0.1]
  by_cases hg : (a + kOf c) / 10 = 0
  · simp [hg, zipAdd, u0, data, norm, tOf]
    omega
  · simp [hg, zipAdd, u0, data, norm, tOf]
    omega

theorem raw_prefix_double (c a b : Nat) (A C : Word) (hc : Phase c)
    (ha : a ≤ 18) (hb : b ≤ 18) :
    advance (padPrefix [a,b] c) (kOf c) =
      (padPrefix (Br c [a,b] A C) (tOf c + tOf c), (data c [a,b] A C).γ) := by
  have hk : kOf c ≤ 1 := by unfold kOf; split <;> omega
  have hband := band_arithmetic c (kOf c) hc hk
  have he : (b + a / 10) / 10 ≤ 1 := by omega
  have hband0 := band_arithmetic c ((b + a / 10) / 10) hc he
  simp only [padPrefix, advance, Br, data, norm, List.reverse_cons,
    List.reverse_nil, List.nil_append, List.cons_append, List.append_nil,
    Nat.add_zero, hband.1]
  by_cases hg : (a + (b + kOf c) / 10) / 10 = 0
  · simp [hg, zipAdd, u0, data, norm, tOf]
    omega
  · simp [hg, zipAdd, u0, data, norm, tOf]
    omega

theorem raw_prefix_long (c a b d : Nat) (bs A C : Word) :
    advance (padPrefix (a :: b :: d :: bs) c) (norm bs.reverse (kOf c)).2 =
      (padPrefix (Br c (a :: b :: d :: bs) A C) (tOf c + tOf c),
        (data c (a :: b :: d :: bs) A C).γ) := by
  simp only [padPrefix, advance, Br, data, norm, List.reverse_cons,
    norm_append, List.reverse_append, List.reverse_reverse,
    List.reverse_nil, List.nil_append, List.cons_append, List.append_nil,
    Nat.add_zero]
  split <;> simp_all [zipAdd]

theorem raw_prefix_step (c : Nat) (B A C : Word) (hc : Phase c) (hB : Bounded B) :
    ∃ e, e ≤ 1 ∧ advance (padPrefix B c) e =
      (padPrefix (Br c B A C) (tOf c + tOf c), (data c B A C).γ) := by
  have hk : kOf c ≤ 1 := by unfold kOf; split <;> omega
  cases B with
  | nil => exact ⟨kOf c, hk, raw_prefix_empty c A C hc⟩
  | cons a bs =>
    have ha := hB a (by simp)
    cases bs with
    | nil => exact ⟨kOf c, hk, raw_prefix_single c a A C hc ha⟩
    | cons b bs =>
      have hb := hB b (by simp)
      cases bs with
      | nil => exact ⟨kOf c, hk, raw_prefix_double c a b A C hc ha hb⟩
      | cons d bs =>
        refine ⟨(norm bs.reverse (kOf c)).2, ?_, raw_prefix_long c a b d bs A C⟩
        apply norm_carry_le _ _ _ hk
        apply bounded_reverse
        intro x hx; exact hB x (by simp [hx])

/-- Exact three-column projection for every accepted local certificate link,
including empty exteriors and any amount of suffix trimming. -/
theorem local_prefix_step (s s' : State) (L L' : Link)
    (hl : LocalOK s s' L L') :
    ∃ e, e ≤ 1 ∧ advance (statePrefix s) e = (statePrefix s', gam s) := by
  obtain ⟨e, he, hs⟩ := raw_prefix_step s.c s.B s.A s.C hl.1 hl.2.1
  have hc := hl.2.2.2.2.1
  have ht := hl.2.2.2.2.2.1
  rw [hc, ht, padPrefix_trim] at hs
  exact ⟨e, he, hs⟩

end Agent110.CertificatePrefix

#print axioms Agent110.CertificatePrefix.prefix_a
#print axioms Agent110.CertificatePrefix.getD_bounded
#print axioms Agent110.CertificatePrefix.prefix_bounds
#print axioms Agent110.CertificatePrefix.getD_replicate_default
#print axioms Agent110.CertificatePrefix.getD_append_replicate
#print axioms Agent110.CertificatePrefix.padPrefix_trim
#print axioms Agent110.CertificatePrefix.band_arithmetic
#print axioms Agent110.CertificatePrefix.raw_prefix_empty
#print axioms Agent110.CertificatePrefix.raw_prefix_single
#print axioms Agent110.CertificatePrefix.raw_prefix_double
#print axioms Agent110.CertificatePrefix.raw_prefix_long
#print axioms Agent110.CertificatePrefix.raw_prefix_step
#print axioms Agent110.CertificatePrefix.local_prefix_step
