import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 4, s0 = 17). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r4_17_0 : cert5.stepRow 4 17 0 = true := by decide +kernel
theorem r4_17_1 : cert5.stepRow 4 17 1 = true := by decide +kernel
theorem r4_17_2 : cert5.stepRow 4 17 2 = true := by decide +kernel
theorem r4_17_3 : cert5.stepRow 4 17 3 = true := by decide +kernel
theorem r4_17_4 : cert5.stepRow 4 17 4 = true := by decide +kernel
theorem r4_17_5 : cert5.stepRow 4 17 5 = true := by decide +kernel
theorem r4_17_6 : cert5.stepRow 4 17 6 = true := by decide +kernel
theorem r4_17_7 : cert5.stepRow 4 17 7 = true := by decide +kernel
theorem r4_17_8 : cert5.stepRow 4 17 8 = true := by decide +kernel
theorem r4_17_9 : cert5.stepRow 4 17 9 = true := by decide +kernel
theorem r4_17_10 : cert5.stepRow 4 17 10 = true := by decide +kernel
theorem r4_17_11 : cert5.stepRow 4 17 11 = true := by decide +kernel
theorem r4_17_12 : cert5.stepRow 4 17 12 = true := by decide +kernel
theorem r4_17_13 : cert5.stepRow 4 17 13 = true := by decide +kernel
theorem r4_17_14 : cert5.stepRow 4 17 14 = true := by decide +kernel
theorem r4_17_15 : cert5.stepRow 4 17 15 = true := by decide +kernel
theorem r4_17_16 : cert5.stepRow 4 17 16 = true := by decide +kernel
theorem r4_17_17 : cert5.stepRow 4 17 17 = true := by decide +kernel
theorem r4_17_18 : cert5.stepRow 4 17 18 = true := by decide +kernel

theorem r4_17 : ∀ b, b ≤ 18 → cert5.stepRow 4 17 b = true :=
  cover19 r4_17_0 r4_17_1 r4_17_2 r4_17_3 r4_17_4 r4_17_5 r4_17_6 r4_17_7 r4_17_8 r4_17_9 r4_17_10 r4_17_11 r4_17_12 r4_17_13 r4_17_14 r4_17_15 r4_17_16 r4_17_17 r4_17_18

end Agent113.FiveLayer
