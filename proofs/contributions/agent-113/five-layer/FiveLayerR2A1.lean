import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 2, s0 = 1). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r2_1_0 : cert5.stepRow 2 1 0 = true := by decide +kernel
theorem r2_1_1 : cert5.stepRow 2 1 1 = true := by decide +kernel
theorem r2_1_2 : cert5.stepRow 2 1 2 = true := by decide +kernel
theorem r2_1_3 : cert5.stepRow 2 1 3 = true := by decide +kernel
theorem r2_1_4 : cert5.stepRow 2 1 4 = true := by decide +kernel
theorem r2_1_5 : cert5.stepRow 2 1 5 = true := by decide +kernel
theorem r2_1_6 : cert5.stepRow 2 1 6 = true := by decide +kernel
theorem r2_1_7 : cert5.stepRow 2 1 7 = true := by decide +kernel
theorem r2_1_8 : cert5.stepRow 2 1 8 = true := by decide +kernel
theorem r2_1_9 : cert5.stepRow 2 1 9 = true := by decide +kernel
theorem r2_1_10 : cert5.stepRow 2 1 10 = true := by decide +kernel
theorem r2_1_11 : cert5.stepRow 2 1 11 = true := by decide +kernel
theorem r2_1_12 : cert5.stepRow 2 1 12 = true := by decide +kernel
theorem r2_1_13 : cert5.stepRow 2 1 13 = true := by decide +kernel
theorem r2_1_14 : cert5.stepRow 2 1 14 = true := by decide +kernel
theorem r2_1_15 : cert5.stepRow 2 1 15 = true := by decide +kernel
theorem r2_1_16 : cert5.stepRow 2 1 16 = true := by decide +kernel
theorem r2_1_17 : cert5.stepRow 2 1 17 = true := by decide +kernel
theorem r2_1_18 : cert5.stepRow 2 1 18 = true := by decide +kernel

theorem r2_1 : ∀ b, b ≤ 18 → cert5.stepRow 2 1 b = true :=
  cover19 r2_1_0 r2_1_1 r2_1_2 r2_1_3 r2_1_4 r2_1_5 r2_1_6 r2_1_7 r2_1_8 r2_1_9 r2_1_10 r2_1_11 r2_1_12 r2_1_13 r2_1_14 r2_1_15 r2_1_16 r2_1_17 r2_1_18

end Agent113.FiveLayer
