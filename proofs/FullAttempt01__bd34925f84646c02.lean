import LychrelDigitSums

/-!
Exact interior birth classification for the actual overflowing decimal update.
The two input coefficients are adjacent in the old admissible word; all carry
bits are the recursively computed `DecimalDigits.carry`, not free parameters.
Only the first alternatives of the two classification theorems inherit an old
equal 0/18 pair. The other alternatives are precisely the new extreme symbols.
-/

namespace RunBirths.Overflow

open DecimalDigits FoldedDecimal

private theorem residue_zero_iff (x a : Nat) (hx : x ≤ 18) (ha : a ≤ 1) :
    (x + a) % 10 = 0 ↔
      (x = 0 ∧ a = 0) ∨ (x = 10 ∧ a = 0) ∨ (x = 9 ∧ a = 1) := by
  have hd : (x + a) / 10 = 0 ∨ (x + a) / 10 = 1 := by omega
  rcases hd with hd | hd <;> omega

private theorem residue_nine_iff (x a : Nat) (hx : x ≤ 18) (ha : a ≤ 1) :
    (x + a) % 10 = 9 ↔
      (x = 9 ∧ a = 0) ∨ (x = 8 ∧ a = 1) ∨ (x = 18 ∧ a = 1) := by
  have hd : (x + a) / 10 = 0 ∨ (x + a) / 10 = 1 := by omega
  rcases hd with hd | hd <;> omega

theorem adjacent_residues_zero_iff (x y a b d e : Nat)
    (hx : x ≤ 18) (hy : y ≤ 18) (ha : a ≤ 1) (he : e ≤ 1)
    (hb : b = (x + a) / 10) (hd : d = (y + e) / 10) :
    (y + b) % 10 + (x + d) % 10 = 0 ↔
      (x = 0 ∧ y = 0) ∨
      (x = 9 ∧ y = 9 ∧ b = 1 ∧ d = 1) ∨
      (x = 9 ∧ y = 10 ∧ b = 0) ∨
      (x = 10 ∧ y = 9 ∧ d = 0) := by
  have hb' : b ≤ 1 := by omega
  have hd' : d ≤ 1 := by omega
  have hz : (y + b) % 10 + (x + d) % 10 = 0 ↔
      (y + b) % 10 = 0 ∧ (x + d) % 10 = 0 := by omega
  rw [hz, residue_zero_iff y b hy hb', residue_zero_iff x d hx hd']
  omega

theorem adjacent_residues_eighteen_iff (x y a b d e : Nat)
    (hx : x ≤ 18) (hy : y ≤ 18) (ha : a ≤ 1) (he : e ≤ 1)
    (hb : b = (x + a) / 10) (hd : d = (y + e) / 10) :
    (y + b) % 10 + (x + d) % 10 = 18 ↔
      (x = 18 ∧ y = 18) ∨
      (x = 9 ∧ y = 9 ∧ b = 0 ∧ d = 0) ∨
      (x = 9 ∧ y = 8 ∧ b = 1) ∨
      (x = 8 ∧ y = 9 ∧ d = 1) := by
  have hb' : b ≤ 1 := by omega
  have hd' : d ≤ 1 := by omega
  have hz : (y + b) % 10 + (x + d) % 10 = 18 ↔
      (y + b) % 10 = 9 ∧ (x + d) % 10 = 9 := by omega
  rw [hz, residue_nine_iff y b hy hb', residue_nine_iff x d hx hd']
  omega

/-- In the overflow branch, an actual interior output combines the normalized
digits of exactly two adjacent old coefficients. -/
theorem next_column_adjacent_residues (q : Nat → Nat) (L i : Nat)
    (hA : Admissible L q) (hi0 : 0 < i) (hi : i < L)
    (hc : carry q L = 1) :
    nextColumns q L i =
      (q i + carry q i) % 10 + (q (i - 1) + carry q (L - i)) % 10 := by
  have hm : L - i < L := by omega
  have hind : L - 1 - (L - i) = i - 1 := by omega
  have hs := hA.2.2.2.1 (L - i) hm
  rw [hind] at hs
  rw [folded_emission_overflow q L i hi hc]
  simp only [extended, if_pos hm, output, hs]

