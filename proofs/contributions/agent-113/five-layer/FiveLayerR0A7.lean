import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 0, s0 = 7). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r0_7_0 : cert5.stepRow 0 7 0 = true := by decide +kernel
theorem r0_7_1 : cert5.stepRow 0 7 1 = true := by decide +kernel
theorem r0_7_2 : cert5.stepRow 0 7 2 = true := by decide +kernel
theorem r0_7_3 : cert5.stepRow 0 7 3 = true := by decide +kernel
theorem r0_7_4 : cert5.stepRow 0 7 4 = true := by decide +kernel
theorem r0_7_5 : cert5.stepRow 0 7 5 = true := by decide +kernel
theorem r0_7_6 : cert5.stepRow 0 7 6 = true := by decide +kernel
theorem r0_7_7 : cert5.stepRow 0 7 7 = true := by decide +kernel
theorem r0_7_8 : cert5.stepRow 0 7 8 = true := by decide +kernel
theorem r0_7_9 : cert5.stepRow 0 7 9 = true := by decide +kernel
theorem r0_7_10 : cert5.stepRow 0 7 10 = true := by decide +kernel
theorem r0_7_11 : cert5.stepRow 0 7 11 = true := by decide +kernel
theorem r0_7_12 : cert5.stepRow 0 7 12 = true := by decide +kernel
theorem r0_7_13 : cert5.stepRow 0 7 13 = true := by decide +kernel
theorem r0_7_14 : cert5.stepRow 0 7 14 = true := by decide +kernel
theorem r0_7_15 : cert5.stepRow 0 7 15 = true := by decide +kernel
theorem r0_7_16 : cert5.stepRow 0 7 16 = true := by decide +kernel
theorem r0_7_17 : cert5.stepRow 0 7 17 = true := by decide +kernel
theorem r0_7_18 : cert5.stepRow 0 7 18 = true := by decide +kernel

theorem r0_7 : ∀ b, b ≤ 18 → cert5.stepRow 0 7 b = true :=
  cover19 r0_7_0 r0_7_1 r0_7_2 r0_7_3 r0_7_4 r0_7_5 r0_7_6 r0_7_7 r0_7_8 r0_7_9 r0_7_10 r0_7_11 r0_7_12 r0_7_13 r0_7_14 r0_7_15 r0_7_16 r0_7_17 r0_7_18

end Agent113.FiveLayer
