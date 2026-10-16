import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf1016 : leaf1016.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf1017 : leaf1017.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf1018 : leaf1018.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf1019 : leaf1019.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch1016 : checkRow ranks (fastLongPred 7) [16,1,7,11,7,17,13] 4 = true := by decide +kernel
theorem row_branch1017 : checkRow ranks (fastLongPred 7) [14,17,13,10,4,8,12] 3 = true := by decide +kernel
theorem row_branch1018 : checkRow ranks (fastLongPred 7) [14,8,17,11,8,17,3] 3 = true := by decide +kernel
theorem row_branch1019 : checkRow ranks (fastLongPred 7) [12,17,6,12,10,12,1] 9 = true := by decide +kernel
end SevenColumn.Certificate739
