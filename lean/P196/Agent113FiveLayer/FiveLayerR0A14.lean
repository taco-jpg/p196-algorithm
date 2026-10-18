import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 0, s0 = 14). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r0_14_0 : cert5.stepRow 0 14 0 = true := by decide +kernel
theorem r0_14_1 : cert5.stepRow 0 14 1 = true := by decide +kernel
theorem r0_14_2 : cert5.stepRow 0 14 2 = true := by decide +kernel
theorem r0_14_3 : cert5.stepRow 0 14 3 = true := by decide +kernel
theorem r0_14_4 : cert5.stepRow 0 14 4 = true := by decide +kernel
theorem r0_14_5 : cert5.stepRow 0 14 5 = true := by decide +kernel
theorem r0_14_6 : cert5.stepRow 0 14 6 = true := by decide +kernel
theorem r0_14_7 : cert5.stepRow 0 14 7 = true := by decide +kernel
theorem r0_14_8 : cert5.stepRow 0 14 8 = true := by decide +kernel
theorem r0_14_9 : cert5.stepRow 0 14 9 = true := by decide +kernel
theorem r0_14_10 : cert5.stepRow 0 14 10 = true := by decide +kernel
theorem r0_14_11 : cert5.stepRow 0 14 11 = true := by decide +kernel
theorem r0_14_12 : cert5.stepRow 0 14 12 = true := by decide +kernel
theorem r0_14_13 : cert5.stepRow 0 14 13 = true := by decide +kernel
theorem r0_14_14 : cert5.stepRow 0 14 14 = true := by decide +kernel
theorem r0_14_15 : cert5.stepRow 0 14 15 = true := by decide +kernel
theorem r0_14_16 : cert5.stepRow 0 14 16 = true := by decide +kernel
theorem r0_14_17 : cert5.stepRow 0 14 17 = true := by decide +kernel
theorem r0_14_18 : cert5.stepRow 0 14 18 = true := by decide +kernel

theorem r0_14 : ∀ b, b ≤ 18 → cert5.stepRow 0 14 b = true :=
  cover19 r0_14_0 r0_14_1 r0_14_2 r0_14_3 r0_14_4 r0_14_5 r0_14_6 r0_14_7 r0_14_8 r0_14_9 r0_14_10 r0_14_11 r0_14_12 r0_14_13 r0_14_14 r0_14_15 r0_14_16 r0_14_17 r0_14_18

end Agent113.FiveLayer
