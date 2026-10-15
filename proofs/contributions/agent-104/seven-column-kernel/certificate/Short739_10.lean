import Rank739
import ShortChecksBase
namespace SevenColumn.Certificate739
open Certificate ShortBoundary
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem shortAt10 : ShortAt ranks 10 := by decide +kernel
#print axioms shortAt10
end SevenColumn.Certificate739
