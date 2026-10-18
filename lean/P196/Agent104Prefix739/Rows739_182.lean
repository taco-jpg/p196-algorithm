import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0728 : leaf0728.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0729 : leaf0729.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0730 : leaf0730.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0731 : leaf0731.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0728 : checkRow ranks (fastLongPred 7) [8,0,18,7,13,9,10] 3 = true := by decide +kernel
theorem row_branch0729 : checkRow ranks (fastLongPred 7) [8,0,13,15,7,18,17] 3 = true := by decide +kernel
theorem row_branch0730 : checkRow ranks (fastLongPred 7) [7,8,18,10,18,8,8] 2 = true := by decide +kernel
theorem row_branch0731 : checkRow ranks (fastLongPred 7) [7,8,12,5,0,6,18] 2 = true := by decide +kernel
end SevenColumn.Certificate739
