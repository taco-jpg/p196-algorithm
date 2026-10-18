import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 3, s0 = 13). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r3_13_0 : cert5.stepRow 3 13 0 = true := by decide +kernel
theorem r3_13_1 : cert5.stepRow 3 13 1 = true := by decide +kernel
theorem r3_13_2 : cert5.stepRow 3 13 2 = true := by decide +kernel
theorem r3_13_3 : cert5.stepRow 3 13 3 = true := by decide +kernel
theorem r3_13_4 : cert5.stepRow 3 13 4 = true := by decide +kernel
theorem r3_13_5 : cert5.stepRow 3 13 5 = true := by decide +kernel
theorem r3_13_6 : cert5.stepRow 3 13 6 = true := by decide +kernel
theorem r3_13_7 : cert5.stepRow 3 13 7 = true := by decide +kernel
theorem r3_13_8 : cert5.stepRow 3 13 8 = true := by decide +kernel
theorem r3_13_9 : cert5.stepRow 3 13 9 = true := by decide +kernel
theorem r3_13_10 : cert5.stepRow 3 13 10 = true := by decide +kernel
theorem r3_13_11 : cert5.stepRow 3 13 11 = true := by decide +kernel
theorem r3_13_12 : cert5.stepRow 3 13 12 = true := by decide +kernel
theorem r3_13_13 : cert5.stepRow 3 13 13 = true := by decide +kernel
theorem r3_13_14 : cert5.stepRow 3 13 14 = true := by decide +kernel
theorem r3_13_15 : cert5.stepRow 3 13 15 = true := by decide +kernel
theorem r3_13_16 : cert5.stepRow 3 13 16 = true := by decide +kernel
theorem r3_13_17 : cert5.stepRow 3 13 17 = true := by decide +kernel
theorem r3_13_18 : cert5.stepRow 3 13 18 = true := by decide +kernel

theorem r3_13 : ∀ b, b ≤ 18 → cert5.stepRow 3 13 b = true :=
  cover19 r3_13_0 r3_13_1 r3_13_2 r3_13_3 r3_13_4 r3_13_5 r3_13_6 r3_13_7 r3_13_8 r3_13_9 r3_13_10 r3_13_11 r3_13_12 r3_13_13 r3_13_14 r3_13_15 r3_13_16 r3_13_17 r3_13_18

end Agent113.FiveLayer
