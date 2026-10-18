import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0948 : leaf0948.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0949 : leaf0949.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0950 : leaf0950.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0951 : leaf0951.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0948 : checkRow ranks (fastLongPred 7) [12,17,6,12,0,10,2] 3 = true := by decide +kernel
theorem row_branch0949 : checkRow ranks (fastLongPred 7) [12,17,6,12,9,2,11] 3 = true := by decide +kernel
theorem row_branch0950 : checkRow ranks (fastLongPred 7) [12,17,6,12,10,1,18] 1 = true := by decide +kernel
theorem row_branch0951 : checkRow ranks (fastLongPred 7) [12,17,6,12,9,11,17] 9 = true := by decide +kernel
end SevenColumn.Certificate739
