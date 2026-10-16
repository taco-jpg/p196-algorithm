import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem row_leaf0229_28 : checkRow ranks (fastLongPred 7) [3,4,6,10,9,10,6] 4 = true := by decide +kernel
theorem row_leaf0229_29 : checkRow ranks (fastLongPred 7) [3,4,6,10,9,10,7] 4 = true := by decide +kernel
theorem row_leaf0229_30 : checkRow ranks (fastLongPred 7) [3,4,6,10,9,10,8] 4 = true := by decide +kernel
theorem row_leaf0229_31 : checkRow ranks (fastLongPred 7) [3,4,6,10,9,10,9] 4 = true := by decide +kernel
theorem row_leaf0229_32 : checkRow ranks (fastLongPred 7) [3,4,6,10,9,10,10] 4 = true := by decide +kernel
theorem row_leaf0229_33 : checkRow ranks (fastLongPred 7) [3,4,6,10,9,10,11] 4 = true := by decide +kernel
theorem row_leaf0229_34 : checkRow ranks (fastLongPred 7) [3,4,6,10,9,10,13] 4 = true := by decide +kernel
theorem row_leaf0229_35 : checkRow ranks (fastLongPred 7) [3,4,6,10,9,10,14] 4 = true := by decide +kernel
theorem row_leaf0229_36 : checkRow ranks (fastLongPred 7) [3,4,6,10,9,11,14] 7 = true := by decide +kernel
theorem row_leaf0229_37 : checkRow ranks (fastLongPred 7) [3,4,6,10,9,11,15] 7 = true := by decide +kernel
theorem row_leaf0229_38 : checkRow ranks (fastLongPred 7) [3,4,6,10,9,11,16] 7 = true := by decide +kernel
theorem row_leaf0229_39 : checkRow ranks (fastLongPred 7) [3,4,6,10,9,11,17] 4 = true := by decide +kernel
theorem row_leaf0229_40 : checkRow ranks (fastLongPred 7) [3,4,6,10,9,11,18] 1 = true := by decide +kernel
theorem row_leaf0229_41 : checkRow ranks (fastLongPred 7) [3,4,6,10,9,12,0] 1 = true := by decide +kernel
end SevenColumn.Certificate739
