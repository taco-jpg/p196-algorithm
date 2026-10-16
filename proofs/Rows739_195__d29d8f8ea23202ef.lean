import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0780 : leaf0780.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0781 : leaf0781.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0782 : leaf0782.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0783 : leaf0783.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0780 : checkRow ranks (fastLongPred 7) [12,1,5,7,9,5,4] 3 = true := by decide +kernel
theorem row_branch0781 : checkRow ranks (fastLongPred 7) [12,1,5,14,13,7,7] 3 = true := by decide +kernel
theorem row_branch0782 : checkRow ranks (fastLongPred 7) [12,1,5,16,7,3,14] 3 = true := by decide +kernel
theorem row_branch0783 : checkRow ranks (fastLongPred 7) [12,1,5,14,13,17,6] 3 = true := by decide +kernel
end SevenColumn.Certificate739
