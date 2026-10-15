import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 2, s0 = 13). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r2_13_0 : cert5.stepRow 2 13 0 = true := by decide +kernel
theorem r2_13_1 : cert5.stepRow 2 13 1 = true := by decide +kernel
theorem r2_13_2 : cert5.stepRow 2 13 2 = true := by decide +kernel
theorem r2_13_3 : cert5.stepRow 2 13 3 = true := by decide +kernel
theorem r2_13_4 : cert5.stepRow 2 13 4 = true := by decide +kernel
theorem r2_13_5 : cert5.stepRow 2 13 5 = true := by decide +kernel
theorem r2_13_6 : cert5.stepRow 2 13 6 = true := by decide +kernel
theorem r2_13_7 : cert5.stepRow 2 13 7 = true := by decide +kernel
theorem r2_13_8 : cert5.stepRow 2 13 8 = true := by decide +kernel
theorem r2_13_9 : cert5.stepRow 2 13 9 = true := by decide +kernel
theorem r2_13_10 : cert5.stepRow 2 13 10 = true := by decide +kernel
theorem r2_13_11 : cert5.stepRow 2 13 11 = true := by decide +kernel
theorem r2_13_12 : cert5.stepRow 2 13 12 = true := by decide +kernel
theorem r2_13_13 : cert5.stepRow 2 13 13 = true := by decide +kernel
theorem r2_13_14 : cert5.stepRow 2 13 14 = true := by decide +kernel
theorem r2_13_15 : cert5.stepRow 2 13 15 = true := by decide +kernel
theorem r2_13_16 : cert5.stepRow 2 13 16 = true := by decide +kernel
theorem r2_13_17 : cert5.stepRow 2 13 17 = true := by decide +kernel
theorem r2_13_18 : cert5.stepRow 2 13 18 = true := by decide +kernel

theorem r2_13 : ∀ b, b ≤ 18 → cert5.stepRow 2 13 b = true :=
  cover19 r2_13_0 r2_13_1 r2_13_2 r2_13_3 r2_13_4 r2_13_5 r2_13_6 r2_13_7 r2_13_8 r2_13_9 r2_13_10 r2_13_11 r2_13_12 r2_13_13 r2_13_14 r2_13_15 r2_13_16 r2_13_17 r2_13_18

end Agent113.FiveLayer
