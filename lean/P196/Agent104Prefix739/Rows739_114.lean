import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0456 : leaf0456.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0457 : leaf0457.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0458 : leaf0458.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0459 : leaf0459.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0456 : checkRow ranks (fastLongPred 7) [6,4,10,17,11,18,16] 1 = true := by decide +kernel
theorem row_branch0457 : checkRow ranks (fastLongPred 7) [6,4,10,17,11,13,10] 2 = true := by decide +kernel
theorem row_branch0458 : checkRow ranks (fastLongPred 7) [6,4,10,16,15,0,18] 2 = true := by decide +kernel
theorem row_branch0459 : checkRow ranks (fastLongPred 7) [6,4,10,13,6,8,10] 2 = true := by decide +kernel
end SevenColumn.Certificate739
