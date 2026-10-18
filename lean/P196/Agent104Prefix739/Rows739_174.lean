import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0696 : leaf0696.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0697 : leaf0697.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0698 : leaf0698.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0699 : leaf0699.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0696 : checkRow ranks (fastLongPred 7) [7,4,2,0,12,8,6] 1 = true := by decide +kernel
theorem row_branch0697 : checkRow ranks (fastLongPred 7) [7,3,9,9,9,6,2] 11 = true := by decide +kernel
theorem row_branch0698 : checkRow ranks (fastLongPred 7) [7,3,9,9,7,3,3] 11 = true := by decide +kernel
theorem row_branch0699 : checkRow ranks (fastLongPred 7) [7,3,9,9,2,7,6] 2 = true := by decide +kernel
end SevenColumn.Certificate739
