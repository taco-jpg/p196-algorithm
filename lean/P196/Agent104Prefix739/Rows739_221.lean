import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0884 : leaf0884.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0885 : leaf0885.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0886 : leaf0886.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0887 : leaf0887.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0884 : checkRow ranks (fastLongPred 7) [12,9,3,17,10,4,9] 1 = true := by decide +kernel
theorem row_branch0885 : checkRow ranks (fastLongPred 7) [12,10,5,5,4,17,5] 3 = true := by decide +kernel
theorem row_branch0886 : checkRow ranks (fastLongPred 7) [12,10,5,7,7,0,4] 0 = true := by decide +kernel
theorem row_branch0887 : checkRow ranks (fastLongPred 7) [12,10,5,5,13,8,16] 2 = true := by decide +kernel
end SevenColumn.Certificate739
