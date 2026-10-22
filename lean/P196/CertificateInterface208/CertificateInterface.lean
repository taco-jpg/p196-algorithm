import P196.CertificateInterface208.RankLifting
import P196.Agent2SaturatedProfile.CertificatePhases

/-! A checked complementary return certificate must contain an interface
of length at least three. The exclusion uses the full local interface update
with arbitrary carry bits; no exterior projection or growth premise is added. -/
namespace Agent208.Interface
open Agent109 Agent109.Cert

/-- Projection of an accepted local link to the independently checked rank. -/
theorem local_rank_decreases (s s' : State) (L L' : Link)
    (h : LocalOK s s' L L') (he : s.c % 2 = 0)
    (hlen : s.A.length ≤ 2) (hlen' : s'.A.length ≤ 2) :
    rank s'.c s'.A < rank s.c s.A := by
  obtain ⟨hc, hB, hA, hC, hp, hBr, hAr, hCr, hnp, hlo, hlo', hg, hh⟩ := h
  have ht : raw s.c s.A (data s.c s.B s.A s.C).γ =
      List.replicate L.j1 (tOf s.c + tOf s.c) ++ s'.A ++
      List.replicate L.j2 (18 - (tOf s.c + tOf s.c)) := by
    rw [← Ar_eq_raw, hp]
    exact hAr
  have hr := rank_decreases s.c s.A s'.A _ L.j1 L.j2 hc he hA hlen
    (gamma_le s.c s.B s.A s.C hB) hlen' ht
  rwa [hp] at hr

/-- Every valid certificate contains a finite interface with at least three
coefficients. The result permits arbitrary finite B and C, arbitrary period,
nonmaximal trims, either phase cycle and all permitted carry schedules. -/
theorem valid_has_wide_interface (cert : Certificate) (hv : Valid cert) :
    ∃ i, i < cert.P ∧ 3 ≤ (cert.st i).A.length := by
  apply Classical.byContradiction
  intro hn
  have hshort : ∀ i, i < cert.P → (cert.st i).A.length ≤ 2 := by
    intro i hi
    have hn' : ¬ 3 ≤ (cert.st i).A.length := fun h => hn ⟨i, hi, h⟩
    omega
  let r := fun i => rank (cert.st (i % cert.P)).c (cert.st (i % cert.P)).A
  have hstep : ∀ i, i < cert.P → r (i + 1) < r i := by
    intro i hi
    have hnxt : (i + 1) % cert.P < cert.P := Nat.mod_lt _ hv.1
    have h := local_rank_decreases _ _ _ _ (hv.2 i hi)
      (Agent110.Phases.valid_phase_even cert hv i hi)
      (hshort i hi) (hshort _ hnxt)
    simpa only [r, Nat.mod_eq_of_lt hi] using h
  have hchain : ∀ n, n ≤ cert.P → r n + n ≤ r 0 := by
    intro n hn
    induction n with
    | zero => omega
    | succ n ih =>
      have hp := ih (by omega)
      have hs := hstep n (by omega)
      omega
  have hend := hchain cert.P (Nat.le_refl _)
  have heq : r cert.P = r 0 := by simp [r]
  have hpos := hv.1
  omega

/-- Direct endpoint for the unchanged original Boolean checker. -/
theorem checked_has_wide_interface (cert : Certificate) (hc : check cert = true) :
    ∃ i, i < cert.P ∧ 3 ≤ (cert.st i).A.length :=
  valid_has_wide_interface cert (check_sound cert hc)

/-- All-interface-cap-two certificates are rejected. -/
theorem short_interfaces_rejected (cert : Certificate)
    (hshort : ∀ i, i < cert.P → (cert.st i).A.length ≤ 2) : check cert = false := by
  cases hc : check cert with
  | false => rfl
  | true =>
    obtain ⟨i, hi, hw⟩ := checked_has_wide_interface cert hc
    have hs := hshort i hi
    omega

end Agent208.Interface
#print axioms Agent208.Interface.local_rank_decreases
#print axioms Agent208.Interface.valid_has_wide_interface
#print axioms Agent208.Interface.checked_has_wide_interface
#print axioms Agent208.Interface.short_interfaces_rejected
