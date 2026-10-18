import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 4, s0 = 16). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r4_16_0 : cert5.stepRow 4 16 0 = true := by decide +kernel
theorem r4_16_1 : cert5.stepRow 4 16 1 = true := by decide +kernel
theorem r4_16_2 : cert5.stepRow 4 16 2 = true := by decide +kernel
theorem r4_16_3 : cert5.stepRow 4 16 3 = true := by decide +kernel
theorem r4_16_4 : cert5.stepRow 4 16 4 = true := by decide +kernel
theorem r4_16_5 : cert5.stepRow 4 16 5 = true := by decide +kernel
theorem r4_16_6 : cert5.stepRow 4 16 6 = true := by decide +kernel
theorem r4_16_7 : cert5.stepRow 4 16 7 = true := by decide +kernel
theorem r4_16_8 : cert5.stepRow 4 16 8 = true := by decide +kernel
theorem r4_16_9 : cert5.stepRow 4 16 9 = true := by decide +kernel
theorem r4_16_10 : cert5.stepRow 4 16 10 = true := by decide +kernel
theorem r4_16_11 : cert5.stepRow 4 16 11 = true := by decide +kernel
theorem r4_16_12 : cert5.stepRow 4 16 12 = true := by decide +kernel
theorem r4_16_13 : cert5.stepRow 4 16 13 = true := by decide +kernel
theorem r4_16_14 : cert5.stepRow 4 16 14 = true := by decide +kernel
theorem r4_16_15 : cert5.stepRow 4 16 15 = true := by decide +kernel
theorem r4_16_16 : cert5.stepRow 4 16 16 = true := by decide +kernel
theorem r4_16_17 : cert5.stepRow 4 16 17 = true := by decide +kernel
theorem r4_16_18 : cert5.stepRow 4 16 18 = true := by decide +kernel

theorem r4_16 : ∀ b, b ≤ 18 → cert5.stepRow 4 16 b = true :=
  cover19 r4_16_0 r4_16_1 r4_16_2 r4_16_3 r4_16_4 r4_16_5 r4_16_6 r4_16_7 r4_16_8 r4_16_9 r4_16_10 r4_16_11 r4_16_12 r4_16_13 r4_16_14 r4_16_15 r4_16_16 r4_16_17 r4_16_18

end Agent113.FiveLayer
