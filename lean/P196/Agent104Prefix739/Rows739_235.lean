import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0940 : leaf0940.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0941 : leaf0941.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0942 : leaf0942.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0943 : leaf0943.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0940 : checkRow ranks (fastLongPred 7) [12,10,16,17,10,8,15] 3 = true := by decide +kernel
theorem row_branch0941 : checkRow ranks (fastLongPred 7) [12,10,16,8,10,17,8] 3 = true := by decide +kernel
theorem row_branch0942 : checkRow ranks (fastLongPred 7) [12,17,6,3,0,12,8] 9 = true := by decide +kernel
theorem row_branch0943 : checkRow ranks (fastLongPred 7) [12,17,6,3,6,12,6] 3 = true := by decide +kernel
end SevenColumn.Certificate739
