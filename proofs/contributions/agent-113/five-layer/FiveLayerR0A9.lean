import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 0, s0 = 9). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r0_9_0 : cert5.stepRow 0 9 0 = true := by decide +kernel
theorem r0_9_1 : cert5.stepRow 0 9 1 = true := by decide +kernel
theorem r0_9_2 : cert5.stepRow 0 9 2 = true := by decide +kernel
theorem r0_9_3 : cert5.stepRow 0 9 3 = true := by decide +kernel
theorem r0_9_4 : cert5.stepRow 0 9 4 = true := by decide +kernel
theorem r0_9_5 : cert5.stepRow 0 9 5 = true := by decide +kernel
theorem r0_9_6 : cert5.stepRow 0 9 6 = true := by decide +kernel
theorem r0_9_7 : cert5.stepRow 0 9 7 = true := by decide +kernel
theorem r0_9_8 : cert5.stepRow 0 9 8 = true := by decide +kernel
theorem r0_9_9 : cert5.stepRow 0 9 9 = true := by decide +kernel
theorem r0_9_10 : cert5.stepRow 0 9 10 = true := by decide +kernel
theorem r0_9_11 : cert5.stepRow 0 9 11 = true := by decide +kernel
theorem r0_9_12 : cert5.stepRow 0 9 12 = true := by decide +kernel
theorem r0_9_13 : cert5.stepRow 0 9 13 = true := by decide +kernel
theorem r0_9_14 : cert5.stepRow 0 9 14 = true := by decide +kernel
theorem r0_9_15 : cert5.stepRow 0 9 15 = true := by decide +kernel
theorem r0_9_16 : cert5.stepRow 0 9 16 = true := by decide +kernel
theorem r0_9_17 : cert5.stepRow 0 9 17 = true := by decide +kernel
theorem r0_9_18 : cert5.stepRow 0 9 18 = true := by decide +kernel

theorem r0_9 : ∀ b, b ≤ 18 → cert5.stepRow 0 9 b = true :=
  cover19 r0_9_0 r0_9_1 r0_9_2 r0_9_3 r0_9_4 r0_9_5 r0_9_6 r0_9_7 r0_9_8 r0_9_9 r0_9_10 r0_9_11 r0_9_12 r0_9_13 r0_9_14 r0_9_15 r0_9_16 r0_9_17 r0_9_18

end Agent113.FiveLayer
