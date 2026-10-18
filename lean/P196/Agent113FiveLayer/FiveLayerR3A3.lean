import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 3, s0 = 3). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r3_3_0 : cert5.stepRow 3 3 0 = true := by decide +kernel
theorem r3_3_1 : cert5.stepRow 3 3 1 = true := by decide +kernel
theorem r3_3_2 : cert5.stepRow 3 3 2 = true := by decide +kernel
theorem r3_3_3 : cert5.stepRow 3 3 3 = true := by decide +kernel
theorem r3_3_4 : cert5.stepRow 3 3 4 = true := by decide +kernel
theorem r3_3_5 : cert5.stepRow 3 3 5 = true := by decide +kernel
theorem r3_3_6 : cert5.stepRow 3 3 6 = true := by decide +kernel
theorem r3_3_7 : cert5.stepRow 3 3 7 = true := by decide +kernel
theorem r3_3_8 : cert5.stepRow 3 3 8 = true := by decide +kernel
theorem r3_3_9 : cert5.stepRow 3 3 9 = true := by decide +kernel
theorem r3_3_10 : cert5.stepRow 3 3 10 = true := by decide +kernel
theorem r3_3_11 : cert5.stepRow 3 3 11 = true := by decide +kernel
theorem r3_3_12 : cert5.stepRow 3 3 12 = true := by decide +kernel
theorem r3_3_13 : cert5.stepRow 3 3 13 = true := by decide +kernel
theorem r3_3_14 : cert5.stepRow 3 3 14 = true := by decide +kernel
theorem r3_3_15 : cert5.stepRow 3 3 15 = true := by decide +kernel
theorem r3_3_16 : cert5.stepRow 3 3 16 = true := by decide +kernel
theorem r3_3_17 : cert5.stepRow 3 3 17 = true := by decide +kernel
theorem r3_3_18 : cert5.stepRow 3 3 18 = true := by decide +kernel

theorem r3_3 : ∀ b, b ≤ 18 → cert5.stepRow 3 3 b = true :=
  cover19 r3_3_0 r3_3_1 r3_3_2 r3_3_3 r3_3_4 r3_3_5 r3_3_6 r3_3_7 r3_3_8 r3_3_9 r3_3_10 r3_3_11 r3_3_12 r3_3_13 r3_3_14 r3_3_15 r3_3_16 r3_3_17 r3_3_18

end Agent113.FiveLayer
