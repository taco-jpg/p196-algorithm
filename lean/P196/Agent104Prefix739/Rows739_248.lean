import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0992 : leaf0992.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0993 : leaf0993.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0994 : leaf0994.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0995 : leaf0995.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0992 : checkRow ranks (fastLongPred 7) [14,17,4,2,0,17,9] 3 = true := by decide +kernel
theorem row_branch0993 : checkRow ranks (fastLongPred 7) [14,16,17,0,0,11,10] 0 = true := by decide +kernel
theorem row_branch0994 : checkRow ranks (fastLongPred 7) [14,17,8,2,8,3,1] 3 = true := by decide +kernel
theorem row_branch0995 : checkRow ranks (fastLongPred 7) [14,17,8,3,17,14,10] 3 = true := by decide +kernel
end SevenColumn.Certificate739
