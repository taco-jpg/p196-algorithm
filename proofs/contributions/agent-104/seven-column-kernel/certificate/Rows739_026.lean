import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0104 : leaf0104.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0105 : leaf0105.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0106 : leaf0106.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0107 : leaf0107.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0104 : checkRow ranks (fastLongPred 7) [1,15,16,11,4,10,0] 0 = true := by decide +kernel
theorem row_branch0105 : checkRow ranks (fastLongPred 7) [1,15,16,11,5,6,2] 0 = true := by decide +kernel
theorem row_branch0106 : checkRow ranks (fastLongPred 7) [1,15,16,11,5,0,1] 0 = true := by decide +kernel
theorem row_branch0107 : checkRow ranks (fastLongPred 7) [1,15,16,11,1,16,16] 0 = true := by decide +kernel
end SevenColumn.Certificate739
