import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 3, s0 = 8). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r3_8_0 : cert5.stepRow 3 8 0 = true := by decide +kernel
theorem r3_8_1 : cert5.stepRow 3 8 1 = true := by decide +kernel
theorem r3_8_2 : cert5.stepRow 3 8 2 = true := by decide +kernel
theorem r3_8_3 : cert5.stepRow 3 8 3 = true := by decide +kernel
theorem r3_8_4 : cert5.stepRow 3 8 4 = true := by decide +kernel
theorem r3_8_5 : cert5.stepRow 3 8 5 = true := by decide +kernel
theorem r3_8_6 : cert5.stepRow 3 8 6 = true := by decide +kernel
theorem r3_8_7 : cert5.stepRow 3 8 7 = true := by decide +kernel
theorem r3_8_8 : cert5.stepRow 3 8 8 = true := by decide +kernel
theorem r3_8_9 : cert5.stepRow 3 8 9 = true := by decide +kernel
theorem r3_8_10 : cert5.stepRow 3 8 10 = true := by decide +kernel
theorem r3_8_11 : cert5.stepRow 3 8 11 = true := by decide +kernel
theorem r3_8_12 : cert5.stepRow 3 8 12 = true := by decide +kernel
theorem r3_8_13 : cert5.stepRow 3 8 13 = true := by decide +kernel
theorem r3_8_14 : cert5.stepRow 3 8 14 = true := by decide +kernel
theorem r3_8_15 : cert5.stepRow 3 8 15 = true := by decide +kernel
theorem r3_8_16 : cert5.stepRow 3 8 16 = true := by decide +kernel
theorem r3_8_17 : cert5.stepRow 3 8 17 = true := by decide +kernel
theorem r3_8_18 : cert5.stepRow 3 8 18 = true := by decide +kernel

theorem r3_8 : ∀ b, b ≤ 18 → cert5.stepRow 3 8 b = true :=
  cover19 r3_8_0 r3_8_1 r3_8_2 r3_8_3 r3_8_4 r3_8_5 r3_8_6 r3_8_7 r3_8_8 r3_8_9 r3_8_10 r3_8_11 r3_8_12 r3_8_13 r3_8_14 r3_8_15 r3_8_16 r3_8_17 r3_8_18

end Agent113.FiveLayer
