import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem row_leaf0389_28 : checkRow ranks (fastLongPred 7) [5,13,12,6,6,13,15] 4 = true := by decide +kernel
theorem row_leaf0389_29 : checkRow ranks (fastLongPred 7) [5,13,12,6,6,13,16] 4 = true := by decide +kernel
theorem row_leaf0389_30 : checkRow ranks (fastLongPred 7) [5,13,12,6,6,18,0] 1 = true := by decide +kernel
theorem row_leaf0389_31 : checkRow ranks (fastLongPred 7) [5,13,12,6,6,18,1] 1 = true := by decide +kernel
theorem row_leaf0389_32 : checkRow ranks (fastLongPred 7) [5,13,12,6,6,18,2] 1 = true := by decide +kernel
theorem row_leaf0389_33 : checkRow ranks (fastLongPred 7) [5,13,12,6,6,18,4] 1 = true := by decide +kernel
theorem row_leaf0389_34 : checkRow ranks (fastLongPred 7) [5,13,12,6,6,18,5] 1 = true := by decide +kernel
theorem row_leaf0389_35 : checkRow ranks (fastLongPred 7) [5,13,12,6,6,18,6] 1 = true := by decide +kernel
theorem row_leaf0389_36 : checkRow ranks (fastLongPred 7) [5,13,12,6,6,18,9] 1 = true := by decide +kernel
theorem row_leaf0389_37 : checkRow ranks (fastLongPred 7) [5,13,16,10,10,11,0] 0 = true := by decide +kernel
theorem row_leaf0389_38 : checkRow ranks (fastLongPred 7) [5,13,16,10,10,11,4] 4 = true := by decide +kernel
theorem row_leaf0389_39 : checkRow ranks (fastLongPred 7) [5,13,16,10,10,12,0] 2 = true := by decide +kernel
theorem row_leaf0389_40 : checkRow ranks (fastLongPred 7) [5,13,16,10,10,12,1] 2 = true := by decide +kernel
theorem row_leaf0389_41 : checkRow ranks (fastLongPred 7) [5,13,16,10,10,12,5] 4 = true := by decide +kernel
end SevenColumn.Certificate739
