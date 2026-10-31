import P196.Drafts.Agent120NeutralBandCalibration.A120Certificate

/-!
# Agent 116: an explicit base-20 neutral-band certificate

An independently reconstructed eight-edge cycle for the unchanged Agent120 checker.
It has two overflows and total trimming gain three. The imported soundness theorem
certifies every template gap at least four. No statement about base ten, 196, or
identity with an omitted historical witness is made.
-/

namespace Agent116.Base20

open Agent120.Neutral

def exterior20_0 : List Nat := [2, 19, 20, 13, 9, 25, 15, 26, 28, 14, 12, 16, 14, 13, 12, 13, 11, 5, 7, 12, 5, 7, 11, 20, 16, 11, 17, 10, 16, 27, 16, 16, 23, 12, 8, 7, 20, 32, 31, 34, 34, 27, 15, 4, 16, 20, 9, 23, 35, 29, 23, 20, 19, 22, 25, 30, 31, 28, 17, 9, 7, 12, 17, 17, 23, 22, 27, 34, 20, 21, 29, 22, 25, 21, 20, 12, 35, 31, 17, 16, 30, 32, 23, 12, 8, 15, 14, 2, 2, 11, 9]

def center20_0 : List Nat := [28, 26, 26, 9, 13, 22, 13, 17, 31, 35, 35, 32, 23, 23, 32, 35, 35, 31, 17, 13, 22, 13, 9, 26, 26, 28]

def exterior20_1 : List Nat := [5, 19, 0, 27, 19, 10, 32, 13, 17, 29, 24, 32, 28, 26, 24, 26, 22, 10, 14, 24, 10, 14, 23, 0, 33, 22, 34, 20, 33, 14, 33, 33, 6, 25, 16, 15, 1, 26, 24, 30, 30, 15, 31, 8, 33, 0, 20, 7, 32, 20, 8, 2, 0, 6, 12, 22, 24, 17, 35, 18, 14, 24, 34, 35, 7, 6, 16, 30, 2, 4, 20, 6, 12, 4, 1, 26, 31, 23, 35, 33, 21, 26, 7, 25, 16, 30, 28, 4, 4, 22]

def center20_1 : List Nat := [17, 14, 13, 19, 27, 4, 27, 35, 23, 32, 32, 26, 8, 8, 26, 32, 32, 23, 35, 27, 4, 27, 19, 13, 14, 17]

def exterior20_2 : List Nat := [10, 38, 1, 14, 19, 22, 24, 27, 35, 19, 10, 26, 18, 14, 10, 14, 5, 21, 29, 8, 21, 29, 6, 2, 27, 6, 30, 2, 27, 30, 27, 27, 14, 10, 33, 30, 3, 13, 10, 22, 21, 32, 22, 18, 26, 2, 0, 16, 25, 1, 17, 4, 0, 12, 25, 5, 9, 36, 30, 37, 29, 9, 30, 31, 15, 12, 33, 20, 5, 9, 0, 13, 24, 8, 3, 13, 24, 8, 32, 28, 4, 13, 16, 10, 34, 21, 17, 9, 9, 4]

def center20_2 : List Nat := [35, 28, 27, 19, 14, 10, 15, 32, 8, 26, 26, 13, 17, 17, 13, 26, 26, 8, 32, 15, 10, 14, 19, 27, 28, 35]

def exterior20_3 : List Nat := [21, 36, 3, 29, 19, 5, 10, 16, 31, 19, 22, 12, 37, 28, 20, 28, 11, 3, 19, 18, 3, 19, 13, 5, 14, 14, 20, 6, 15, 22, 16, 15, 29, 21, 27, 21, 7, 26, 21, 5, 4, 26, 5, 38, 12, 5, 0, 33, 10, 3, 34, 8, 0, 25, 10, 11, 19, 33, 22, 36, 19, 20, 21, 23, 31, 25, 27, 1, 11, 18, 0, 27, 8, 17, 6, 27, 8, 18, 25, 17, 9, 26, 32, 21, 29, 3, 35, 18, 18, 9]

def center20_3 : List Nat := [31, 18, 15, 19, 29, 20, 31, 24, 18, 13, 13, 27, 34, 34, 27, 13, 13, 18, 24, 31, 20, 29, 19, 15, 18, 31]

def exterior20_4 : List Nat := [2, 19, 20, 13, 9, 25, 15, 26, 28, 12, 3, 15, 30, 27, 10, 10, 20, 14, 22, 37, 21, 22, 32, 18, 19, 28, 15, 7, 21, 18, 19, 31, 25, 12, 10, 10, 9, 14, 9, 7, 9, 11, 12, 24, 31, 17, 5, 14, 24, 13, 18, 23, 8, 6, 16, 21, 31, 13, 17, 20, 17, 1, 3, 6, 16, 18, 14, 9, 12, 29, 18, 8, 16, 25, 23, 14, 16, 26, 24, 23, 26, 16, 20, 15, 12, 13, 19, 34, 36, 27, 29]

def center20_4 : List Nat := [11, 30, 33, 35, 9, 11, 13, 17, 23, 31, 26, 21, 23, 30, 23, 21, 26, 31, 23, 17, 13, 11, 9, 35, 33, 30, 11]

