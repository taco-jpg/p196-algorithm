import Rank4Data
import FourColumnAncestry
namespace FourColumnKernel.Certificate
open SevenColumn.Certificate
set_option maxRecDepth 10000
set_option maxHeartbeats 100000000
open FourColumnKernel
theorem shortDescent4 : ShortDescent ranks4 :=
  shortDescent_of_all ranks4 (by decide +kernel)
#print axioms shortDescent4
end FourColumnKernel.Certificate
