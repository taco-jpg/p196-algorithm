import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0448 : leaf0448.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0449 : leaf0449.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0450 : leaf0450.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0451 : leaf0451.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0448 : checkRow ranks (fastLongPred 7) [6,4,10,13,1,13,13] 2 = true := by decide +kernel
theorem row_branch0449 : checkRow ranks (fastLongPred 7) [6,4,10,13,6,2,13] 2 = true := by decide +kernel
theorem row_branch0450 : checkRow ranks (fastLongPred 7) [6,4,10,13,2,9,9] 2 = true := by decide +kernel
theorem row_branch0451 : checkRow ranks (fastLongPred 7) [6,4,10,12,6,2,11] 2 = true := by decide +kernel
end SevenColumn.Certificate739
