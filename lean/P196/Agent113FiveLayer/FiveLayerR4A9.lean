import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 4, s0 = 9). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r4_9_0 : cert5.stepRow 4 9 0 = true := by decide +kernel
theorem r4_9_1 : cert5.stepRow 4 9 1 = true := by decide +kernel
theorem r4_9_2 : cert5.stepRow 4 9 2 = true := by decide +kernel
theorem r4_9_3 : cert5.stepRow 4 9 3 = true := by decide +kernel
theorem r4_9_4 : cert5.stepRow 4 9 4 = true := by decide +kernel
theorem r4_9_5 : cert5.stepRow 4 9 5 = true := by decide +kernel
theorem r4_9_6 : cert5.stepRow 4 9 6 = true := by decide +kernel
theorem r4_9_7 : cert5.stepRow 4 9 7 = true := by decide +kernel
theorem r4_9_8 : cert5.stepRow 4 9 8 = true := by decide +kernel
theorem r4_9_9 : cert5.stepRow 4 9 9 = true := by decide +kernel
theorem r4_9_10 : cert5.stepRow 4 9 10 = true := by decide +kernel
theorem r4_9_11 : cert5.stepRow 4 9 11 = true := by decide +kernel
theorem r4_9_12 : cert5.stepRow 4 9 12 = true := by decide +kernel
theorem r4_9_13 : cert5.stepRow 4 9 13 = true := by decide +kernel
theorem r4_9_14 : cert5.stepRow 4 9 14 = true := by decide +kernel
theorem r4_9_15 : cert5.stepRow 4 9 15 = true := by decide +kernel
theorem r4_9_16 : cert5.stepRow 4 9 16 = true := by decide +kernel
theorem r4_9_17 : cert5.stepRow 4 9 17 = true := by decide +kernel
theorem r4_9_18 : cert5.stepRow 4 9 18 = true := by decide +kernel

theorem r4_9 : ∀ b, b ≤ 18 → cert5.stepRow 4 9 b = true :=
  cover19 r4_9_0 r4_9_1 r4_9_2 r4_9_3 r4_9_4 r4_9_5 r4_9_6 r4_9_7 r4_9_8 r4_9_9 r4_9_10 r4_9_11 r4_9_12 r4_9_13 r4_9_14 r4_9_15 r4_9_16 r4_9_17 r4_9_18

end Agent113.FiveLayer
