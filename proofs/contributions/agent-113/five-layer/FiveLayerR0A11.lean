import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 0, s0 = 11). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r0_11_0 : cert5.stepRow 0 11 0 = true := by decide +kernel
theorem r0_11_1 : cert5.stepRow 0 11 1 = true := by decide +kernel
theorem r0_11_2 : cert5.stepRow 0 11 2 = true := by decide +kernel
theorem r0_11_3 : cert5.stepRow 0 11 3 = true := by decide +kernel
theorem r0_11_4 : cert5.stepRow 0 11 4 = true := by decide +kernel
theorem r0_11_5 : cert5.stepRow 0 11 5 = true := by decide +kernel
theorem r0_11_6 : cert5.stepRow 0 11 6 = true := by decide +kernel
theorem r0_11_7 : cert5.stepRow 0 11 7 = true := by decide +kernel
theorem r0_11_8 : cert5.stepRow 0 11 8 = true := by decide +kernel
theorem r0_11_9 : cert5.stepRow 0 11 9 = true := by decide +kernel
theorem r0_11_10 : cert5.stepRow 0 11 10 = true := by decide +kernel
theorem r0_11_11 : cert5.stepRow 0 11 11 = true := by decide +kernel
theorem r0_11_12 : cert5.stepRow 0 11 12 = true := by decide +kernel
theorem r0_11_13 : cert5.stepRow 0 11 13 = true := by decide +kernel
theorem r0_11_14 : cert5.stepRow 0 11 14 = true := by decide +kernel
theorem r0_11_15 : cert5.stepRow 0 11 15 = true := by decide +kernel
theorem r0_11_16 : cert5.stepRow 0 11 16 = true := by decide +kernel
theorem r0_11_17 : cert5.stepRow 0 11 17 = true := by decide +kernel
theorem r0_11_18 : cert5.stepRow 0 11 18 = true := by decide +kernel

theorem r0_11 : ∀ b, b ≤ 18 → cert5.stepRow 0 11 b = true :=
  cover19 r0_11_0 r0_11_1 r0_11_2 r0_11_3 r0_11_4 r0_11_5 r0_11_6 r0_11_7 r0_11_8 r0_11_9 r0_11_10 r0_11_11 r0_11_12 r0_11_13 r0_11_14 r0_11_15 r0_11_16 r0_11_17 r0_11_18

end Agent113.FiveLayer
