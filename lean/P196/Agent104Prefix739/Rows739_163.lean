import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0652 : leaf0652.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0653 : leaf0653.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0654 : leaf0654.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0655 : leaf0655.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0652 : checkRow ranks (fastLongPred 7) [7,3,9,6,9,9,1] 2 = true := by decide +kernel
theorem row_branch0653 : checkRow ranks (fastLongPred 7) [7,3,9,7,5,0,6] 2 = true := by decide +kernel
theorem row_branch0654 : checkRow ranks (fastLongPred 7) [7,3,9,7,6,2,0] 2 = true := by decide +kernel
theorem row_branch0655 : checkRow ranks (fastLongPred 7) [7,3,9,7,5,6,3] 2 = true := by decide +kernel
end SevenColumn.Certificate739
