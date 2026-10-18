import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0892 : leaf0892.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0893 : leaf0893.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0894 : leaf0894.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0895 : leaf0895.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0892 : checkRow ranks (fastLongPred 7) [12,8,6,12,0,11,8] 1 = true := by decide +kernel
theorem row_branch0893 : checkRow ranks (fastLongPred 7) [12,10,5,7,7,12,2] 3 = true := by decide +kernel
theorem row_branch0894 : checkRow ranks (fastLongPred 7) [12,10,5,7,9,8,6] 6 = true := by decide +kernel
theorem row_branch0895 : checkRow ranks (fastLongPred 7) [12,10,5,7,7,18,5] 3 = true := by decide +kernel
end SevenColumn.Certificate739
