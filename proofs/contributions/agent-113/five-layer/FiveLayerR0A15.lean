import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 0, s0 = 15). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r0_15_0 : cert5.stepRow 0 15 0 = true := by decide +kernel
theorem r0_15_1 : cert5.stepRow 0 15 1 = true := by decide +kernel
theorem r0_15_2 : cert5.stepRow 0 15 2 = true := by decide +kernel
theorem r0_15_3 : cert5.stepRow 0 15 3 = true := by decide +kernel
theorem r0_15_4 : cert5.stepRow 0 15 4 = true := by decide +kernel
theorem r0_15_5 : cert5.stepRow 0 15 5 = true := by decide +kernel
theorem r0_15_6 : cert5.stepRow 0 15 6 = true := by decide +kernel
theorem r0_15_7 : cert5.stepRow 0 15 7 = true := by decide +kernel
theorem r0_15_8 : cert5.stepRow 0 15 8 = true := by decide +kernel
theorem r0_15_9 : cert5.stepRow 0 15 9 = true := by decide +kernel
theorem r0_15_10 : cert5.stepRow 0 15 10 = true := by decide +kernel
theorem r0_15_11 : cert5.stepRow 0 15 11 = true := by decide +kernel
theorem r0_15_12 : cert5.stepRow 0 15 12 = true := by decide +kernel
theorem r0_15_13 : cert5.stepRow 0 15 13 = true := by decide +kernel
theorem r0_15_14 : cert5.stepRow 0 15 14 = true := by decide +kernel
theorem r0_15_15 : cert5.stepRow 0 15 15 = true := by decide +kernel
theorem r0_15_16 : cert5.stepRow 0 15 16 = true := by decide +kernel
theorem r0_15_17 : cert5.stepRow 0 15 17 = true := by decide +kernel
theorem r0_15_18 : cert5.stepRow 0 15 18 = true := by decide +kernel

theorem r0_15 : ∀ b, b ≤ 18 → cert5.stepRow 0 15 b = true :=
  cover19 r0_15_0 r0_15_1 r0_15_2 r0_15_3 r0_15_4 r0_15_5 r0_15_6 r0_15_7 r0_15_8 r0_15_9 r0_15_10 r0_15_11 r0_15_12 r0_15_13 r0_15_14 r0_15_15 r0_15_16 r0_15_17 r0_15_18

end Agent113.FiveLayer
