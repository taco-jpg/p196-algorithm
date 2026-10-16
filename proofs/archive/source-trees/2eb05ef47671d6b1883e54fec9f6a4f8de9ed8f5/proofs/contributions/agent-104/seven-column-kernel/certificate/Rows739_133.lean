import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0532 : leaf0532.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0533 : leaf0533.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0534 : leaf0534.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0535 : leaf0535.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0532 : checkRow ranks (fastLongPred 7) [7,3,9,0,3,6,4] 0 = true := by decide +kernel
theorem row_branch0533 : checkRow ranks (fastLongPred 7) [7,3,9,0,6,5,0] 0 = true := by decide +kernel
theorem row_branch0534 : checkRow ranks (fastLongPred 7) [7,3,9,0,7,6,4] 0 = true := by decide +kernel
theorem row_branch0535 : checkRow ranks (fastLongPred 7) [7,3,9,0,7,0,7] 0 = true := by decide +kernel
end SevenColumn.Certificate739
