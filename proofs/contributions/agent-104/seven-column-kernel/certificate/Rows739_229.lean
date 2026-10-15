import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0916 : leaf0916.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0917 : leaf0917.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0918 : leaf0918.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0919 : leaf0919.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0916 : checkRow ranks (fastLongPred 7) [12,10,14,7,7,0,8] 3 = true := by decide +kernel
theorem row_branch0917 : checkRow ranks (fastLongPred 7) [12,10,14,5,13,14,6] 3 = true := by decide +kernel
theorem row_branch0918 : checkRow ranks (fastLongPred 7) [12,10,14,7,7,12,6] 3 = true := by decide +kernel
theorem row_branch0919 : checkRow ranks (fastLongPred 7) [12,10,14,7,9,8,12] 6 = true := by decide +kernel
end SevenColumn.Certificate739
