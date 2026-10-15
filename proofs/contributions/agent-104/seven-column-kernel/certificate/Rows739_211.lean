import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0844 : leaf0844.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0845 : leaf0845.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0846 : leaf0846.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0847 : leaf0847.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0844 : checkRow ranks (fastLongPred 7) [12,8,15,12,9,13,6] 3 = true := by decide +kernel
theorem row_branch0845 : checkRow ranks (fastLongPred 7) [12,8,15,12,15,12,0] 3 = true := by decide +kernel
theorem row_branch0846 : checkRow ranks (fastLongPred 7) [12,8,15,12,10,3,7] 3 = true := by decide +kernel
theorem row_branch0847 : checkRow ranks (fastLongPred 7) [12,9,1,5,4,2,17] 3 = true := by decide +kernel
end SevenColumn.Certificate739
