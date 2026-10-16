import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0644 : leaf0644.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0645 : leaf0645.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0646 : leaf0646.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0647 : leaf0647.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0644 : checkRow ranks (fastLongPred 7) [7,3,9,6,7,6,2] 2 = true := by decide +kernel
theorem row_branch0645 : checkRow ranks (fastLongPred 7) [7,3,9,7,0,4,9] 1 = true := by decide +kernel
theorem row_branch0646 : checkRow ranks (fastLongPred 7) [7,3,9,7,1,6,3] 1 = true := by decide +kernel
theorem row_branch0647 : checkRow ranks (fastLongPred 7) [7,3,9,7,1,0,6] 1 = true := by decide +kernel
end SevenColumn.Certificate739
