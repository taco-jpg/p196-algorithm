import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0380 : leaf0380.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0381 : leaf0381.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0382 : leaf0382.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0383 : leaf0383.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0380 : checkRow ranks (fastLongPred 7) [3,12,2,17,10,6,12] 1 = true := by decide +kernel
theorem row_branch0381 : checkRow ranks (fastLongPred 7) [3,11,14,3,13,0,1] 1 = true := by decide +kernel
theorem row_branch0382 : checkRow ranks (fastLongPred 7) [5,9,0,0,14,17,17] 2 = true := by decide +kernel
theorem row_branch0383 : checkRow ranks (fastLongPred 7) [5,12,15,8,0,6,17] 1 = true := by decide +kernel
end SevenColumn.Certificate739
