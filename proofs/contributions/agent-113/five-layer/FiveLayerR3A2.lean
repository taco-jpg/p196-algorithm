import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 3, s0 = 2). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r3_2_0 : cert5.stepRow 3 2 0 = true := by decide +kernel
theorem r3_2_1 : cert5.stepRow 3 2 1 = true := by decide +kernel
theorem r3_2_2 : cert5.stepRow 3 2 2 = true := by decide +kernel
theorem r3_2_3 : cert5.stepRow 3 2 3 = true := by decide +kernel
theorem r3_2_4 : cert5.stepRow 3 2 4 = true := by decide +kernel
theorem r3_2_5 : cert5.stepRow 3 2 5 = true := by decide +kernel
theorem r3_2_6 : cert5.stepRow 3 2 6 = true := by decide +kernel
theorem r3_2_7 : cert5.stepRow 3 2 7 = true := by decide +kernel
theorem r3_2_8 : cert5.stepRow 3 2 8 = true := by decide +kernel
theorem r3_2_9 : cert5.stepRow 3 2 9 = true := by decide +kernel
theorem r3_2_10 : cert5.stepRow 3 2 10 = true := by decide +kernel
theorem r3_2_11 : cert5.stepRow 3 2 11 = true := by decide +kernel
theorem r3_2_12 : cert5.stepRow 3 2 12 = true := by decide +kernel
theorem r3_2_13 : cert5.stepRow 3 2 13 = true := by decide +kernel
theorem r3_2_14 : cert5.stepRow 3 2 14 = true := by decide +kernel
theorem r3_2_15 : cert5.stepRow 3 2 15 = true := by decide +kernel
theorem r3_2_16 : cert5.stepRow 3 2 16 = true := by decide +kernel
theorem r3_2_17 : cert5.stepRow 3 2 17 = true := by decide +kernel
theorem r3_2_18 : cert5.stepRow 3 2 18 = true := by decide +kernel

theorem r3_2 : ∀ b, b ≤ 18 → cert5.stepRow 3 2 b = true :=
  cover19 r3_2_0 r3_2_1 r3_2_2 r3_2_3 r3_2_4 r3_2_5 r3_2_6 r3_2_7 r3_2_8 r3_2_9 r3_2_10 r3_2_11 r3_2_12 r3_2_13 r3_2_14 r3_2_15 r3_2_16 r3_2_17 r3_2_18

end Agent113.FiveLayer
