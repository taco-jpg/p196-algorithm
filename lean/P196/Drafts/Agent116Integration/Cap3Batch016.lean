import P196.Drafts.Agent116Cap3Kernel.Cap3Base
namespace P196.Agent116.Cap3
set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem batch016 : BatchCheck 2048 128 := by
  decide +kernel
#print axioms batch016
end P196.Agent116.Cap3
