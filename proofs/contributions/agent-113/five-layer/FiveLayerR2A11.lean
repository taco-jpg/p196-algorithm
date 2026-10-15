import FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 2, s0 = 11). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r2_11_0 : cert5.stepRow 2 11 0 = true := by decide +kernel
theorem r2_11_1 : cert5.stepRow 2 11 1 = true := by decide +kernel
theorem r2_11_2 : cert5.stepRow 2 11 2 = true := by decide +kernel
theorem r2_11_3 : cert5.stepRow 2 11 3 = true := by decide +kernel
theorem r2_11_4 : cert5.stepRow 2 11 4 = true := by decide +kernel
theorem r2_11_5 : cert5.stepRow 2 11 5 = true := by decide +kernel
theorem r2_11_6 : cert5.stepRow 2 11 6 = true := by decide +kernel
theorem r2_11_7 : cert5.stepRow 2 11 7 = true := by decide +kernel
theorem r2_11_8 : cert5.stepRow 2 11 8 = true := by decide +kernel
theorem r2_11_9 : cert5.stepRow 2 11 9 = true := by decide +kernel
theorem r2_11_10 : cert5.stepRow 2 11 10 = true := by decide +kernel
theorem r2_11_11 : cert5.stepRow 2 11 11 = true := by decide +kernel
theorem r2_11_12 : cert5.stepRow 2 11 12 = true := by decide +kernel
theorem r2_11_13 : cert5.stepRow 2 11 13 = true := by decide +kernel
theorem r2_11_14 : cert5.stepRow 2 11 14 = true := by decide +kernel
theorem r2_11_15 : cert5.stepRow 2 11 15 = true := by decide +kernel
theorem r2_11_16 : cert5.stepRow 2 11 16 = true := by decide +kernel
theorem r2_11_17 : cert5.stepRow 2 11 17 = true := by decide +kernel
theorem r2_11_18 : cert5.stepRow 2 11 18 = true := by decide +kernel

theorem r2_11 : ∀ b, b ≤ 18 → cert5.stepRow 2 11 b = true :=
  cover19 r2_11_0 r2_11_1 r2_11_2 r2_11_3 r2_11_4 r2_11_5 r2_11_6 r2_11_7 r2_11_8 r2_11_9 r2_11_10 r2_11_11 r2_11_12 r2_11_13 r2_11_14 r2_11_15 r2_11_16 r2_11_17 r2_11_18

end Agent113.FiveLayer
