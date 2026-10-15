import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 3, s0 = 1). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r3_1_0 : cert5.stepRow 3 1 0 = true := by decide +kernel
theorem r3_1_1 : cert5.stepRow 3 1 1 = true := by decide +kernel
theorem r3_1_2 : cert5.stepRow 3 1 2 = true := by decide +kernel
theorem r3_1_3 : cert5.stepRow 3 1 3 = true := by decide +kernel
theorem r3_1_4 : cert5.stepRow 3 1 4 = true := by decide +kernel
theorem r3_1_5 : cert5.stepRow 3 1 5 = true := by decide +kernel
theorem r3_1_6 : cert5.stepRow 3 1 6 = true := by decide +kernel
theorem r3_1_7 : cert5.stepRow 3 1 7 = true := by decide +kernel
theorem r3_1_8 : cert5.stepRow 3 1 8 = true := by decide +kernel
theorem r3_1_9 : cert5.stepRow 3 1 9 = true := by decide +kernel
theorem r3_1_10 : cert5.stepRow 3 1 10 = true := by decide +kernel
theorem r3_1_11 : cert5.stepRow 3 1 11 = true := by decide +kernel
theorem r3_1_12 : cert5.stepRow 3 1 12 = true := by decide +kernel
theorem r3_1_13 : cert5.stepRow 3 1 13 = true := by decide +kernel
theorem r3_1_14 : cert5.stepRow 3 1 14 = true := by decide +kernel
theorem r3_1_15 : cert5.stepRow 3 1 15 = true := by decide +kernel
theorem r3_1_16 : cert5.stepRow 3 1 16 = true := by decide +kernel
theorem r3_1_17 : cert5.stepRow 3 1 17 = true := by decide +kernel
theorem r3_1_18 : cert5.stepRow 3 1 18 = true := by decide +kernel

theorem r3_1 : ∀ b, b ≤ 18 → cert5.stepRow 3 1 b = true :=
  cover19 r3_1_0 r3_1_1 r3_1_2 r3_1_3 r3_1_4 r3_1_5 r3_1_6 r3_1_7 r3_1_8 r3_1_9 r3_1_10 r3_1_11 r3_1_12 r3_1_13 r3_1_14 r3_1_15 r3_1_16 r3_1_17 r3_1_18

end Agent113.FiveLayer
