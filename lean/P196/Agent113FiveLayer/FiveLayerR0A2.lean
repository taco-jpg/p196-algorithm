import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 0, s0 = 2). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r0_2_0 : cert5.stepRow 0 2 0 = true := by decide +kernel
theorem r0_2_1 : cert5.stepRow 0 2 1 = true := by decide +kernel
theorem r0_2_2 : cert5.stepRow 0 2 2 = true := by decide +kernel
theorem r0_2_3 : cert5.stepRow 0 2 3 = true := by decide +kernel
theorem r0_2_4 : cert5.stepRow 0 2 4 = true := by decide +kernel
theorem r0_2_5 : cert5.stepRow 0 2 5 = true := by decide +kernel
theorem r0_2_6 : cert5.stepRow 0 2 6 = true := by decide +kernel
theorem r0_2_7 : cert5.stepRow 0 2 7 = true := by decide +kernel
theorem r0_2_8 : cert5.stepRow 0 2 8 = true := by decide +kernel
theorem r0_2_9 : cert5.stepRow 0 2 9 = true := by decide +kernel
theorem r0_2_10 : cert5.stepRow 0 2 10 = true := by decide +kernel
theorem r0_2_11 : cert5.stepRow 0 2 11 = true := by decide +kernel
theorem r0_2_12 : cert5.stepRow 0 2 12 = true := by decide +kernel
theorem r0_2_13 : cert5.stepRow 0 2 13 = true := by decide +kernel
theorem r0_2_14 : cert5.stepRow 0 2 14 = true := by decide +kernel
theorem r0_2_15 : cert5.stepRow 0 2 15 = true := by decide +kernel
theorem r0_2_16 : cert5.stepRow 0 2 16 = true := by decide +kernel
theorem r0_2_17 : cert5.stepRow 0 2 17 = true := by decide +kernel
theorem r0_2_18 : cert5.stepRow 0 2 18 = true := by decide +kernel

theorem r0_2 : ∀ b, b ≤ 18 → cert5.stepRow 0 2 b = true :=
  cover19 r0_2_0 r0_2_1 r0_2_2 r0_2_3 r0_2_4 r0_2_5 r0_2_6 r0_2_7 r0_2_8 r0_2_9 r0_2_10 r0_2_11 r0_2_12 r0_2_13 r0_2_14 r0_2_15 r0_2_16 r0_2_17 r0_2_18

end Agent113.FiveLayer
