import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem row_leaf0235_14 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,4,2] 1 = true := by decide +kernel
theorem row_leaf0235_15 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,4,3] 1 = true := by decide +kernel
theorem row_leaf0235_16 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,4,4] 7 = true := by decide +kernel
theorem row_leaf0235_17 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,9,0] 7 = true := by decide +kernel
theorem row_leaf0235_18 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,9,1] 7 = true := by decide +kernel
theorem row_leaf0235_19 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,9,2] 7 = true := by decide +kernel
theorem row_leaf0235_20 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,9,3] 7 = true := by decide +kernel
theorem row_leaf0235_21 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,9,4] 7 = true := by decide +kernel
theorem row_leaf0235_22 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,9,9] 7 = true := by decide +kernel
theorem row_leaf0235_23 : checkRow ranks (fastLongPred 7) [3,4,6,12,18,5,0] 1 = true := by decide +kernel
theorem row_leaf0235_24 : checkRow ranks (fastLongPred 7) [3,4,6,12,18,5,1] 1 = true := by decide +kernel
theorem row_leaf0235_25 : checkRow ranks (fastLongPred 7) [3,4,6,12,18,5,2] 1 = true := by decide +kernel
theorem row_leaf0235_26 : checkRow ranks (fastLongPred 7) [3,4,6,12,18,5,3] 1 = true := by decide +kernel
theorem row_leaf0235_27 : checkRow ranks (fastLongPred 7) [3,4,6,12,18,7,4] 1 = true := by decide +kernel
end SevenColumn.Certificate739
