import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0720 : leaf0720.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0721 : leaf0721.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0722 : leaf0722.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0723 : leaf0723.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0720 : checkRow ranks (fastLongPred 7) [7,8,18,10,13,13,1] 2 = true := by decide +kernel
theorem row_branch0721 : checkRow ranks (fastLongPred 7) [7,8,16,14,16,3,16] 2 = true := by decide +kernel
theorem row_branch0722 : checkRow ranks (fastLongPred 7) [7,8,16,10,1,18,10] 2 = true := by decide +kernel
theorem row_branch0723 : checkRow ranks (fastLongPred 7) [7,8,18,15,3,18,13] 2 = true := by decide +kernel
end SevenColumn.Certificate739
