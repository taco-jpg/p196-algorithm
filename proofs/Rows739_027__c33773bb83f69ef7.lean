import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0108 : leaf0108.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0109 : leaf0109.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0110 : leaf0110.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0111 : leaf0111.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0108 : checkRow ranks (fastLongPred 7) [1,15,16,11,0,5,10] 0 = true := by decide +kernel
theorem row_branch0109 : checkRow ranks (fastLongPred 7) [1,15,16,11,6,4,10] 0 = true := by decide +kernel
theorem row_branch0110 : checkRow ranks (fastLongPred 7) [1,15,16,11,9,4,15] 0 = true := by decide +kernel
theorem row_branch0111 : checkRow ranks (fastLongPred 7) [1,15,16,11,6,10,14] 0 = true := by decide +kernel
end SevenColumn.Certificate739
