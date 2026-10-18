import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0836 : leaf0836.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0837 : leaf0837.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0838 : leaf0838.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0839 : leaf0839.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0836 : checkRow ranks (fastLongPred 7) [12,8,15,3,1,3,17] 3 = true := by decide +kernel
theorem row_branch0837 : checkRow ranks (fastLongPred 7) [12,8,15,3,10,11,2] 1 = true := by decide +kernel
theorem row_branch0838 : checkRow ranks (fastLongPred 7) [12,8,15,3,10,1,0] 0 = true := by decide +kernel
theorem row_branch0839 : checkRow ranks (fastLongPred 7) [12,8,15,12,0,11,9] 0 = true := by decide +kernel
end SevenColumn.Certificate739
