import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 0, s0 = 5). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r0_5_0 : cert5.stepRow 0 5 0 = true := by decide +kernel
theorem r0_5_1 : cert5.stepRow 0 5 1 = true := by decide +kernel
theorem r0_5_2 : cert5.stepRow 0 5 2 = true := by decide +kernel
theorem r0_5_3 : cert5.stepRow 0 5 3 = true := by decide +kernel
theorem r0_5_4 : cert5.stepRow 0 5 4 = true := by decide +kernel
theorem r0_5_5 : cert5.stepRow 0 5 5 = true := by decide +kernel
theorem r0_5_6 : cert5.stepRow 0 5 6 = true := by decide +kernel
theorem r0_5_7 : cert5.stepRow 0 5 7 = true := by decide +kernel
theorem r0_5_8 : cert5.stepRow 0 5 8 = true := by decide +kernel
theorem r0_5_9 : cert5.stepRow 0 5 9 = true := by decide +kernel
theorem r0_5_10 : cert5.stepRow 0 5 10 = true := by decide +kernel
theorem r0_5_11 : cert5.stepRow 0 5 11 = true := by decide +kernel
theorem r0_5_12 : cert5.stepRow 0 5 12 = true := by decide +kernel
theorem r0_5_13 : cert5.stepRow 0 5 13 = true := by decide +kernel
theorem r0_5_14 : cert5.stepRow 0 5 14 = true := by decide +kernel
theorem r0_5_15 : cert5.stepRow 0 5 15 = true := by decide +kernel
theorem r0_5_16 : cert5.stepRow 0 5 16 = true := by decide +kernel
theorem r0_5_17 : cert5.stepRow 0 5 17 = true := by decide +kernel
theorem r0_5_18 : cert5.stepRow 0 5 18 = true := by decide +kernel

theorem r0_5 : ∀ b, b ≤ 18 → cert5.stepRow 0 5 b = true :=
  cover19 r0_5_0 r0_5_1 r0_5_2 r0_5_3 r0_5_4 r0_5_5 r0_5_6 r0_5_7 r0_5_8 r0_5_9 r0_5_10 r0_5_11 r0_5_12 r0_5_13 r0_5_14 r0_5_15 r0_5_16 r0_5_17 r0_5_18

end Agent113.FiveLayer
