import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem row_leaf0391_0 : checkRow ranks (fastLongPred 7) [5,13,16,15,0,11,14] 0 = true := by decide +kernel
theorem row_leaf0391_1 : checkRow ranks (fastLongPred 7) [5,13,16,15,0,12,10] 0 = true := by decide +kernel
theorem row_leaf0391_2 : checkRow ranks (fastLongPred 7) [5,13,16,15,0,12,11] 0 = true := by decide +kernel
theorem row_leaf0391_3 : checkRow ranks (fastLongPred 7) [5,13,16,15,0,12,15] 0 = true := by decide +kernel
theorem row_leaf0391_4 : checkRow ranks (fastLongPred 7) [5,13,16,15,0,12,16] 0 = true := by decide +kernel
theorem row_leaf0391_5 : checkRow ranks (fastLongPred 7) [5,13,16,15,0,16,0] 0 = true := by decide +kernel
theorem row_leaf0391_6 : checkRow ranks (fastLongPred 7) [5,13,16,15,0,16,4] 0 = true := by decide +kernel
theorem row_leaf0391_7 : checkRow ranks (fastLongPred 7) [5,13,16,15,0,16,9] 0 = true := by decide +kernel
theorem row_leaf0391_8 : checkRow ranks (fastLongPred 7) [5,13,16,15,0,17,0] 0 = true := by decide +kernel
theorem row_leaf0391_9 : checkRow ranks (fastLongPred 7) [5,13,16,15,0,17,1] 0 = true := by decide +kernel
theorem row_leaf0391_10 : checkRow ranks (fastLongPred 7) [5,13,16,15,0,17,5] 0 = true := by decide +kernel
theorem row_leaf0391_11 : checkRow ranks (fastLongPred 7) [5,13,16,15,0,17,6] 0 = true := by decide +kernel
theorem row_leaf0391_12 : checkRow ranks (fastLongPred 7) [5,13,16,15,5,1,10] 2 = true := by decide +kernel
theorem row_leaf0391_13 : checkRow ranks (fastLongPred 7) [5,13,16,15,5,1,15] 2 = true := by decide +kernel
end SevenColumn.Certificate739
