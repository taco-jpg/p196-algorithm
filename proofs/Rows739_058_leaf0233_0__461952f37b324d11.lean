import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem row_leaf0233_0 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,12,9] 7 = true := by decide +kernel
theorem row_leaf0233_1 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,12,10] 7 = true := by decide +kernel
theorem row_leaf0233_2 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,12,11] 7 = true := by decide +kernel
theorem row_leaf0233_3 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,12,13] 7 = true := by decide +kernel
theorem row_leaf0233_4 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,12,14] 7 = true := by decide +kernel
theorem row_leaf0233_5 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,13,14] 7 = true := by decide +kernel
theorem row_leaf0233_6 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,13,15] 7 = true := by decide +kernel
theorem row_leaf0233_7 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,13,16] 7 = true := by decide +kernel
theorem row_leaf0233_8 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,13,17] 1 = true := by decide +kernel
theorem row_leaf0233_9 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,13,18] 1 = true := by decide +kernel
theorem row_leaf0233_10 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,14,0] 0 = true := by decide +kernel
theorem row_leaf0233_11 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,14,1] 1 = true := by decide +kernel
theorem row_leaf0233_12 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,14,2] 1 = true := by decide +kernel
theorem row_leaf0233_13 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,14,4] 1 = true := by decide +kernel
end SevenColumn.Certificate739
