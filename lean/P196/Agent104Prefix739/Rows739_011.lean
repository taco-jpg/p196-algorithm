import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0044 : leaf0044.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0045 : leaf0045.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0046 : leaf0046.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0047 : leaf0047.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0044 : checkRow ranks (fastLongPred 7) [1,11,2,8,8,8,15] 0 = true := by decide +kernel
theorem row_branch0045 : checkRow ranks (fastLongPred 7) [1,11,2,4,2,15,13] 0 = true := by decide +kernel
theorem row_branch0046 : checkRow ranks (fastLongPred 7) [1,11,5,4,5,15,13] 0 = true := by decide +kernel
theorem row_branch0047 : checkRow ranks (fastLongPred 7) [1,11,6,5,7,15,10] 0 = true := by decide +kernel
end SevenColumn.Certificate739
