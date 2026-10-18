import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 3, s0 = 5). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r3_5_0 : cert5.stepRow 3 5 0 = true := by decide +kernel
theorem r3_5_1 : cert5.stepRow 3 5 1 = true := by decide +kernel
theorem r3_5_2 : cert5.stepRow 3 5 2 = true := by decide +kernel
theorem r3_5_3 : cert5.stepRow 3 5 3 = true := by decide +kernel
theorem r3_5_4 : cert5.stepRow 3 5 4 = true := by decide +kernel
theorem r3_5_5 : cert5.stepRow 3 5 5 = true := by decide +kernel
theorem r3_5_6 : cert5.stepRow 3 5 6 = true := by decide +kernel
theorem r3_5_7 : cert5.stepRow 3 5 7 = true := by decide +kernel
theorem r3_5_8 : cert5.stepRow 3 5 8 = true := by decide +kernel
theorem r3_5_9 : cert5.stepRow 3 5 9 = true := by decide +kernel
theorem r3_5_10 : cert5.stepRow 3 5 10 = true := by decide +kernel
theorem r3_5_11 : cert5.stepRow 3 5 11 = true := by decide +kernel
theorem r3_5_12 : cert5.stepRow 3 5 12 = true := by decide +kernel
theorem r3_5_13 : cert5.stepRow 3 5 13 = true := by decide +kernel
theorem r3_5_14 : cert5.stepRow 3 5 14 = true := by decide +kernel
theorem r3_5_15 : cert5.stepRow 3 5 15 = true := by decide +kernel
theorem r3_5_16 : cert5.stepRow 3 5 16 = true := by decide +kernel
theorem r3_5_17 : cert5.stepRow 3 5 17 = true := by decide +kernel
theorem r3_5_18 : cert5.stepRow 3 5 18 = true := by decide +kernel

theorem r3_5 : ∀ b, b ≤ 18 → cert5.stepRow 3 5 b = true :=
  cover19 r3_5_0 r3_5_1 r3_5_2 r3_5_3 r3_5_4 r3_5_5 r3_5_6 r3_5_7 r3_5_8 r3_5_9 r3_5_10 r3_5_11 r3_5_12 r3_5_13 r3_5_14 r3_5_15 r3_5_16 r3_5_17 r3_5_18

end Agent113.FiveLayer
