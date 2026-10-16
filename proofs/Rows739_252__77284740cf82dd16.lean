import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf1008 : leaf1008.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf1009 : leaf1009.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf1010 : leaf1010.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf1011 : leaf1011.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch1008 : checkRow ranks (fastLongPred 7) [14,17,17,3,17,5,0] 3 = true := by decide +kernel
theorem row_branch1009 : checkRow ranks (fastLongPred 7) [16,1,16,2,7,17,4] 1 = true := by decide +kernel
theorem row_branch1010 : checkRow ranks (fastLongPred 7) [16,9,0,9,0,1,17] 2 = true := by decide +kernel
theorem row_branch1011 : checkRow ranks (fastLongPred 7) [16,1,16,11,7,8,17] 4 = true := by decide +kernel
end SevenColumn.Certificate739
