import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0744 : leaf0744.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0745 : leaf0745.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0746 : leaf0746.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0747 : leaf0747.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0744 : checkRow ranks (fastLongPred 7) [10,18,9,9,16,16,9] 8 = true := by decide +kernel
theorem row_branch0745 : checkRow ranks (fastLongPred 7) [10,18,0,0,8,17,17] 3 = true := by decide +kernel
theorem row_branch0746 : checkRow ranks (fastLongPred 7) [10,9,3,6,4,6,4] 7 = true := by decide +kernel
theorem row_branch0747 : checkRow ranks (fastLongPred 7) [11,7,5,4,13,18,12] 1 = true := by decide +kernel
end SevenColumn.Certificate739
