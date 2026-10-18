import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 3, s0 = 9). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r3_9_0 : cert5.stepRow 3 9 0 = true := by decide +kernel
theorem r3_9_1 : cert5.stepRow 3 9 1 = true := by decide +kernel
theorem r3_9_2 : cert5.stepRow 3 9 2 = true := by decide +kernel
theorem r3_9_3 : cert5.stepRow 3 9 3 = true := by decide +kernel
theorem r3_9_4 : cert5.stepRow 3 9 4 = true := by decide +kernel
theorem r3_9_5 : cert5.stepRow 3 9 5 = true := by decide +kernel
theorem r3_9_6 : cert5.stepRow 3 9 6 = true := by decide +kernel
theorem r3_9_7 : cert5.stepRow 3 9 7 = true := by decide +kernel
theorem r3_9_8 : cert5.stepRow 3 9 8 = true := by decide +kernel
theorem r3_9_9 : cert5.stepRow 3 9 9 = true := by decide +kernel
theorem r3_9_10 : cert5.stepRow 3 9 10 = true := by decide +kernel
theorem r3_9_11 : cert5.stepRow 3 9 11 = true := by decide +kernel
theorem r3_9_12 : cert5.stepRow 3 9 12 = true := by decide +kernel
theorem r3_9_13 : cert5.stepRow 3 9 13 = true := by decide +kernel
theorem r3_9_14 : cert5.stepRow 3 9 14 = true := by decide +kernel
theorem r3_9_15 : cert5.stepRow 3 9 15 = true := by decide +kernel
theorem r3_9_16 : cert5.stepRow 3 9 16 = true := by decide +kernel
theorem r3_9_17 : cert5.stepRow 3 9 17 = true := by decide +kernel
theorem r3_9_18 : cert5.stepRow 3 9 18 = true := by decide +kernel

theorem r3_9 : ∀ b, b ≤ 18 → cert5.stepRow 3 9 b = true :=
  cover19 r3_9_0 r3_9_1 r3_9_2 r3_9_3 r3_9_4 r3_9_5 r3_9_6 r3_9_7 r3_9_8 r3_9_9 r3_9_10 r3_9_11 r3_9_12 r3_9_13 r3_9_14 r3_9_15 r3_9_16 r3_9_17 r3_9_18

end Agent113.FiveLayer
