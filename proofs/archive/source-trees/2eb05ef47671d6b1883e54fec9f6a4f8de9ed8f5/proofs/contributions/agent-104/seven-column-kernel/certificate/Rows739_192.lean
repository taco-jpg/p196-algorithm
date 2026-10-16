import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0768 : leaf0768.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0769 : leaf0769.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0770 : leaf0770.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0771 : leaf0771.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0768 : checkRow ranks (fastLongPred 7) [12,1,5,5,4,8,13] 2 = true := by decide +kernel
theorem row_branch0769 : checkRow ranks (fastLongPred 7) [12,1,5,7,7,2,2] 3 = true := by decide +kernel
theorem row_branch0770 : checkRow ranks (fastLongPred 7) [12,1,5,7,7,13,8] 3 = true := by decide +kernel
theorem row_branch0771 : checkRow ranks (fastLongPred 7) [12,1,5,7,7,7,2] 3 = true := by decide +kernel
end SevenColumn.Certificate739
