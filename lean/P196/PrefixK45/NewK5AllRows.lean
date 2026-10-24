import P196.PrefixK45.NewK5Rows000
import P196.PrefixK45.NewK5Rows001
import P196.PrefixK45.NewK5Branch

/-! Generated certificate data (untrusted; kernel-checked use). -/
namespace PrefixK45.NewK5
open Agent124.CodeCert
set_option maxRecDepth 100000

open Agent124.PrefixR

set_option maxHeartbeats 100000000
theorem allRowsAll : ranks.All (fun c r => rowOK ranks 5 c r = true) :=
  ⟨⟨⟨rows_leaf0000, row_branch0000, rows_leaf0001⟩, row_branch0002, ⟨rows_leaf0002, row_branch0001, rows_leaf0003⟩⟩, row_branch0006, ⟨⟨rows_leaf0004, row_branch0003, rows_leaf0005⟩, row_branch0005, ⟨rows_leaf0006, row_branch0004, rows_leaf0007⟩⟩⟩

theorem allRows : RowsClosed 5 (R ranks) := rowsClosed_of_all (by decide) allRowsAll

#print axioms allRows

end PrefixK45.NewK5
