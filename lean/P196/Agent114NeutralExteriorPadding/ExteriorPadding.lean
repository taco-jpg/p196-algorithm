import P196.Drafts.Agent120NeutralBandCalibration.A120Template

/-!
# Agent 114: exact exterior neutral-suffix covariance

Appending any number of neutral coefficients to the exterior preserves its
two interface carries and overflow, appends the same neutral suffix to the
next exterior, and leaves the next center unchanged.  These identities hold
in every base at least two, including empty exterior words.  They do not
assert that a decimal cycle exists or supply a cycle canonicalizer.
-/

namespace Agent114.NeutralExteriorPadding

open Agent120.Neutral

/-- Append a neutral coefficient suffix to an exterior word. -/
def suffixPad (b a : Nat) (B : List Nat) : List Nat :=
  B ++ List.replicate a (b - 1)

theorem norm_suffixPad (b a c : Nat) (B : List Nat)
    (hb : 2 ≤ b) (he : (norm b B c).2 ≤ 1) :
    norm b (suffixPad b a B) c =
      ((norm b B c).1 ++ List.replicate a ((b - 1) * (1 - (norm b B c).2)),
        (norm b B c).2) := by
  unfold suffixPad
  rw [norm_append, norm_replicate_neutral b hb a _ he]

theorem e1_suffixPad_of_bound {b : Nat} {B : List Nat}
    (hb : 2 ≤ b) (hB : ∀ x ∈ B, x ≤ 2 * (b - 1)) (a : Nat) :
    e1 b (suffixPad b a B) = e1 b B := by
  have he : (norm b B 0).2 ≤ 1 :=
    norm_carry_le_one b (by omega) B 0 hB (by omega)
  have hn := congrArg (fun p : List Nat × Nat => p.2)
    (norm_suffixPad b a 0 B hb he)
  exact hn

theorem bound_suffixPad {b : Nat} {B : List Nat}
    (hB : ∀ x ∈ B, x ≤ 2 * (b - 1)) (a : Nat) :
    ∀ x ∈ suffixPad b a B, x ≤ 2 * (b - 1) := by
  intro x hx
  simp only [suffixPad, List.mem_append, List.mem_replicate] at hx
  rcases hx with hx | ⟨_, hx⟩
  · exact hB x hx
  · omega

theorem head_suffixPad_iff {b : Nat} (hb : 2 ≤ b) (a : Nat) (B : List Nat) :
    (suffixPad b a B).head? ≠ some 0 ↔ B.head? ≠ some 0 := by
  cases B with
  | nil =>
      cases a with
      | zero => simp [suffixPad]
      | succ a =>
          have hn : b - 1 ≠ 0 := by omega
          simp [suffixPad, List.replicate_succ, hn]
  | cons x xs => simp [suffixPad]

section
variable {b : Nat} {B C : List Nat}

theorem e1_suffixPad (h : Hyp b B C) (a : Nat) :
    e1 b (suffixPad b a B) = e1 b B :=
  e1_suffixPad_of_bound h.base h.boundB a

theorem e2_suffixPad (h : Hyp b B C) (a : Nat) :
    e2 b (suffixPad b a B) C = e2 b B C := by
  unfold e2
  rw [e1_suffixPad h a]

theorem DB_suffixPad (h : Hyp b B C) (a : Nat) :
    DB b (suffixPad b a B) = DB b B ++ List.replicate a (xd b B) := by
  exact congrArg Prod.fst (norm_suffixPad b a 0 B h.base h.e1_le)

theorem DC_suffixPad (h : Hyp b B C) (a : Nat) :
    DC b (suffixPad b a B) C = DC b B C := by
  unfold DC
  rw [e1_suffixPad h a]

theorem xd_suffixPad (h : Hyp b B C) (a : Nat) :
    xd b (suffixPad b a B) = xd b B := by
  unfold xd
  rw [e1_suffixPad h a]

theorem yd_suffixPad (h : Hyp b B C) (a : Nat) :
    yd b (suffixPad b a B) C = yd b B C := by
  unfold yd
  rw [e2_suffixPad h a]

