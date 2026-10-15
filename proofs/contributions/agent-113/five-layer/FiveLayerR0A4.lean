import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 0, s0 = 4). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r0_4_0 : cert5.stepRow 0 4 0 = true := by decide +kernel
theorem r0_4_1 : cert5.stepRow 0 4 1 = true := by decide +kernel
theorem r0_4_2 : cert5.stepRow 0 4 2 = true := by decide +kernel
theorem r0_4_3 : cert5.stepRow 0 4 3 = true := by decide +kernel
theorem r0_4_4 : cert5.stepRow 0 4 4 = true := by decide +kernel
theorem r0_4_5 : cert5.stepRow 0 4 5 = true := by decide +kernel
theorem r0_4_6 : cert5.stepRow 0 4 6 = true := by decide +kernel
theorem r0_4_7 : cert5.stepRow 0 4 7 = true := by decide +kernel
theorem r0_4_8 : cert5.stepRow 0 4 8 = true := by decide +kernel
theorem r0_4_9 : cert5.stepRow 0 4 9 = true := by decide +kernel
theorem r0_4_10 : cert5.stepRow 0 4 10 = true := by decide +kernel
theorem r0_4_11 : cert5.stepRow 0 4 11 = true := by decide +kernel
theorem r0_4_12 : cert5.stepRow 0 4 12 = true := by decide +kernel
theorem r0_4_13 : cert5.stepRow 0 4 13 = true := by decide +kernel
theorem r0_4_14 : cert5.stepRow 0 4 14 = true := by decide +kernel
theorem r0_4_15 : cert5.stepRow 0 4 15 = true := by decide +kernel
theorem r0_4_16 : cert5.stepRow 0 4 16 = true := by decide +kernel
theorem r0_4_17 : cert5.stepRow 0 4 17 = true := by decide +kernel
theorem r0_4_18 : cert5.stepRow 0 4 18 = true := by decide +kernel

theorem r0_4 : ∀ b, b ≤ 18 → cert5.stepRow 0 4 b = true :=
  cover19 r0_4_0 r0_4_1 r0_4_2 r0_4_3 r0_4_4 r0_4_5 r0_4_6 r0_4_7 r0_4_8 r0_4_9 r0_4_10 r0_4_11 r0_4_12 r0_4_13 r0_4_14 r0_4_15 r0_4_16 r0_4_17 r0_4_18

end Agent113.FiveLayer
