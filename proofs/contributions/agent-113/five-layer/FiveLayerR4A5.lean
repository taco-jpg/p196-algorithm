import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 4, s0 = 5). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r4_5_0 : cert5.stepRow 4 5 0 = true := by decide +kernel
theorem r4_5_1 : cert5.stepRow 4 5 1 = true := by decide +kernel
theorem r4_5_2 : cert5.stepRow 4 5 2 = true := by decide +kernel
theorem r4_5_3 : cert5.stepRow 4 5 3 = true := by decide +kernel
theorem r4_5_4 : cert5.stepRow 4 5 4 = true := by decide +kernel
theorem r4_5_5 : cert5.stepRow 4 5 5 = true := by decide +kernel
theorem r4_5_6 : cert5.stepRow 4 5 6 = true := by decide +kernel
theorem r4_5_7 : cert5.stepRow 4 5 7 = true := by decide +kernel
theorem r4_5_8 : cert5.stepRow 4 5 8 = true := by decide +kernel
theorem r4_5_9 : cert5.stepRow 4 5 9 = true := by decide +kernel
theorem r4_5_10 : cert5.stepRow 4 5 10 = true := by decide +kernel
theorem r4_5_11 : cert5.stepRow 4 5 11 = true := by decide +kernel
theorem r4_5_12 : cert5.stepRow 4 5 12 = true := by decide +kernel
theorem r4_5_13 : cert5.stepRow 4 5 13 = true := by decide +kernel
theorem r4_5_14 : cert5.stepRow 4 5 14 = true := by decide +kernel
theorem r4_5_15 : cert5.stepRow 4 5 15 = true := by decide +kernel
theorem r4_5_16 : cert5.stepRow 4 5 16 = true := by decide +kernel
theorem r4_5_17 : cert5.stepRow 4 5 17 = true := by decide +kernel
theorem r4_5_18 : cert5.stepRow 4 5 18 = true := by decide +kernel

theorem r4_5 : ∀ b, b ≤ 18 → cert5.stepRow 4 5 b = true :=
  cover19 r4_5_0 r4_5_1 r4_5_2 r4_5_3 r4_5_4 r4_5_5 r4_5_6 r4_5_7 r4_5_8 r4_5_9 r4_5_10 r4_5_11 r4_5_12 r4_5_13 r4_5_14 r4_5_15 r4_5_16 r4_5_17 r4_5_18

end Agent113.FiveLayer
