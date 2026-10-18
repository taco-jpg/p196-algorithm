import P196.Agent113FiveLayer.FiveLayerData

/-! Generated (Agent #113): kernel checks of closure rows (layer 1, s0 = 6). -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem r1_6_0 : cert5.stepRow 1 6 0 = true := by decide +kernel
theorem r1_6_1 : cert5.stepRow 1 6 1 = true := by decide +kernel
theorem r1_6_2 : cert5.stepRow 1 6 2 = true := by decide +kernel
theorem r1_6_3 : cert5.stepRow 1 6 3 = true := by decide +kernel
theorem r1_6_4 : cert5.stepRow 1 6 4 = true := by decide +kernel
theorem r1_6_5 : cert5.stepRow 1 6 5 = true := by decide +kernel
theorem r1_6_6 : cert5.stepRow 1 6 6 = true := by decide +kernel
theorem r1_6_7 : cert5.stepRow 1 6 7 = true := by decide +kernel
theorem r1_6_8 : cert5.stepRow 1 6 8 = true := by decide +kernel
theorem r1_6_9 : cert5.stepRow 1 6 9 = true := by decide +kernel
theorem r1_6_10 : cert5.stepRow 1 6 10 = true := by decide +kernel
theorem r1_6_11 : cert5.stepRow 1 6 11 = true := by decide +kernel
theorem r1_6_12 : cert5.stepRow 1 6 12 = true := by decide +kernel
theorem r1_6_13 : cert5.stepRow 1 6 13 = true := by decide +kernel
theorem r1_6_14 : cert5.stepRow 1 6 14 = true := by decide +kernel
theorem r1_6_15 : cert5.stepRow 1 6 15 = true := by decide +kernel
theorem r1_6_16 : cert5.stepRow 1 6 16 = true := by decide +kernel
theorem r1_6_17 : cert5.stepRow 1 6 17 = true := by decide +kernel
theorem r1_6_18 : cert5.stepRow 1 6 18 = true := by decide +kernel

theorem r1_6 : ∀ b, b ≤ 18 → cert5.stepRow 1 6 b = true :=
  cover19 r1_6_0 r1_6_1 r1_6_2 r1_6_3 r1_6_4 r1_6_5 r1_6_6 r1_6_7 r1_6_8 r1_6_9 r1_6_10 r1_6_11 r1_6_12 r1_6_13 r1_6_14 r1_6_15 r1_6_16 r1_6_17 r1_6_18

end Agent113.FiveLayer
