import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem row_leaf0235_0 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,1,14] 1 = true := by decide +kernel
theorem row_leaf0235_1 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,1,15] 1 = true := by decide +kernel
theorem row_leaf0235_2 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,1,17] 1 = true := by decide +kernel
theorem row_leaf0235_3 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,1,18] 0 = true := by decide +kernel
theorem row_leaf0235_4 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,2,0] 1 = true := by decide +kernel
theorem row_leaf0235_5 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,2,1] 1 = true := by decide +kernel
theorem row_leaf0235_6 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,2,2] 7 = true := by decide +kernel
theorem row_leaf0235_7 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,2,4] 7 = true := by decide +kernel
theorem row_leaf0235_8 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,2,5] 7 = true := by decide +kernel
theorem row_leaf0235_9 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,2,6] 7 = true := by decide +kernel
theorem row_leaf0235_10 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,2,7] 7 = true := by decide +kernel
theorem row_leaf0235_11 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,2,8] 7 = true := by decide +kernel
theorem row_leaf0235_12 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,2,9] 7 = true := by decide +kernel
theorem row_leaf0235_13 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,4,0] 1 = true := by decide +kernel
end SevenColumn.Certificate739
