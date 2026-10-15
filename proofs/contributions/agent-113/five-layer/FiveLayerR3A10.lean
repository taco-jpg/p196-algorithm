import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 3, s0 = 10). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r3_10_0 : cert5.stepRow 3 10 0 = true := by decide +kernel
theorem r3_10_1 : cert5.stepRow 3 10 1 = true := by decide +kernel
theorem r3_10_2 : cert5.stepRow 3 10 2 = true := by decide +kernel
theorem r3_10_3 : cert5.stepRow 3 10 3 = true := by decide +kernel
theorem r3_10_4 : cert5.stepRow 3 10 4 = true := by decide +kernel
theorem r3_10_5 : cert5.stepRow 3 10 5 = true := by decide +kernel
theorem r3_10_6 : cert5.stepRow 3 10 6 = true := by decide +kernel
theorem r3_10_7 : cert5.stepRow 3 10 7 = true := by decide +kernel
theorem r3_10_8 : cert5.stepRow 3 10 8 = true := by decide +kernel
theorem r3_10_9 : cert5.stepRow 3 10 9 = true := by decide +kernel
theorem r3_10_10 : cert5.stepRow 3 10 10 = true := by decide +kernel
theorem r3_10_11 : cert5.stepRow 3 10 11 = true := by decide +kernel
theorem r3_10_12 : cert5.stepRow 3 10 12 = true := by decide +kernel
theorem r3_10_13 : cert5.stepRow 3 10 13 = true := by decide +kernel
theorem r3_10_14 : cert5.stepRow 3 10 14 = true := by decide +kernel
theorem r3_10_15 : cert5.stepRow 3 10 15 = true := by decide +kernel
theorem r3_10_16 : cert5.stepRow 3 10 16 = true := by decide +kernel
theorem r3_10_17 : cert5.stepRow 3 10 17 = true := by decide +kernel
theorem r3_10_18 : cert5.stepRow 3 10 18 = true := by decide +kernel

theorem r3_10 : ∀ b, b ≤ 18 → cert5.stepRow 3 10 b = true :=
  cover19 r3_10_0 r3_10_1 r3_10_2 r3_10_3 r3_10_4 r3_10_5 r3_10_6 r3_10_7 r3_10_8 r3_10_9 r3_10_10 r3_10_11 r3_10_12 r3_10_13 r3_10_14 r3_10_15 r3_10_16 r3_10_17 r3_10_18

end Agent113.FiveLayer
