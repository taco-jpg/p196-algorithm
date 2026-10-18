import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0912 : leaf0912.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0913 : leaf0913.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0914 : leaf0914.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0915 : leaf0915.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0912 : checkRow ranks (fastLongPred 7) [12,10,7,17,10,8,10] 3 = true := by decide +kernel
theorem row_branch0913 : checkRow ranks (fastLongPred 7) [12,10,7,8,10,17,3] 2 = true := by decide +kernel
theorem row_branch0914 : checkRow ranks (fastLongPred 7) [12,10,5,16,18,14,2] 6 = true := by decide +kernel
theorem row_branch0915 : checkRow ranks (fastLongPred 7) [12,10,14,5,4,17,9] 6 = true := by decide +kernel
end SevenColumn.Certificate739
