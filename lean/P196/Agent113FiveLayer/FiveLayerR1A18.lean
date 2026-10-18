import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 1, s0 = 18). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r1_18_0 : cert5.stepRow 1 18 0 = true := by decide +kernel
theorem r1_18_1 : cert5.stepRow 1 18 1 = true := by decide +kernel
theorem r1_18_2 : cert5.stepRow 1 18 2 = true := by decide +kernel
theorem r1_18_3 : cert5.stepRow 1 18 3 = true := by decide +kernel
theorem r1_18_4 : cert5.stepRow 1 18 4 = true := by decide +kernel
theorem r1_18_5 : cert5.stepRow 1 18 5 = true := by decide +kernel
theorem r1_18_6 : cert5.stepRow 1 18 6 = true := by decide +kernel
theorem r1_18_7 : cert5.stepRow 1 18 7 = true := by decide +kernel
theorem r1_18_8 : cert5.stepRow 1 18 8 = true := by decide +kernel
theorem r1_18_9 : cert5.stepRow 1 18 9 = true := by decide +kernel
theorem r1_18_10 : cert5.stepRow 1 18 10 = true := by decide +kernel
theorem r1_18_11 : cert5.stepRow 1 18 11 = true := by decide +kernel
theorem r1_18_12 : cert5.stepRow 1 18 12 = true := by decide +kernel
theorem r1_18_13 : cert5.stepRow 1 18 13 = true := by decide +kernel
theorem r1_18_14 : cert5.stepRow 1 18 14 = true := by decide +kernel
theorem r1_18_15 : cert5.stepRow 1 18 15 = true := by decide +kernel
theorem r1_18_16 : cert5.stepRow 1 18 16 = true := by decide +kernel
theorem r1_18_17 : cert5.stepRow 1 18 17 = true := by decide +kernel
theorem r1_18_18 : cert5.stepRow 1 18 18 = true := by decide +kernel

theorem r1_18 : ∀ b, b ≤ 18 → cert5.stepRow 1 18 b = true :=
  cover19 r1_18_0 r1_18_1 r1_18_2 r1_18_3 r1_18_4 r1_18_5 r1_18_6 r1_18_7 r1_18_8 r1_18_9 r1_18_10 r1_18_11 r1_18_12 r1_18_13 r1_18_14 r1_18_15 r1_18_16 r1_18_17 r1_18_18

end Agent113.FiveLayer
