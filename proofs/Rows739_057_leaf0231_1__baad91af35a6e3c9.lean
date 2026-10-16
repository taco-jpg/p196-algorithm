import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem row_leaf0231_14 : checkRow ranks (fastLongPred 7) [3,4,6,10,12,2,14] 1 = true := by decide +kernel
theorem row_leaf0231_15 : checkRow ranks (fastLongPred 7) [3,4,6,10,13,5,4] 1 = true := by decide +kernel
theorem row_leaf0231_16 : checkRow ranks (fastLongPred 7) [3,4,6,10,13,5,5] 1 = true := by decide +kernel
theorem row_leaf0231_17 : checkRow ranks (fastLongPred 7) [3,4,6,10,13,5,6] 1 = true := by decide +kernel
theorem row_leaf0231_18 : checkRow ranks (fastLongPred 7) [3,4,6,10,13,5,7] 1 = true := by decide +kernel
theorem row_leaf0231_19 : checkRow ranks (fastLongPred 7) [3,4,6,10,13,5,8] 1 = true := by decide +kernel
theorem row_leaf0231_20 : checkRow ranks (fastLongPred 7) [3,4,6,10,13,7,9] 7 = true := by decide +kernel
theorem row_leaf0231_21 : checkRow ranks (fastLongPred 7) [3,4,6,10,13,7,10] 7 = true := by decide +kernel
theorem row_leaf0231_22 : checkRow ranks (fastLongPred 7) [3,4,6,10,13,7,11] 7 = true := by decide +kernel
theorem row_leaf0231_23 : checkRow ranks (fastLongPred 7) [3,4,6,10,13,7,12] 7 = true := by decide +kernel
theorem row_leaf0231_24 : checkRow ranks (fastLongPred 7) [3,4,6,10,13,7,13] 7 = true := by decide +kernel
theorem row_leaf0231_25 : checkRow ranks (fastLongPred 7) [3,4,6,10,13,7,14] 4 = true := by decide +kernel
theorem row_leaf0231_26 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,4,4] 1 = true := by decide +kernel
theorem row_leaf0231_27 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,4,5] 1 = true := by decide +kernel
end SevenColumn.Certificate739
