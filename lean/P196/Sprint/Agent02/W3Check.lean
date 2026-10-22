import P196.Sprint.Agent02.W3Data
import P196.Agent124ForwardInvariant.A124W3Tree

/-! Kernel checks of the width-3 trees of `W3Data` (sprint agent 02). -/

namespace Sprint.Agent02.W3

open Agent124.CodeCert Agent124.FwdW3 Sprint.Agent02

set_option maxRecDepth 100000

set_option maxHeartbeats 0 in
theorem fromT_check : allNodes (fromOK 3 fromT W0) fromT = true := by
  decide +kernel

set_option maxHeartbeats 0 in
theorem toT_check : allNodes (toOK 3 toT W0) toT = true := by
  decide +kernel

set_option maxHeartbeats 0 in
theorem fset_in_fromT : keysIn fromT fset = true := by
  decide +kernel

set_option maxHeartbeats 0 in
theorem fset_in_toT : keysIn toT fset = true := by
  decide +kernel

set_option maxHeartbeats 0 in
theorem U0_in_fromT : (lookupC fromT U0).isSome = true := by
  decide +kernel

set_option maxHeartbeats 0 in
theorem U0_edge : Agent117.edgeOK (decode W0) (decode U0) E0 = true := by
  decide +kernel

theorem W0_word : decode W0 = [8, 8, 13] := by decide +kernel

theorem fromT_ok : fromT.All (fun c v => fromOK 3 fromT W0 c v = true) :=
  allNodes_sound fromT_check

theorem toT_ok : toT.All (fun c v => toOK 3 toT W0 c v = true) :=
  allNodes_sound toT_check

end Sprint.Agent02.W3

#print axioms Sprint.Agent02.W3.fromT_ok
#print axioms Sprint.Agent02.W3.toT_ok
#print axioms Sprint.Agent02.W3.fset_in_fromT
#print axioms Sprint.Agent02.W3.fset_in_toT
#print axioms Sprint.Agent02.W3.U0_edge
