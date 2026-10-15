import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem row_leaf0341_0 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,4,14] 10 = true := by decide +kernel
theorem row_leaf0341_1 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,9,9] 10 = true := by decide +kernel
theorem row_leaf0341_2 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,9,10] 10 = true := by decide +kernel
theorem row_leaf0341_3 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,9,11] 10 = true := by decide +kernel
theorem row_leaf0341_4 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,9,12] 10 = true := by decide +kernel
theorem row_leaf0341_5 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,9,13] 10 = true := by decide +kernel
theorem row_leaf0341_6 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,9,14] 10 = true := by decide +kernel
theorem row_leaf0341_7 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,10,0] 10 = true := by decide +kernel
theorem row_leaf0341_8 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,10,1] 10 = true := by decide +kernel
theorem row_leaf0341_9 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,10,2] 10 = true := by decide +kernel
theorem row_leaf0341_10 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,10,3] 10 = true := by decide +kernel
theorem row_leaf0341_11 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,10,4] 10 = true := by decide +kernel
theorem row_leaf0341_12 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,10,9] 10 = true := by decide +kernel
theorem row_leaf0341_13 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,10,10] 1 = true := by decide +kernel
end SevenColumn.Certificate739
