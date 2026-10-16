import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0864 : leaf0864.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0865 : leaf0865.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0866 : leaf0866.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0867 : leaf0867.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0864 : checkRow ranks (fastLongPred 7) [12,9,1,16,4,5,15] 3 = true := by decide +kernel
theorem row_branch0865 : checkRow ranks (fastLongPred 7) [12,9,1,14,13,4,12] 3 = true := by decide +kernel
theorem row_branch0866 : checkRow ranks (fastLongPred 7) [12,9,1,14,10,8,15] 3 = true := by decide +kernel
theorem row_branch0867 : checkRow ranks (fastLongPred 7) [12,9,1,16,4,17,13] 2 = true := by decide +kernel
end SevenColumn.Certificate739
