import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 2, s0 = 2). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r2_2_0 : cert5.stepRow 2 2 0 = true := by decide +kernel
theorem r2_2_1 : cert5.stepRow 2 2 1 = true := by decide +kernel
theorem r2_2_2 : cert5.stepRow 2 2 2 = true := by decide +kernel
theorem r2_2_3 : cert5.stepRow 2 2 3 = true := by decide +kernel
theorem r2_2_4 : cert5.stepRow 2 2 4 = true := by decide +kernel
theorem r2_2_5 : cert5.stepRow 2 2 5 = true := by decide +kernel
theorem r2_2_6 : cert5.stepRow 2 2 6 = true := by decide +kernel
theorem r2_2_7 : cert5.stepRow 2 2 7 = true := by decide +kernel
theorem r2_2_8 : cert5.stepRow 2 2 8 = true := by decide +kernel
theorem r2_2_9 : cert5.stepRow 2 2 9 = true := by decide +kernel
theorem r2_2_10 : cert5.stepRow 2 2 10 = true := by decide +kernel
theorem r2_2_11 : cert5.stepRow 2 2 11 = true := by decide +kernel
theorem r2_2_12 : cert5.stepRow 2 2 12 = true := by decide +kernel
theorem r2_2_13 : cert5.stepRow 2 2 13 = true := by decide +kernel
theorem r2_2_14 : cert5.stepRow 2 2 14 = true := by decide +kernel
theorem r2_2_15 : cert5.stepRow 2 2 15 = true := by decide +kernel
theorem r2_2_16 : cert5.stepRow 2 2 16 = true := by decide +kernel
theorem r2_2_17 : cert5.stepRow 2 2 17 = true := by decide +kernel
theorem r2_2_18 : cert5.stepRow 2 2 18 = true := by decide +kernel

theorem r2_2 : ∀ b, b ≤ 18 → cert5.stepRow 2 2 b = true :=
  cover19 r2_2_0 r2_2_1 r2_2_2 r2_2_3 r2_2_4 r2_2_5 r2_2_6 r2_2_7 r2_2_8 r2_2_9 r2_2_10 r2_2_11 r2_2_12 r2_2_13 r2_2_14 r2_2_15 r2_2_16 r2_2_17 r2_2_18

end Agent113.FiveLayer
