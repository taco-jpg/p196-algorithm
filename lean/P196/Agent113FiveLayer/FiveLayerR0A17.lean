import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 0, s0 = 17). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r0_17_0 : cert5.stepRow 0 17 0 = true := by decide +kernel
theorem r0_17_1 : cert5.stepRow 0 17 1 = true := by decide +kernel
theorem r0_17_2 : cert5.stepRow 0 17 2 = true := by decide +kernel
theorem r0_17_3 : cert5.stepRow 0 17 3 = true := by decide +kernel
theorem r0_17_4 : cert5.stepRow 0 17 4 = true := by decide +kernel
theorem r0_17_5 : cert5.stepRow 0 17 5 = true := by decide +kernel
theorem r0_17_6 : cert5.stepRow 0 17 6 = true := by decide +kernel
theorem r0_17_7 : cert5.stepRow 0 17 7 = true := by decide +kernel
theorem r0_17_8 : cert5.stepRow 0 17 8 = true := by decide +kernel
theorem r0_17_9 : cert5.stepRow 0 17 9 = true := by decide +kernel
theorem r0_17_10 : cert5.stepRow 0 17 10 = true := by decide +kernel
theorem r0_17_11 : cert5.stepRow 0 17 11 = true := by decide +kernel
theorem r0_17_12 : cert5.stepRow 0 17 12 = true := by decide +kernel
theorem r0_17_13 : cert5.stepRow 0 17 13 = true := by decide +kernel
theorem r0_17_14 : cert5.stepRow 0 17 14 = true := by decide +kernel
theorem r0_17_15 : cert5.stepRow 0 17 15 = true := by decide +kernel
theorem r0_17_16 : cert5.stepRow 0 17 16 = true := by decide +kernel
theorem r0_17_17 : cert5.stepRow 0 17 17 = true := by decide +kernel
theorem r0_17_18 : cert5.stepRow 0 17 18 = true := by decide +kernel

theorem r0_17 : ∀ b, b ≤ 18 → cert5.stepRow 0 17 b = true :=
  cover19 r0_17_0 r0_17_1 r0_17_2 r0_17_3 r0_17_4 r0_17_5 r0_17_6 r0_17_7 r0_17_8 r0_17_9 r0_17_10 r0_17_11 r0_17_12 r0_17_13 r0_17_14 r0_17_15 r0_17_16 r0_17_17 r0_17_18

end Agent113.FiveLayer
