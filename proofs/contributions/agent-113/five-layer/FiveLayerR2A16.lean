import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 2, s0 = 16). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r2_16_0 : cert5.stepRow 2 16 0 = true := by decide +kernel
theorem r2_16_1 : cert5.stepRow 2 16 1 = true := by decide +kernel
theorem r2_16_2 : cert5.stepRow 2 16 2 = true := by decide +kernel
theorem r2_16_3 : cert5.stepRow 2 16 3 = true := by decide +kernel
theorem r2_16_4 : cert5.stepRow 2 16 4 = true := by decide +kernel
theorem r2_16_5 : cert5.stepRow 2 16 5 = true := by decide +kernel
theorem r2_16_6 : cert5.stepRow 2 16 6 = true := by decide +kernel
theorem r2_16_7 : cert5.stepRow 2 16 7 = true := by decide +kernel
theorem r2_16_8 : cert5.stepRow 2 16 8 = true := by decide +kernel
theorem r2_16_9 : cert5.stepRow 2 16 9 = true := by decide +kernel
theorem r2_16_10 : cert5.stepRow 2 16 10 = true := by decide +kernel
theorem r2_16_11 : cert5.stepRow 2 16 11 = true := by decide +kernel
theorem r2_16_12 : cert5.stepRow 2 16 12 = true := by decide +kernel
theorem r2_16_13 : cert5.stepRow 2 16 13 = true := by decide +kernel
theorem r2_16_14 : cert5.stepRow 2 16 14 = true := by decide +kernel
theorem r2_16_15 : cert5.stepRow 2 16 15 = true := by decide +kernel
theorem r2_16_16 : cert5.stepRow 2 16 16 = true := by decide +kernel
theorem r2_16_17 : cert5.stepRow 2 16 17 = true := by decide +kernel
theorem r2_16_18 : cert5.stepRow 2 16 18 = true := by decide +kernel

theorem r2_16 : ∀ b, b ≤ 18 → cert5.stepRow 2 16 b = true :=
  cover19 r2_16_0 r2_16_1 r2_16_2 r2_16_3 r2_16_4 r2_16_5 r2_16_6 r2_16_7 r2_16_8 r2_16_9 r2_16_10 r2_16_11 r2_16_12 r2_16_13 r2_16_14 r2_16_15 r2_16_16 r2_16_17 r2_16_18

end Agent113.FiveLayer
