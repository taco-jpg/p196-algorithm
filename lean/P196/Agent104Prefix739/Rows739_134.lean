import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0536 : leaf0536.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0537 : leaf0537.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0538 : leaf0538.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0539 : leaf0539.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0536 : checkRow ranks (fastLongPred 7) [7,3,9,0,8,7,8] 0 = true := by decide +kernel
theorem row_branch0537 : checkRow ranks (fastLongPred 7) [7,3,9,0,9,9,2] 0 = true := by decide +kernel
theorem row_branch0538 : checkRow ranks (fastLongPred 7) [7,3,9,0,9,3,5] 0 = true := by decide +kernel
theorem row_branch0539 : checkRow ranks (fastLongPred 7) [7,3,9,0,8,2,1] 0 = true := by decide +kernel
end SevenColumn.Certificate739
