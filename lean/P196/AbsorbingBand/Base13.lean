import P196.AbsorbingBand.Cert

/-!
# Base 13: a ten-edge absorbing-band cycle (merged symmetric lattice format, uniform band)

Data from `cert_b13_rec0.json` (|B| = 75, band values alternate 16, 8, overflow word 1010010000).
The cycle is checked by `decide`; the theorem then follows from `lychrel_of_lcycle`.
-/

namespace AbsorbingBand.Base13

open AbsorbingBand Agent120.Neutral

def B0 : List Nat := [19, 9, 8, 19, 13, 19, 11, 9, 14, 1, 23, 12, 7, 21, 3, 10, 12, 0, 1, 17, 0, 1, 10, 16, 9, 2, 5, 23, 14, 14, 1, 11, 22, 9, 12, 11, 18, 4, 19, 19, 19, 21, 21, 23, 19, 1, 17, 4, 21, 17, 3, 22, 24, 23, 17, 19, 12, 1, 14, 6, 3, 16, 15, 9, 16, 1, 23, 12, 20, 23, 6, 12, 16, 16, 16]

def B1 : List Nat := [7, 16, 17, 15, 8, 8, 18, 20, 11, 3, 12, 10, 20, 16, 12, 13, 22, 12, 1, 6, 5, 1, 11, 14, 13, 11, 7, 16, 13, 4, 3, 12, 21, 19, 21, 23, 17, 10, 11, 14, 14, 16, 18, 20, 18, 8, 6, 9, 13, 14, 8, 13, 22, 23, 16, 12, 6, 14, 3, 8, 9, 7, 7, 12, 13, 5, 12, 11, 8, 19, 17, 19, 3, 8, 8]

def B2 : List Nat := [15, 7, 10, 5, 17, 17, 11, 15, 23, 6, 24, 21, 15, 8, 0, 2, 19, 12, 3, 12, 10, 2, 23, 3, 1, 23, 15, 7, 1, 9, 7, 12, 17, 14, 18, 22, 9, 21, 23, 3, 4, 8, 12, 16, 11, 17, 12, 19, 1, 3, 18, 1, 20, 22, 7, 12, 14, 2, 7, 16, 18, 14, 15, 12, 0, 11, 24, 22, 17, 13, 10, 13, 7, 16, 16]

def B3 : List Nat := [3, 10, 17, 15, 10, 10, 16, 14, 14, 17, 18, 21, 12, 11, 8, 2, 9, 6, 16, 15, 22, 12, 13, 14, 4, 12, 14, 10, 8, 10, 16, 20, 4, 7, 8, 16, 19, 18, 20, 14, 7, 12, 21, 3, 15, 16, 5, 7, 8, 4, 9, 7, 9, 18, 17, 20, 1, 4, 9, 11, 10, 8, 5, 2, 13, 11, 23, 22, 15, 6, 11, 11, 8, 11, 8]

def B4 : List Nat := [6, 21, 9, 5, 21, 21, 7, 4, 4, 10, 12, 17, 12, 23, 16, 4, 18, 13, 7, 6, 20, 0, 2, 3, 10, 12, 2, 21, 16, 21, 7, 15, 9, 14, 17, 7, 14, 12, 16, 3, 16, 12, 16, 8, 5, 7, 11, 14, 16, 8, 18, 14, 19, 11, 10, 15, 3, 8, 18, 22, 20, 16, 10, 5, 0, 24, 21, 20, 5, 13, 22, 22, 16, 22, 16]

def B5 : List Nat := [13, 16, 19, 11, 17, 17, 15, 8, 8, 21, 12, 9, 0, 22, 7, 10, 11, 1, 15, 13, 14, 1, 4, 6, 20, 24, 5, 17, 8, 17, 16, 4, 20, 3, 9, 16, 3, 0, 7, 8, 7, 0, 7, 17, 10, 14, 23, 3, 7, 18, 11, 4, 13, 23, 21, 4, 7, 17, 11, 20, 16, 7, 21, 10, 1, 23, 18, 15, 12, 1, 20, 20, 8, 20, 8]

