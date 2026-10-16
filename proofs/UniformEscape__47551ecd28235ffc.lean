import ProfileIsolation

/-!
Uniform escape from a prescribed mass ceiling for concrete decimal
half-line profiles.  The escape horizon depends only on the ceiling,
not on the support width of the initial profile.
-/

namespace DecimalProfile

open DecimalDigits DecimalMass DecimalZeroGap DecimalUnboundedMass

/-- A deliberately coarse, computable horizon for uniform mass escape. -/
def escapeBound : Nat → Nat
  | 0 => 0
  | M + 1 => 4 * ((M + 2) * (2 * escapeBound M + M + 5)) + 5

theorem escapeBound_le_succ (M : Nat) :
    escapeBound M ≤ escapeBound (M + 1) := by
  have hm := Nat.mul_le_mul_right (2 * escapeBound M + M + 5)
    (show 1 ≤ M + 2 by omega)
  simp only [Nat.one_mul] at hm
  simp only [escapeBound]
  omega

theorem mass_positive (s : State) (hv : Valid s.1 s.2) : 0 < mass s := by
  have hsum := wordSum_mono_length s.2 1 s.1 (by exact hv.1)
  have hzero := hv.2.1
  simp only [wordSum, Nat.zero_add] at hsum
  exact Nat.lt_of_lt_of_le hzero hsum

/-- A failed zero-run bound supplies an actual interval, with both ends
strictly inside a valid profile. -/
theorem long_zero_interval (L : Nat) (q : Nat → Nat) (K : Nat)
    (hv : Valid L q) (hz : ¬ ZeroBound q L K) :
    ∃ a k, K < k ∧ 0 < a ∧ a + k < L ∧
      (∀ i, a ≤ i → i < a + k → q i = 0) := by
  have hex : ∃ a k, K < k ∧ a + k ≤ L ∧
      (∀ i, a ≤ i → i < a + k → q i = 0) := by
    apply Classical.byContradiction
    intro hn
    apply hz
    intro a k hk hlen hzero
    by_cases hlarge : K < k
    · exact False.elim (hn ⟨a, k, hlarge, hlen, hzero⟩)
    · omega
  obtain ⟨a, k, hk, hlen, hzero⟩ := hex
  have ha : 0 < a := by
    by_cases ha0 : a = 0
    · have hq0 := hzero 0 (by omega) (by omega)
      have hpos := hv.2.1
      omega
    · omega
  have hend : a + k < L := by
    by_cases hlast : a + k = L
    · have hqend := hzero (L - 1) (by omega) (by omega)
      have hpos := hv.2.2.2.2
      omega
    · omega
  exact ⟨a, k, hk, ha, hend, hzero⟩

/-- The nonzero finite prefix can be trimmed to its exact last position. -/
theorem prefix_last_positive (q : Nat → Nat) (a : Nat)
    (hzero : 0 < q 0) (ha : 0 < a) :
    ∃ A, 0 < A ∧ A ≤ a ∧ 0 < q (A - 1) ∧
      (∀ i, A ≤ i → i < a → q i = 0) := by
  induction a with
  | zero => omega
  | succ a ih =>
    by_cases hqa : 0 < q a
    · refine ⟨a + 1, by omega, by omega, ?_, ?_⟩
      · simpa using hqa
      · intro i hlo hhi
        omega
    · have ha' : 0 < a := by
        by_cases heq : a = 0
        · subst a
          omega
        · omega
      obtain ⟨A, hA, hAa, hpos, htail⟩ := ih ha'
      refine ⟨A, hA, by omega, hpos, ?_⟩
      intro i hlo hhi
      by_cases hi : i < a
      · exact htail i hlo hi
      · have heq : i = a := by omega
        subst i
        omega

/-- A sufficiently long internal zero interval splits off a valid left
profile and a nonzero right component with the required separation. -/
theorem long_gap_split (L : Nat) (q : Nat → Nat) (T : Nat)
    (hv : Valid L q) (hz : ¬ ZeroBound q L (2 * T + 1)) :
    ∃ (A D : Nat) (p v : Nat → Nat),
      Valid A p ∧
      (∀ i, q i = p i + v i) ∧
      (∀ i, i < D → v i = 0) ∧
      (∃ i, 0 < v i) ∧ A + 2 * T + 2 ≤ D := by
  obtain ⟨a, k, hk, ha, hlen, hzero⟩ := long_zero_interval L q (2 * T + 1) hv hz
  obtain ⟨A, hA, hAa, hpos, htail⟩ := prefix_last_positive q a hv.2.1 ha
  let p : Nat → Nat := fun i => if i < A then q i else 0
  let v : Nat → Nat := fun i => if i < A then 0 else q i
  have hp : Valid A p := by
    refine ⟨hA, ?_, ?_, ?_, ?_⟩
    · simpa only [p, if_pos hA] using hv.2.1
    · intro i
      dsimp [p]
      split
      · exact hv.2.2.1 i
      · omega
    · intro i hi
      simp only [p, if_neg (by omega : ¬ i < A)]
    · simpa only [p, if_pos (by omega : A - 1 < A)] using hpos
  refine ⟨A, a + k, p, v, hp, ?_, ?_, ?_, by omega⟩
  · intro i
    by_cases hi : i < A <;> simp [p, v, hi]
  · intro i hi
    by_cases hiA : i < A
    · simp only [v, if_pos hiA]
    · simp only [v, if_neg hiA]
      by_cases hia : i < a
      · exact htail i (by omega) hia
      · exact hzero i (by omega) hi
  · refine ⟨L - 1, ?_⟩
    simpa only [v, if_neg (by omega : ¬ L - 1 < A)] using hv.2.2.2.2

