import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 4, s0 = 4). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r4_4_0 : cert5.stepRow 4 4 0 = true := by decide +kernel
theorem r4_4_1 : cert5.stepRow 4 4 1 = true := by decide +kernel
theorem r4_4_2 : cert5.stepRow 4 4 2 = true := by decide +kernel
theorem r4_4_3 : cert5.stepRow 4 4 3 = true := by decide +kernel
theorem r4_4_4 : cert5.stepRow 4 4 4 = true := by decide +kernel
theorem r4_4_5 : cert5.stepRow 4 4 5 = true := by decide +kernel
theorem r4_4_6 : cert5.stepRow 4 4 6 = true := by decide +kernel
theorem r4_4_7 : cert5.stepRow 4 4 7 = true := by decide +kernel
theorem r4_4_8 : cert5.stepRow 4 4 8 = true := by decide +kernel
theorem r4_4_9 : cert5.stepRow 4 4 9 = true := by decide +kernel
theorem r4_4_10 : cert5.stepRow 4 4 10 = true := by decide +kernel
theorem r4_4_11 : cert5.stepRow 4 4 11 = true := by decide +kernel
theorem r4_4_12 : cert5.stepRow 4 4 12 = true := by decide +kernel
theorem r4_4_13 : cert5.stepRow 4 4 13 = true := by decide +kernel
theorem r4_4_14 : cert5.stepRow 4 4 14 = true := by decide +kernel
theorem r4_4_15 : cert5.stepRow 4 4 15 = true := by decide +kernel
theorem r4_4_16 : cert5.stepRow 4 4 16 = true := by decide +kernel
theorem r4_4_17 : cert5.stepRow 4 4 17 = true := by decide +kernel
theorem r4_4_18 : cert5.stepRow 4 4 18 = true := by decide +kernel

theorem r4_4 : ∀ b, b ≤ 18 → cert5.stepRow 4 4 b = true :=
  cover19 r4_4_0 r4_4_1 r4_4_2 r4_4_3 r4_4_4 r4_4_5 r4_4_6 r4_4_7 r4_4_8 r4_4_9 r4_4_10 r4_4_11 r4_4_12 r4_4_13 r4_4_14 r4_4_15 r4_4_16 r4_4_17 r4_4_18

end Agent113.FiveLayer
