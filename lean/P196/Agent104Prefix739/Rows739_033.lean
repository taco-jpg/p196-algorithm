import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0132 : leaf0132.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0133 : leaf0133.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0134 : leaf0134.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0135 : leaf0135.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0132 : checkRow ranks (fastLongPred 7) [1,16,11,16,16,9,11] 0 = true := by decide +kernel
theorem row_branch0133 : checkRow ranks (fastLongPred 7) [1,16,1,7,15,13,18] 0 = true := by decide +kernel
theorem row_branch0134 : checkRow ranks (fastLongPred 7) [1,17,2,15,2,16,18] 0 = true := by decide +kernel
theorem row_branch0135 : checkRow ranks (fastLongPred 7) [1,17,3,7,10,9,4] 0 = true := by decide +kernel
end SevenColumn.Certificate739
