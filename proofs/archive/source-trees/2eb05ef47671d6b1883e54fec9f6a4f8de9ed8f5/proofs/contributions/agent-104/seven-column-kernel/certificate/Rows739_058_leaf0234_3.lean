import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem row_leaf0234_42 : checkRow ranks (fastLongPred 7) [3,4,6,12,16,17,14] 7 = true := by decide +kernel
theorem row_leaf0234_43 : checkRow ranks (fastLongPred 7) [3,4,6,12,16,18,14] 7 = true := by decide +kernel
theorem row_leaf0234_44 : checkRow ranks (fastLongPred 7) [3,4,6,12,16,18,15] 7 = true := by decide +kernel
theorem row_leaf0234_45 : checkRow ranks (fastLongPred 7) [3,4,6,12,16,18,16] 7 = true := by decide +kernel
theorem row_leaf0234_46 : checkRow ranks (fastLongPred 7) [3,4,6,12,16,18,17] 7 = true := by decide +kernel
theorem row_leaf0234_47 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,0,0] 7 = true := by decide +kernel
theorem row_leaf0234_48 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,0,1] 7 = true := by decide +kernel
theorem row_leaf0234_49 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,0,2] 7 = true := by decide +kernel
theorem row_leaf0234_50 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,0,3] 7 = true := by decide +kernel
theorem row_leaf0234_51 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,0,4] 7 = true := by decide +kernel
theorem row_leaf0234_52 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,1,9] 7 = true := by decide +kernel
theorem row_leaf0234_53 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,1,10] 7 = true := by decide +kernel
theorem row_leaf0234_54 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,1,11] 7 = true := by decide +kernel
theorem row_leaf0234_55 : checkRow ranks (fastLongPred 7) [3,4,6,12,17,1,12] 1 = true := by decide +kernel
end SevenColumn.Certificate739