/-- The same zero-run budget persists throughout a finite bounded-mass
prefix of the concrete profile orbit. -/
theorem bounded_prefix_zeroBound (s : State) (hv : Valid s.1 s.2)
    (M K N : Nat) (hK : M + 2 ≤ K)
    (hzero : ZeroBound s.2 s.1 K)
    (hm : ∀ t, t ≤ N → mass (iter s t) ≤ M) :
    ∀ t, t ≤ N → ZeroBound (iter s t).2 (iter s t).1 K := by
  intro t
  induction t with
  | zero =>
    intro _
    exact hzero
  | succ t ih =>
    intro ht
    exact zeroBound_phi (iter s t).2 (iter s t).1 M K
      (iter_valid s t hv) (hm t (by omega)) (ih (by omega)) hK

/-- Finite counting converts mass and zero-run bounds into a width bound. -/
theorem bounded_prefix_width (s : State) (hv : Valid s.1 s.2)
    (M K N : Nat) (hK : M + 2 ≤ K)
    (hzero : ZeroBound s.2 s.1 K)
    (hm : ∀ t, t ≤ N → mass (iter s t) ≤ M) :
    ∀ t, t ≤ N → (iter s t).1 ≤ (M + 1) * (K + 1) := by
  intro t ht
  exact length_le_of_mass_zero_runs (iter s t).2 (iter s t).1 M K
    (hm t ht) (bounded_prefix_zeroBound s hv M K N hK hzero hm t ht)

/-- Every concrete finite anchored decimal profile exceeds each mass
ceiling by a time depending only on that ceiling. No initial mass or
initial width restriction is assumed. -/
theorem uniform_escape (s : State) (hv : Valid s.1 s.2) (M : Nat) :
    ∃ t, t ≤ escapeBound M ∧ M < mass (iter s t) := by
  induction M generalizing s with
  | zero =>
    exact ⟨0, Nat.le_refl 0, mass_positive s hv⟩
  | succ M ih =>
    apply Classical.byContradiction
    intro hnone
    have hm : ∀ t, t ≤ escapeBound (M + 1) → mass (iter s t) ≤ M + 1 := by
      intro t ht
      by_cases hgt : M + 1 < mass (iter s t)
      · exact False.elim (hnone ⟨t, ht, hgt⟩)
      · omega
    let T := escapeBound M
    let K := 2 * T + M + 4
    let H := (M + 2) * (K + 1)
    have hK : (M + 1) + 2 ≤ K := by dsimp [K]; omega
    have htime : escapeBound (M + 1) = 4 * H + 5 := by
      simp only [escapeBound, H, K, T, Nat.add_assoc]
    by_cases hz : ZeroBound s.2 s.1 K
    · have hwidth := bounded_prefix_width s hv (M + 1) K
        (escapeBound (M + 1)) hK hz hm
        (escapeBound (M + 1)) (Nat.le_refl _)
      have hclock := iter_width_clock s (escapeBound (M + 1)) hv
      change (iter s (escapeBound (M + 1))).1 ≤ H at hwidth
      omega
    · have hzsmall : ¬ ZeroBound s.2 s.1 (2 * T + 1) := by
        intro hsmall
        apply hz
        intro a k hk hlen hzero
        have hbound := hsmall a k hk hlen hzero
        dsimp [K]
        omega
      obtain ⟨A, D, p, v, hp, heq, hvz, hvnon, hgap⟩ :=
        long_gap_split s.1 s.2 T hv hzsmall
      have hisolate := isolated_mass s.2 p v s.1 A D T hv hp heq hvz hvnon hgap
      obtain ⟨t, ht, hgt⟩ := ih (A, p) hp
      have hpart := hisolate t ht
      change mass (iter (A, p) t) + 1 ≤ mass (iter s t) at hpart
      have hwhole := hm t (Nat.le_trans ht (escapeBound_le_succ M))
      omega

#print axioms uniform_escape

end DecimalProfile
