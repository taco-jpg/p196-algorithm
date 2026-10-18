import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0964 : leaf0964.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0965 : leaf0965.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0966 : leaf0966.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0967 : leaf0967.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0964 : checkRow ranks (fastLongPred 7) [12,17,15,12,9,11,18] 3 = true := by decide +kernel
theorem row_branch0965 : checkRow ranks (fastLongPred 7) [12,17,15,12,9,2,16] 3 = true := by decide +kernel
theorem row_branch0966 : checkRow ranks (fastLongPred 7) [12,17,15,12,10,12,6] 3 = true := by decide +kernel
theorem row_branch0967 : checkRow ranks (fastLongPred 7) [14,7,17,0,0,6,17] 3 = true := by decide +kernel
end SevenColumn.Certificate739
