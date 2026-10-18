import P196.Agent113FiveLayer.FiveLayerR4A1
import P196.Agent113FiveLayer.FiveLayerR4A2
import P196.Agent113FiveLayer.FiveLayerR4A3
import P196.Agent113FiveLayer.FiveLayerR4A4
import P196.Agent113FiveLayer.FiveLayerR4A5
import P196.Agent113FiveLayer.FiveLayerR4A6
import P196.Agent113FiveLayer.FiveLayerR4A7
import P196.Agent113FiveLayer.FiveLayerR4A8
import P196.Agent113FiveLayer.FiveLayerR4A9
import P196.Agent113FiveLayer.FiveLayerR4A10
import P196.Agent113FiveLayer.FiveLayerR4A11
import P196.Agent113FiveLayer.FiveLayerR4A12
import P196.Agent113FiveLayer.FiveLayerR4A13
import P196.Agent113FiveLayer.FiveLayerR4A14
import P196.Agent113FiveLayer.FiveLayerR4A15
import P196.Agent113FiveLayer.FiveLayerR4A16
import P196.Agent113FiveLayer.FiveLayerR4A17
import P196.Agent113FiveLayer.FiveLayerR4A18

/-! Generated (Agent #113): all closure rows of layer 4. -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem rows4 : ∀ a, 1 ≤ a → a ≤ 18 → ∀ b, b ≤ 18 → cert5.stepRow 4 a b = true :=
  cover18 (P := fun a => ∀ b, b ≤ 18 → cert5.stepRow 4 a b = true) r4_1 r4_2 r4_3 r4_4 r4_5 r4_6 r4_7 r4_8 r4_9 r4_10 r4_11 r4_12 r4_13 r4_14 r4_15 r4_16 r4_17 r4_18

end Agent113.FiveLayer
