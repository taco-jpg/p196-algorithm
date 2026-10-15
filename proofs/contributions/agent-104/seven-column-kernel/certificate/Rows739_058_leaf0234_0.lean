import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem row_leaf0234_0 : checkRow ranks (fastLongPred 7) [3,4,6,12,16,14,7] 7 = true := by decide +kernel
theorem row_leaf0234_1 : checkRow ranks (fastLongPred 7) [3,4,6,12,16,14,8] 7 = true := by decide +kernel
theorem row_leaf0234_2 : checkRow ranks (fastLongPred 7) [3,4,6,12,16,14,9] 7 = true := by decide +kernel
theorem row_leaf0234_3 : checkRow ranks (fastLongPred 7) [3,4,6,12,16,14,10] 7 = true := by decide +kernel
theorem row_leaf0234_4 : checkRow ranks (fastLongPred 7) [3,4,6,12,16,14,11] 7 = true := by decide +kernel
theorem row_leaf0234_5 : checkRow ranks (fastLongPred 7) [3,4,6,12,16,14,12] 7 = true := by decide +kernel
theorem row_leaf0234_6 : checkRow ranks (fastLongPred 7) [3,4,6,12,16,14,13] 7 = true := by decide +kernel
theorem row_leaf0234_7 : checkRow ranks (fastLongPred 7) [3,4,6,12,16,14,14] 7 = true := by decide +kernel
theorem row_leaf0234_8 : checkRow ranks (fastLongPred 7) [3,4,6,12,16,14,16] 1 = true := by decide +kernel
theorem row_leaf0234_9 : checkRow ranks (fastLongPred 7) [3,4,6,12,16,14,17] 1 = true := by decide +kernel
theorem row_leaf0234_10 : checkRow ranks (fastLongPred 7) [3,4,6,12,16,14,18] 1 = true := by decide +kernel
theorem row_leaf0234_11 : checkRow ranks (fastLongPred 7) [3,4,6,12,16,15,0] 1 = true := by decide +kernel
theorem row_leaf0234_12 : checkRow ranks (fastLongPred 7) [3,4,6,12,16,15,1] 1 = true := by decide +kernel
theorem row_leaf0234_13 : checkRow ranks (fastLongPred 7) [3,4,6,12,16,15,3] 1 = true := by decide +kernel
end SevenColumn.Certificate739
