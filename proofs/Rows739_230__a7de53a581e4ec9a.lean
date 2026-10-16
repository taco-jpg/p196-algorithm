import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0920 : leaf0920.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0921 : leaf0921.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0922 : leaf0922.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0923 : leaf0923.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0920 : checkRow ranks (fastLongPred 7) [12,10,14,7,7,18,8] 3 = true := by decide +kernel
theorem row_branch0921 : checkRow ranks (fastLongPred 7) [12,10,14,7,7,5,14] 3 = true := by decide +kernel
theorem row_branch0922 : checkRow ranks (fastLongPred 7) [12,10,14,5,4,8,1] 6 = true := by decide +kernel
theorem row_branch0923 : checkRow ranks (fastLongPred 7) [12,10,5,16,16,0,15] 6 = true := by decide +kernel
end SevenColumn.Certificate739
