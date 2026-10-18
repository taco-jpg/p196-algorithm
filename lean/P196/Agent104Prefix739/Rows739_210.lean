import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0840 : leaf0840.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0841 : leaf0841.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0842 : leaf0842.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0843 : leaf0843.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0840 : checkRow ranks (fastLongPred 7) [12,8,15,12,1,12,16] 1 = true := by decide +kernel
theorem row_branch0841 : checkRow ranks (fastLongPred 7) [12,8,15,12,1,1,10] 1 = true := by decide +kernel
theorem row_branch0842 : checkRow ranks (fastLongPred 7) [12,8,15,12,0,2,8] 0 = true := by decide +kernel
theorem row_branch0843 : checkRow ranks (fastLongPred 7) [12,8,15,3,0,13,15] 3 = true := by decide +kernel
end SevenColumn.Certificate739