/-- Exact zero classification. The first alternative is inheritance from an
old adjacent zero pair; the remaining three alternatives are new births. -/
theorem next_column_zero_iff (q : Nat → Nat) (L i : Nat)
    (hA : Admissible L q) (hi0 : 0 < i) (hi : i < L)
    (hc : carry q L = 1) :
    nextColumns q L i = 0 ↔
      (q (i - 1) = 0 ∧ q i = 0) ∨
      (q (i - 1) = 9 ∧ q i = 9 ∧ carry q i = 1 ∧ carry q (L - i) = 1) ∨
      (q (i - 1) = 9 ∧ q i = 10 ∧ carry q i = 0) ∨
      (q (i - 1) = 10 ∧ q i = 9 ∧ carry q (L - i) = 0) := by
  have hbnd := carry_bounded q L hA.2.2.1
  have hip : i - 1 + 1 = i := by omega
  have hmp : L - i - 1 + 1 = L - i := by omega
  have hsym : q (L - i - 1) = q i := by
    have h := hA.2.2.2.1 (L - i - 1) (by omega)
    have hind : L - 1 - (L - i - 1) = i := by omega
    simpa only [hind] using h
  have hb : carry q i = (q (i - 1) + carry q (i - 1)) / 10 := by
    simpa only [hip] using
      (show carry q (i - 1 + 1) = (q (i - 1) + carry q (i - 1)) / 10 from rfl)
  have hd : carry q (L - i) = (q i + carry q (L - i - 1)) / 10 := by
    simpa only [hmp, hsym] using
      (show carry q (L - i - 1 + 1) =
        (q (L - i - 1) + carry q (L - i - 1)) / 10 from rfl)
  rw [next_column_adjacent_residues q L i hA hi0 hi hc]
  exact adjacent_residues_zero_iff _ _ _ _ _ _
    (hA.2.2.1 (i - 1) (by omega)) (hA.2.2.1 i hi)
    (hbnd (i - 1) (by omega)) (hbnd (L - i - 1) (by omega)) hb hd

/-- Exact eighteen classification. The first alternative is inheritance from
an old adjacent eighteen pair; the remaining three alternatives are births. -/
theorem next_column_eighteen_iff (q : Nat → Nat) (L i : Nat)
    (hA : Admissible L q) (hi0 : 0 < i) (hi : i < L)
    (hc : carry q L = 1) :
    nextColumns q L i = 18 ↔
      (q (i - 1) = 18 ∧ q i = 18) ∨
      (q (i - 1) = 9 ∧ q i = 9 ∧ carry q i = 0 ∧ carry q (L - i) = 0) ∨
      (q (i - 1) = 9 ∧ q i = 8 ∧ carry q i = 1) ∨
      (q (i - 1) = 8 ∧ q i = 9 ∧ carry q (L - i) = 1) := by
  have hbnd := carry_bounded q L hA.2.2.1
  have hip : i - 1 + 1 = i := by omega
  have hmp : L - i - 1 + 1 = L - i := by omega
  have hsym : q (L - i - 1) = q i := by
    have h := hA.2.2.2.1 (L - i - 1) (by omega)
    have hind : L - 1 - (L - i - 1) = i := by omega
    simpa only [hind] using h
  have hb : carry q i = (q (i - 1) + carry q (i - 1)) / 10 := by
    simpa only [hip] using
      (show carry q (i - 1 + 1) = (q (i - 1) + carry q (i - 1)) / 10 from rfl)
  have hd : carry q (L - i) = (q i + carry q (L - i - 1)) / 10 := by
    simpa only [hmp, hsym] using
      (show carry q (L - i - 1 + 1) =
        (q (L - i - 1) + carry q (L - i - 1)) / 10 from rfl)
  rw [next_column_adjacent_residues q L i hA hi0 hi hc]
  exact adjacent_residues_eighteen_iff _ _ _ _ _ _
    (hA.2.2.1 (i - 1) (by omega)) (hA.2.2.1 i hi)
    (hbnd (i - 1) (by omega)) (hbnd (L - i - 1) (by omega)) hb hd

/-- Both actual endpoints have the appended carry 1 as one of their digits. -/
theorem next_endpoints (q : Nat → Nat) (L : Nat)
    (hA : Admissible L q) (hc : carry q L = 1) :
    nextColumns q L 0 = 1 + q 0 % 10 ∧
      nextColumns q L L = 1 + q 0 % 10 := by
  have hzero : nextColumns q L 0 = 1 + q 0 % 10 := by
    rw [folded_emission_overflow q L 0 hA.1 hc]
    simp only [carry, Nat.add_zero, Nat.sub_zero, extended,
      Nat.lt_irrefl, if_false, hc]
    omega
  refine ⟨hzero, ?_⟩
  have hs : nextColumns q L 0 = nextColumns q L L := by
    simp only [nextColumns, hc, Nat.one_ne_zero, if_false]
    have h := columnSum_symmetric (extended q L) (L + 1) 0 (by omega)
    simpa using h
  omega

/-- Neither endpoint can inherit or create an extreme 0/18 coefficient. -/
theorem next_endpoints_not_extreme (q : Nat → Nat) (L : Nat)
    (hA : Admissible L q) (hc : carry q L = 1) :
    nextColumns q L 0 ≠ 0 ∧ nextColumns q L 0 ≠ 18 ∧
      nextColumns q L L ≠ 0 ∧ nextColumns q L L ≠ 18 := by
  have h := next_endpoints q L hA hc
  omega

#print axioms adjacent_residues_zero_iff
#print axioms adjacent_residues_eighteen_iff
#print axioms next_column_adjacent_residues
#print axioms next_column_zero_iff
#print axioms next_column_eighteen_iff
#print axioms next_endpoints
#print axioms next_endpoints_not_extreme
end RunBirths.Overflow
