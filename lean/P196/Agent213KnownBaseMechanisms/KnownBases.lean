import P196.Drafts.Agent120NeutralBandCalibration.A120Certificate

/-!
# Agent 213: neutral-band calibration in bases 11, 17, 26

These certificates reconstruct known six-step families in bases 11 and 17
and the known four-step base-26 family. They do not establish a decimal
Lychrel number. All coefficient lists are LSD-first.
-/

namespace Agent213.KnownBases

open Agent120.Neutral

def exteriorQ : List Nat := [24, 28, 19, 36, 30, 15, 19, 12]
def exteriorR : List Nat := [49, 4, 40, 21, 9, 31, 38, 25]
def centerA : List Nat := [32, 20, 20, 32]
def centerB : List Nat := [12, 41, 41, 12]
def centerC : List Nat := [38, 28, 32, 28, 38]
def centerD : List Nat := [25, 6, 14, 6, 25]

def cert26 : List Edge :=
  [⟨exteriorQ, centerA, exteriorR, centerB, 0, 0⟩,
   ⟨exteriorR, centerB, exteriorQ, centerC, 1, 0⟩,
   ⟨exteriorQ, centerC, exteriorR, centerD, 0, 0⟩,
   ⟨exteriorR, centerD, exteriorQ, centerA, 1, 1⟩]

theorem cert26_ok : cycleOK 26 cert26 exteriorQ centerA = true := by decide
theorem cert26_overflows : sumGam 26 cert26 = 2 := by decide
theorem cert26_gain : sumGain cert26 = 3 := by decide

theorem lychrel26_template (g : Nat) (hg : 4 ≤ g) :
    Lychrel 26 (val 26 (tmpl 26 exteriorQ centerA g)) :=
  lychrel_of_cycle 26 cert26 exteriorQ centerA cert26_ok g
    (by rw [cert26_overflows]; exact hg)

def seed26 : Nat := val 26 (tmpl 26 exteriorQ centerA 4)

theorem lychrel26_seed : Lychrel 26 seed26 :=
  lychrel26_template 4 (Nat.le_refl 4)

theorem exists_lychrel26 : ∃ n, Lychrel 26 n := ⟨seed26, lychrel26_seed⟩

/-! ## Known base-11 six-step certificate -/

def exterior11_0 : List Nat := [3, 6, 9, 8, 9, 15, 7]

def center11_0 : List Nat := [11, 8, 8, 3, 7, 6, 7, 14, 13, 11, 14, 9, 9, 9, 8, 5, 15, 15, 1, 9, 11, 11, 9, 1, 15, 15, 5, 8, 9, 9, 9, 14, 11, 13, 14, 7, 6, 7, 3, 8, 8, 11]

def exterior11_1 : List Nat := [6, 12, 18, 16, 19, 8, 16]

def center11_1 : List Nat := [0, 17, 16, 6, 14, 12, 15, 7, 6, 2, 7, 19, 18, 18, 16, 11, 9, 9, 3, 19, 1, 1, 19, 3, 9, 9, 11, 16, 18, 18, 19, 7, 2, 6, 7, 15, 12, 14, 6, 16, 17, 0]

def exterior11_2 : List Nat := [13, 3, 16, 12, 17, 18, 10]

def center11_2 : List Nat := [2, 13, 11, 14, 7, 4, 9, 15, 12, 4, 15, 17, 16, 16, 12, 1, 19, 18, 7, 16, 3, 3, 16, 7, 18, 19, 1, 12, 16, 16, 17, 15, 4, 12, 15, 9, 4, 7, 14, 11, 13, 2]

def exterior11_3 : List Nat := [3, 6, 9, 8, 9, 15, 7]

def center11_3 : List Nat := [13, 5, 4, 5, 11, 11, 13, 14, 7, 6, 9, 12, 13, 12, 8, 3, 10, 17, 15, 13, 9, 6, 9, 13, 15, 17, 10, 3, 8, 12, 13, 12, 9, 6, 7, 14, 13, 11, 11, 5, 4, 5, 13]

