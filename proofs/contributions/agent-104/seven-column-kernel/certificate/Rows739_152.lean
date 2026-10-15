import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0608 : leaf0608.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0609 : leaf0609.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0610 : leaf0610.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0611 : leaf0611.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0608 : checkRow ranks (fastLongPred 7) [7,3,9,4,9,9,1] 2 = true := by decide +kernel
theorem row_branch0609 : checkRow ranks (fastLongPred 7) [7,3,9,5,1,0,5] 2 = true := by decide +kernel
theorem row_branch0610 : checkRow ranks (fastLongPred 7) [7,3,9,5,0,4,8] 2 = true := by decide +kernel
theorem row_branch0611 : checkRow ranks (fastLongPred 7) [7,3,9,4,9,3,4] 2 = true := by decide +kernel
end SevenColumn.Certificate739
