import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 4, s0 = 3). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r4_3_0 : cert5.stepRow 4 3 0 = true := by decide +kernel
theorem r4_3_1 : cert5.stepRow 4 3 1 = true := by decide +kernel
theorem r4_3_2 : cert5.stepRow 4 3 2 = true := by decide +kernel
theorem r4_3_3 : cert5.stepRow 4 3 3 = true := by decide +kernel
theorem r4_3_4 : cert5.stepRow 4 3 4 = true := by decide +kernel
theorem r4_3_5 : cert5.stepRow 4 3 5 = true := by decide +kernel
theorem r4_3_6 : cert5.stepRow 4 3 6 = true := by decide +kernel
theorem r4_3_7 : cert5.stepRow 4 3 7 = true := by decide +kernel
theorem r4_3_8 : cert5.stepRow 4 3 8 = true := by decide +kernel
theorem r4_3_9 : cert5.stepRow 4 3 9 = true := by decide +kernel
theorem r4_3_10 : cert5.stepRow 4 3 10 = true := by decide +kernel
theorem r4_3_11 : cert5.stepRow 4 3 11 = true := by decide +kernel
theorem r4_3_12 : cert5.stepRow 4 3 12 = true := by decide +kernel
theorem r4_3_13 : cert5.stepRow 4 3 13 = true := by decide +kernel
theorem r4_3_14 : cert5.stepRow 4 3 14 = true := by decide +kernel
theorem r4_3_15 : cert5.stepRow 4 3 15 = true := by decide +kernel
theorem r4_3_16 : cert5.stepRow 4 3 16 = true := by decide +kernel
theorem r4_3_17 : cert5.stepRow 4 3 17 = true := by decide +kernel
theorem r4_3_18 : cert5.stepRow 4 3 18 = true := by decide +kernel

theorem r4_3 : ∀ b, b ≤ 18 → cert5.stepRow 4 3 b = true :=
  cover19 r4_3_0 r4_3_1 r4_3_2 r4_3_3 r4_3_4 r4_3_5 r4_3_6 r4_3_7 r4_3_8 r4_3_9 r4_3_10 r4_3_11 r4_3_12 r4_3_13 r4_3_14 r4_3_15 r4_3_16 r4_3_17 r4_3_18

end Agent113.FiveLayer
