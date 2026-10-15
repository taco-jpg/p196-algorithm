import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 1, s0 = 17). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r1_17_0 : cert5.stepRow 1 17 0 = true := by decide +kernel
theorem r1_17_1 : cert5.stepRow 1 17 1 = true := by decide +kernel
theorem r1_17_2 : cert5.stepRow 1 17 2 = true := by decide +kernel
theorem r1_17_3 : cert5.stepRow 1 17 3 = true := by decide +kernel
theorem r1_17_4 : cert5.stepRow 1 17 4 = true := by decide +kernel
theorem r1_17_5 : cert5.stepRow 1 17 5 = true := by decide +kernel
theorem r1_17_6 : cert5.stepRow 1 17 6 = true := by decide +kernel
theorem r1_17_7 : cert5.stepRow 1 17 7 = true := by decide +kernel
theorem r1_17_8 : cert5.stepRow 1 17 8 = true := by decide +kernel
theorem r1_17_9 : cert5.stepRow 1 17 9 = true := by decide +kernel
theorem r1_17_10 : cert5.stepRow 1 17 10 = true := by decide +kernel
theorem r1_17_11 : cert5.stepRow 1 17 11 = true := by decide +kernel
theorem r1_17_12 : cert5.stepRow 1 17 12 = true := by decide +kernel
theorem r1_17_13 : cert5.stepRow 1 17 13 = true := by decide +kernel
theorem r1_17_14 : cert5.stepRow 1 17 14 = true := by decide +kernel
theorem r1_17_15 : cert5.stepRow 1 17 15 = true := by decide +kernel
theorem r1_17_16 : cert5.stepRow 1 17 16 = true := by decide +kernel
theorem r1_17_17 : cert5.stepRow 1 17 17 = true := by decide +kernel
theorem r1_17_18 : cert5.stepRow 1 17 18 = true := by decide +kernel

theorem r1_17 : ∀ b, b ≤ 18 → cert5.stepRow 1 17 b = true :=
  cover19 r1_17_0 r1_17_1 r1_17_2 r1_17_3 r1_17_4 r1_17_5 r1_17_6 r1_17_7 r1_17_8 r1_17_9 r1_17_10 r1_17_11 r1_17_12 r1_17_13 r1_17_14 r1_17_15 r1_17_16 r1_17_17 r1_17_18

end Agent113.FiveLayer
