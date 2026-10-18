import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0888 : leaf0888.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0889 : leaf0889.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0890 : leaf0890.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0891 : leaf0891.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0888 : checkRow ranks (fastLongPred 7) [12,10,5,5,4,7,17] 3 = true := by decide +kernel
theorem row_branch0889 : checkRow ranks (fastLongPred 7) [12,9,3,17,1,3,1] 1 = true := by decide +kernel
theorem row_branch0890 : checkRow ranks (fastLongPred 7) [12,9,3,7,17,3,1] 3 = true := by decide +kernel
theorem row_branch0891 : checkRow ranks (fastLongPred 7) [12,9,1,7,15,18,4] 2 = true := by decide +kernel
end SevenColumn.Certificate739
