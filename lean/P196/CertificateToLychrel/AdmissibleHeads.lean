import P196.CertificateToLychrel.SymbolicGrowth

namespace Agent112.Admissibility
open Agent109 Agent109.Cert

def HeadPos (w : Word) : Prop := ∀ x, w.head? = some x → 0 < x

theorem pair_preserves_lastPos (w : Word) (hw : LastPos w) : LastPos (pair w) := by
  cases he : w.reverse with
  | nil =>
    have : w = [] := by simpa using congrArg List.reverse he
    subst w; intro x hx; simp [pair, zipAdd] at hx
  | cons z E =>
    have he' : w = E.reverse ++ [z] := by simpa using congrArg List.reverse he
    rw [he'] at hw ⊢
    exact pair_last _ z (hw z (by simp))

theorem stepWord_preserves_lastPos (w : Word) (hb : Bounded w) (hp : LastPos w) :
    LastPos (stepWord w) := by
  apply pair_preserves_lastPos
  exact ((canon_iff _).mp (canon_normalize w 0 hb (by decide) hp)).2

theorem template_head_of_last (c : Nat) (B A C : Word) (g h : Nat)
    (hl : LastPos (template c B A C g h)) : HeadPos B := by
  intro b hb
  have he : (template c B A C g h).getLast? = some b := by
    unfold template
    rw [List.getLast?_append]
    simp [List.getLast?_reverse, hb]
  exact hl b he

theorem local_symbolic_step (s s' : State) (L L' : Link) (hv : LocalOK s s' L L')
    (G H : Nat) (hG : L.lo ≤ G) (hH : L.lo' ≤ H) :
    ∃ G' H', L'.lo ≤ G' ∧ L'.lo' ≤ H' ∧
      stepWord (template s.c s.B s.A s.C G H) = template s'.c s'.B s'.A s'.C G' H' := by
  obtain ⟨hc, hB, hA, hC, hc', hBr, hAr, hCr, _, h2, h2', hlo, hlo'⟩ := hv
  obtain ⟨g, rfl⟩ : ∃ g, G = g + 2 := ⟨G - 2, by omega⟩
  obtain ⟨h, rfl⟩ : ∃ h, H = h + 2 := ⟨H - 2, by omega⟩
  have hs := stepWord_template s.c s.B s.A s.C g h hc hB hA hC
  rw [hc', hBr, hAr, hCr, template_trim] at hs
  refine ⟨_, _, ?_, ?_, hs⟩ <;> unfold gam at * <;> omega

theorem local_headPos (s s' : State) (L L' : Link) (hv : LocalOK s s' L L')
    (hp : HeadPos s.B) : HeadPos s'.B := by
  obtain ⟨G, H, _, _, hs⟩ := local_symbolic_step s s' L L' hv L.lo L.lo'
    (Nat.le_refl _) (Nat.le_refl _)
  have hb := template_bounded s.c s.B s.A s.C L.lo L.lo' hv.1 hv.2.1 hv.2.2.1 hv.2.2.2.1
  have h2 : 2 ≤ L.lo := hv.2.2.2.2.2.2.2.2.2.1
  have hl := template_lastPos s.c s.B s.A s.C L.lo L.lo' hv.1 (by omega) hp
  have hn := stepWord_preserves_lastPos _ hb hl
  rw [hs] at hn
  exact template_head_of_last s'.c s'.B s'.A s'.C G H hn

theorem cyclic_headPos (cert : Certificate) (hv : Valid cert) (j : Nat) (hj : j < cert.P)
    (hp : HeadPos (cert.st j).B) (i : Nat) (hi : i < cert.P) : HeadPos (cert.st i).B := by
  have hk : ∀ k, HeadPos (cert.st ((j + k) % cert.P)).B := by
    intro k
    induction k with
    | zero => simpa [Nat.mod_eq_of_lt hj] using hp
    | succ k ih =>
      have hh := local_headPos _ _ _ _ (hv.2 _ (Nat.mod_lt _ hv.1)) ih
      have he : ((j + k) % cert.P + 1) % cert.P = (j + (k + 1)) % cert.P := by
        simp [Nat.add_assoc]
      simpa [he] using hh
  have he : j + (i + cert.P - j) = i + cert.P := by omega
  have hh := hk (i + cert.P - j)
  rw [he, Nat.add_mod, Nat.mod_self, Nat.add_zero, Nat.mod_mod, Nat.mod_eq_of_lt hi] at hh
  exact hh

theorem gamma_zero_of_not_head (s : State) (hb : Bounded s.B) (hn : ¬ HeadPos s.B) : gam s = 0 := by
  cases he : s.B with
  | nil => exfalso; apply hn; intro x hx; simp [he] at hx
  | cons b E =>
    have h0 : b = 0 := by
      apply Classical.byContradiction
      intro hh
      apply hn
      intro x hx
      simp [he] at hx
      omega
    subst b
    have hbE : Bounded E.reverse := by
      intro x hx
      apply hb x
      simp only [he, List.mem_cons]
      exact Or.inr (List.mem_reverse.mp hx)
    have hc := norm_carry_le E.reverse (kOf s.c) hbE (by unfold kOf; split <;> omega)
    unfold gam data
    simp only [he, List.reverse_cons, norm_append, norm]
    omega

/-- A certificate may initially be treated solely as a symbolic word system.
Canonical integer realizability is not an assumption in this invariant. -/
def WordInv (cert : Certificate) (w : Word) : Prop :=
  ∃ i, i < cert.P ∧ ∃ G H,
    w = template (cert.st i).c (cert.st i).B (cert.st i).A (cert.st i).C G H ∧
    (cert.lk i).lo ≤ G ∧ (cert.lk i).lo' ≤ H

theorem wordInv_step (cert : Certificate) (hv : Valid cert) (w : Word)
    (hw : WordInv cert w) : WordInv cert (stepWord w) := by
  obtain ⟨i, hi, G, H, rfl, hG, hH⟩ := hw
  obtain ⟨G', H', hG', hH', he⟩ := local_symbolic_step _ _ _ _ (hv.2 i hi) G H hG hH
  exact ⟨(i + 1) % cert.P, Nat.mod_lt _ hv.1, G', H', he, hG', hH'⟩

theorem wordInv_bounded (cert : Certificate) (hv : Valid cert) (w : Word)
    (hw : WordInv cert w) : Bounded w := by
  obtain ⟨i, hi, G, H, rfl, _, _⟩ := hw
  obtain ⟨hc, hB, hA, hC, _⟩ := hv.2 i hi
  exact template_bounded _ _ _ _ G H hc hB hA hC

theorem wordInv_pos (cert : Certificate) (hv : Valid cert) (w : Word)
    (hw : WordInv cert w) : 0 < evalL w := by
  obtain ⟨i, hi, G, H, rfl, hG, _⟩ := hw
  have hl := hv.2 i hi
  obtain ⟨hc, _, _, _, _, _, _, _, _, h2, _⟩ := hl
  apply (evalL_pos_iff _).mpr
  refine ⟨(cert.st i).c, ?_, hc.1⟩
  have hm : (cert.st i).c ∈ List.replicate G (cert.st i).c := by simp; omega
  simp only [template, List.mem_append]
  simp [hm]

theorem wordInv_same_length (cert : Certificate) (hv : Valid cert)
    (hn : ∀ i, i < cert.P → ¬ HeadPos (cert.st i).B) (w : Word) (hw : WordInv cert w) :
    (stepWord w).length = w.length := by
  obtain ⟨i, hi, G, H, rfl, hG, hH⟩ := hw
  obtain ⟨hc, hB, hA, hC, _, _, _, _, _, h2, h2', _⟩ := hv.2 i hi
  obtain ⟨g, rfl⟩ : ∃ g, G = g + 1 := ⟨G - 1, by omega⟩
  obtain ⟨h, rfl⟩ : ∃ h, H = h + 1 := ⟨H - 1, by omega⟩
  have hz := gamma_zero_of_not_head (cert.st i) hB (hn i hi)
  have ht := norm_template _ _ _ _ g h hc hB hA hC
  have hcarry : (norm (template (cert.st i).c (cert.st i).B (cert.st i).A (cert.st i).C
      (g + 1) (h + 1)) 0).2 = 0 := by rw [ht]; exact hz
  unfold stepWord pair
  rw [zipAdd_length _ _ (by simp), normalize_eq_norm, List.length_append]
  simp [hcarry, carryWord, norm_length]

/-- Every accepted cyclic state has a positive exterior head (or empty exterior).
The proof does not assume canonical realizability: a zero-head cycle would give
an unbounded increasing positive symbolic evaluation at fixed width. -/
theorem valid_headPos (cert : Certificate) (hv : Valid cert) (i : Nat) (hi : i < cert.P) :
    HeadPos (cert.st i).B := by
  apply Classical.byContradiction
  intro hn
  have hall : ∀ j, j < cert.P → ¬ HeadPos (cert.st j).B := by
    intro j hj hp
    exact hn (cyclic_headPos cert hv j hj hp i hi)
  let w := template (cert.st 0).c (cert.st 0).B (cert.st 0).A (cert.st 0).C
    (cert.lk 0).lo (cert.lk 0).lo'
  have hw : WordInv cert w := ⟨0, hv.1, _, _, rfl, Nat.le_refl _, Nat.le_refl _⟩
  have hk : ∀ k, WordInv cert (orbitWord w k) := by
    intro k
    induction k with
    | zero => exact hw
    | succ k ih => exact wordInv_step cert hv _ ih
  have hlen : ∀ k, (orbitWord w k).length = w.length := by
    intro k
    induction k with
    | zero => rfl
    | succ k ih =>
      change (stepWord (orbitWord w k)).length = w.length
      rw [wordInv_same_length cert hv hall _ (hk k), ih]
  exact no_bounded_width_orbit w (wordInv_pos cert hv w hw) w.length
    (fun k => wordInv_bounded cert hv _ (hk k)) hlen

theorem automatic_admissibility (cert : Certificate) (hc : check cert = true) :
    ∃ H M, Admissible0 cert H M := by
  have hv := check_sound cert hc
  exact admissible_of_valid_head cert hv (valid_headPos cert hv 0 hv.1)

theorem certificate_existence_of_check (cert : Certificate)
    (hc : check cert = true) : ∃ m, ∀ k, ¬ Palindrome (orbit m k) := by
  have hv := check_sound cert hc
  exact certificate_existence_of_head cert hc (valid_headPos cert hv 0 hv.1)

end Agent112.Admissibility
#print axioms Agent112.Admissibility.pair_preserves_lastPos
#print axioms Agent112.Admissibility.stepWord_preserves_lastPos
#print axioms Agent112.Admissibility.template_head_of_last
#print axioms Agent112.Admissibility.local_symbolic_step
#print axioms Agent112.Admissibility.local_headPos
#print axioms Agent112.Admissibility.cyclic_headPos
#print axioms Agent112.Admissibility.gamma_zero_of_not_head
#print axioms Agent112.Admissibility.wordInv_step
#print axioms Agent112.Admissibility.wordInv_bounded
#print axioms Agent112.Admissibility.wordInv_pos
#print axioms Agent112.Admissibility.wordInv_same_length
#print axioms Agent112.Admissibility.valid_headPos
#print axioms Agent112.Admissibility.automatic_admissibility
#print axioms Agent112.Admissibility.certificate_existence_of_check
