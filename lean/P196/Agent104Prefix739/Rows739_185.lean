import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0740 : leaf0740.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0741 : leaf0741.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0742 : leaf0742.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0743 : leaf0743.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0740 : checkRow ranks (fastLongPred 7) [10,16,9,18,18,4,3] 0 = true := by decide +kernel
theorem row_branch0741 : checkRow ranks (fastLongPred 7) [10,16,0,18,17,1,8] 1 = true := by decide +kernel
theorem row_branch0742 : checkRow ranks (fastLongPred 7) [10,18,0,1,9,14,1] 3 = true := by decide +kernel
theorem row_branch0743 : checkRow ranks (fastLongPred 7) [11,5,2,17,0,13,15] 0 = true := by decide +kernel
end SevenColumn.Certificate739
