import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0672 : leaf0672.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0673 : leaf0673.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0674 : leaf0674.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0675 : leaf0675.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0672 : checkRow ranks (fastLongPred 7) [7,3,9,8,6,4,8] 2 = true := by decide +kernel
theorem row_branch0673 : checkRow ranks (fastLongPred 7) [7,3,9,8,7,6,2] 2 = true := by decide +kernel
theorem row_branch0674 : checkRow ranks (fastLongPred 7) [7,3,9,8,7,0,5] 2 = true := by decide +kernel
theorem row_branch0675 : checkRow ranks (fastLongPred 7) [7,3,9,8,5,9,1] 1 = true := by decide +kernel
end SevenColumn.Certificate739
