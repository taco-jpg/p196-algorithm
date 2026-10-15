import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem row_leaf0390_0 : checkRow ranks (fastLongPred 7) [5,13,16,10,15,5,10] 2 = true := by decide +kernel
theorem row_leaf0390_1 : checkRow ranks (fastLongPred 7) [5,13,16,10,15,5,14] 2 = true := by decide +kernel
theorem row_leaf0390_2 : checkRow ranks (fastLongPred 7) [5,13,16,10,15,5,15] 2 = true := by decide +kernel
theorem row_leaf0390_3 : checkRow ranks (fastLongPred 7) [5,13,16,10,15,6,11] 2 = true := by decide +kernel
theorem row_leaf0390_4 : checkRow ranks (fastLongPred 7) [5,13,16,10,15,6,12] 2 = true := by decide +kernel
theorem row_leaf0390_5 : checkRow ranks (fastLongPred 7) [5,13,16,10,15,6,15] 2 = true := by decide +kernel
theorem row_leaf0390_6 : checkRow ranks (fastLongPred 7) [5,13,16,10,15,6,16] 2 = true := by decide +kernel
theorem row_leaf0390_7 : checkRow ranks (fastLongPred 7) [5,13,16,11,11,13,0] 2 = true := by decide +kernel
theorem row_leaf0390_8 : checkRow ranks (fastLongPred 7) [5,13,16,11,11,13,1] 2 = true := by decide +kernel
theorem row_leaf0390_9 : checkRow ranks (fastLongPred 7) [5,13,16,11,11,13,2] 2 = true := by decide +kernel
theorem row_leaf0390_10 : checkRow ranks (fastLongPred 7) [5,13,16,11,11,13,5] 4 = true := by decide +kernel
theorem row_leaf0390_11 : checkRow ranks (fastLongPred 7) [5,13,16,11,11,13,6] 4 = true := by decide +kernel
theorem row_leaf0390_12 : checkRow ranks (fastLongPred 7) [5,13,16,11,11,14,0] 2 = true := by decide +kernel
theorem row_leaf0390_13 : checkRow ranks (fastLongPred 7) [5,13,16,11,11,14,1] 2 = true := by decide +kernel
end SevenColumn.Certificate739
