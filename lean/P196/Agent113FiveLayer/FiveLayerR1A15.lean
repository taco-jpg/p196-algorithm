import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 1, s0 = 15). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r1_15_0 : cert5.stepRow 1 15 0 = true := by decide +kernel
theorem r1_15_1 : cert5.stepRow 1 15 1 = true := by decide +kernel
theorem r1_15_2 : cert5.stepRow 1 15 2 = true := by decide +kernel
theorem r1_15_3 : cert5.stepRow 1 15 3 = true := by decide +kernel
theorem r1_15_4 : cert5.stepRow 1 15 4 = true := by decide +kernel
theorem r1_15_5 : cert5.stepRow 1 15 5 = true := by decide +kernel
theorem r1_15_6 : cert5.stepRow 1 15 6 = true := by decide +kernel
theorem r1_15_7 : cert5.stepRow 1 15 7 = true := by decide +kernel
theorem r1_15_8 : cert5.stepRow 1 15 8 = true := by decide +kernel
theorem r1_15_9 : cert5.stepRow 1 15 9 = true := by decide +kernel
theorem r1_15_10 : cert5.stepRow 1 15 10 = true := by decide +kernel
theorem r1_15_11 : cert5.stepRow 1 15 11 = true := by decide +kernel
theorem r1_15_12 : cert5.stepRow 1 15 12 = true := by decide +kernel
theorem r1_15_13 : cert5.stepRow 1 15 13 = true := by decide +kernel
theorem r1_15_14 : cert5.stepRow 1 15 14 = true := by decide +kernel
theorem r1_15_15 : cert5.stepRow 1 15 15 = true := by decide +kernel
theorem r1_15_16 : cert5.stepRow 1 15 16 = true := by decide +kernel
theorem r1_15_17 : cert5.stepRow 1 15 17 = true := by decide +kernel
theorem r1_15_18 : cert5.stepRow 1 15 18 = true := by decide +kernel

theorem r1_15 : ∀ b, b ≤ 18 → cert5.stepRow 1 15 b = true :=
  cover19 r1_15_0 r1_15_1 r1_15_2 r1_15_3 r1_15_4 r1_15_5 r1_15_6 r1_15_7 r1_15_8 r1_15_9 r1_15_10 r1_15_11 r1_15_12 r1_15_13 r1_15_14 r1_15_15 r1_15_16 r1_15_17 r1_15_18

end Agent113.FiveLayer
