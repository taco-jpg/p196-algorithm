import P196.Agent2SaturatedProfile.CertificateAccounting

/-! Exact feasibility of cyclic lower bounds.  The increments are signed;
the threshold witnesses themselves are natural numbers, as in Agent109.Link.
No return certificate or decimal Lychrel witness is supplied. -/
namespace Agent218.ThresholdFeasibility

open Agent110.Accounting

/-- A finite collection of integer values has a common integer translate
above the requested floor. -/
theorem finite_translate (f : Nat → Int) (P : Nat) (floor : Int) :
    ∃ M : Int, ∀ i, i < P → floor ≤ M + f i := by
  induction P with
  | zero => exact ⟨0, by intro i hi; omega⟩
  | succ P ih =>
    obtain ⟨M, hM⟩ := ih
    refine ⟨max M (floor - f P), ?_⟩
    intro i hi
    have hleft : M ≤ max M (floor - f P) := Int.le_max_left _ _
    have hright : floor - f P ≤ max M (floor - f P) := Int.le_max_right _ _
    by_cases h : i < P
    · have := hM i h; omega
    · have : i = P := by omega
      subst i
      omega

/-- Integer thresholds round to natural thresholds without changing any
active value, because the floor is nonnegative. -/
theorem naturalize (b : Nat → Int) (P : Nat) (floor : Nat)
    (h : ∀ i, i < P → (floor : Int) ≤ b i) :
    ∀ i, i < P → ((b i).toNat : Int) = b i := by
  intro i hi
  have hb := h i hi
  exact Int.toNat_of_nonneg (by omega)

/-- The exact checker-shaped feasibility condition for one cyclic band. -/
def Feasible (P : Nat) (floor : Nat) (d : Nat → Int) : Prop :=
  ∃ lo : Nat → Nat, (∀ i, i < P → floor ≤ lo i) ∧
    ∀ i, i < P → (lo ((i + 1) % P) : Int) ≤ (lo i : Int) + d i

/-- Cyclic lower bounds exist exactly when the total signed increment is
nonnegative. The construction is a translated prefix-sum potential. -/
theorem feasible_iff_total_nonnegative (P : Nat) (hP : 0 < P)
    (floor : Nat) (d : Nat → Int) :
    Feasible P floor d ↔ 0 ≤ sumPrefix d P := by
  constructor
  · rintro ⟨lo, _, hlo⟩
    have hsum := sumPrefix_le P
      (f := fun i => (lo ((i + 1) % P) : Int) - (lo i : Int))
      (g := d) (by intro i hi; have := hlo i hi; dsimp; omega)
    rw [sumPrefix_cyclic_difference (fun i => (lo i : Int)) P] at hsum
    exact hsum
  · intro htotal
    obtain ⟨M, hM⟩ := finite_translate (sumPrefix d) P (floor : Int)
    let b : Nat → Int := fun i => M + sumPrefix d i
    let lo : Nat → Nat := fun i => (b i).toNat
    have hb : ∀ i, i < P → (lo i : Int) = b i :=
      naturalize b P floor hM
    refine ⟨lo, ?_, ?_⟩
    · intro i hi
      have hh := hM i hi
      have he := hb i hi
      dsimp [b] at he
      omega
    · intro i hi
      rw [hb i hi, hb ((i + 1) % P) (Nat.mod_lt _ hP)]
      by_cases hnext : i + 1 < P
      · rw [Nat.mod_eq_of_lt hnext]
        simp only [b, sumPrefix]
        omega
      · have hlast : i + 1 = P := by omega
        rw [hlast, Nat.mod_self]
        have he : sumPrefix d P = sumPrefix d i + d i := by
          rw [← hlast]
          rfl
        simp only [b, sumPrefix]
        omega

/-- Independent outer and inner lower bounds impose exactly the two total
gain inequalities, with no additional coupled feasibility condition. -/
theorem two_band_feasible_iff (P : Nat) (hP : 0 < P)
    (d e : Nat → Int) :
    (Feasible P 2 d ∧ Feasible P 2 e) ↔
      (0 ≤ sumPrefix d P ∧ 0 ≤ sumPrefix e P) := by
  rw [feasible_iff_total_nonnegative P hP 2 d,
    feasible_iff_total_nonnegative P hP 2 e]

/-- The four exact natural-number lower-bound clauses in `LocalOK`, with
all states and trimming counts held fixed. -/
def ThresholdsFit (cert : Agent109.Cert.Certificate) : Prop :=
  ∃ lo hi : Nat → Nat, ∀ i, i < cert.P →
    2 ≤ lo i ∧ 2 ≤ hi i ∧
    lo ((i + 1) % cert.P) + 2 ≤ lo i + Agent109.Cert.gam (cert.st i) +
      (cert.lk i).j + (cert.lk i).j1 ∧
    hi ((i + 1) % cert.P) + 2 ≤ hi i + Agent109.Cert.gam (cert.st i) +
      (cert.lk i).j2 + (cert.lk i).k

/-- Exact specialization to the existing return checker: its four threshold
clauses can be filled exactly when both cycle gains are nonnegative. -/
theorem thresholdsFit_iff (cert : Agent109.Cert.Certificate) (hP : 0 < cert.P) :
    ThresholdsFit cert ↔ 0 ≤ totalG cert ∧ 0 ≤ totalH cert := by
  have he := two_band_feasible_iff cert.P hP
    (fun i => dg (cert.st i) (cert.lk i))
    (fun i => dh (cert.st i) (cert.lk i))
  change _ ↔ 0 ≤ totalG cert ∧ 0 ≤ totalH cert at he
  rw [← he]
  constructor
  · rintro ⟨lo, hi, hh⟩
    constructor
    · refine ⟨lo, ?_, ?_⟩
      · intro i hi'; exact (hh i hi').1
      · intro i hi'
        have h := (hh i hi').2.2.1
        dsimp [dg]
        omega
    · refine ⟨hi, ?_, ?_⟩
      · intro i hi'; exact (hh i hi').2.1
      · intro i hi'
        have h := (hh i hi').2.2.2
        dsimp [dh]
        omega
  · rintro ⟨⟨lo, hlo, hg⟩, ⟨hi, hhi, hh⟩⟩
    refine ⟨lo, hi, ?_⟩
    intro i hi'
    have hg' := hg i hi'
    have hh' := hh i hi'
    dsimp [dg] at hg'
    dsimp [dh] at hh'
    exact ⟨hlo i hi', hhi i hi', by omega, by omega⟩

end Agent218.ThresholdFeasibility

#print axioms Agent218.ThresholdFeasibility.feasible_iff_total_nonnegative
#print axioms Agent218.ThresholdFeasibility.two_band_feasible_iff
#print axioms Agent218.ThresholdFeasibility.thresholdsFit_iff
