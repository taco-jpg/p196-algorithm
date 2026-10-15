import FiveLayerR1A1
import FiveLayerR1A2
import FiveLayerR1A3
import FiveLayerR1A4
import FiveLayerR1A5
import FiveLayerR1A6
import FiveLayerR1A7
import FiveLayerR1A8
import FiveLayerR1A9
import FiveLayerR1A10
import FiveLayerR1A11
import FiveLayerR1A12
import FiveLayerR1A13
import FiveLayerR1A14
import FiveLayerR1A15
import FiveLayerR1A16
import FiveLayerR1A17
import FiveLayerR1A18

/-! Generated (Agent #113): all closure rows of layer 1. -/

namespace Agent113.FiveLayer

open Agent113.FourColumn

theorem rows1 : ∀ a, 1 ≤ a → a ≤ 18 → ∀ b, b ≤ 18 → cert5.stepRow 1 a b = true :=
  cover18 (P := fun a => ∀ b, b ≤ 18 → cert5.stepRow 1 a b = true) r1_1 r1_2 r1_3 r1_4 r1_5 r1_6 r1_7 r1_8 r1_9 r1_10 r1_11 r1_12 r1_13 r1_14 r1_15 r1_16 r1_17 r1_18

end Agent113.FiveLayer
