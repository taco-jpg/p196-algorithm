import P196.LatticeBand.Cert

/-!
# Base 9: a ten-edge lattice cycle (period block of length 4, |B| = 61)

Data from `cert_b9_rec0.json` (symmetry axis 1, `l0 = 2` modulo the period).
The cycle is checked by `decide`; the theorem then follows from `lychrel_of_lcycle`.
Overflow word `1100011000`; band phase `ρ` along the cycle: `[2, 3, 0, 0, 0, 0, 1, 2, 2, 2]`.
-/

namespace LatticeBand.Base9

open LatticeBand Agent120.Neutral

def B0 : List Nat := [8, 9, 10, 13, 14, 12, 3, 14, 10, 0, 11, 7, 10, 9, 7, 8, 8, 14, 15, 2, 9, 7, 0, 5, 8, 3, 8, 11, 8, 6, 8, 7, 5, 14, 11, 3, 9, 3, 8, 14, 7, 12, 8, 2, 0, 12, 1, 5, 13, 8, 1, 16, 15, 9, 1, 7, 6, 2, 1, 15, 15]

def B1 : List Nat := [9, 0, 3, 7, 11, 10, 7, 9, 8, 2, 3, 10, 9, 3, 8, 16, 8, 5, 13, 9, 3, 8, 7, 5, 13, 11, 12, 2, 2, 15, 14, 15, 12, 11, 9, 6, 4, 4, 12, 5, 13, 11, 3, 11, 2, 4, 5, 6, 10, 4, 10, 9, 15, 8, 2, 8, 13, 8, 3, 8, 14]

def B2 : List Nat := [1, 1, 3, 10, 10, 5, 9, 8, 0, 11, 5, 5, 3, 4, 12, 7, 7, 14, 10, 6, 4, 11, 15, 12, 10, 8, 7, 6, 4, 9, 13, 13, 11, 7, 4, 7, 10, 8, 8, 9, 10, 8, 6, 6, 5, 6, 9, 11, 8, 6, 6, 3, 8, 6, 11, 11, 4, 4, 12, 12, 5]

def B3 : List Nat := [2, 2, 7, 3, 3, 12, 0, 8, 2, 4, 11, 10, 6, 9, 6, 15, 15, 11, 3, 13, 9, 5, 14, 8, 3, 8, 15, 12, 9, 1, 10, 10, 5, 15, 8, 15, 3, 0, 0, 2, 3, 8, 13, 12, 10, 13, 1, 5, 8, 13, 12, 6, 16, 13, 5, 5, 9, 9, 7, 7, 11]

def B4 : List Nat := [4, 4, 14, 6, 7, 6, 1, 16, 4, 9, 5, 3, 14, 0, 14, 13, 14, 5, 8, 9, 1, 12, 10, 8, 8, 8, 13, 8, 1, 4, 3, 3, 12, 13, 0, 13, 7, 0, 0, 4, 7, 8, 9, 8, 4, 9, 3, 11, 8, 9, 7, 14, 15, 9, 11, 11, 1, 1, 15, 15, 5]

def B5 : List Nat := [8, 9, 10, 13, 14, 12, 3, 14, 10, 0, 11, 7, 10, 2, 11, 10, 11, 12, 8, 0, 4, 7, 4, 0, 0, 0, 9, 8, 3, 8, 6, 7, 7, 9, 2, 8, 15, 0, 0, 8, 15, 8, 0, 8, 10, 0, 8, 5, 0, 1, 16, 11, 14, 2, 6, 5, 3, 3, 13, 13, 11]

def B6 : List Nat := [9, 0, 3, 7, 11, 10, 7, 9, 8, 2, 3, 10, 9, 4, 5, 5, 5, 7, 3, 9, 4, 11, 11, 4, 0, 0, 1, 0, 12, 11, 14, 13, 14, 8, 3, 11, 6, 7, 0, 9, 6, 6, 9, 9, 1, 2, 8, 13, 5, 1, 9, 11, 9, 8, 8, 11, 8, 6, 8, 10, 8]

