import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 2, s0 = 12). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r2_12_0 : cert5.stepRow 2 12 0 = true := by decide +kernel
theorem r2_12_1 : cert5.stepRow 2 12 1 = true := by decide +kernel
theorem r2_12_2 : cert5.stepRow 2 12 2 = true := by decide +kernel
theorem r2_12_3 : cert5.stepRow 2 12 3 = true := by decide +kernel
theorem r2_12_4 : cert5.stepRow 2 12 4 = true := by decide +kernel
theorem r2_12_5 : cert5.stepRow 2 12 5 = true := by decide +kernel
theorem r2_12_6 : cert5.stepRow 2 12 6 = true := by decide +kernel
theorem r2_12_7 : cert5.stepRow 2 12 7 = true := by decide +kernel
theorem r2_12_8 : cert5.stepRow 2 12 8 = true := by decide +kernel
theorem r2_12_9 : cert5.stepRow 2 12 9 = true := by decide +kernel
theorem r2_12_10 : cert5.stepRow 2 12 10 = true := by decide +kernel
theorem r2_12_11 : cert5.stepRow 2 12 11 = true := by decide +kernel
theorem r2_12_12 : cert5.stepRow 2 12 12 = true := by decide +kernel
theorem r2_12_13 : cert5.stepRow 2 12 13 = true := by decide +kernel
theorem r2_12_14 : cert5.stepRow 2 12 14 = true := by decide +kernel
theorem r2_12_15 : cert5.stepRow 2 12 15 = true := by decide +kernel
theorem r2_12_16 : cert5.stepRow 2 12 16 = true := by decide +kernel
theorem r2_12_17 : cert5.stepRow 2 12 17 = true := by decide +kernel
theorem r2_12_18 : cert5.stepRow 2 12 18 = true := by decide +kernel

theorem r2_12 : ∀ b, b ≤ 18 → cert5.stepRow 2 12 b = true :=
  cover19 r2_12_0 r2_12_1 r2_12_2 r2_12_3 r2_12_4 r2_12_5 r2_12_6 r2_12_7 r2_12_8 r2_12_9 r2_12_10 r2_12_11 r2_12_12 r2_12_13 r2_12_14 r2_12_15 r2_12_16 r2_12_17 r2_12_18

end Agent113.FiveLayer