def exterior20_5 : List Nat := [5, 19, 0, 27, 19, 10, 32, 13, 17, 25, 6, 31, 21, 15, 21, 21, 0, 30, 5, 36, 4, 6, 25, 38, 19, 16, 31, 15, 2, 38, 19, 23, 11, 25, 20, 20, 18, 28, 18, 14, 18, 22, 25, 9, 23, 35, 10, 29, 8, 27, 37, 6, 17, 12, 33, 3, 23, 27, 35, 0, 35, 2, 6, 12, 32, 36, 28, 18, 25, 18, 37, 16, 33, 11, 7, 29, 33, 13, 10, 8, 13, 34, 0, 31, 24, 27, 19, 29, 34, 16]

def center20_5 : List Nat := [24, 21, 28, 31, 19, 22, 26, 35, 7, 24, 14, 4, 8, 22, 8, 4, 14, 24, 7, 35, 26, 22, 19, 31, 28, 21, 24]

def exterior20_6 : List Nat := [10, 38, 1, 14, 19, 22, 24, 27, 35, 10, 14, 23, 3, 32, 3, 3, 2, 20, 12, 32, 9, 13, 11, 37, 19, 34, 22, 31, 5, 37, 0, 7, 24, 11, 2, 1, 38, 16, 37, 28, 37, 5, 11, 20, 7, 31, 22, 18, 18, 15, 35, 13, 34, 25, 26, 8, 7, 16, 31, 2, 30, 5, 12, 25, 25, 34, 17, 38, 10, 38, 34, 34, 26, 23, 15, 19, 27, 27, 20, 16, 27, 28, 2, 23, 10, 16, 0, 20, 29, 34]

def center20_6 : List Nat := [9, 4, 18, 24, 0, 6, 14, 31, 16, 8, 29, 8, 17, 4, 17, 8, 29, 8, 16, 31, 14, 6, 0, 24, 18, 4, 9]

def exterior20_7 : List Nat := [21, 36, 3, 29, 19, 5, 10, 16, 31, 21, 29, 6, 8, 24, 7, 6, 5, 0, 26, 24, 19, 26, 23, 35, 0, 30, 6, 23, 12, 34, 1, 15, 8, 23, 4, 3, 36, 34, 35, 18, 35, 11, 23, 0, 16, 23, 5, 37, 36, 31, 30, 28, 29, 12, 13, 17, 14, 33, 22, 6, 20, 11, 25, 11, 12, 29, 36, 36, 22, 37, 30, 30, 14, 7, 32, 19, 15, 16, 1, 34, 15, 17, 6, 6, 21, 32, 1, 1, 20, 29]

def center20_7 : List Nat := [8, 37, 8, 1, 12, 29, 22, 33, 17, 18, 17, 34, 8, 34, 17, 18, 17, 33, 22, 29, 12, 1, 8, 37, 8]

def cert20 : List Edge :=
  [⟨exterior20_0, center20_0, exterior20_1, center20_1, 1, 0⟩,
   ⟨exterior20_1, center20_1, exterior20_2, center20_2, 0, 0⟩,
   ⟨exterior20_2, center20_2, exterior20_3, center20_3, 0, 0⟩,
   ⟨exterior20_3, center20_3, exterior20_4, center20_4, 0, 0⟩,
   ⟨exterior20_4, center20_4, exterior20_5, center20_5, 1, 0⟩,
   ⟨exterior20_5, center20_5, exterior20_6, center20_6, 0, 0⟩,
   ⟨exterior20_6, center20_6, exterior20_7, center20_7, 0, 1⟩,
   ⟨exterior20_7, center20_7, exterior20_0, center20_0, 0, 0⟩]

set_option maxRecDepth 8192 in
set_option maxHeartbeats 4000000 in
theorem cert20_ok : cycleOK 20 cert20 exterior20_0 center20_0 = true := by decide

set_option maxRecDepth 8192 in
theorem cert20_overflows : sumGam 20 cert20 = 2 := by decide

theorem cert20_gain : sumGain cert20 = 3 := by decide

theorem lychrel20_template (g : Nat) (hg : 4 ≤ g) :
    Lychrel 20 (val 20 (tmpl 20 exterior20_0 center20_0 g)) :=
  lychrel_of_cycle 20 cert20 exterior20_0 center20_0 cert20_ok g
    (by rw [cert20_overflows]; exact hg)

def seed20 : Nat := val 20 (tmpl 20 exterior20_0 center20_0 4)

theorem lychrel20_seed : Lychrel 20 seed20 :=
  lychrel20_template 4 (Nat.le_refl 4)

theorem exists_lychrel20 : ∃ n, Lychrel 20 n := ⟨seed20, lychrel20_seed⟩

end Agent116.Base20

#print axioms Agent116.Base20.cert20_ok
#print axioms Agent116.Base20.cert20_overflows
#print axioms Agent116.Base20.cert20_gain
#print axioms Agent116.Base20.lychrel20_template
#print axioms Agent116.Base20.lychrel20_seed
#print axioms Agent116.Base20.exists_lychrel20
