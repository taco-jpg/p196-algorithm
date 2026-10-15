import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 3, s0 = 14). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r3_14_0 : cert5.stepRow 3 14 0 = true := by decide +kernel
theorem r3_14_1 : cert5.stepRow 3 14 1 = true := by decide +kernel
theorem r3_14_2 : cert5.stepRow 3 14 2 = true := by decide +kernel
theorem r3_14_3 : cert5.stepRow 3 14 3 = true := by decide +kernel
theorem r3_14_4 : cert5.stepRow 3 14 4 = true := by decide +kernel
theorem r3_14_5 : cert5.stepRow 3 14 5 = true := by decide +kernel
theorem r3_14_6 : cert5.stepRow 3 14 6 = true := by decide +kernel
theorem r3_14_7 : cert5.stepRow 3 14 7 = true := by decide +kernel
theorem r3_14_8 : cert5.stepRow 3 14 8 = true := by decide +kernel
theorem r3_14_9 : cert5.stepRow 3 14 9 = true := by decide +kernel
theorem r3_14_10 : cert5.stepRow 3 14 10 = true := by decide +kernel
theorem r3_14_11 : cert5.stepRow 3 14 11 = true := by decide +kernel
theorem r3_14_12 : cert5.stepRow 3 14 12 = true := by decide +kernel
theorem r3_14_13 : cert5.stepRow 3 14 13 = true := by decide +kernel
theorem r3_14_14 : cert5.stepRow 3 14 14 = true := by decide +kernel
theorem r3_14_15 : cert5.stepRow 3 14 15 = true := by decide +kernel
theorem r3_14_16 : cert5.stepRow 3 14 16 = true := by decide +kernel
theorem r3_14_17 : cert5.stepRow 3 14 17 = true := by decide +kernel
theorem r3_14_18 : cert5.stepRow 3 14 18 = true := by decide +kernel

theorem r3_14 : ∀ b, b ≤ 18 → cert5.stepRow 3 14 b = true :=
  cover19 r3_14_0 r3_14_1 r3_14_2 r3_14_3 r3_14_4 r3_14_5 r3_14_6 r3_14_7 r3_14_8 r3_14_9 r3_14_10 r3_14_11 r3_14_12 r3_14_13 r3_14_14 r3_14_15 r3_14_16 r3_14_17 r3_14_18

end Agent113.FiveLayer
