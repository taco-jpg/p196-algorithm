import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0076 : leaf0076.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0077 : leaf0077.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0078 : leaf0078.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0079 : leaf0079.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0076 : checkRow ranks (fastLongPred 7) [1,15,16,9,15,14,15] 0 = true := by decide +kernel
theorem row_branch0077 : checkRow ranks (fastLongPred 7) [1,15,16,9,11,15,0] 0 = true := by decide +kernel
theorem row_branch0078 : checkRow ranks (fastLongPred 7) [1,15,16,10,0,16,16] 0 = true := by decide +kernel
theorem row_branch0079 : checkRow ranks (fastLongPred 7) [1,15,16,10,1,12,1] 0 = true := by decide +kernel
end SevenColumn.Certificate739
