import Agent1PeriodicOuter
import Agent1PeriodicCatalogOrder

/-! Exact original product certificate, split into phase blocks for kernel checking.
No label, ordering, node or edge changes. Arbitrary paths are not realized. -/
set_option maxRecDepth 16384
set_option maxHeartbeats 16000000
namespace Agent1.Periodic
open Agent8

private def outerNodes00 : List OuterNode := [
  ([0,0,0,0],1),
  ([0,0,0,0],2),
  ([0,0,0,0],3),
  ([0,0,0,0],4),
  ([0,0,0,0],5),
  ([0,0,0,0],6),
  ([0,0,0,0],7),
  ([0,0,0,0],8),
  ([0,0,0,0],9),
  ([0,0,0,0],10),
  ([0,0,0,0],11),
  ([0,0,0,0],12),
  ([0,0,0,0],13),
  ([0,0,0,0],14),
  ([0,0,0,0],15),
  ([0,0,0,0],16),
  ([0,0,0,0],17),
  ([0,0,0,0],18)
]

private def outerEdges00 : List OuterEdge := [
  ⟨([0,0,0,0],1), 0, none, ([0,0,0,0],2)⟩,
  ⟨([0,0,0,0],1), 0, none, ([0,0,0,0],3)⟩,
  ⟨([0,0,0,0],2), 0, none, ([0,0,0,0],4)⟩,
  ⟨([0,0,0,0],2), 0, none, ([0,0,0,0],5)⟩,
  ⟨([0,0,0,0],3), 0, none, ([0,0,0,0],6)⟩,
  ⟨([0,0,0,0],3), 0, none, ([0,0,0,0],7)⟩,
  ⟨([0,0,0,0],4), 0, none, ([0,0,0,0],8)⟩,
  ⟨([0,0,0,0],4), 0, none, ([0,0,0,0],9)⟩,
  ⟨([0,0,0,0],5), 0, none, ([0,0,0,0],10)⟩,
  ⟨([0,0,0,0],5), 0, none, ([0,0,0,0],11)⟩,
  ⟨([0,0,0,0],6), 0, none, ([0,0,0,0],12)⟩,
  ⟨([0,0,0,0],6), 0, none, ([0,0,0,0],13)⟩,
  ⟨([0,0,0,0],7), 0, none, ([0,0,0,0],14)⟩,
  ⟨([0,0,0,0],7), 0, none, ([0,0,0,0],15)⟩,
  ⟨([0,0,0,0],8), 0, none, ([0,0,0,0],16)⟩,
  ⟨([0,0,0,0],8), 0, none, ([0,0,0,0],17)⟩,
  ⟨([0,0,0,0],9), 0, none, ([0,0,0,0],18)⟩,
  ⟨([0,0,0,0],9), 1, none, ([0,0,0,0],10)⟩,
  ⟨([0,0,0,0],10), 1, none, ([0,0,0,0],1)⟩,
  ⟨([0,0,0,0],11), 1, none, ([0,0,0,0],2)⟩,
  ⟨([0,0,0,0],12), 1, none, ([0,0,0,0],3)⟩,
  ⟨([0,0,0,0],13), 1, none, ([0,0,0,0],4)⟩,
  ⟨([0,0,0,0],14), 1, none, ([0,0,0,0],5)⟩,
  ⟨([0,0,0,0],15), 1, none, ([0,0,0,0],6)⟩,
  ⟨([0,0,0,0],16), 1, none, ([0,0,0,0],7)⟩,
  ⟨([0,0,0,0],17), 1, none, ([0,0,0,0],8)⟩,
  ⟨([0,0,0,0],18), 1, none, ([0,0,0,0],9)⟩
]

#eval do
  let o ← IO.getStdout
  o.putStrLn "BLOCK00_DEFS_DONE"
  o.flush

private theorem outerBlockSpec00 : outerEdges00 = outerNodes00.flatMap outerOutputs := by rfl


#eval do
  let o ← IO.getStdout
  o.putStrLn "BLOCK00_SPEC_DONE"
  o.flush
end Agent1.Periodic
