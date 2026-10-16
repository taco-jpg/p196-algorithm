import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0180 : leaf0180.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0181 : leaf0181.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0182 : leaf0182.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0183 : leaf0183.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0180 : checkRow ranks (fastLongPred 7) [3,2,1,13,1,0,18] 1 = true := by decide +kernel
theorem row_branch0181 : checkRow ranks (fastLongPred 7) [3,2,3,15,14,4,12] 1 = true := by decide +kernel
theorem row_branch0182 : checkRow ranks (fastLongPred 7) [3,2,1,13,1,18,6] 1 = true := by decide +kernel
theorem row_branch0183 : checkRow ranks (fastLongPred 7) [3,2,3,15,16,16,18] 0 = true := by decide +kernel
end SevenColumn.Certificate739
