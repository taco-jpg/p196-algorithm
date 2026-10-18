import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0564 : leaf0564.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0565 : leaf0565.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0566 : leaf0566.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0567 : leaf0567.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0564 : checkRow ranks (fastLongPred 7) [7,3,9,2,4,7,8] 2 = true := by decide +kernel
theorem row_branch0565 : checkRow ranks (fastLongPred 7) [7,3,9,2,5,9,2] 2 = true := by decide +kernel
theorem row_branch0566 : checkRow ranks (fastLongPred 7) [7,3,9,2,5,3,5] 2 = true := by decide +kernel
theorem row_branch0567 : checkRow ranks (fastLongPred 7) [7,3,9,2,7,0,6] 2 = true := by decide +kernel
end SevenColumn.Certificate739
