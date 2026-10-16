import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0848 : leaf0848.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0849 : leaf0849.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0850 : leaf0850.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0851 : leaf0851.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0848 : checkRow ranks (fastLongPred 7) [12,9,1,5,11,0,18] 3 = true := by decide +kernel
theorem row_branch0849 : checkRow ranks (fastLongPred 7) [12,9,1,5,4,14,4] 3 = true := by decide +kernel
theorem row_branch0850 : checkRow ranks (fastLongPred 7) [12,9,1,5,1,18,16] 3 = true := by decide +kernel
theorem row_branch0851 : checkRow ranks (fastLongPred 7) [12,9,1,5,13,14,4] 3 = true := by decide +kernel
end SevenColumn.Certificate739
