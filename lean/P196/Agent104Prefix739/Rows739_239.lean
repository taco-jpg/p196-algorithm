import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0956 : leaf0956.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0957 : leaf0957.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0958 : leaf0958.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0959 : leaf0959.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0956 : checkRow ranks (fastLongPred 7) [12,17,15,3,0,3,8] 0 = true := by decide +kernel
theorem row_branch0957 : checkRow ranks (fastLongPred 7) [12,17,15,3,1,2,10] 3 = true := by decide +kernel
theorem row_branch0958 : checkRow ranks (fastLongPred 7) [12,17,15,3,0,12,9] 0 = true := by decide +kernel
theorem row_branch0959 : checkRow ranks (fastLongPred 7) [12,17,15,3,10,9,18] 2 = true := by decide +kernel
end SevenColumn.Certificate739
