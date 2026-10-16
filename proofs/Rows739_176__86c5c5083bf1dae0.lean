import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0704 : leaf0704.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0705 : leaf0705.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0706 : leaf0706.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0707 : leaf0707.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0704 : checkRow ranks (fastLongPred 7) [7,4,6,10,16,3,11] 2 = true := by decide +kernel
theorem row_branch0705 : checkRow ranks (fastLongPred 7) [7,4,6,15,11,18,14] 2 = true := by decide +kernel
theorem row_branch0706 : checkRow ranks (fastLongPred 7) [7,4,6,15,4,7,14] 2 = true := by decide +kernel
theorem row_branch0707 : checkRow ranks (fastLongPred 7) [7,4,4,6,4,4,12] 2 = true := by decide +kernel
end SevenColumn.Certificate739
