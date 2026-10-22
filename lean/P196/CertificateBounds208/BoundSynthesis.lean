import P196.Agent2SaturatedProfile.CertificateAccounting
import P196.Drafts.Agent109TemplateStepSafety.NoPalStep
import P196.CertificateToLychrel.AdmissibleHeads

/-!
Agent 208: exact synthesis of the original return-checker lower bounds.
The finite structural return equations imply the safety guard by the existing
Agent109.NoPal theorem. Bounds exist exactly when both total signed gains are
nonnegative. This supplies no structural cycle or Lychrel witness.
-/

namespace Agent208.CertificateBounds

open Agent109 Agent109.Cert Agent110.Accounting

/-- Minimum of the prefix sums, including the empty prefix. -/
def prefixFloor (f : Nat → Int) : Nat → Int
  | 0 => 0
  | n + 1 =>
      if prefixFloor f n ≤ sumPrefix f (n + 1)
      then prefixFloor f n else sumPrefix f (n + 1)

theorem prefixFloor_le (f : Nat → Int) (n i : Nat) (hi : i ≤ n) :
    prefixFloor f n ≤ sumPrefix f i := by
  induction n with
  | zero =>
      have he : i = 0 := by omega
      subst i
      exact Int.le_refl _
  | succ n ih =>
      by_cases hin : i ≤ n
      · have hp := ih hin
        simp only [prefixFloor]
        split <;> omega
      · have he : i = n + 1 := by omega
        subst i
        simp only [prefixFloor]
        split <;> omega

/-- Explicit natural lower bound for each point of a finite gain cycle. -/
def boundAt (f : Nat → Int) (P i : Nat) : Nat :=
  (2 + sumPrefix f i - prefixFloor f P).toNat

theorem boundAt_cast (f : Nat → Int) (P i : Nat) (hi : i ≤ P) :
    (boundAt f P i : Int) = 2 + sumPrefix f i - prefixFloor f P := by
  have hf := prefixFloor_le f P i hi
  exact Int.toNat_of_nonneg (by omega)

theorem boundAt_ge_two (f : Nat → Int) (P i : Nat) (hi : i ≤ P) :
    2 ≤ boundAt f P i := by
  have he := boundAt_cast f P i hi
  have hf := prefixFloor_le f P i hi
  omega

