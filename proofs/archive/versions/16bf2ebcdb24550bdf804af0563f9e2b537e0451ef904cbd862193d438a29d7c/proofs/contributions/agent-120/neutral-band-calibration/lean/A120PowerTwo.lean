import A120Certificate

/-!
# Agent #120: kernel-checked neutral-band certificates in bases 2, 4, 8, 16, 32

These are **not decimal results** and say nothing about 196. They calibrate
the base-generic template method of `A120Certificate` against bases where
Lychrel numbers are known to exist (all powers of two; no novelty is claimed).

For `b = 2^m` the certified cycle starts at exterior `[b]` and center
`[b-2, b-2]` and has `2m + 2` edges, two overflows and three neutral
coefficients moved into the band per cycle (net gap gain one).

Every certificate check is `decide` (kernel reduction); no `native_decide`.
The seeds `22` (base 2), `318` (base 4), `4522` (base 8) and `69630`
(base 16) are checked to reach the certified template with gap four,
without an earlier palindrome.
-/

namespace Agent120.Neutral.PowerTwo

open Agent120.Neutral

def cert2 : List Edge :=
  [⟨[2], [0, 0], [1, 0], [2, 0, 2], 0, 0⟩,
   ⟨[1, 0], [2, 0, 2], [2], [0, 2, 0], 1, 0⟩,
   ⟨[2], [0, 2, 0], [1, 0], [2, 1, 1, 2], 0, 0⟩,
   ⟨[1, 0], [2, 1, 1, 2], [2], [0, 0], 1, 1⟩]

def cert4 : List Edge :=
  [⟨[4], [2, 2], [1, 0], [6, 4, 6], 0, 0⟩,
   ⟨[1, 0], [6, 4, 6], [2, 1], [5, 2, 5], 0, 0⟩,
   ⟨[2, 1], [5, 2, 5], [4], [2, 6, 2], 1, 0⟩,
   ⟨[4], [2, 6, 2], [1, 0], [6, 5, 5, 6], 0, 0⟩,
   ⟨[1, 0], [6, 5, 5, 6], [2, 1], [5, 4, 4, 5], 0, 0⟩,
   ⟨[2, 1], [5, 4, 4, 5], [4], [2, 2], 1, 1⟩]

def cert8 : List Edge :=
  [⟨[8], [6, 6], [1, 0], [14, 12, 14], 0, 0⟩,
   ⟨[1, 0], [14, 12, 14], [2, 1], [13, 10, 13], 0, 0⟩,
   ⟨[2, 1], [13, 10, 13], [4, 3], [11, 6, 11], 0, 0⟩,
   ⟨[4, 3], [11, 6, 11], [8], [6, 14, 6], 1, 0⟩,
   ⟨[8], [6, 14, 6], [1, 0], [14, 13, 13, 14], 0, 0⟩,
   ⟨[1, 0], [14, 13, 13, 14], [2, 1], [13, 12, 12, 13], 0, 0⟩,
   ⟨[2, 1], [13, 12, 12, 13], [4, 3], [11, 10, 10, 11], 0, 0⟩,
   ⟨[4, 3], [11, 10, 10, 11], [8], [6, 6], 1, 1⟩]

def cert16 : List Edge :=
  [⟨[16], [14, 14], [1, 0], [30, 28, 30], 0, 0⟩,
   ⟨[1, 0], [30, 28, 30], [2, 1], [29, 26, 29], 0, 0⟩,
   ⟨[2, 1], [29, 26, 29], [4, 3], [27, 22, 27], 0, 0⟩,
   ⟨[4, 3], [27, 22, 27], [8, 7], [23, 14, 23], 0, 0⟩,
   ⟨[8, 7], [23, 14, 23], [16], [14, 30, 14], 1, 0⟩,
   ⟨[16], [14, 30, 14], [1, 0], [30, 29, 29, 30], 0, 0⟩,
   ⟨[1, 0], [30, 29, 29, 30], [2, 1], [29, 28, 28, 29], 0, 0⟩,
   ⟨[2, 1], [29, 28, 28, 29], [4, 3], [27, 26, 26, 27], 0, 0⟩,
   ⟨[4, 3], [27, 26, 26, 27], [8, 7], [23, 22, 22, 23], 0, 0⟩,
   ⟨[8, 7], [23, 22, 22, 23], [16], [14, 14], 1, 1⟩]

def cert32 : List Edge :=
  [⟨[32], [30, 30], [1, 0], [62, 60, 62], 0, 0⟩,
   ⟨[1, 0], [62, 60, 62], [2, 1], [61, 58, 61], 0, 0⟩,
   ⟨[2, 1], [61, 58, 61], [4, 3], [59, 54, 59], 0, 0⟩,
   ⟨[4, 3], [59, 54, 59], [8, 7], [55, 46, 55], 0, 0⟩,
   ⟨[8, 7], [55, 46, 55], [16, 15], [47, 30, 47], 0, 0⟩,
   ⟨[16, 15], [47, 30, 47], [32], [30, 62, 30], 1, 0⟩,
   ⟨[32], [30, 62, 30], [1, 0], [62, 61, 61, 62], 0, 0⟩,
   ⟨[1, 0], [62, 61, 61, 62], [2, 1], [61, 60, 60, 61], 0, 0⟩,
   ⟨[2, 1], [61, 60, 60, 61], [4, 3], [59, 58, 58, 59], 0, 0⟩,
   ⟨[4, 3], [59, 58, 58, 59], [8, 7], [55, 54, 54, 55], 0, 0⟩,
   ⟨[8, 7], [55, 54, 54, 55], [16, 15], [47, 46, 46, 47], 0, 0⟩,
   ⟨[16, 15], [47, 46, 46, 47], [32], [30, 30], 1, 1⟩]

