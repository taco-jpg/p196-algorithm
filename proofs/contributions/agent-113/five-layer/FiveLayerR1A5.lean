import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 1, s0 = 5). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r1_5_0 : cert5.stepRow 1 5 0 = true := by decide +kernel
theorem r1_5_1 : cert5.stepRow 1 5 1 = true := by decide +kernel
theorem r1_5_2 : cert5.stepRow 1 5 2 = true := by decide +kernel
theorem r1_5_3 : cert5.stepRow 1 5 3 = true := by decide +kernel
theorem r1_5_4 : cert5.stepRow 1 5 4 = true := by decide +kernel
theorem r1_5_5 : cert5.stepRow 1 5 5 = true := by decide +kernel
theorem r1_5_6 : cert5.stepRow 1 5 6 = true := by decide +kernel
theorem r1_5_7 : cert5.stepRow 1 5 7 = true := by decide +kernel
theorem r1_5_8 : cert5.stepRow 1 5 8 = true := by decide +kernel
theorem r1_5_9 : cert5.stepRow 1 5 9 = true := by decide +kernel
theorem r1_5_10 : cert5.stepRow 1 5 10 = true := by decide +kernel
theorem r1_5_11 : cert5.stepRow 1 5 11 = true := by decide +kernel
theorem r1_5_12 : cert5.stepRow 1 5 12 = true := by decide +kernel
theorem r1_5_13 : cert5.stepRow 1 5 13 = true := by decide +kernel
theorem r1_5_14 : cert5.stepRow 1 5 14 = true := by decide +kernel
theorem r1_5_15 : cert5.stepRow 1 5 15 = true := by decide +kernel
theorem r1_5_16 : cert5.stepRow 1 5 16 = true := by decide +kernel
theorem r1_5_17 : cert5.stepRow 1 5 17 = true := by decide +kernel
theorem r1_5_18 : cert5.stepRow 1 5 18 = true := by decide +kernel

theorem r1_5 : ∀ b, b ≤ 18 → cert5.stepRow 1 5 b = true :=
  cover19 r1_5_0 r1_5_1 r1_5_2 r1_5_3 r1_5_4 r1_5_5 r1_5_6 r1_5_7 r1_5_8 r1_5_9 r1_5_10 r1_5_11 r1_5_12 r1_5_13 r1_5_14 r1_5_15 r1_5_16 r1_5_17 r1_5_18

end Agent113.FiveLayer
