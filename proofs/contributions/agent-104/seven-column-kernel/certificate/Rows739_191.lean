import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0764 : leaf0764.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0765 : leaf0765.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0766 : leaf0766.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0767 : leaf0767.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0764 : checkRow ranks (fastLongPred 7) [7,4,2,5,9,16,8] 1 = true := by decide +kernel
theorem row_branch0765 : checkRow ranks (fastLongPred 7) [7,3,9,6,5,3,3] 2 = true := by decide +kernel
theorem row_branch0766 : checkRow ranks (fastLongPred 7) [11,18,14,18,0,0,3] 0 = true := by decide +kernel
theorem row_branch0767 : checkRow ranks (fastLongPred 7) [12,1,5,5,13,5,5] 3 = true := by decide +kernel
end SevenColumn.Certificate739
