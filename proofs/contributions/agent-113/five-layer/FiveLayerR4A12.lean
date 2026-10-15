import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 4, s0 = 12). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r4_12_0 : cert5.stepRow 4 12 0 = true := by decide +kernel
theorem r4_12_1 : cert5.stepRow 4 12 1 = true := by decide +kernel
theorem r4_12_2 : cert5.stepRow 4 12 2 = true := by decide +kernel
theorem r4_12_3 : cert5.stepRow 4 12 3 = true := by decide +kernel
theorem r4_12_4 : cert5.stepRow 4 12 4 = true := by decide +kernel
theorem r4_12_5 : cert5.stepRow 4 12 5 = true := by decide +kernel
theorem r4_12_6 : cert5.stepRow 4 12 6 = true := by decide +kernel
theorem r4_12_7 : cert5.stepRow 4 12 7 = true := by decide +kernel
theorem r4_12_8 : cert5.stepRow 4 12 8 = true := by decide +kernel
theorem r4_12_9 : cert5.stepRow 4 12 9 = true := by decide +kernel
theorem r4_12_10 : cert5.stepRow 4 12 10 = true := by decide +kernel
theorem r4_12_11 : cert5.stepRow 4 12 11 = true := by decide +kernel
theorem r4_12_12 : cert5.stepRow 4 12 12 = true := by decide +kernel
theorem r4_12_13 : cert5.stepRow 4 12 13 = true := by decide +kernel
theorem r4_12_14 : cert5.stepRow 4 12 14 = true := by decide +kernel
theorem r4_12_15 : cert5.stepRow 4 12 15 = true := by decide +kernel
theorem r4_12_16 : cert5.stepRow 4 12 16 = true := by decide +kernel
theorem r4_12_17 : cert5.stepRow 4 12 17 = true := by decide +kernel
theorem r4_12_18 : cert5.stepRow 4 12 18 = true := by decide +kernel

theorem r4_12 : ∀ b, b ≤ 18 → cert5.stepRow 4 12 b = true :=
  cover19 r4_12_0 r4_12_1 r4_12_2 r4_12_3 r4_12_4 r4_12_5 r4_12_6 r4_12_7 r4_12_8 r4_12_9 r4_12_10 r4_12_11 r4_12_12 r4_12_13 r4_12_14 r4_12_15 r4_12_16 r4_12_17 r4_12_18

end Agent113.FiveLayer
