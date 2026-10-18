import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0808 : leaf0808.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0809 : leaf0809.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0810 : leaf0810.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0811 : leaf0811.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0808 : checkRow ranks (fastLongPred 7) [12,1,14,16,7,4,6] 3 = true := by decide +kernel
theorem row_branch0809 : checkRow ranks (fastLongPred 7) [12,1,14,14,13,17,9] 1 = true := by decide +kernel
theorem row_branch0810 : checkRow ranks (fastLongPred 7) [12,1,14,14,4,15,9] 3 = true := by decide +kernel
theorem row_branch0811 : checkRow ranks (fastLongPred 7) [12,1,14,7,16,14,8] 3 = true := by decide +kernel
end SevenColumn.Certificate739
