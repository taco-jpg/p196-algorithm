import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0960 : leaf0960.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0961 : leaf0961.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0962 : leaf0962.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0963 : leaf0963.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0960 : checkRow ranks (fastLongPred 7) [12,17,15,12,0,10,2] 3 = true := by decide +kernel
theorem row_branch0961 : checkRow ranks (fastLongPred 7) [12,17,15,12,0,1,1] 3 = true := by decide +kernel
theorem row_branch0962 : checkRow ranks (fastLongPred 7) [12,17,15,3,6,12,9] 3 = true := by decide +kernel
theorem row_branch0963 : checkRow ranks (fastLongPred 7) [12,17,15,12,1,11,10] 3 = true := by decide +kernel
end SevenColumn.Certificate739
