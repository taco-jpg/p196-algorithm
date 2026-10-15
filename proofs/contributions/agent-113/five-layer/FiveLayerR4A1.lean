import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 4, s0 = 1). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r4_1_0 : cert5.stepRow 4 1 0 = true := by decide +kernel
theorem r4_1_1 : cert5.stepRow 4 1 1 = true := by decide +kernel
theorem r4_1_2 : cert5.stepRow 4 1 2 = true := by decide +kernel
theorem r4_1_3 : cert5.stepRow 4 1 3 = true := by decide +kernel
theorem r4_1_4 : cert5.stepRow 4 1 4 = true := by decide +kernel
theorem r4_1_5 : cert5.stepRow 4 1 5 = true := by decide +kernel
theorem r4_1_6 : cert5.stepRow 4 1 6 = true := by decide +kernel
theorem r4_1_7 : cert5.stepRow 4 1 7 = true := by decide +kernel
theorem r4_1_8 : cert5.stepRow 4 1 8 = true := by decide +kernel
theorem r4_1_9 : cert5.stepRow 4 1 9 = true := by decide +kernel
theorem r4_1_10 : cert5.stepRow 4 1 10 = true := by decide +kernel
theorem r4_1_11 : cert5.stepRow 4 1 11 = true := by decide +kernel
theorem r4_1_12 : cert5.stepRow 4 1 12 = true := by decide +kernel
theorem r4_1_13 : cert5.stepRow 4 1 13 = true := by decide +kernel
theorem r4_1_14 : cert5.stepRow 4 1 14 = true := by decide +kernel
theorem r4_1_15 : cert5.stepRow 4 1 15 = true := by decide +kernel
theorem r4_1_16 : cert5.stepRow 4 1 16 = true := by decide +kernel
theorem r4_1_17 : cert5.stepRow 4 1 17 = true := by decide +kernel
theorem r4_1_18 : cert5.stepRow 4 1 18 = true := by decide +kernel

theorem r4_1 : ∀ b, b ≤ 18 → cert5.stepRow 4 1 b = true :=
  cover19 r4_1_0 r4_1_1 r4_1_2 r4_1_3 r4_1_4 r4_1_5 r4_1_6 r4_1_7 r4_1_8 r4_1_9 r4_1_10 r4_1_11 r4_1_12 r4_1_13 r4_1_14 r4_1_15 r4_1_16 r4_1_17 r4_1_18

end Agent113.FiveLayer
