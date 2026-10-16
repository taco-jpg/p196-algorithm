import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0784 : leaf0784.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0785 : leaf0785.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0786 : leaf0786.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0787 : leaf0787.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0784 : checkRow ranks (fastLongPred 7) [12,1,5,16,7,15,17] 3 = true := by decide +kernel
theorem row_branch0785 : checkRow ranks (fastLongPred 7) [12,1,5,16,16,7,13] 3 = true := by decide +kernel
theorem row_branch0786 : checkRow ranks (fastLongPred 7) [12,1,5,16,16,2,14] 3 = true := by decide +kernel
theorem row_branch0787 : checkRow ranks (fastLongPred 7) [12,1,5,16,7,9,12] 3 = true := by decide +kernel
end SevenColumn.Certificate739
