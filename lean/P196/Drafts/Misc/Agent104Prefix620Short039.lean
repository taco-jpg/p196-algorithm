/- Agent #104 finite-list partition of the frozen 620 instance.
Agent #124's original semantic checker and enumerations are unchanged. -/
import P196.Drafts.Misc.Agent104Prefix620DataTree
import P196.Drafts.Misc.Agent104Prefix620DataShortWords

namespace Agent104.Prefix620
open Agent124.CodeCert Agent124.PrefixK Agent124.PrefixR
set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem short_ok039 : short_block039.all (shortOKC ranks) = true := by
  decide +kernel

end Agent104.Prefix620
