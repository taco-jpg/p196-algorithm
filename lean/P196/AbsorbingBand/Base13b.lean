import P196.AbsorbingBand.Cert

/-!
# Base 13: a ten-edge absorbing-band cycle (merged symmetric lattice format, uniform band)

Data from `cert_b13_rec1.json` (|B| = 55, band values alternate 8, 16, overflow word 1010010000).
The cycle is checked by `decide`; the theorem then follows from `lychrel_of_lcycle`.
-/

namespace AbsorbingBand.Base13b

open AbsorbingBand Agent120.Neutral

def B0 : List Nat := [19, 9, 8, 19, 13, 6, 16, 11, 11, 10, 23, 13, 2, 15, 12, 13, 6, 20, 5, 5, 5, 3, 3, 1, 5, 23, 7, 20, 3, 7, 21, 2, 0, 1, 7, 5, 12, 23, 10, 18, 21, 8, 9, 15, 8, 23, 1, 12, 4, 1, 18, 12, 8, 8, 8]

def B1 : List Nat := [7, 16, 17, 15, 8, 7, 10, 15, 22, 21, 21, 12, 3, 5, 3, 1, 7, 14, 13, 10, 10, 8, 6, 4, 6, 16, 18, 15, 11, 10, 16, 11, 2, 1, 8, 12, 18, 10, 21, 16, 15, 17, 17, 12, 11, 19, 12, 13, 16, 5, 7, 5, 21, 16, 16]

def B2 : List Nat := [15, 7, 10, 5, 17, 14, 21, 5, 20, 18, 17, 12, 7, 10, 6, 2, 15, 3, 1, 21, 20, 16, 12, 8, 13, 7, 12, 5, 23, 21, 6, 23, 4, 2, 17, 12, 10, 22, 17, 8, 6, 10, 9, 12, 24, 13, 0, 2, 7, 11, 14, 11, 17, 8, 8]

def B3 : List Nat := [3, 10, 17, 15, 10, 7, 11, 14, 13, 14, 11, 4, 20, 17, 16, 8, 5, 6, 4, 10, 17, 12, 3, 21, 9, 8, 19, 17, 16, 20, 15, 17, 15, 6, 7, 4, 23, 20, 15, 13, 14, 16, 19, 22, 11, 13, 1, 2, 9, 18, 13, 13, 16, 13, 16]

def B4 : List Nat := [6, 21, 9, 5, 21, 14, 23, 3, 2, 3, 23, 9, 15, 10, 7, 17, 10, 12, 8, 21, 8, 12, 8, 16, 19, 17, 13, 10, 8, 16, 6, 10, 5, 13, 14, 9, 21, 16, 6, 2, 4, 8, 14, 19, 24, 0, 3, 4, 19, 11, 2, 2, 8, 2, 8]

def B5 : List Nat := [13, 16, 19, 11, 17, 4, 21, 7, 4, 7, 20, 20, 4, 21, 15, 8, 21, 24, 17, 16, 17, 24, 17, 7, 14, 10, 1, 21, 17, 6, 13, 20, 11, 1, 3, 20, 17, 7, 13, 4, 8, 17, 3, 14, 23, 1, 6, 9, 12, 23, 4, 4, 16, 4, 16]

def B6 : List Nat := [1, 5, 11, 18, 16, 9, 13, 16, 11, 11, 15, 16, 12, 13, 12, 11, 17, 21, 17, 9, 9, 17, 17, 12, 9, 12, 11, 10, 14, 11, 7, 9, 19, 12, 4, 11, 13, 12, 8, 5, 12, 13, 8, 5, 13, 12, 7, 15, 22, 10, 15, 8, 8, 8, 8]

def B7 : List Nat := [2, 10, 23, 11, 7, 20, 1, 7, 23, 23, 5, 8, 0, 1, 12, 24, 9, 18, 9, 19, 19, 9, 9, 12, 19, 24, 22, 21, 2, 23, 14, 19, 12, 12, 9, 23, 0, 12, 17, 11, 12, 0, 17, 11, 0, 12, 16, 5, 19, 22, 4, 17, 16, 16, 16]

def B8 : List Nat := [4, 21, 20, 23, 15, 14, 3, 15, 21, 21, 11, 16, 0, 3, 12, 22, 20, 10, 20, 13, 13, 19, 19, 12, 13, 24, 20, 17, 6, 21, 4, 13, 12, 12, 20, 20, 2, 12, 8, 23, 24, 1, 8, 23, 1, 12, 6, 12, 13, 19, 10, 9, 8, 8, 8]

def B9 : List Nat := [9, 17, 16, 22, 6, 3, 8, 5, 18, 17, 24, 6, 1, 7, 12, 19, 15, 22, 15, 2, 2, 14, 14, 0, 2, 24, 16, 9, 14, 16, 10, 1, 0, 0, 16, 15, 5, 24, 17, 21, 23, 3, 17, 20, 3, 24, 13, 12, 1, 13, 21, 18, 16, 16, 16]

def cert : List LEdge :=
  [⟨B0, 8, B1, 16, 1⟩,
   ⟨B1, 16, B2, 8, 1⟩,
   ⟨B2, 8, B3, 16, 1⟩,
   ⟨B3, 16, B4, 8, 1⟩,
   ⟨B4, 8, B5, 16, 1⟩,
   ⟨B5, 16, B6, 8, 1⟩,
   ⟨B6, 8, B7, 16, 1⟩,
   ⟨B7, 16, B8, 8, 1⟩,
   ⟨B8, 8, B9, 16, 1⟩,
   ⟨B9, 16, B0, 8, 1⟩]

set_option maxRecDepth 100000 in
set_option maxHeartbeats 4000000 in
theorem cert_ok : lcycleOK 13 cert B0 8 = true := by decide

set_option maxRecDepth 100000 in
theorem cert_minL : minL 13 cert = 1 := by decide

set_option maxRecDepth 100000 in
theorem cert_sumGam : sumGamL 13 cert = 3 := by decide

theorem cert_sumU : sumU cert = 10 := by decide

/-- Every band length `l ≥ 1`. -/
theorem lychrel_template (l : Nat) (hl : 1 ≤ l) : Lychrel 13 (val 13 (ltmpl B0 8 l)) :=
  lychrel_of_lcycle 13 cert B0 8 cert_ok l (by rw [cert_minL]; exact hl)

def seed : Nat := val 13 (ltmpl B0 8 1)

theorem lychrel_seed : Lychrel 13 seed := lychrel_template 1 (Nat.le_refl 1)

theorem exists_lychrel13 : ∃ n, Lychrel 13 n := ⟨seed, lychrel_seed⟩

end AbsorbingBand.Base13b

#print axioms AbsorbingBand.Base13b.cert_ok
#print axioms AbsorbingBand.Base13b.cert_minL
#print axioms AbsorbingBand.Base13b.lychrel_template
#print axioms AbsorbingBand.Base13b.exists_lychrel13
