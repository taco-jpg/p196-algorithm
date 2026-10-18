import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 4, s0 = 7). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r4_7_0 : cert5.stepRow 4 7 0 = true := by decide +kernel
theorem r4_7_1 : cert5.stepRow 4 7 1 = true := by decide +kernel
theorem r4_7_2 : cert5.stepRow 4 7 2 = true := by decide +kernel
theorem r4_7_3 : cert5.stepRow 4 7 3 = true := by decide +kernel
theorem r4_7_4 : cert5.stepRow 4 7 4 = true := by decide +kernel
theorem r4_7_5 : cert5.stepRow 4 7 5 = true := by decide +kernel
theorem r4_7_6 : cert5.stepRow 4 7 6 = true := by decide +kernel
theorem r4_7_7 : cert5.stepRow 4 7 7 = true := by decide +kernel
theorem r4_7_8 : cert5.stepRow 4 7 8 = true := by decide +kernel
theorem r4_7_9 : cert5.stepRow 4 7 9 = true := by decide +kernel
theorem r4_7_10 : cert5.stepRow 4 7 10 = true := by decide +kernel
theorem r4_7_11 : cert5.stepRow 4 7 11 = true := by decide +kernel
theorem r4_7_12 : cert5.stepRow 4 7 12 = true := by decide +kernel
theorem r4_7_13 : cert5.stepRow 4 7 13 = true := by decide +kernel
theorem r4_7_14 : cert5.stepRow 4 7 14 = true := by decide +kernel
theorem r4_7_15 : cert5.stepRow 4 7 15 = true := by decide +kernel
theorem r4_7_16 : cert5.stepRow 4 7 16 = true := by decide +kernel
theorem r4_7_17 : cert5.stepRow 4 7 17 = true := by decide +kernel
theorem r4_7_18 : cert5.stepRow 4 7 18 = true := by decide +kernel

theorem r4_7 : ∀ b, b ≤ 18 → cert5.stepRow 4 7 b = true :=
  cover19 r4_7_0 r4_7_1 r4_7_2 r4_7_3 r4_7_4 r4_7_5 r4_7_6 r4_7_7 r4_7_8 r4_7_9 r4_7_10 r4_7_11 r4_7_12 r4_7_13 r4_7_14 r4_7_15 r4_7_16 r4_7_17 r4_7_18

end Agent113.FiveLayer
