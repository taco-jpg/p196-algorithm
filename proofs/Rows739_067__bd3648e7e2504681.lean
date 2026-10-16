import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0268 : leaf0268.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0269 : leaf0269.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0270 : leaf0270.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0271 : leaf0271.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0268 : checkRow ranks (fastLongPred 7) [3,11,14,1,3,3,3] 1 = true := by decide +kernel
theorem row_branch0269 : checkRow ranks (fastLongPred 7) [3,11,14,1,1,3,10] 1 = true := by decide +kernel
theorem row_branch0270 : checkRow ranks (fastLongPred 7) [3,11,14,1,10,2,11] 1 = true := by decide +kernel
theorem row_branch0271 : checkRow ranks (fastLongPred 7) [3,11,14,1,11,3,0] 1 = true := by decide +kernel
end SevenColumn.Certificate739
