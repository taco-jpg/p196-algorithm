import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 1, s0 = 9). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r1_9_0 : cert5.stepRow 1 9 0 = true := by decide +kernel
theorem r1_9_1 : cert5.stepRow 1 9 1 = true := by decide +kernel
theorem r1_9_2 : cert5.stepRow 1 9 2 = true := by decide +kernel
theorem r1_9_3 : cert5.stepRow 1 9 3 = true := by decide +kernel
theorem r1_9_4 : cert5.stepRow 1 9 4 = true := by decide +kernel
theorem r1_9_5 : cert5.stepRow 1 9 5 = true := by decide +kernel
theorem r1_9_6 : cert5.stepRow 1 9 6 = true := by decide +kernel
theorem r1_9_7 : cert5.stepRow 1 9 7 = true := by decide +kernel
theorem r1_9_8 : cert5.stepRow 1 9 8 = true := by decide +kernel
theorem r1_9_9 : cert5.stepRow 1 9 9 = true := by decide +kernel
theorem r1_9_10 : cert5.stepRow 1 9 10 = true := by decide +kernel
theorem r1_9_11 : cert5.stepRow 1 9 11 = true := by decide +kernel
theorem r1_9_12 : cert5.stepRow 1 9 12 = true := by decide +kernel
theorem r1_9_13 : cert5.stepRow 1 9 13 = true := by decide +kernel
theorem r1_9_14 : cert5.stepRow 1 9 14 = true := by decide +kernel
theorem r1_9_15 : cert5.stepRow 1 9 15 = true := by decide +kernel
theorem r1_9_16 : cert5.stepRow 1 9 16 = true := by decide +kernel
theorem r1_9_17 : cert5.stepRow 1 9 17 = true := by decide +kernel
theorem r1_9_18 : cert5.stepRow 1 9 18 = true := by decide +kernel

theorem r1_9 : ∀ b, b ≤ 18 → cert5.stepRow 1 9 b = true :=
  cover19 r1_9_0 r1_9_1 r1_9_2 r1_9_3 r1_9_4 r1_9_5 r1_9_6 r1_9_7 r1_9_8 r1_9_9 r1_9_10 r1_9_11 r1_9_12 r1_9_13 r1_9_14 r1_9_15 r1_9_16 r1_9_17 r1_9_18

end Agent113.FiveLayer
