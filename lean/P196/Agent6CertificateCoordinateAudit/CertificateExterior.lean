import P196.Agent6CertificateCoordinateAudit.CertificateRealization
import P196.Agent6CertificateCoordinateAudit.ExteriorNormalization

/-!
Every canonically realizable accepted return certificate must exceed any
exterior cap for which the deterministic outer map has a universal escape
proof.  The accepted cap-two theorem is instantiated below.  Arbitrary partial
certificate trims are normalized before taking the cyclic projection.
-/

namespace Agent116.CertificateExterior

open Agent109 Agent109.Cert Agent109.Outer P196.Agent7.Finite
open Agent116.Exterior

set_option maxHeartbeats 0

/-- The maximally suffix-trimmed exterior of a listed state. -/
def stateOuter (s : State) : Outer := ⟨s.c, stripSuffix s.c s.B⟩

/-- A checked link projects to the exact deterministic outer transition. -/
theorem local_outer_step (s s' : State) (L L' : Link)
    (h : LocalOK s s' L L') : outerNext (stateOuter s) = stateOuter s' := by
  obtain ⟨hc, hB, _, _, hc', hBr, _, _, _, _, _, _, _⟩ := h
  exact outerNext_of_partial_trim s.c s'.c s.B s'.B s.A s.C L.j hc hB hc'.symm hBr

/-- The unbounded outer trajectory is the periodic list of normalized
certificate exteriors, even when the certificate uses nonmaximal trims. -/
theorem certificate_outer_orbit (cert : Certificate) (hv : Valid cert) (n : Nat) :
    outerIterate n (stateOuter (cert.st 0)) = stateOuter (cert.st (n % cert.P)) := by
  rw [outerIterate_eq]
  induction n with
  | zero => simp [outerIter]
  | succ n ih =>
    rw [outerIter, ih]
    have hs := local_outer_step _ _ _ _ (hv.2 (n % cert.P) (Nat.mod_lt n hv.1))
    rw [hs]
    congr 2
    simp [Nat.add_mod]

/-- Every certificate phase, including state zero, is an even periodic phase.
The last link is essential because the checker initially permits odd phases. -/
theorem certificate_phase_index (cert : Certificate) (hv : Valid cert) :
    ∃ p : Fin 8, (cert.st 0).c = 2 * (p.val + 1) := by
  have hP := hv.1
  have hp : cert.P - 1 < cert.P := by omega
  have hwrap : (cert.P - 1 + 1) % cert.P = 0 := by
    have he : cert.P - 1 + 1 = cert.P := by omega
    simp [he]
  obtain ⟨hc, _, _, _, he, _, _, _, _, _, _, _, _⟩ := hv.2 (cert.P - 1) hp
  rw [hwrap] at he
  have ht : 1 ≤ tOf (cert.st (cert.P - 1)).c ∧
      tOf (cert.st (cert.P - 1)).c ≤ 8 := by
    obtain ⟨h1, h17, h9⟩ := hc
    unfold tOf kOf
    split <;> omega
  refine ⟨⟨tOf (cert.st (cert.P - 1)).c - 1, by omega⟩, ?_⟩
  simp only
  omega

/-- Maximal normalization and positive head give the precise finite graph
validity predicate, without an implicit canonicality assumption. -/
theorem stateOuter_valid (s : State) (hb : Bounded s.B)
    (hpos : ∀ b bs, s.B = b :: bs → 0 < b) :
    validOuter (stateOuter s) = true := by
  have hbound := stripSuffix_bounded s.c s.B hb
  have hhead := stripSuffix_head_pos s.c s.B hpos
  have hlast := stripSuffix_last s.c s.B
  unfold validOuter stateOuter
  simp only [Bool.and_eq_true]
  constructor
  ·
    constructor
    · apply List.all_eq_true.mpr
      intro x hx
      exact decide_eq_true (hbound x hx)
    · cases he : stripSuffix s.c s.B with
      | nil => rfl
      | cons a as => simp only; exact decide_eq_true (hhead a as he)
  · cases he : (stripSuffix s.c s.B).getLast? with
    | none => rfl
    | some a => simpa using hlast a he

