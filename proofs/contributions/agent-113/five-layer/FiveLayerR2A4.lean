import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 2, s0 = 4). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r2_4_0 : cert5.stepRow 2 4 0 = true := by decide +kernel
theorem r2_4_1 : cert5.stepRow 2 4 1 = true := by decide +kernel
theorem r2_4_2 : cert5.stepRow 2 4 2 = true := by decide +kernel
theorem r2_4_3 : cert5.stepRow 2 4 3 = true := by decide +kernel
theorem r2_4_4 : cert5.stepRow 2 4 4 = true := by decide +kernel
theorem r2_4_5 : cert5.stepRow 2 4 5 = true := by decide +kernel
theorem r2_4_6 : cert5.stepRow 2 4 6 = true := by decide +kernel
theorem r2_4_7 : cert5.stepRow 2 4 7 = true := by decide +kernel
theorem r2_4_8 : cert5.stepRow 2 4 8 = true := by decide +kernel
theorem r2_4_9 : cert5.stepRow 2 4 9 = true := by decide +kernel
theorem r2_4_10 : cert5.stepRow 2 4 10 = true := by decide +kernel
theorem r2_4_11 : cert5.stepRow 2 4 11 = true := by decide +kernel
theorem r2_4_12 : cert5.stepRow 2 4 12 = true := by decide +kernel
theorem r2_4_13 : cert5.stepRow 2 4 13 = true := by decide +kernel
theorem r2_4_14 : cert5.stepRow 2 4 14 = true := by decide +kernel
theorem r2_4_15 : cert5.stepRow 2 4 15 = true := by decide +kernel
theorem r2_4_16 : cert5.stepRow 2 4 16 = true := by decide +kernel
theorem r2_4_17 : cert5.stepRow 2 4 17 = true := by decide +kernel
theorem r2_4_18 : cert5.stepRow 2 4 18 = true := by decide +kernel

theorem r2_4 : ∀ b, b ≤ 18 → cert5.stepRow 2 4 b = true :=
  cover19 r2_4_0 r2_4_1 r2_4_2 r2_4_3 r2_4_4 r2_4_5 r2_4_6 r2_4_7 r2_4_8 r2_4_9 r2_4_10 r2_4_11 r2_4_12 r2_4_13 r2_4_14 r2_4_15 r2_4_16 r2_4_17 r2_4_18

end Agent113.FiveLayer
