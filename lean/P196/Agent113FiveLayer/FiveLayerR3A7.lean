import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 3, s0 = 7). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r3_7_0 : cert5.stepRow 3 7 0 = true := by decide +kernel
theorem r3_7_1 : cert5.stepRow 3 7 1 = true := by decide +kernel
theorem r3_7_2 : cert5.stepRow 3 7 2 = true := by decide +kernel
theorem r3_7_3 : cert5.stepRow 3 7 3 = true := by decide +kernel
theorem r3_7_4 : cert5.stepRow 3 7 4 = true := by decide +kernel
theorem r3_7_5 : cert5.stepRow 3 7 5 = true := by decide +kernel
theorem r3_7_6 : cert5.stepRow 3 7 6 = true := by decide +kernel
theorem r3_7_7 : cert5.stepRow 3 7 7 = true := by decide +kernel
theorem r3_7_8 : cert5.stepRow 3 7 8 = true := by decide +kernel
theorem r3_7_9 : cert5.stepRow 3 7 9 = true := by decide +kernel
theorem r3_7_10 : cert5.stepRow 3 7 10 = true := by decide +kernel
theorem r3_7_11 : cert5.stepRow 3 7 11 = true := by decide +kernel
theorem r3_7_12 : cert5.stepRow 3 7 12 = true := by decide +kernel
theorem r3_7_13 : cert5.stepRow 3 7 13 = true := by decide +kernel
theorem r3_7_14 : cert5.stepRow 3 7 14 = true := by decide +kernel
theorem r3_7_15 : cert5.stepRow 3 7 15 = true := by decide +kernel
theorem r3_7_16 : cert5.stepRow 3 7 16 = true := by decide +kernel
theorem r3_7_17 : cert5.stepRow 3 7 17 = true := by decide +kernel
theorem r3_7_18 : cert5.stepRow 3 7 18 = true := by decide +kernel

theorem r3_7 : ∀ b, b ≤ 18 → cert5.stepRow 3 7 b = true :=
  cover19 r3_7_0 r3_7_1 r3_7_2 r3_7_3 r3_7_4 r3_7_5 r3_7_6 r3_7_7 r3_7_8 r3_7_9 r3_7_10 r3_7_11 r3_7_12 r3_7_13 r3_7_14 r3_7_15 r3_7_16 r3_7_17 r3_7_18

end Agent113.FiveLayer
