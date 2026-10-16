import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0200 : leaf0200.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0201 : leaf0201.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0202 : leaf0202.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0203 : leaf0203.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0200 : checkRow ranks (fastLongPred 7) [3,2,5,16,13,12,14] 1 = true := by decide +kernel
theorem row_branch0201 : checkRow ranks (fastLongPred 7) [3,2,5,18,16,5,15] 1 = true := by decide +kernel
theorem row_branch0202 : checkRow ranks (fastLongPred 7) [3,2,5,16,16,15,1] 1 = true := by decide +kernel
theorem row_branch0203 : checkRow ranks (fastLongPred 7) [3,2,5,8,18,16,10] 1 = true := by decide +kernel
end SevenColumn.Certificate739
