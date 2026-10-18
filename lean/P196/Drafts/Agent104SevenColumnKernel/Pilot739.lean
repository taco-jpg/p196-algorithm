import P196.Agent104Prefix739.Rank739
import P196.Agent104P620Witness.FastInverse
namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000
def fastLongPred (p : List Nat) : List (List Nat) := if p.length = 7 then fastPrefixPredecessors p else []
theorem pilot0 : checkRow ranks fastLongPred [7,3,9,9,3,7] 0 = true := by decide
#print axioms pilot0
theorem pilot1 : checkRow ranks fastLongPred [7,3,9,9,9,2,0] 38 = true := by decide
#print axioms pilot1
theorem pilot2 : checkRow ranks fastLongPred [16,10,16,16,16,9,17] 1 = true := by decide
#print axioms pilot2
theorem pilot3 : checkRow ranks fastLongPred [3,4,6,10,9,9,9] 7 = true := by decide
#print axioms pilot3
end SevenColumn.Certificate739