def B7 : List Nat := [1, 1, 3, 10, 10, 5, 9, 8, 0, 11, 5, 5, 3, 5, 9, 10, 10, 12, 10, 4, 5, 7, 6, 7, 4, 0, 1, 1, 4, 7, 9, 11, 11, 5, 12, 6, 9, 13, 7, 1, 7, 12, 7, 2, 2, 3, 11, 4, 10, 6, 2, 4, 4, 1, 0, 3, 2, 15, 15, 1, 1]

def B8 : List Nat := [2, 2, 7, 3, 3, 12, 0, 8, 2, 4, 11, 10, 6, 11, 1, 4, 4, 8, 3, 9, 10, 14, 12, 14, 8, 0, 2, 2, 8, 15, 1, 6, 5, 12, 6, 14, 1, 9, 15, 2, 15, 6, 15, 4, 4, 7, 4, 10, 2, 13, 4, 8, 8, 2, 0, 6, 5, 13, 13, 3, 3]

def B9 : List Nat := [4, 4, 14, 6, 7, 6, 1, 16, 4, 9, 5, 3, 14, 4, 3, 8, 8, 16, 7, 1, 4, 12, 8, 11, 8, 1, 4, 5, 8, 12, 3, 12, 11, 6, 14, 10, 4, 1, 13, 6, 12, 14, 12, 9, 8, 14, 9, 2, 6, 8, 9, 16, 16, 4, 0, 12, 11, 9, 9, 7, 7]

def W0 : List Nat := [1, 1, 15, 15]

def W1 : List Nat := [8, 2, 8, 14]

def W2 : List Nat := [5, 11, 11, 5]

def W3 : List Nat := [11, 5, 5, 11]

def W4 : List Nat := [5, 11, 11, 5]

def W5 : List Nat := [11, 5, 5, 11]

def W6 : List Nat := [6, 8, 10, 8]

def W7 : List Nat := [15, 15, 1, 1]

def W8 : List Nat := [13, 13, 3, 3]

def W9 : List Nat := [9, 9, 7, 7]

def cert : List LEdge :=
  [⟨B0, W0, 2, B1, W1⟩,
   ⟨B1, W1, 3, B2, W2⟩,
   ⟨B2, W2, 0, B3, W3⟩,
   ⟨B3, W3, 0, B4, W4⟩,
   ⟨B4, W4, 0, B5, W5⟩,
   ⟨B5, W5, 0, B6, W6⟩,
   ⟨B6, W6, 1, B7, W7⟩,
   ⟨B7, W7, 2, B8, W8⟩,
   ⟨B8, W8, 2, B9, W9⟩,
   ⟨B9, W9, 2, B0, W0⟩]

set_option maxRecDepth 100000 in
set_option maxHeartbeats 4000000 in
theorem cert_ok : lcycleOK 9 cert B0 W0 2 = true := by decide +kernel

theorem cert_sumGam : sumGamL 9 cert = 4 := by decide +kernel

/-- Every band length `l ≥ 8` with `l ≡ 2 (mod 4)`. -/
theorem lychrel_template (l : Nat) (hl : 8 ≤ l) (hρ : l % 4 = 2) :
    Lychrel 9 (val 9 (tm B0 W0 l)) :=
  lychrel_of_lcycle 9 cert B0 W0 2 cert_ok l
    (by have h4 : W0.length = 4 := rfl; omega)
    (by have h4 : W0.length = 4 := rfl; rw [h4]; exact hρ)

def seed : Nat := val 9 (tm B0 W0 10)

theorem lychrel_seed : Lychrel 9 seed :=
  lychrel_template 10 (by omega) (by decide)

theorem exists_lychrel9 : ∃ n, Lychrel 9 n := ⟨seed, lychrel_seed⟩

/-- Negative control: the same data with a wrong starting phase is rejected by the checker. -/
theorem cert_wrong_phase : lcycleOK 9 cert B0 W0 3 = false := by decide +kernel

end LatticeBand.Base9

#print axioms LatticeBand.Base9.cert_ok
#print axioms LatticeBand.Base9.exists_lychrel9
