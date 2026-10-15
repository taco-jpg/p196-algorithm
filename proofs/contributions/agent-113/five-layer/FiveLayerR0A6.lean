import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 0, s0 = 6). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r0_6_0 : cert5.stepRow 0 6 0 = true := by decide +kernel
theorem r0_6_1 : cert5.stepRow 0 6 1 = true := by decide +kernel
theorem r0_6_2 : cert5.stepRow 0 6 2 = true := by decide +kernel
theorem r0_6_3 : cert5.stepRow 0 6 3 = true := by decide +kernel
theorem r0_6_4 : cert5.stepRow 0 6 4 = true := by decide +kernel
theorem r0_6_5 : cert5.stepRow 0 6 5 = true := by decide +kernel
theorem r0_6_6 : cert5.stepRow 0 6 6 = true := by decide +kernel
theorem r0_6_7 : cert5.stepRow 0 6 7 = true := by decide +kernel
theorem r0_6_8 : cert5.stepRow 0 6 8 = true := by decide +kernel
theorem r0_6_9 : cert5.stepRow 0 6 9 = true := by decide +kernel
theorem r0_6_10 : cert5.stepRow 0 6 10 = true := by decide +kernel
theorem r0_6_11 : cert5.stepRow 0 6 11 = true := by decide +kernel
theorem r0_6_12 : cert5.stepRow 0 6 12 = true := by decide +kernel
theorem r0_6_13 : cert5.stepRow 0 6 13 = true := by decide +kernel
theorem r0_6_14 : cert5.stepRow 0 6 14 = true := by decide +kernel
theorem r0_6_15 : cert5.stepRow 0 6 15 = true := by decide +kernel
theorem r0_6_16 : cert5.stepRow 0 6 16 = true := by decide +kernel
theorem r0_6_17 : cert5.stepRow 0 6 17 = true := by decide +kernel
theorem r0_6_18 : cert5.stepRow 0 6 18 = true := by decide +kernel

theorem r0_6 : ∀ b, b ≤ 18 → cert5.stepRow 0 6 b = true :=
  cover19 r0_6_0 r0_6_1 r0_6_2 r0_6_3 r0_6_4 r0_6_5 r0_6_6 r0_6_7 r0_6_8 r0_6_9 r0_6_10 r0_6_11 r0_6_12 r0_6_13 r0_6_14 r0_6_15 r0_6_16 r0_6_17 r0_6_18

end Agent113.FiveLayer
