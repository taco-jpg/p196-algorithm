import Rank739
import FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem row_leaf0232_42 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,11,11] 7 = true := by decide +kernel
theorem row_leaf0232_43 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,11,12] 7 = true := by decide +kernel
theorem row_leaf0232_44 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,11,13] 7 = true := by decide +kernel
theorem row_leaf0232_45 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,11,14] 7 = true := by decide +kernel
theorem row_leaf0232_46 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,11,15] 1 = true := by decide +kernel
theorem row_leaf0232_47 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,11,16] 1 = true := by decide +kernel
theorem row_leaf0232_48 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,11,17] 1 = true := by decide +kernel
theorem row_leaf0232_49 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,11,18] 1 = true := by decide +kernel
theorem row_leaf0232_50 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,12,0] 0 = true := by decide +kernel
theorem row_leaf0232_51 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,12,1] 1 = true := by decide +kernel
theorem row_leaf0232_52 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,12,2] 1 = true := by decide +kernel
theorem row_leaf0232_53 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,12,3] 1 = true := by decide +kernel
theorem row_leaf0232_54 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,12,4] 4 = true := by decide +kernel
theorem row_leaf0232_55 : checkRow ranks (fastLongPred 7) [3,4,6,12,14,12,6] 7 = true := by decide +kernel
end SevenColumn.Certificate739
