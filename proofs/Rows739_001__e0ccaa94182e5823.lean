import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0004 : leaf0004.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0005 : leaf0005.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0006 : leaf0006.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0007 : leaf0007.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0004 : checkRow ranks (fastLongPred 7) [1,5,17,6,9,10,0] 0 = true := by decide +kernel
theorem row_branch0005 : checkRow ranks (fastLongPred 7) [1,4,16,4,4,8,6] 0 = true := by decide +kernel
theorem row_branch0006 : checkRow ranks (fastLongPred 7) [1,2,9,3,11,18,12] 0 = true := by decide +kernel
theorem row_branch0007 : checkRow ranks (fastLongPred 7) [1,7,4,9,15,12,10] 0 = true := by decide +kernel
end SevenColumn.Certificate739
