import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 4, s0 = 6). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r4_6_0 : cert5.stepRow 4 6 0 = true := by decide +kernel
theorem r4_6_1 : cert5.stepRow 4 6 1 = true := by decide +kernel
theorem r4_6_2 : cert5.stepRow 4 6 2 = true := by decide +kernel
theorem r4_6_3 : cert5.stepRow 4 6 3 = true := by decide +kernel
theorem r4_6_4 : cert5.stepRow 4 6 4 = true := by decide +kernel
theorem r4_6_5 : cert5.stepRow 4 6 5 = true := by decide +kernel
theorem r4_6_6 : cert5.stepRow 4 6 6 = true := by decide +kernel
theorem r4_6_7 : cert5.stepRow 4 6 7 = true := by decide +kernel
theorem r4_6_8 : cert5.stepRow 4 6 8 = true := by decide +kernel
theorem r4_6_9 : cert5.stepRow 4 6 9 = true := by decide +kernel
theorem r4_6_10 : cert5.stepRow 4 6 10 = true := by decide +kernel
theorem r4_6_11 : cert5.stepRow 4 6 11 = true := by decide +kernel
theorem r4_6_12 : cert5.stepRow 4 6 12 = true := by decide +kernel
theorem r4_6_13 : cert5.stepRow 4 6 13 = true := by decide +kernel
theorem r4_6_14 : cert5.stepRow 4 6 14 = true := by decide +kernel
theorem r4_6_15 : cert5.stepRow 4 6 15 = true := by decide +kernel
theorem r4_6_16 : cert5.stepRow 4 6 16 = true := by decide +kernel
theorem r4_6_17 : cert5.stepRow 4 6 17 = true := by decide +kernel
theorem r4_6_18 : cert5.stepRow 4 6 18 = true := by decide +kernel

theorem r4_6 : ∀ b, b ≤ 18 → cert5.stepRow 4 6 b = true :=
  cover19 r4_6_0 r4_6_1 r4_6_2 r4_6_3 r4_6_4 r4_6_5 r4_6_6 r4_6_7 r4_6_8 r4_6_9 r4_6_10 r4_6_11 r4_6_12 r4_6_13 r4_6_14 r4_6_15 r4_6_16 r4_6_17 r4_6_18

end Agent113.FiveLayer
