import P196.Agent113FiveLayer.FiveLayerR0A1
import P196.Agent113FiveLayer.FiveLayerR0A2
import P196.Agent113FiveLayer.FiveLayerR0A3
import P196.Agent113FiveLayer.FiveLayerR0A4
import P196.Agent113FiveLayer.FiveLayerR0A5
import P196.Agent113FiveLayer.FiveLayerR0A6
import P196.Agent113FiveLayer.FiveLayerR0A7
import P196.Agent113FiveLayer.FiveLayerR0A8
import P196.Agent113FiveLayer.FiveLayerR0A9
import P196.Agent113FiveLayer.FiveLayerR0A10
import P196.Agent113FiveLayer.FiveLayerR0A11
import P196.Agent113FiveLayer.FiveLayerR0A12
import P196.Agent113FiveLayer.FiveLayerR0A13
import P196.Agent113FiveLayer.FiveLayerR0A14
import P196.Agent113FiveLayer.FiveLayerR0A15
import P196.Agent113FiveLayer.FiveLayerR0A16
import P196.Agent113FiveLayer.FiveLayerR0A17
import P196.Agent113FiveLayer.FiveLayerR0A18

/-! Generated (Agent #113): all closure rows of layer 0. -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem rows0 : ∀ a, 1 ≤ a → a ≤ 18 → ∀ b, b ≤ 18 → cert5.stepRow 0 a b = true :=
  cover18 (P := fun a => ∀ b, b ≤ 18 → cert5.stepRow 0 a b = true) r0_1 r0_2 r0_3 r0_4 r0_5 r0_6 r0_7 r0_8 r0_9 r0_10 r0_11 r0_12 r0_13 r0_14 r0_15 r0_16 r0_17 r0_18

end Agent113.FiveLayer
