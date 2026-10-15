import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0012 : leaf0012.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0013 : leaf0013.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0014 : leaf0014.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0015 : leaf0015.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0012 : checkRow ranks (fastLongPred 7) [1,8,8,17,12,3,0] 0 = true := by decide +kernel
theorem row_branch0013 : checkRow ranks (fastLongPred 7) [1,7,5,18,11,7,4] 4 = true := by decide +kernel
theorem row_branch0014 : checkRow ranks (fastLongPred 7) [1,6,2,14,8,1,15] 0 = true := by decide +kernel
theorem row_branch0015 : checkRow ranks (fastLongPred 7) [1,10,2,13,5,5,18] 0 = true := by decide +kernel
end SevenColumn.Certificate739
