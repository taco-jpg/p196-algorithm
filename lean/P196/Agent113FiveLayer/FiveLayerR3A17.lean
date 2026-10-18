import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 3, s0 = 17). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r3_17_0 : cert5.stepRow 3 17 0 = true := by decide +kernel
theorem r3_17_1 : cert5.stepRow 3 17 1 = true := by decide +kernel
theorem r3_17_2 : cert5.stepRow 3 17 2 = true := by decide +kernel
theorem r3_17_3 : cert5.stepRow 3 17 3 = true := by decide +kernel
theorem r3_17_4 : cert5.stepRow 3 17 4 = true := by decide +kernel
theorem r3_17_5 : cert5.stepRow 3 17 5 = true := by decide +kernel
theorem r3_17_6 : cert5.stepRow 3 17 6 = true := by decide +kernel
theorem r3_17_7 : cert5.stepRow 3 17 7 = true := by decide +kernel
theorem r3_17_8 : cert5.stepRow 3 17 8 = true := by decide +kernel
theorem r3_17_9 : cert5.stepRow 3 17 9 = true := by decide +kernel
theorem r3_17_10 : cert5.stepRow 3 17 10 = true := by decide +kernel
theorem r3_17_11 : cert5.stepRow 3 17 11 = true := by decide +kernel
theorem r3_17_12 : cert5.stepRow 3 17 12 = true := by decide +kernel
theorem r3_17_13 : cert5.stepRow 3 17 13 = true := by decide +kernel
theorem r3_17_14 : cert5.stepRow 3 17 14 = true := by decide +kernel
theorem r3_17_15 : cert5.stepRow 3 17 15 = true := by decide +kernel
theorem r3_17_16 : cert5.stepRow 3 17 16 = true := by decide +kernel
theorem r3_17_17 : cert5.stepRow 3 17 17 = true := by decide +kernel
theorem r3_17_18 : cert5.stepRow 3 17 18 = true := by decide +kernel

theorem r3_17 : ∀ b, b ≤ 18 → cert5.stepRow 3 17 b = true :=
  cover19 r3_17_0 r3_17_1 r3_17_2 r3_17_3 r3_17_4 r3_17_5 r3_17_6 r3_17_7 r3_17_8 r3_17_9 r3_17_10 r3_17_11 r3_17_12 r3_17_13 r3_17_14 r3_17_15 r3_17_16 r3_17_17 r3_17_18

end Agent113.FiveLayer
