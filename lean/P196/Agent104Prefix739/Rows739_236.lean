import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastRowsBase
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
theorem checked_leaf0944 : leaf0944.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0945 : leaf0945.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0946 : leaf0946.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem checked_leaf0947 : leaf0947.All (fun p r => checkRow ranks (fastLongPred 7) p r = true) := by decide +kernel
theorem row_branch0944 : checkRow ranks (fastLongPred 7) [12,17,6,3,1,2,9] 3 = true := by decide +kernel
theorem row_branch0945 : checkRow ranks (fastLongPred 7) [12,17,6,3,0,3,7] 6 = true := by decide +kernel
theorem row_branch0946 : checkRow ranks (fastLongPred 7) [12,17,6,12,0,1,1] 9 = true := by decide +kernel
theorem row_branch0947 : checkRow ranks (fastLongPred 7) [12,17,6,12,1,0,3] 3 = true := by decide +kernel
end SevenColumn.Certificate739
