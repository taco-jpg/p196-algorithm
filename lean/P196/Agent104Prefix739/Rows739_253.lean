import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf1012 : leaf1012.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf1013 : leaf1013.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf1014 : leaf1014.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf1015 : leaf1015.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch1012 : checkRow ranks (fastLongPred 7) [16,10,7,11,7,17,11] 4 = true := by decide +kernel
theorem row_branch1013 : checkRow ranks (fastLongPred 7) [16,10,16,11,7,8,13] 4 = true := by decide +kernel
theorem row_branch1014 : checkRow ranks (fastLongPred 7) [16,10,16,2,7,9,18] 4 = true := by decide +kernel
theorem row_branch1015 : checkRow ranks (fastLongPred 7) [16,10,7,2,16,8,4] 4 = true := by decide +kernel
end SevenColumn.Certificate739
