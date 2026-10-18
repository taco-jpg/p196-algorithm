import P196.Agent104ExactMass.SharedProfile

/-!
The nonsymmetric finite-profile dynamics contains ordinary decimal
reverse-and-add exactly.  Padding is explicit; no tail convention is
silently imposed on the older finite-word representation.
-/

namespace DecimalProfile.NumericBridge

open DecimalDigits DecimalMass FoldedDecimal OverflowCarryNormalization
  CarryHistory Lychrel196 DecimalUnboundedMass

def pad (q : Nat → Nat) (L i : Nat) : Nat :=
  if i < L then q i else 0

def embed (s : State) : State := (s.1, pad s.2 s.1)

theorem pad_inside (q : Nat → Nat) (L i : Nat) (hi : i < L) :
    pad q L i = q i := by simp [pad, hi]

theorem carry_pad (q : Nat → Nat) (L i : Nat) (hi : i ≤ L) :
    carry (pad q L) i = carry q i :=
  carry_congr_upto _ _ L (fun j hj => pad_inside q L j hj) i hi

theorem output_pad (q : Nat → Nat) (L i : Nat) (hi : i < L) :
    output (pad q L) i = output q i :=
  output_congr_upto _ _ L (fun j hj => pad_inside q L j hj) i hi

theorem reflect_pad (q : Nat → Nat) (L : Nat) (ha : Admissible L q) :
    reflect (pad q L) L = pad q L := by
  funext i
  by_cases hi : i < L
  · have hj : L - 1 - i < L := by omega
    simp only [reflect, pad, hi, hj, if_true]
    exact (ha.2.2.2.1 i hi).symm
  · simp [reflect, pad, hi]

theorem backCarry_pad_zero (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) : backCarry (pad q L) L 0 = carry q L := by
  simp only [backCarry, Nat.sub_zero, reflect_pad q L ha]
  exact carry_pad q L L (Nat.le_refl L)

theorem backOutput_pad (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi : i < L) :
    backOutput (pad q L) L i = output q (L - 1 - i) := by
  simp only [backOutput, hi, if_true, reflect_pad q L ha]
  exact output_pad q L (L - 1 - i) (by omega)

theorem pad_valid (q : Nat → Nat) (L : Nat) (ha : Admissible L q) :
    Valid L (pad q L) := by
  have hL := ha.1
  refine ⟨ha.1, ?_, ?_, ?_, ?_⟩
  · simpa only [pad, ha.1, if_true] using ha.2.1
  · intro i
    by_cases hi : i < L
    · simpa only [pad, hi, if_true] using ha.2.2.1 i hi
    · simp [pad, hi]
  · intro i hi
    simp [pad, Nat.not_lt.mpr hi]
  · have hi : L - 1 < L := by omega
    have hs := ha.2.2.2.1 0 ha.1
    simp only [Nat.sub_zero] at hs
    simpa only [pad, hi, if_true, ← hs] using ha.2.1

theorem output_pad_terminal (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) : output (pad q L) L = carry q L := by
  have hc := carry_bounded q L ha.2.2.1 L (Nat.le_refl L)
  simp only [output, pad, Nat.lt_irrefl, if_false, Nat.zero_add,
    carry_pad q L L (Nat.le_refl L)]
  exact Nat.mod_eq_of_lt (by omega)

theorem carry_pad_tail (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi : L < i) : carry (pad q L) i = 0 := by
  have hfirst : carry (pad q L) (L + 1) = 0 := by
    have hc := carry_bounded q L ha.2.2.1 L (Nat.le_refl L)
    simp only [carry, pad, Nat.lt_irrefl, if_false, Nat.zero_add,
      carry_pad q L L (Nat.le_refl L)]
    omega
  have hall : ∀ k, carry (pad q L) (L + 1 + k) = 0 := by
    intro k
    induction k with
    | zero => simpa using hfirst
    | succ k ih =>
      have hn : ¬ L + 1 + k < L := by omega
      change (pad q L (L + 1 + k) + carry (pad q L) (L + 1 + k)) / 10 = 0
      simp only [pad, hn, if_false, ih, Nat.zero_add, Nat.zero_div]
  have he : L + 1 + (i - (L + 1)) = i := by omega
  simpa only [he] using hall (i - (L + 1))

theorem output_pad_tail (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hi : L < i) : output (pad q L) i = 0 := by
  simp only [output, pad, Nat.not_lt.mpr (by omega : L ≤ i), if_false,
    carry_pad_tail q L i ha hi, Nat.zero_add, Nat.zero_mod]

