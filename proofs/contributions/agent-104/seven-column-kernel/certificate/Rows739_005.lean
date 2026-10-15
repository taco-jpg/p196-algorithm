import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0020 : leaf0020.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0021 : leaf0021.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0022 : leaf0022.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0023 : leaf0023.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0020 : checkRow ranks (fastLongPred 7) [1,10,2,14,8,18,15] 0 = true := by decide +kernel
theorem row_branch0021 : checkRow ranks (fastLongPred 7) [1,10,2,14,2,8,4] 0 = true := by decide +kernel
theorem row_branch0022 : checkRow ranks (fastLongPred 7) [1,10,3,15,16,5,6] 0 = true := by decide +kernel
theorem row_branch0023 : checkRow ranks (fastLongPred 7) [1,10,3,16,17,12,0] 0 = true := by decide +kernel
end SevenColumn.Certificate739