def exterior11_4 : List Nat := [6, 12, 18, 16, 19, 8, 16]

def center11_4 : List Nat := [4, 11, 8, 11, 1, 2, 6, 7, 15, 12, 19, 3, 6, 3, 17, 7, 10, 13, 10, 5, 19, 12, 19, 5, 10, 13, 10, 7, 17, 3, 6, 3, 19, 12, 15, 7, 6, 2, 1, 11, 8, 11, 4]

def exterior11_5 : List Nat := [13, 3, 16, 12, 17, 18, 10]

def center11_5 : List Nat := [10, 0, 18, 0, 3, 4, 12, 15, 9, 4, 17, 7, 12, 7, 12, 16, 10, 4, 10, 12, 17, 4, 17, 12, 10, 4, 10, 16, 12, 7, 12, 7, 17, 4, 9, 15, 12, 4, 3, 0, 18, 0, 10]

def cert11 : List Edge :=
  [⟨exterior11_0, center11_0, exterior11_1, center11_1, 0, 0⟩,
   ⟨exterior11_1, center11_1, exterior11_2, center11_2, 0, 0⟩,
   ⟨exterior11_2, center11_2, exterior11_3, center11_3, 1, 0⟩,
   ⟨exterior11_3, center11_3, exterior11_4, center11_4, 0, 0⟩,
   ⟨exterior11_4, center11_4, exterior11_5, center11_5, 0, 0⟩,
   ⟨exterior11_5, center11_5, exterior11_0, center11_0, 1, 1⟩]

theorem cert11_ok : cycleOK 11 cert11 exterior11_0 center11_0 = true := by decide

theorem cert11_overflows : sumGam 11 cert11 = 2 := by decide

theorem cert11_gain : sumGain cert11 = 3 := by decide

theorem lychrel11_template (g : Nat) (hg : 4 ≤ g) :
    Lychrel 11 (val 11 (tmpl 11 exterior11_0 center11_0 g)) :=
  lychrel_of_cycle 11 cert11 exterior11_0 center11_0 cert11_ok g
    (by rw [cert11_overflows]; exact hg)

def seed11 : Nat := val 11 (tmpl 11 exterior11_0 center11_0 4)

theorem lychrel11_seed : Lychrel 11 seed11 :=
  lychrel11_template 4 (Nat.le_refl 4)

theorem exists_lychrel11 : ∃ n, Lychrel 11 n := ⟨seed11, lychrel11_seed⟩

/-! ## Known base-17 six-step certificate -/

def exterior17_0 : List Nat := [17, 0, 2, 5, 14, 21, 19, 11, 16, 17, 14, 20, 18, 10, 14, 28, 31, 29, 27, 17, 10, 11, 21, 20, 20, 17, 1, 17, 16]

def center17_0 : List Nat := [15, 31, 28, 12, 18, 1, 15, 31, 21, 5, 5, 21, 31, 15, 1, 18, 12, 28, 31, 15]

def exterior17_1 : List Nat := [1, 1, 2, 7, 19, 19, 8, 14, 28, 0, 15, 18, 6, 12, 24, 26, 27, 28, 24, 12, 11, 21, 16, 9, 8, 5, 2, 2, 0]

def center17_1 : List Nat := [32, 30, 27, 24, 14, 3, 16, 30, 20, 10, 10, 10, 20, 30, 16, 3, 14, 24, 27, 30, 32]

def exterior17_2 : List Nat := [2, 2, 4, 15, 5, 5, 17, 29, 22, 1, 31, 2, 13, 25, 15, 20, 22, 24, 15, 25, 23, 8, 16, 19, 16, 10, 4, 4, 1]

def center17_2 : List Nat := [31, 28, 22, 15, 29, 7, 16, 27, 7, 21, 20, 21, 7, 27, 16, 7, 29, 15, 22, 28, 31]

