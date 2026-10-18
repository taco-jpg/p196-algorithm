import P196.Agent113FiveLayer.FiveLayerR3A1
import P196.Agent113FiveLayer.FiveLayerR3A2
import P196.Agent113FiveLayer.FiveLayerR3A3
import P196.Agent113FiveLayer.FiveLayerR3A4
import P196.Agent113FiveLayer.FiveLayerR3A5
import P196.Agent113FiveLayer.FiveLayerR3A6
import P196.Agent113FiveLayer.FiveLayerR3A7
import P196.Agent113FiveLayer.FiveLayerR3A8
import P196.Agent113FiveLayer.FiveLayerR3A9
import P196.Agent113FiveLayer.FiveLayerR3A10
import P196.Agent113FiveLayer.FiveLayerR3A11
import P196.Agent113FiveLayer.FiveLayerR3A12
import P196.Agent113FiveLayer.FiveLayerR3A13
import P196.Agent113FiveLayer.FiveLayerR3A14
import P196.Agent113FiveLayer.FiveLayerR3A15
import P196.Agent113FiveLayer.FiveLayerR3A16
import P196.Agent113FiveLayer.FiveLayerR3A17
import P196.Agent113FiveLayer.FiveLayerR3A18

/-! Generated (Agent #113): all closure rows of layer 3. -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem rows3 : ∀ a, 1 ≤ a → a ≤ 18 → ∀ b, b ≤ 18 → cert5.stepRow 3 a b = true :=
  cover18 (P := fun a => ∀ b, b ≤ 18 → cert5.stepRow 3 a b = true) r3_1 r3_2 r3_3 r3_4 r3_5 r3_6 r3_7 r3_8 r3_9 r3_10 r3_11 r3_12 r3_13 r3_14 r3_15 r3_16 r3_17 r3_18

end Agent113.FiveLayer
