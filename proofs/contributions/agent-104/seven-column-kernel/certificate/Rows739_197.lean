import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0788 : leaf0788.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0789 : leaf0789.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0790 : leaf0790.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0791 : leaf0791.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0788 : checkRow ranks (fastLongPred 7) [12,1,5,16,18,5,14] 1 = true := by decide +kernel
theorem row_branch0789 : checkRow ranks (fastLongPred 7) [12,1,7,8,1,8,11] 3 = true := by decide +kernel
theorem row_branch0790 : checkRow ranks (fastLongPred 7) [12,1,5,16,18,14,16] 1 = true := by decide +kernel
theorem row_branch0791 : checkRow ranks (fastLongPred 7) [12,1,7,17,10,17,8] 1 = true := by decide +kernel
end SevenColumn.Certificate739
