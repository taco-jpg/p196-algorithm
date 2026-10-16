import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf1020 : leaf1020.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf1021 : leaf1021.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf1022 : leaf1022.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf1023 : leaf1023.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch1020 : checkRow ranks (fastLongPred 7) [12,10,5,7,7,5,10] 6 = true := by decide +kernel
theorem row_branch1021 : checkRow ranks (fastLongPred 7) [11,18,14,8,8,1,9] 0 = true := by decide +kernel
theorem row_branch1022 : checkRow ranks (fastLongPred 7) [6,8,13,1,7,16,2] 8 = true := by decide +kernel
end SevenColumn.Certificate739
