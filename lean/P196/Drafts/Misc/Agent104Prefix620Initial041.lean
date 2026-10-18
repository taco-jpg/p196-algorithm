/- Agent #104 finite-list partition of the frozen 620 instance.
Agent #124's original semantic checker and enumerations are unchanged. -/
import P196.Drafts.Misc.Agent104Prefix620DataTree
import P196.Drafts.Misc.Agent104Prefix620DataInitialWords

namespace Agent104.Prefix620
open Agent124.CodeCert Agent124.PrefixK Agent124.PrefixR
set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem initial_ok041 : initial_block041.all (initOKC ranks 11) = true := by
  decide +kernel

end Agent104.Prefix620
