import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0016 : leaf0016.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0017 : leaf0017.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0018 : leaf0018.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0019 : leaf0019.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0016 : checkRow ranks (fastLongPred 7) [1,10,2,13,6,15,11] 0 = true := by decide +kernel
theorem row_branch0017 : checkRow ranks (fastLongPred 7) [1,10,2,13,6,7,15] 0 = true := by decide +kernel
theorem row_branch0018 : checkRow ranks (fastLongPred 7) [1,10,2,14,7,15,10] 0 = true := by decide +kernel
theorem row_branch0019 : checkRow ranks (fastLongPred 7) [1,10,3,15,10,18,14] 0 = true := by decide +kernel
end SevenColumn.Certificate739