/-- An escape theorem for all valid even-phase exteriors at the stated cap.
This hypothesis is instantiated by kernel certificates, not by computation
outside Lean. -/
def EscapeAt (cap : Nat) : Prop :=
  ∀ (p : Fin 8) (B : Word), Bounded B →
    validOuter ⟨2 * (p.val + 1), B⟩ = true → B.length ≤ cap →
    ∃ t, cap < (outerIterate t ⟨2 * (p.val + 1), B⟩).B.length

/-- Generic certificate-complexity obstruction with explicit exterior
positivity.  Only state zero's positivity is needed by the escape argument. -/
theorem valid_exceeds_cap (cert : Certificate) (hv : Valid cert)
    (hpos : ∀ b bs, (cert.st 0).B = b :: bs → 0 < b)
    (cap : Nat) (hexit : EscapeAt cap) :
    ∃ i, i < cert.P ∧ cap < (stripSuffix (cert.st i).c (cert.st i).B).length := by
  have hB := (hv.2 0 hv.1).2.1
  have hvalid := stateOuter_valid (cert.st 0) hB hpos
  obtain ⟨p, hp⟩ := certificate_phase_index cert hv
  let B := stripSuffix (cert.st 0).c (cert.st 0).B
  have hbound : Bounded B := stripSuffix_bounded _ _ hB
  have houter : stateOuter (cert.st 0) = ⟨2 * (p.val + 1), B⟩ := by
    change ({c := (cert.st 0).c, B := B} : Outer) = _
    congr 1
  by_cases hlen : B.length ≤ cap
  · have hvalid' : validOuter ⟨2 * (p.val + 1), B⟩ = true := by
      rw [← houter]
      exact hvalid
    obtain ⟨t, ht⟩ := hexit p B hbound hvalid' hlen
    rw [← houter, certificate_outer_orbit cert hv t] at ht
    exact ⟨t % cert.P, Nat.mod_lt t hv.1, ht⟩
  · exact ⟨0, hv.1, Nat.lt_of_not_ge hlen⟩

/-- The canonical first-state admissibility premise discharges positivity. -/
theorem accepted_admissible_exceeds_cap (cert : Certificate)
    (hc : check cert = true) (H M : Word) (hadm : Admissible0 cert H M)
    (cap : Nat) (hexit : EscapeAt cap) :
    ∃ i, i < cert.P ∧ cap < (stripSuffix (cert.st i).c (cert.st i).B).length := by
  have hv := check_sound cert hc
  exact valid_exceeds_cap cert hv
    (admissible_heads_positive cert hv H M hadm 0 hv.1) cap hexit

/-- Existing kernel cap-two checks satisfy the generic escape contract. -/
theorem escapeAt_two : EscapeAt 2 := by
  intro p B hB hvalid hlen
  obtain ⟨t, _, ht⟩ := cap2_exit_witness p B hlen hB hvalid
  exact ⟨t, ht⟩

/-- No accepted canonically admissible certificate stays within exterior cap
 two after maximal trimming.  There is no certificate instance or Lychrel
 witness asserted here. -/
theorem accepted_admissible_exceeds_two (cert : Certificate)
    (hc : check cert = true) (H M : Word) (hadm : Admissible0 cert H M) :
    ∃ i, i < cert.P ∧ 2 < (stripSuffix (cert.st i).c (cert.st i).B).length :=
  accepted_admissible_exceeds_cap cert hc H M hadm 2 escapeAt_two

end Agent116.CertificateExterior

#print axioms Agent116.CertificateExterior.local_outer_step
#print axioms Agent116.CertificateExterior.certificate_outer_orbit
#print axioms Agent116.CertificateExterior.certificate_phase_index
#print axioms Agent116.CertificateExterior.stateOuter_valid
#print axioms Agent116.CertificateExterior.valid_exceeds_cap
#print axioms Agent116.CertificateExterior.accepted_admissible_exceeds_cap
#print axioms Agent116.CertificateExterior.escapeAt_two
#print axioms Agent116.CertificateExterior.accepted_admissible_exceeds_two
