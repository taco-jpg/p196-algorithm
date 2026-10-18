import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 1, s0 = 2). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r1_2_0 : cert5.stepRow 1 2 0 = true := by decide +kernel
theorem r1_2_1 : cert5.stepRow 1 2 1 = true := by decide +kernel
theorem r1_2_2 : cert5.stepRow 1 2 2 = true := by decide +kernel
theorem r1_2_3 : cert5.stepRow 1 2 3 = true := by decide +kernel
theorem r1_2_4 : cert5.stepRow 1 2 4 = true := by decide +kernel
theorem r1_2_5 : cert5.stepRow 1 2 5 = true := by decide +kernel
theorem r1_2_6 : cert5.stepRow 1 2 6 = true := by decide +kernel
theorem r1_2_7 : cert5.stepRow 1 2 7 = true := by decide +kernel
theorem r1_2_8 : cert5.stepRow 1 2 8 = true := by decide +kernel
theorem r1_2_9 : cert5.stepRow 1 2 9 = true := by decide +kernel
theorem r1_2_10 : cert5.stepRow 1 2 10 = true := by decide +kernel
theorem r1_2_11 : cert5.stepRow 1 2 11 = true := by decide +kernel
theorem r1_2_12 : cert5.stepRow 1 2 12 = true := by decide +kernel
theorem r1_2_13 : cert5.stepRow 1 2 13 = true := by decide +kernel
theorem r1_2_14 : cert5.stepRow 1 2 14 = true := by decide +kernel
theorem r1_2_15 : cert5.stepRow 1 2 15 = true := by decide +kernel
theorem r1_2_16 : cert5.stepRow 1 2 16 = true := by decide +kernel
theorem r1_2_17 : cert5.stepRow 1 2 17 = true := by decide +kernel
theorem r1_2_18 : cert5.stepRow 1 2 18 = true := by decide +kernel

theorem r1_2 : ∀ b, b ≤ 18 → cert5.stepRow 1 2 b = true :=
  cover19 r1_2_0 r1_2_1 r1_2_2 r1_2_3 r1_2_4 r1_2_5 r1_2_6 r1_2_7 r1_2_8 r1_2_9 r1_2_10 r1_2_11 r1_2_12 r1_2_13 r1_2_14 r1_2_15 r1_2_16 r1_2_17 r1_2_18

end Agent113.FiveLayer
