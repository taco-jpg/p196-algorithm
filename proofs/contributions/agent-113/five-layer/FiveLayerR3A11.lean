import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 3, s0 = 11). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r3_11_0 : cert5.stepRow 3 11 0 = true := by decide +kernel
theorem r3_11_1 : cert5.stepRow 3 11 1 = true := by decide +kernel
theorem r3_11_2 : cert5.stepRow 3 11 2 = true := by decide +kernel
theorem r3_11_3 : cert5.stepRow 3 11 3 = true := by decide +kernel
theorem r3_11_4 : cert5.stepRow 3 11 4 = true := by decide +kernel
theorem r3_11_5 : cert5.stepRow 3 11 5 = true := by decide +kernel
theorem r3_11_6 : cert5.stepRow 3 11 6 = true := by decide +kernel
theorem r3_11_7 : cert5.stepRow 3 11 7 = true := by decide +kernel
theorem r3_11_8 : cert5.stepRow 3 11 8 = true := by decide +kernel
theorem r3_11_9 : cert5.stepRow 3 11 9 = true := by decide +kernel
theorem r3_11_10 : cert5.stepRow 3 11 10 = true := by decide +kernel
theorem r3_11_11 : cert5.stepRow 3 11 11 = true := by decide +kernel
theorem r3_11_12 : cert5.stepRow 3 11 12 = true := by decide +kernel
theorem r3_11_13 : cert5.stepRow 3 11 13 = true := by decide +kernel
theorem r3_11_14 : cert5.stepRow 3 11 14 = true := by decide +kernel
theorem r3_11_15 : cert5.stepRow 3 11 15 = true := by decide +kernel
theorem r3_11_16 : cert5.stepRow 3 11 16 = true := by decide +kernel
theorem r3_11_17 : cert5.stepRow 3 11 17 = true := by decide +kernel
theorem r3_11_18 : cert5.stepRow 3 11 18 = true := by decide +kernel

theorem r3_11 : ∀ b, b ≤ 18 → cert5.stepRow 3 11 b = true :=
  cover19 r3_11_0 r3_11_1 r3_11_2 r3_11_3 r3_11_4 r3_11_5 r3_11_6 r3_11_7 r3_11_8 r3_11_9 r3_11_10 r3_11_11 r3_11_12 r3_11_13 r3_11_14 r3_11_15 r3_11_16 r3_11_17 r3_11_18

end Agent113.FiveLayer
