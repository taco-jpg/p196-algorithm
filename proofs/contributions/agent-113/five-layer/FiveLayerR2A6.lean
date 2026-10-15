import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 2, s0 = 6). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r2_6_0 : cert5.stepRow 2 6 0 = true := by decide +kernel
theorem r2_6_1 : cert5.stepRow 2 6 1 = true := by decide +kernel
theorem r2_6_2 : cert5.stepRow 2 6 2 = true := by decide +kernel
theorem r2_6_3 : cert5.stepRow 2 6 3 = true := by decide +kernel
theorem r2_6_4 : cert5.stepRow 2 6 4 = true := by decide +kernel
theorem r2_6_5 : cert5.stepRow 2 6 5 = true := by decide +kernel
theorem r2_6_6 : cert5.stepRow 2 6 6 = true := by decide +kernel
theorem r2_6_7 : cert5.stepRow 2 6 7 = true := by decide +kernel
theorem r2_6_8 : cert5.stepRow 2 6 8 = true := by decide +kernel
theorem r2_6_9 : cert5.stepRow 2 6 9 = true := by decide +kernel
theorem r2_6_10 : cert5.stepRow 2 6 10 = true := by decide +kernel
theorem r2_6_11 : cert5.stepRow 2 6 11 = true := by decide +kernel
theorem r2_6_12 : cert5.stepRow 2 6 12 = true := by decide +kernel
theorem r2_6_13 : cert5.stepRow 2 6 13 = true := by decide +kernel
theorem r2_6_14 : cert5.stepRow 2 6 14 = true := by decide +kernel
theorem r2_6_15 : cert5.stepRow 2 6 15 = true := by decide +kernel
theorem r2_6_16 : cert5.stepRow 2 6 16 = true := by decide +kernel
theorem r2_6_17 : cert5.stepRow 2 6 17 = true := by decide +kernel
theorem r2_6_18 : cert5.stepRow 2 6 18 = true := by decide +kernel

theorem r2_6 : ∀ b, b ≤ 18 → cert5.stepRow 2 6 b = true :=
  cover19 r2_6_0 r2_6_1 r2_6_2 r2_6_3 r2_6_4 r2_6_5 r2_6_6 r2_6_7 r2_6_8 r2_6_9 r2_6_10 r2_6_11 r2_6_12 r2_6_13 r2_6_14 r2_6_15 r2_6_16 r2_6_17 r2_6_18

end Agent113.FiveLayer
