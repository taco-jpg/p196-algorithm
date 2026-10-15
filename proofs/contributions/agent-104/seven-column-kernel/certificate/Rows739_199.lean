import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0796 : leaf0796.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0797 : leaf0797.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0798 : leaf0798.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0799 : leaf0799.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0796 : checkRow ranks (fastLongPred 7) [12,1,5,14,4,15,4] 3 = true := by decide +kernel
theorem row_branch0797 : checkRow ranks (fastLongPred 7) [12,1,14,7,7,2,7] 3 = true := by decide +kernel
theorem row_branch0798 : checkRow ranks (fastLongPred 7) [12,1,14,7,7,13,17] 1 = true := by decide +kernel
theorem row_branch0799 : checkRow ranks (fastLongPred 7) [12,1,14,7,7,7,6] 3 = true := by decide +kernel
end SevenColumn.Certificate739
