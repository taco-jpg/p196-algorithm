import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0816 : leaf0816.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0817 : leaf0817.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0818 : leaf0818.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0819 : leaf0819.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0816 : checkRow ranks (fastLongPred 7) [12,1,16,8,1,8,15] 3 = true := by decide +kernel
theorem row_branch0817 : checkRow ranks (fastLongPred 7) [12,1,14,16,18,15,0] 0 = true := by decide +kernel
theorem row_branch0818 : checkRow ranks (fastLongPred 7) [12,1,14,16,16,14,9] 3 = true := by decide +kernel
theorem row_branch0819 : checkRow ranks (fastLongPred 7) [12,1,16,17,10,17,13] 7 = true := by decide +kernel
end SevenColumn.Certificate739
