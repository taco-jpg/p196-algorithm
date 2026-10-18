import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 0, s0 = 18). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r0_18_0 : cert5.stepRow 0 18 0 = true := by decide +kernel
theorem r0_18_1 : cert5.stepRow 0 18 1 = true := by decide +kernel
theorem r0_18_2 : cert5.stepRow 0 18 2 = true := by decide +kernel
theorem r0_18_3 : cert5.stepRow 0 18 3 = true := by decide +kernel
theorem r0_18_4 : cert5.stepRow 0 18 4 = true := by decide +kernel
theorem r0_18_5 : cert5.stepRow 0 18 5 = true := by decide +kernel
theorem r0_18_6 : cert5.stepRow 0 18 6 = true := by decide +kernel
theorem r0_18_7 : cert5.stepRow 0 18 7 = true := by decide +kernel
theorem r0_18_8 : cert5.stepRow 0 18 8 = true := by decide +kernel
theorem r0_18_9 : cert5.stepRow 0 18 9 = true := by decide +kernel
theorem r0_18_10 : cert5.stepRow 0 18 10 = true := by decide +kernel
theorem r0_18_11 : cert5.stepRow 0 18 11 = true := by decide +kernel
theorem r0_18_12 : cert5.stepRow 0 18 12 = true := by decide +kernel
theorem r0_18_13 : cert5.stepRow 0 18 13 = true := by decide +kernel
theorem r0_18_14 : cert5.stepRow 0 18 14 = true := by decide +kernel
theorem r0_18_15 : cert5.stepRow 0 18 15 = true := by decide +kernel
theorem r0_18_16 : cert5.stepRow 0 18 16 = true := by decide +kernel
theorem r0_18_17 : cert5.stepRow 0 18 17 = true := by decide +kernel
theorem r0_18_18 : cert5.stepRow 0 18 18 = true := by decide +kernel

theorem r0_18 : ∀ b, b ≤ 18 → cert5.stepRow 0 18 b = true :=
  cover19 r0_18_0 r0_18_1 r0_18_2 r0_18_3 r0_18_4 r0_18_5 r0_18_6 r0_18_7 r0_18_8 r0_18_9 r0_18_10 r0_18_11 r0_18_12 r0_18_13 r0_18_14 r0_18_15 r0_18_16 r0_18_17 r0_18_18

end Agent113.FiveLayer
