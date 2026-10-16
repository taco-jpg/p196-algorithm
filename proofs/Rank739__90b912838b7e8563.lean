import Rank739Data15

namespace SevenColumn.Certificate739
open Certificate
set_option maxRecDepth 10000

def ranks : RankTree := branch1022
def rank (w : List Nat) : Option Nat := lookup ranks w
end SevenColumn.Certificate739
