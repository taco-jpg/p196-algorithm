import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0120 : leaf0120.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0121 : leaf0121.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0122 : leaf0122.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0123 : leaf0123.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0120 : checkRow ranks (fastLongPred 7) [1,15,18,16,11,12,3] 0 = true := by decide +kernel
theorem row_branch0121 : checkRow ranks (fastLongPred 7) [1,15,16,14,4,1,0] 0 = true := by decide +kernel
theorem row_branch0122 : checkRow ranks (fastLongPred 7) [1,15,16,14,1,0,10] 0 = true := by decide +kernel
theorem row_branch0123 : checkRow ranks (fastLongPred 7) [1,15,16,11,11,5,17] 0 = true := by decide +kernel
end SevenColumn.Certificate739
