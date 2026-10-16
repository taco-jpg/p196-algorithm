import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0588 : leaf0588.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0589 : leaf0589.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0590 : leaf0590.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0591 : leaf0591.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0588 : checkRow ranks (fastLongPred 7) [7,3,9,3,3,3,4] 2 = true := by decide +kernel
theorem row_branch0589 : checkRow ranks (fastLongPred 7) [7,3,9,3,8,4,9] 2 = true := by decide +kernel
theorem row_branch0590 : checkRow ranks (fastLongPred 7) [7,3,9,3,9,6,3] 2 = true := by decide +kernel
theorem row_branch0591 : checkRow ranks (fastLongPred 7) [7,3,9,3,9,0,6] 2 = true := by decide +kernel
end SevenColumn.Certificate739