def exterior17_3 : List Nat := [4, 4, 8, 30, 10, 11, 1, 26, 11, 4, 28, 5, 27, 16, 32, 7, 12, 15, 32, 17, 13, 18, 16, 4, 16, 21, 8, 8, 3]

def center17_3 : List Nat := [29, 24, 11, 32, 24, 16, 16, 20, 16, 9, 8, 9, 16, 20, 16, 16, 24, 32, 11, 24, 29]

def exterior17_4 : List Nat := [8, 8, 17, 26, 21, 22, 3, 18, 23, 9, 22, 12, 21, 0, 31, 15, 24, 31, 31, 1, 28, 2, 16, 10, 16, 8, 17, 16, 7]

def center17_4 : List Nat := [25, 15, 24, 31, 16, 0, 0, 7, 16, 19, 16, 19, 16, 7, 0, 0, 16, 31, 24, 15, 25]

def exterior17_5 : List Nat := [16, 17, 1, 20, 10, 11, 8, 3, 13, 20, 10, 26, 8, 2, 28, 32, 15, 30, 29, 4, 22, 5, 32, 20, 32, 17, 0, 16, 16]

def center17_5 : List Nat := [16, 32, 15, 29, 16, 1, 0, 15, 16, 5, 0, 5, 16, 15, 0, 1, 16, 29, 15, 32, 16]

def cert17 : List Edge :=
  [⟨exterior17_0, center17_0, exterior17_1, center17_1, 1, 0⟩,
   ⟨exterior17_1, center17_1, exterior17_2, center17_2, 0, 0⟩,
   ⟨exterior17_2, center17_2, exterior17_3, center17_3, 0, 0⟩,
   ⟨exterior17_3, center17_3, exterior17_4, center17_4, 0, 0⟩,
   ⟨exterior17_4, center17_4, exterior17_5, center17_5, 0, 0⟩,
   ⟨exterior17_5, center17_5, exterior17_0, center17_0, 1, 1⟩]

theorem cert17_ok : cycleOK 17 cert17 exterior17_0 center17_0 = true := by decide

set_option maxRecDepth 2048 in
theorem cert17_overflows : sumGam 17 cert17 = 2 := by decide

theorem cert17_gain : sumGain cert17 = 3 := by decide

theorem lychrel17_template (g : Nat) (hg : 4 ≤ g) :
    Lychrel 17 (val 17 (tmpl 17 exterior17_0 center17_0 g)) :=
  lychrel_of_cycle 17 cert17 exterior17_0 center17_0 cert17_ok g
    (by rw [cert17_overflows]; exact hg)

def seed17 : Nat := val 17 (tmpl 17 exterior17_0 center17_0 4)

theorem lychrel17_seed : Lychrel 17 seed17 :=
  lychrel17_template 4 (Nat.le_refl 4)

theorem exists_lychrel17 : ∃ n, Lychrel 17 n := ⟨seed17, lychrel17_seed⟩

end Agent213.KnownBases

#print axioms Agent213.KnownBases.cert26_ok
#print axioms Agent213.KnownBases.cert26_overflows
#print axioms Agent213.KnownBases.cert26_gain
#print axioms Agent213.KnownBases.lychrel26_template
#print axioms Agent213.KnownBases.lychrel26_seed
#print axioms Agent213.KnownBases.exists_lychrel26

#print axioms Agent213.KnownBases.cert11_ok
#print axioms Agent213.KnownBases.cert11_overflows
#print axioms Agent213.KnownBases.cert11_gain
#print axioms Agent213.KnownBases.lychrel11_template
#print axioms Agent213.KnownBases.lychrel11_seed
#print axioms Agent213.KnownBases.exists_lychrel11
#print axioms Agent213.KnownBases.cert17_ok
#print axioms Agent213.KnownBases.cert17_overflows
#print axioms Agent213.KnownBases.cert17_gain
#print axioms Agent213.KnownBases.lychrel17_template
#print axioms Agent213.KnownBases.lychrel17_seed
#print axioms Agent213.KnownBases.exists_lychrel17
