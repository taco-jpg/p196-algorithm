import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0464 : leaf0464.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0465 : leaf0465.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0466 : leaf0466.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0467 : leaf0467.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0464 : checkRow ranks (fastLongPred 7) [6,4,11,17,13,16,14] 2 = true := by decide +kernel
theorem row_branch0465 : checkRow ranks (fastLongPred 7) [6,4,11,13,14,17,3] 2 = true := by decide +kernel
theorem row_branch0466 : checkRow ranks (fastLongPred 7) [6,4,11,13,9,18,14] 2 = true := by decide +kernel
theorem row_branch0467 : checkRow ranks (fastLongPred 7) [6,4,11,18,4,9,1] 0 = true := by decide +kernel
end SevenColumn.Certificate739
