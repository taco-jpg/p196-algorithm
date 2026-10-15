import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0508 : leaf0508.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0509 : leaf0509.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0510 : leaf0510.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0511 : leaf0511.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0508 : checkRow ranks (fastLongPred 7) [6,4,7,16,9,5,5] 2 = true := by decide +kernel
theorem row_branch0509 : checkRow ranks (fastLongPred 7) [5,9,0,0,8,18,2] 2 = true := by decide +kernel
theorem row_branch0510 : checkRow ranks (fastLongPred 7) [3,11,14,0,12,2,9] 1 = true := by decide +kernel
theorem row_branch0511 : checkRow ranks (fastLongPred 7) [6,8,13,5,9,15,10] 8 = true := by decide +kernel
end SevenColumn.Certificate739