theorem DR_suffixPad (h : Hyp b B C) (a : Nat) :
    DR b (suffixPad b a B) C = List.replicate a (yd b B C) ++ DR b B C := by
  unfold DR
  rw [e2_suffixPad h a]
  simp only [suffixPad, List.reverse_append, List.reverse_replicate]
  rw [norm_append, norm_replicate_neutral b h.base a _ h.e2_le]
  rfl

theorem gam_suffixPad (h : Hyp b B C) (a : Nat) :
    gam b (suffixPad b a B) C = gam b B C := by
  unfold gam
  rw [e2_suffixPad h a]
  simp only [suffixPad, List.reverse_append, List.reverse_replicate]
  rw [norm_append, norm_replicate_neutral b h.base a _ h.e2_le]

theorem hyp_suffixPad (h : Hyp b B C) (a : Nat) :
    Hyp b (suffixPad b a B) C := by
  refine ⟨h.base, bound_suffixPad h.boundB a, h.boundC,
    (head_suffixPad_iff h.base a B).2 h.ext, ?_⟩
  rw [e1_suffixPad h a, e2_suffixPad h a]
  exact h.flip

theorem hyp_of_suffixPad (a : Nat) (h : Hyp b (suffixPad b a B) C) :
    Hyp b B C := by
  have hB : ∀ x ∈ B, x ≤ 2 * (b - 1) := by
    intro x hx
    exact h.boundB x (List.mem_append_left _ hx)
  have he1 := e1_suffixPad_of_bound h.base hB a
  have he2 : e2 b (suffixPad b a B) C = e2 b B C := by
    unfold e2
    rw [he1]
  refine ⟨h.base, hB, h.boundC,
    (head_suffixPad_iff h.base a B).1 h.ext, ?_⟩
  have hf := h.flip
  rw [he1, he2] at hf
  exact hf

/-- Adding or removing a neutral exterior suffix preserves every hypothesis. -/
theorem hyp_suffixPad_iff (a : Nat) :
    Hyp b (suffixPad b a B) C ↔ Hyp b B C :=
  ⟨hyp_of_suffixPad a, fun h => hyp_suffixPad h a⟩

/-- The next exterior carries exactly the same appended neutral suffix. -/
theorem nextB_suffixPad (h : Hyp b B C) (a : Nat) :
    nextB b (suffixPad b a B) C = suffixPad b a (nextB b B C) := by
  unfold nextB
  rw [gam_suffixPad h a, DB_suffixPad h a, DR_suffixPad h a, xd_suffixPad h a]
  simp only [List.reverse_append, List.reverse_replicate]
  unfold suffixPad
  by_cases hg : gam b B C = 0
  · simp only [hg, if_true]
    rw [List.zipWith_append (by simp [length_DB, length_DR])]
    rw [List.zipWith_replicate, Nat.min_self, h.xy]
  · simp only [hg, if_false]
    have hp : (DB b B ++ List.replicate a (xd b B)) ++ [xd b B] =
        (DB b B ++ [xd b B]) ++ List.replicate a (xd b B) := by
      rw [List.append_assoc, ← List.replicate_succ']
      simp [List.replicate_succ, List.append_assoc]
    rw [hp]
    change List.zipWith (· + ·)
        ((DB b B ++ [xd b B]) ++ List.replicate a (xd b B))
        ((1 :: (DR b B C).reverse) ++ List.replicate a (yd b B C)) = _
    rw [List.zipWith_append (by simp [length_DB, length_DR])]
    rw [List.zipWith_replicate, Nat.min_self, h.xy]

/-- The next center is independent of neutral exterior suffix padding. -/
theorem nextC_suffixPad (h : Hyp b B C) (a : Nat) :
    nextC b (suffixPad b a B) C = nextC b B C := by
  unfold nextC
  rw [gam_suffixPad h a, DC_suffixPad h a, yd_suffixPad h a]

end

end Agent114.NeutralExteriorPadding

#print axioms Agent114.NeutralExteriorPadding.hyp_suffixPad_iff
#print axioms Agent114.NeutralExteriorPadding.e1_suffixPad
#print axioms Agent114.NeutralExteriorPadding.e2_suffixPad
#print axioms Agent114.NeutralExteriorPadding.gam_suffixPad
#print axioms Agent114.NeutralExteriorPadding.nextB_suffixPad
#print axioms Agent114.NeutralExteriorPadding.nextC_suffixPad
