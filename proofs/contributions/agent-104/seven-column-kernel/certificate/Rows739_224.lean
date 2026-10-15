import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0896 : leaf0896.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0897 : leaf0897.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0898 : leaf0898.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0899 : leaf0899.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0896 : checkRow ranks (fastLongPred 7) [12,10,5,7,16,6,17] 3 = true := by decide +kernel
theorem row_branch0897 : checkRow ranks (fastLongPred 7) [12,10,5,7,16,18,18] 1 = true := by decide +kernel
theorem row_branch0898 : checkRow ranks (fastLongPred 7) [12,10,5,7,16,12,14] 3 = true := by decide +kernel
theorem row_branch0899 : checkRow ranks (fastLongPred 7) [12,10,5,7,16,0,15] 3 = true := by decide +kernel
end SevenColumn.Certificate739
