import FiveLayerR2A1
import FiveLayerR2A2
import FiveLayerR2A3
import FiveLayerR2A4
import FiveLayerR2A5
import FiveLayerR2A6
import FiveLayerR2A7
import FiveLayerR2A8
import FiveLayerR2A9
import FiveLayerR2A10
import FiveLayerR2A11
import FiveLayerR2A12
import FiveLayerR2A13
import FiveLayerR2A14
import FiveLayerR2A15
import FiveLayerR2A16
import FiveLayerR2A17
import FiveLayerR2A18

/-! Generated (Agent #113): all closure rows of layer 2. -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem rows2 : ∀ a, 1 ≤ a → a ≤ 18 → ∀ b, b ≤ 18 → cert5.stepRow 2 a b = true :=
  cover18 (P := fun a => ∀ b, b ≤ 18 → cert5.stepRow 2 a b = true) r2_1 r2_2 r2_3 r2_4 r2_5 r2_6 r2_7 r2_8 r2_9 r2_10 r2_11 r2_12 r2_13 r2_14 r2_15 r2_16 r2_17 r2_18

end Agent113.FiveLayer
