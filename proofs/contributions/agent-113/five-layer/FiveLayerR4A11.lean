import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 4, s0 = 11). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r4_11_0 : cert5.stepRow 4 11 0 = true := by decide +kernel
theorem r4_11_1 : cert5.stepRow 4 11 1 = true := by decide +kernel
theorem r4_11_2 : cert5.stepRow 4 11 2 = true := by decide +kernel
theorem r4_11_3 : cert5.stepRow 4 11 3 = true := by decide +kernel
theorem r4_11_4 : cert5.stepRow 4 11 4 = true := by decide +kernel
theorem r4_11_5 : cert5.stepRow 4 11 5 = true := by decide +kernel
theorem r4_11_6 : cert5.stepRow 4 11 6 = true := by decide +kernel
theorem r4_11_7 : cert5.stepRow 4 11 7 = true := by decide +kernel
theorem r4_11_8 : cert5.stepRow 4 11 8 = true := by decide +kernel
theorem r4_11_9 : cert5.stepRow 4 11 9 = true := by decide +kernel
theorem r4_11_10 : cert5.stepRow 4 11 10 = true := by decide +kernel
theorem r4_11_11 : cert5.stepRow 4 11 11 = true := by decide +kernel
theorem r4_11_12 : cert5.stepRow 4 11 12 = true := by decide +kernel
theorem r4_11_13 : cert5.stepRow 4 11 13 = true := by decide +kernel
theorem r4_11_14 : cert5.stepRow 4 11 14 = true := by decide +kernel
theorem r4_11_15 : cert5.stepRow 4 11 15 = true := by decide +kernel
theorem r4_11_16 : cert5.stepRow 4 11 16 = true := by decide +kernel
theorem r4_11_17 : cert5.stepRow 4 11 17 = true := by decide +kernel
theorem r4_11_18 : cert5.stepRow 4 11 18 = true := by decide +kernel

theorem r4_11 : ∀ b, b ≤ 18 → cert5.stepRow 4 11 b = true :=
  cover19 r4_11_0 r4_11_1 r4_11_2 r4_11_3 r4_11_4 r4_11_5 r4_11_6 r4_11_7 r4_11_8 r4_11_9 r4_11_10 r4_11_11 r4_11_12 r4_11_13 r4_11_14 r4_11_15 r4_11_16 r4_11_17 r4_11_18

end Agent113.FiveLayer
