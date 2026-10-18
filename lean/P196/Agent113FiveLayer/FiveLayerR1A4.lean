import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 1, s0 = 4). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r1_4_0 : cert5.stepRow 1 4 0 = true := by decide +kernel
theorem r1_4_1 : cert5.stepRow 1 4 1 = true := by decide +kernel
theorem r1_4_2 : cert5.stepRow 1 4 2 = true := by decide +kernel
theorem r1_4_3 : cert5.stepRow 1 4 3 = true := by decide +kernel
theorem r1_4_4 : cert5.stepRow 1 4 4 = true := by decide +kernel
theorem r1_4_5 : cert5.stepRow 1 4 5 = true := by decide +kernel
theorem r1_4_6 : cert5.stepRow 1 4 6 = true := by decide +kernel
theorem r1_4_7 : cert5.stepRow 1 4 7 = true := by decide +kernel
theorem r1_4_8 : cert5.stepRow 1 4 8 = true := by decide +kernel
theorem r1_4_9 : cert5.stepRow 1 4 9 = true := by decide +kernel
theorem r1_4_10 : cert5.stepRow 1 4 10 = true := by decide +kernel
theorem r1_4_11 : cert5.stepRow 1 4 11 = true := by decide +kernel
theorem r1_4_12 : cert5.stepRow 1 4 12 = true := by decide +kernel
theorem r1_4_13 : cert5.stepRow 1 4 13 = true := by decide +kernel
theorem r1_4_14 : cert5.stepRow 1 4 14 = true := by decide +kernel
theorem r1_4_15 : cert5.stepRow 1 4 15 = true := by decide +kernel
theorem r1_4_16 : cert5.stepRow 1 4 16 = true := by decide +kernel
theorem r1_4_17 : cert5.stepRow 1 4 17 = true := by decide +kernel
theorem r1_4_18 : cert5.stepRow 1 4 18 = true := by decide +kernel

theorem r1_4 : ∀ b, b ≤ 18 → cert5.stepRow 1 4 b = true :=
  cover19 r1_4_0 r1_4_1 r1_4_2 r1_4_3 r1_4_4 r1_4_5 r1_4_6 r1_4_7 r1_4_8 r1_4_9 r1_4_10 r1_4_11 r1_4_12 r1_4_13 r1_4_14 r1_4_15 r1_4_16 r1_4_17 r1_4_18

end Agent113.FiveLayer
