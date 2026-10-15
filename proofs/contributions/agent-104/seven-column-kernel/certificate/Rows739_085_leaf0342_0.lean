import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem row_leaf0342_0 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,14,10] 1 = true := by decide +kernel
theorem row_leaf0342_1 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,14,11] 1 = true := by decide +kernel
theorem row_leaf0342_2 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,14,12] 1 = true := by decide +kernel
theorem row_leaf0342_3 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,14,13] 1 = true := by decide +kernel
theorem row_leaf0342_4 : checkRow ranks (fastLongPred 7) [3,11,14,9,3,14,14] 1 = true := by decide +kernel
theorem row_leaf0342_5 : checkRow ranks (fastLongPred 7) [3,11,14,9,4,0,0] 0 = true := by decide +kernel
theorem row_leaf0342_6 : checkRow ranks (fastLongPred 7) [3,11,14,9,4,0,1] 1 = true := by decide +kernel
theorem row_leaf0342_7 : checkRow ranks (fastLongPred 7) [3,11,14,9,4,0,2] 1 = true := by decide +kernel
theorem row_leaf0342_8 : checkRow ranks (fastLongPred 7) [3,11,14,9,4,0,3] 1 = true := by decide +kernel
theorem row_leaf0342_9 : checkRow ranks (fastLongPred 7) [3,11,14,9,4,0,4] 1 = true := by decide +kernel
theorem row_leaf0342_10 : checkRow ranks (fastLongPred 7) [3,11,14,9,4,0,9] 10 = true := by decide +kernel
theorem row_leaf0342_11 : checkRow ranks (fastLongPred 7) [3,11,14,9,4,0,10] 10 = true := by decide +kernel
theorem row_leaf0342_12 : checkRow ranks (fastLongPred 7) [3,11,14,9,4,0,11] 10 = true := by decide +kernel
theorem row_leaf0342_13 : checkRow ranks (fastLongPred 7) [3,11,14,9,4,0,12] 10 = true := by decide +kernel
end SevenColumn.Certificate739
