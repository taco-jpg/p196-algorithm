import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 4, s0 = 2). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r4_2_0 : cert5.stepRow 4 2 0 = true := by decide +kernel
theorem r4_2_1 : cert5.stepRow 4 2 1 = true := by decide +kernel
theorem r4_2_2 : cert5.stepRow 4 2 2 = true := by decide +kernel
theorem r4_2_3 : cert5.stepRow 4 2 3 = true := by decide +kernel
theorem r4_2_4 : cert5.stepRow 4 2 4 = true := by decide +kernel
theorem r4_2_5 : cert5.stepRow 4 2 5 = true := by decide +kernel
theorem r4_2_6 : cert5.stepRow 4 2 6 = true := by decide +kernel
theorem r4_2_7 : cert5.stepRow 4 2 7 = true := by decide +kernel
theorem r4_2_8 : cert5.stepRow 4 2 8 = true := by decide +kernel
theorem r4_2_9 : cert5.stepRow 4 2 9 = true := by decide +kernel
theorem r4_2_10 : cert5.stepRow 4 2 10 = true := by decide +kernel
theorem r4_2_11 : cert5.stepRow 4 2 11 = true := by decide +kernel
theorem r4_2_12 : cert5.stepRow 4 2 12 = true := by decide +kernel
theorem r4_2_13 : cert5.stepRow 4 2 13 = true := by decide +kernel
theorem r4_2_14 : cert5.stepRow 4 2 14 = true := by decide +kernel
theorem r4_2_15 : cert5.stepRow 4 2 15 = true := by decide +kernel
theorem r4_2_16 : cert5.stepRow 4 2 16 = true := by decide +kernel
theorem r4_2_17 : cert5.stepRow 4 2 17 = true := by decide +kernel
theorem r4_2_18 : cert5.stepRow 4 2 18 = true := by decide +kernel

theorem r4_2 : ∀ b, b ≤ 18 → cert5.stepRow 4 2 b = true :=
  cover19 r4_2_0 r4_2_1 r4_2_2 r4_2_3 r4_2_4 r4_2_5 r4_2_6 r4_2_7 r4_2_8 r4_2_9 r4_2_10 r4_2_11 r4_2_12 r4_2_13 r4_2_14 r4_2_15 r4_2_16 r4_2_17 r4_2_18

end Agent113.FiveLayer
