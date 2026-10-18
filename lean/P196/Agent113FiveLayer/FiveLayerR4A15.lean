import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 4, s0 = 15). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r4_15_0 : cert5.stepRow 4 15 0 = true := by decide +kernel
theorem r4_15_1 : cert5.stepRow 4 15 1 = true := by decide +kernel
theorem r4_15_2 : cert5.stepRow 4 15 2 = true := by decide +kernel
theorem r4_15_3 : cert5.stepRow 4 15 3 = true := by decide +kernel
theorem r4_15_4 : cert5.stepRow 4 15 4 = true := by decide +kernel
theorem r4_15_5 : cert5.stepRow 4 15 5 = true := by decide +kernel
theorem r4_15_6 : cert5.stepRow 4 15 6 = true := by decide +kernel
theorem r4_15_7 : cert5.stepRow 4 15 7 = true := by decide +kernel
theorem r4_15_8 : cert5.stepRow 4 15 8 = true := by decide +kernel
theorem r4_15_9 : cert5.stepRow 4 15 9 = true := by decide +kernel
theorem r4_15_10 : cert5.stepRow 4 15 10 = true := by decide +kernel
theorem r4_15_11 : cert5.stepRow 4 15 11 = true := by decide +kernel
theorem r4_15_12 : cert5.stepRow 4 15 12 = true := by decide +kernel
theorem r4_15_13 : cert5.stepRow 4 15 13 = true := by decide +kernel
theorem r4_15_14 : cert5.stepRow 4 15 14 = true := by decide +kernel
theorem r4_15_15 : cert5.stepRow 4 15 15 = true := by decide +kernel
theorem r4_15_16 : cert5.stepRow 4 15 16 = true := by decide +kernel
theorem r4_15_17 : cert5.stepRow 4 15 17 = true := by decide +kernel
theorem r4_15_18 : cert5.stepRow 4 15 18 = true := by decide +kernel

theorem r4_15 : ∀ b, b ≤ 18 → cert5.stepRow 4 15 b = true :=
  cover19 r4_15_0 r4_15_1 r4_15_2 r4_15_3 r4_15_4 r4_15_5 r4_15_6 r4_15_7 r4_15_8 r4_15_9 r4_15_10 r4_15_11 r4_15_12 r4_15_13 r4_15_14 r4_15_15 r4_15_16 r4_15_17 r4_15_18

end Agent113.FiveLayer
