import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0064 : leaf0064.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0065 : leaf0065.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0066 : leaf0066.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0067 : leaf0067.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0064 : checkRow ranks (fastLongPred 7) [1,15,16,9,9,11,5] 0 = true := by decide +kernel
theorem row_branch0065 : checkRow ranks (fastLongPred 7) [1,12,3,18,17,15,14] 0 = true := by decide +kernel
theorem row_branch0066 : checkRow ranks (fastLongPred 7) [1,15,16,9,10,9,9] 0 = true := by decide +kernel
theorem row_branch0067 : checkRow ranks (fastLongPred 7) [1,15,16,9,11,5,16] 0 = true := by decide +kernel
end SevenColumn.Certificate739
