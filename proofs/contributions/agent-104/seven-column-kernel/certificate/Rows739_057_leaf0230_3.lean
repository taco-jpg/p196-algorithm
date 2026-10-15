import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem row_leaf0230_42 : checkRow ranks (fastLongPred 7) [3,4,6,10,11,2,12] 1 = true := by decide +kernel
theorem row_leaf0230_43 : checkRow ranks (fastLongPred 7) [3,4,6,10,11,2,13] 1 = true := by decide +kernel
theorem row_leaf0230_44 : checkRow ranks (fastLongPred 7) [3,4,6,10,12,0,0] 0 = true := by decide +kernel
theorem row_leaf0230_45 : checkRow ranks (fastLongPred 7) [3,4,6,10,12,0,1] 1 = true := by decide +kernel
theorem row_leaf0230_46 : checkRow ranks (fastLongPred 7) [3,4,6,10,12,0,2] 1 = true := by decide +kernel
theorem row_leaf0230_47 : checkRow ranks (fastLongPred 7) [3,4,6,10,12,0,4] 1 = true := by decide +kernel
theorem row_leaf0230_48 : checkRow ranks (fastLongPred 7) [3,4,6,10,12,0,5] 1 = true := by decide +kernel
theorem row_leaf0230_49 : checkRow ranks (fastLongPred 7) [3,4,6,10,12,0,6] 1 = true := by decide +kernel
theorem row_leaf0230_50 : checkRow ranks (fastLongPred 7) [3,4,6,10,12,0,7] 1 = true := by decide +kernel
theorem row_leaf0230_51 : checkRow ranks (fastLongPred 7) [3,4,6,10,12,0,8] 1 = true := by decide +kernel
theorem row_leaf0230_52 : checkRow ranks (fastLongPred 7) [3,4,6,10,12,0,9] 1 = true := by decide +kernel
theorem row_leaf0230_53 : checkRow ranks (fastLongPred 7) [3,4,6,10,12,1,9] 1 = true := by decide +kernel
theorem row_leaf0230_54 : checkRow ranks (fastLongPred 7) [3,4,6,10,12,1,14] 1 = true := by decide +kernel
theorem row_leaf0230_55 : checkRow ranks (fastLongPred 7) [3,4,6,10,12,1,15] 1 = true := by decide +kernel
end SevenColumn.Certificate739
