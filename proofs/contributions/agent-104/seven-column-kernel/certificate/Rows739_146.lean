import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0584 : leaf0584.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0585 : leaf0585.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0586 : leaf0586.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0587 : leaf0587.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0584 : checkRow ranks (fastLongPred 7) [7,3,9,3,6,2,0] 2 = true := by decide +kernel
theorem row_branch0585 : checkRow ranks (fastLongPred 7) [7,3,9,3,7,3,4] 2 = true := by decide +kernel
theorem row_branch0586 : checkRow ranks (fastLongPred 7) [7,3,9,3,6,7,7] 2 = true := by decide +kernel
theorem row_branch0587 : checkRow ranks (fastLongPred 7) [7,3,9,3,5,6,3] 2 = true := by decide +kernel
end SevenColumn.Certificate739
