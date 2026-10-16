import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0008 : leaf0008.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0009 : leaf0009.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0010 : leaf0010.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0011 : leaf0011.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0008 : checkRow ranks (fastLongPred 7) [1,7,4,14,16,13,15] 0 = true := by decide +kernel
theorem row_branch0009 : checkRow ranks (fastLongPred 7) [1,7,4,9,18,8,8] 0 = true := by decide +kernel
theorem row_branch0010 : checkRow ranks (fastLongPred 7) [1,8,7,15,2,6,17] 0 = true := by decide +kernel
theorem row_branch0011 : checkRow ranks (fastLongPred 7) [1,9,6,1,14,18,12] 0 = true := by decide +kernel
end SevenColumn.Certificate739
