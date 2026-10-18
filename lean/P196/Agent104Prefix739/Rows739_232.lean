import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0928 : leaf0928.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0929 : leaf0929.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0930 : leaf0930.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0931 : leaf0931.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0928 : checkRow ranks (fastLongPred 7) [12,10,14,14,13,6,4] 3 = true := by decide +kernel
theorem row_branch0929 : checkRow ranks (fastLongPred 7) [12,10,14,14,4,14,7] 3 = true := by decide +kernel
theorem row_branch0930 : checkRow ranks (fastLongPred 7) [12,10,14,7,18,14,5] 0 = true := by decide +kernel
theorem row_branch0931 : checkRow ranks (fastLongPred 7) [12,10,14,16,7,2,18] 3 = true := by decide +kernel
end SevenColumn.Certificate739
