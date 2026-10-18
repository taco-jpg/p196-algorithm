import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0736 : leaf0736.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0737 : leaf0737.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0738 : leaf0738.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0739 : leaf0739.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0736 : checkRow ranks (fastLongPred 7) [10,9,1,4,7,4,5] 2 = true := by decide +kernel
theorem row_branch0737 : checkRow ranks (fastLongPred 7) [10,7,0,9,8,10,17] 3 = true := by decide +kernel
theorem row_branch0738 : checkRow ranks (fastLongPred 7) [9,9,11,11,5,17,3] 3 = true := by decide +kernel
theorem row_branch0739 : checkRow ranks (fastLongPred 7) [10,15,9,8,3,6,2] 3 = true := by decide +kernel
end SevenColumn.Certificate739