theorem boundAt_cyclic (f : Nat → Int) (P : Nat) (hp : 0 < P)
    (hs : 0 ≤ sumPrefix f P) (i : Nat) (hi : i < P) :
    (boundAt f P ((i + 1) % P) : Int) ≤ (boundAt f P i : Int) + f i := by
  have hi' : i ≤ P := by omega
  have hn : (i + 1) % P ≤ P := Nat.le_of_lt (Nat.mod_lt _ hp)
  rw [boundAt_cast f P _ hn, boundAt_cast f P i hi']
  by_cases hlast : i + 1 < P
  · rw [Nat.mod_eq_of_lt hlast, sumPrefix]
    omega
  · have he : i + 1 = P := by omega
    rw [he, Nat.mod_self]
    have hx : sumPrefix f P = sumPrefix f i + f i := by rw [← he]; rfl
    simp only [sumPrefix]
    omega

/-- The lower-bound difference constraints on a cycle are feasible exactly
when its total signed increment is nonnegative. -/
theorem cyclic_bounds_iff (f : Nat → Int) (P : Nat) (hp : 0 < P) :
    (∃ b : Nat → Nat, (∀ i < P, 2 ≤ b i) ∧
      ∀ i < P, (b ((i + 1) % P) : Int) ≤ (b i : Int) + f i) ↔
    0 ≤ sumPrefix f P := by
  constructor
  · rintro ⟨b, _, hb⟩
    have hsum := sumPrefix_le P
      (f := fun i => (b ((i + 1) % P) : Int) - (b i : Int))
      (g := f) (fun i hi => by
        have hh := hb i hi
        dsimp
        omega)
    rw [sumPrefix_cyclic_difference (fun i => (b i : Int)) P] at hsum
    exact hsum
  · intro hs
    refine ⟨boundAt f P, ?_, ?_⟩
    · intro i hi
      exact boundAt_ge_two f P i (by omega)
    · exact boundAt_cyclic f P hp hs

/-- The original exact local phase/block equations, without redundant safety
or the two lower-bound fields. -/
def StructuralLocal (s s' : State) (L : Link) : Prop :=
  Phase s.c ∧ Bounded s.B ∧ Bounded s.A ∧ Bounded s.C ∧
  tOf s.c + tOf s.c = s'.c ∧
  Br s.c s.B s.A s.C = s'.B ++ List.replicate L.j s'.c ∧
  Ar s.c s.B s.A s.C =
    List.replicate L.j1 s'.c ++ s'.A ++ List.replicate L.j2 (18 - s'.c) ∧
  Cr s.c s.B s.A s.C =
    List.replicate L.k (18 - s'.c) ++ s'.C ++ List.replicate L.k (18 - s'.c)

def StructuralValid (cert : Certificate) : Prop :=
  0 < cert.P ∧ ∀ i < cert.P,
    StructuralLocal (cert.st i) (cert.st ((i + 1) % cert.P)) (cert.lk i)

/-- Keep all states and all four trims; synthesize exactly one link per state. -/
def withBounds (cert : Certificate) (b h : Nat → Nat) : Certificate :=
  { states := cert.states,
    links := (List.range cert.P).map fun i => { cert.lk i with lo := b i, lo' := h i } }

@[simp] theorem withBounds_P (cert : Certificate) (b h : Nat → Nat) :
    (withBounds cert b h).P = cert.P := rfl

@[simp] theorem withBounds_st (cert : Certificate) (b h : Nat → Nat) (i : Nat) :
    (withBounds cert b h).st i = cert.st i := rfl

theorem withBounds_lk (cert : Certificate) (b h : Nat → Nat) (i : Nat)
    (hi : i < cert.P) :
    (withBounds cert b h).lk i = { cert.lk i with lo := b i, lo' := h i } := by
  simp [withBounds, Certificate.lk, List.getD_eq_getElem?_getD,
    List.getElem?_map, hi]

theorem valid_structural (cert : Certificate) (hv : Valid cert) : StructuralValid cert := by
  refine ⟨hv.1, ?_⟩
  intro i hi
  obtain ⟨hc, hB, hA, hC, hn, hBr, hAr, hCr, _⟩ := hv.2 i hi
  exact ⟨hc, hB, hA, hC, hn, hBr, hAr, hCr⟩

theorem structural_withBounds (cert : Certificate) (b h : Nat → Nat) :
    StructuralValid (withBounds cert b h) ↔ StructuralValid cert := by
  unfold StructuralValid
  simp only [withBounds_P, withBounds_st]
  constructor
  · rintro ⟨hp, hv⟩
    refine ⟨hp, ?_⟩
    intro i hi
    have hh := hv i hi
    rw [withBounds_lk cert b h i hi] at hh
    exact hh
  · rintro ⟨hp, hv⟩
    refine ⟨hp, ?_⟩
    intro i hi
    rw [withBounds_lk cert b h i hi]
    exact hv i hi

theorem gainG_withBounds (cert : Certificate) (b h : Nat → Nat) :
    totalG (withBounds cert b h) = totalG cert := by
  unfold totalG
  simp only [withBounds_P, withBounds_st]
  apply sumPrefix_congr
  intro i hi
  rw [withBounds_lk cert b h i hi]
  rfl

theorem gainH_withBounds (cert : Certificate) (b h : Nat → Nat) :
    totalH (withBounds cert b h) = totalH cert := by
  unfold totalH
  simp only [withBounds_P, withBounds_st]
  apply sumPrefix_congr
  intro i hi
  rw [withBounds_lk cert b h i hi]
  rfl

/-- Original checker completeness; this changes no checker definition. -/
theorem check_of_valid (cert : Certificate) (hv : Valid cert) : check cert = true := by
  unfold check
  simp only [Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, List.mem_range]
  exact hv

theorem synthesize_valid (cert : Certificate) (hc : StructuralValid cert)
    (hG : 0 ≤ totalG cert) (hH : 0 ≤ totalH cert) :
    Valid (withBounds cert
      (boundAt (fun i => dg (cert.st i) (cert.lk i)) cert.P)
      (boundAt (fun i => dh (cert.st i) (cert.lk i)) cert.P)) := by
  let b := boundAt (fun i => dg (cert.st i) (cert.lk i)) cert.P
  let h := boundAt (fun i => dh (cert.st i) (cert.lk i)) cert.P
  change Valid (withBounds cert b h)
  refine ⟨hc.1, ?_⟩
  intro i hi
  have hn : (i + 1) % cert.P < cert.P := Nat.mod_lt _ hc.1
  simp only [withBounds_P, withBounds_st] at hi ⊢
  rw [withBounds_lk cert b h i hi, withBounds_lk cert b h _ hn]
  obtain ⟨hp, hB, hA, hC, hp', hBr, hAr, hCr⟩ := hc.2 i hi
  have hb2 := boundAt_ge_two (fun j => dg (cert.st j) (cert.lk j)) cert.P i
    (by omega)
  have hh2 := boundAt_ge_two (fun j => dh (cert.st j) (cert.lk j)) cert.P i
    (by omega)
  have hbg := boundAt_cyclic (fun j => dg (cert.st j) (cert.lk j)) cert.P hc.1 hG i hi
  have hhg := boundAt_cyclic (fun j => dh (cert.st j) (cert.lk j)) cert.P hc.1 hH i hi
  change 2 ≤ b i at hb2
  change 2 ≤ h i at hh2
  change (b ((i + 1) % cert.P) : Int) ≤ (b i : Int) + dg (cert.st i) (cert.lk i) at hbg
  change (h ((i + 1) % cert.P) : Int) ≤ (h i : Int) + dh (cert.st i) (cert.lk i) at hhg
  refine ⟨hp, hB, hA, hC, hp', hBr, hAr, hCr,
    Agent109.NoPal.not_stepPal _ _ _ _ hp hB hA, hb2, hh2, ?_, ?_⟩
  · unfold dg at hbg
    dsimp
    omega
  · unfold dh at hhg
    dsimp
    omega

/-- Exact elimination of both lower-bound fields and the safety clause:
the original Boolean checker accepts some choice of bounds precisely when the
unchanged structural equations hold and both cyclic signed gains are nonnegative. -/
theorem bounds_exist_iff (cert : Certificate) :
    (∃ b h : Nat → Nat, check (withBounds cert b h) = true) ↔
    StructuralValid cert ∧ 0 ≤ totalG cert ∧ 0 ≤ totalH cert := by
  constructor
  · rintro ⟨b, h, hk⟩
    have hv := check_sound _ hk
    have hs := (structural_withBounds cert b h).mp (valid_structural _ hv)
    have hG := totalG_nonneg _ hv
    have hH := totalH_nonneg _ hv
    rw [gainG_withBounds] at hG
    rw [gainH_withBounds] at hH
    exact ⟨hs, hG, hH⟩
  · rintro ⟨hs, hG, hH⟩
    exact ⟨_, _, check_of_valid _ (synthesize_valid cert hs hG hH)⟩

/-- A structural return with two nonnegative gains suffices for a decimal
Lychrel number, via the unchanged original checker and realization bridge.
This conditional theorem supplies no such structural return. -/
theorem structural_cycle_existence (cert : Certificate) (hs : StructuralValid cert)
    (hG : 0 ≤ totalG cert) (hH : 0 ≤ totalH cert) :
    ∃ m, ∀ k, ¬ Palindrome (orbit m k) := by
  exact Agent112.Admissibility.certificate_existence_of_check _
    (check_of_valid _ (synthesize_valid cert hs hG hH))

end Agent208.CertificateBounds

#print axioms Agent208.CertificateBounds.cyclic_bounds_iff
#print axioms Agent208.CertificateBounds.synthesize_valid
#print axioms Agent208.CertificateBounds.bounds_exist_iff
#print axioms Agent208.CertificateBounds.structural_cycle_existence
