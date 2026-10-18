import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0984 : leaf0984.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0985 : leaf0985.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0986 : leaf0986.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0987 : leaf0987.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0984 : checkRow ranks (fastLongPred 7) [14,8,13,11,0,4,6] 3 = true := by decide +kernel
theorem row_branch0985 : checkRow ranks (fastLongPred 7) [14,8,8,12,8,18,2] 3 = true := by decide +kernel
theorem row_branch0986 : checkRow ranks (fastLongPred 7) [14,8,4,1,4,17,7] 2 = true := by decide +kernel
theorem row_branch0987 : checkRow ranks (fastLongPred 7) [14,8,17,12,8,14,1] 3 = true := by decide +kernel
end SevenColumn.Certificate739