theorem nextLen_pad (q : Nat → Nat) (L : Nat) (ha : Admissible L q) :
    nextLen (pad q L) L = nextWidth q L := by
  simp only [nextLen, carry_pad q L L (Nat.le_refl L),
    backCarry_pad_zero q L ha, and_self, nextWidth]

theorem phi_pad (q : Nat → Nat) (L : Nat) (ha : Admissible L q) :
    phi (pad q L) L = pad (nextColumns q L) (nextWidth q L) := by
  funext i
  have hc := carry_bounded q L ha.2.2.1 L (Nat.le_refl L)
  by_cases hz : carry q L = 0
  · simp only [phi, backCarry_pad_zero q L ha, hz, if_true,
      nextWidth, pad, nextColumns]
    by_cases hi : i < L
    · rw [if_pos hi, output_pad q L i hi, backOutput_pad q L i ha hi]
      rfl
    · rw [if_neg hi]
      have hb : backOutput (pad q L) L i = 0 := by simp [backOutput, hi]
      rw [hb, Nat.add_zero]
      by_cases he : i = L
      · subst i
        rw [output_pad_terminal q L ha, hz]
      · exact output_pad_tail q L i ha (by omega)
  · have ho : carry q L = 1 := by omega
    have hn : ¬ carry q L = 0 := hz
    simp only [phi, backCarry_pad_zero q L ha, hz, if_false,
      nextWidth, pad, nextColumns]
    by_cases hi : i < L + 1
    · rw [if_pos hi]
      by_cases hi0 : i = 0
      · subst i
        simp only [if_true, output_pad q L 0 ha.1, columnSum,
          reflected, Nat.add_sub_cancel, Nat.sub_zero, extended,
          ha.1, if_true, Nat.lt_irrefl, if_false, ho]
      · rw [if_neg hi0]
        by_cases hiL : i < L
        · have him : i - 1 < L := by omega
          have hmir : L - 1 - (i - 1) = L - i := by omega
          have hmirL : L - i < L := by omega
          rw [output_pad q L i hiL, backOutput_pad q L (i - 1) ha him]
          simp only [columnSum, reflected, Nat.add_sub_cancel, extended,
            hiL, hmirL, if_true, hmir]
        · have he : i = L := by omega
          subst i
          have hLm : L - 1 < L := by omega
          have hmir : L - 1 - (L - 1) = 0 := by omega
          rw [output_pad_terminal q L ha,
            backOutput_pad q L (L - 1) ha hLm]
          simp only [columnSum, reflected, Nat.add_sub_cancel,
            Nat.sub_self, extended, Nat.lt_irrefl, if_false, ha.1,
            if_true, hmir]
    · rw [if_neg hi]
      have hi0 : i ≠ 0 := by omega
      have him : ¬ i - 1 < L := by omega
      simp only [if_neg hi0, backOutput, him, if_false, Nat.add_zero]
      exact output_pad_tail q L i ha (by omega)

theorem step_embed (q : Nat → Nat) (L : Nat) (ha : Admissible L q) :
    DecimalProfile.step (embed (L, q)) =
      embed (nextWidth q L, nextColumns q L) := by
  change (nextLen (pad q L) L, phi (pad q L) L) =
    (nextWidth q L, pad (nextColumns q L) (nextWidth q L))
  rw [nextLen_pad q L ha, phi_pad q L ha]

theorem iter_embed (q : Nat → Nat) (L t : Nat) (ha : Admissible L q) :
    iter (embed (L, q)) t = embed (iterPairs q L t) := by
  induction t with
  | zero => rfl
  | succ t ih =>
    simp only [iter, ih, iterPairs]
    exact step_embed _ _ (iterPairs_admissible q L t ha)

theorem mass_embed (s : State) : mass (embed s) = wordSum s.2 s.1 := by
  exact wordSum_congr _ _ _ (fun i hi => pad_inside s.2 s.1 i hi)

theorem mass_numeric_iter (n : Nat) (d : Nat → Nat) (L t : Nat)
    (hc : Canonical n d L) :
    mass (iter (embed (L, columnSum d L)) t) =
      2 * digitSum (orbit n t) := by
  have ha := NormalizationBridge.canonical_admissible n d L hc
  rw [iter_embed _ _ _ ha, mass_embed]
  exact iterPairs_wordSum n d (columnSum d L) L t hc (fun _ _ => rfl)

#print axioms step_embed
#print axioms iter_embed
#print axioms mass_numeric_iter

end DecimalProfile.NumericBridge
