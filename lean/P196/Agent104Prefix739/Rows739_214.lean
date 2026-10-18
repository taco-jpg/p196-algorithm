import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0856 : leaf0856.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0857 : leaf0857.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0858 : leaf0858.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0859 : leaf0859.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0856 : checkRow ranks (fastLongPred 7) [12,9,1,7,13,8,4] 3 = true := by decide +kernel
theorem row_branch0857 : checkRow ranks (fastLongPred 7) [12,9,1,7,6,9,14] 3 = true := by decide +kernel
theorem row_branch0858 : checkRow ranks (fastLongPred 7) [12,9,1,5,13,2,16] 3 = true := by decide +kernel
theorem row_branch0859 : checkRow ranks (fastLongPred 7) [12,8,15,12,9,3,18] 3 = true := by decide +kernel
end SevenColumn.Certificate739