theorem cert2_ok : cycleOK 2 cert2 [2] [0, 0] = true := by decide
theorem cert4_ok : cycleOK 4 cert4 [4] [2, 2] = true := by decide
theorem cert8_ok : cycleOK 8 cert8 [8] [6, 6] = true := by decide
theorem cert16_ok : cycleOK 16 cert16 [16] [14, 14] = true := by decide
theorem cert32_ok : cycleOK 32 cert32 [32] [30, 30] = true := by decide

theorem sumGam2 : sumGam 2 cert2 = 2 := by decide
theorem sumGam4 : sumGam 4 cert4 = 2 := by decide
theorem sumGam8 : sumGam 8 cert8 = 2 := by decide
theorem sumGam16 : sumGam 16 cert16 = 2 := by decide
theorem sumGam32 : sumGam 32 cert32 = 2 := by decide

/-- Every template value with gap at least four is a base-2 Lychrel number. -/
theorem lychrel2_template (g : Nat) (hg : 4 ≤ g) : Lychrel 2 (val 2 (tmpl 2 [2] [0, 0] g)) :=
  lychrel_of_cycle 2 cert2 [2] [0, 0] cert2_ok g (by rw [sumGam2]; omega)

theorem lychrel4_template (g : Nat) (hg : 4 ≤ g) : Lychrel 4 (val 4 (tmpl 4 [4] [2, 2] g)) :=
  lychrel_of_cycle 4 cert4 [4] [2, 2] cert4_ok g (by rw [sumGam4]; omega)

theorem lychrel8_template (g : Nat) (hg : 4 ≤ g) : Lychrel 8 (val 8 (tmpl 8 [8] [6, 6] g)) :=
  lychrel_of_cycle 8 cert8 [8] [6, 6] cert8_ok g (by rw [sumGam8]; omega)

theorem lychrel16_template (g : Nat) (hg : 4 ≤ g) :
    Lychrel 16 (val 16 (tmpl 16 [16] [14, 14] g)) :=
  lychrel_of_cycle 16 cert16 [16] [14, 14] cert16_ok g (by rw [sumGam16]; omega)

theorem lychrel32_template (g : Nat) (hg : 4 ≤ g) :
    Lychrel 32 (val 32 (tmpl 32 [32] [30, 30] g)) :=
  lychrel_of_cycle 32 cert32 [32] [30, 30] cert32_ok g (by rw [sumGam32]; omega)

/-! ## Explicit seeds -/

theorem entry22 : orbit 2 22 14 = val 2 (tmpl 2 [2] [0, 0] 4) := by decide
theorem prefix22 : ∀ k, k < 14 → ¬ IsPal 2 (orbit 2 22 k) := by decide

/-- `22 = 10110₂` is a base-2 Lychrel number (kernel-checked; known in the literature). -/
theorem lychrel2_22 : Lychrel 2 22 :=
  lychrel_of_entry 2 22 14 _ prefix22 entry22 (lychrel2_template 4 (Nat.le_refl 4))

theorem entry318 : orbit 4 318 20 = val 4 (tmpl 4 [4] [2, 2] 4) := by decide
theorem prefix318 : ∀ k, k < 20 → ¬ IsPal 4 (orbit 4 318 k) := by decide

/-- `318 = 10332₄` is a base-4 Lychrel number. -/
theorem lychrel4_318 : Lychrel 4 318 :=
  lychrel_of_entry 4 318 20 _ prefix318 entry318 (lychrel4_template 4 (Nat.le_refl 4))

theorem entry4522 : orbit 8 4522 24 = val 8 (tmpl 8 [8] [6, 6] 4) := by decide
theorem prefix4522 : ∀ k, k < 24 → ¬ IsPal 8 (orbit 8 4522 k) := by decide

/-- `4522 = 10652₈` is a base-8 Lychrel number. -/
theorem lychrel8_4522 : Lychrel 8 4522 :=
  lychrel_of_entry 8 4522 24 _ prefix4522 entry4522 (lychrel8_template 4 (Nat.le_refl 4))

theorem entry69630 : orbit 16 69630 32 = val 16 (tmpl 16 [16] [14, 14] 4) := by decide
theorem prefix69630 : ∀ k, k < 32 → ¬ IsPal 16 (orbit 16 69630 k) := by decide

/-- `69630 = 10FFE₁₆` is a base-16 Lychrel number. -/
theorem lychrel16_69630 : Lychrel 16 69630 :=
  lychrel_of_entry 16 69630 32 _ prefix69630 entry69630 (lychrel16_template 4 (Nat.le_refl 4))

end Agent120.Neutral.PowerTwo

#print axioms Agent120.Neutral.PowerTwo.cert2_ok
#print axioms Agent120.Neutral.PowerTwo.lychrel2_22
#print axioms Agent120.Neutral.PowerTwo.lychrel4_318
#print axioms Agent120.Neutral.PowerTwo.lychrel8_4522
#print axioms Agent120.Neutral.PowerTwo.lychrel16_69630
#print axioms Agent120.Neutral.PowerTwo.lychrel32_template