def B6 : List Nat := [1, 5, 11, 18, 16, 10, 8, 11, 16, 17, 8, 22, 9, 10, 17, 17, 21, 12, 4, 4, 3, 3, 5, 10, 14, 20, 17, 10, 13, 13, 9, 8, 12, 11, 12, 13, 7, 3, 7, 15, 15, 7, 7, 12, 15, 12, 13, 14, 10, 13, 17, 15, 5, 12, 20, 13, 11, 12, 16, 19, 12, 11, 16, 19, 11, 12, 17, 9, 2, 14, 9, 16, 16, 16, 16]

def B7 : List Nat := [2, 10, 23, 11, 7, 21, 16, 23, 7, 9, 18, 18, 19, 21, 9, 10, 17, 12, 9, 8, 6, 6, 10, 21, 3, 16, 9, 22, 1, 1, 19, 16, 24, 23, 12, 0, 15, 6, 15, 5, 5, 15, 15, 12, 5, 0, 2, 3, 22, 1, 10, 5, 12, 12, 15, 1, 24, 12, 7, 13, 12, 24, 7, 13, 24, 12, 8, 19, 5, 2, 20, 7, 8, 8, 8]

def B8 : List Nat := [4, 21, 20, 23, 15, 17, 8, 21, 15, 19, 11, 12, 14, 17, 19, 21, 8, 12, 19, 16, 12, 12, 21, 16, 8, 6, 20, 18, 3, 3, 13, 8, 24, 21, 12, 2, 4, 14, 4, 11, 11, 5, 5, 12, 11, 0, 4, 7, 18, 3, 20, 11, 12, 12, 4, 4, 22, 12, 16, 1, 0, 23, 16, 1, 23, 12, 18, 12, 11, 5, 14, 15, 16, 16, 16]

def B9 : List Nat := [9, 17, 16, 22, 6, 9, 18, 17, 6, 13, 24, 12, 3, 10, 14, 17, 18, 12, 13, 8, 0, 0, 18, 7, 17, 13, 15, 11, 7, 7, 0, 18, 23, 17, 12, 5, 9, 2, 9, 22, 22, 10, 10, 24, 22, 0, 8, 15, 10, 8, 14, 23, 24, 24, 8, 9, 19, 0, 7, 3, 1, 21, 7, 4, 21, 0, 11, 12, 23, 11, 3, 6, 8, 8, 8]

def cert : List LEdge :=
  [⟨B0, 16, B1, 8, 1⟩,
   ⟨B1, 8, B2, 16, 1⟩,
   ⟨B2, 16, B3, 8, 1⟩,
   ⟨B3, 8, B4, 16, 1⟩,
   ⟨B4, 16, B5, 8, 1⟩,
   ⟨B5, 8, B6, 16, 1⟩,
   ⟨B6, 16, B7, 8, 1⟩,
   ⟨B7, 8, B8, 16, 1⟩,
   ⟨B8, 16, B9, 8, 1⟩,
   ⟨B9, 8, B0, 16, 1⟩]

set_option maxRecDepth 100000 in
set_option maxHeartbeats 4000000 in
theorem cert_ok : lcycleOK 13 cert B0 16 = true := by decide

set_option maxRecDepth 100000 in
theorem cert_minL : minL 13 cert = 1 := by decide

set_option maxRecDepth 100000 in
theorem cert_sumGam : sumGamL 13 cert = 3 := by decide

theorem cert_sumU : sumU cert = 10 := by decide

/-- Every band length `l ≥ 1`. -/
theorem lychrel_template (l : Nat) (hl : 1 ≤ l) : Lychrel 13 (val 13 (ltmpl B0 16 l)) :=
  lychrel_of_lcycle 13 cert B0 16 cert_ok l (by rw [cert_minL]; exact hl)

def seed : Nat := val 13 (ltmpl B0 16 1)

theorem lychrel_seed : Lychrel 13 seed := lychrel_template 1 (Nat.le_refl 1)

theorem exists_lychrel13 : ∃ n, Lychrel 13 n := ⟨seed, lychrel_seed⟩

end AbsorbingBand.Base13

#print axioms AbsorbingBand.Base13.cert_ok
#print axioms AbsorbingBand.Base13.cert_minL
#print axioms AbsorbingBand.Base13.lychrel_template
#print axioms AbsorbingBand.Base13.exists_lychrel13
