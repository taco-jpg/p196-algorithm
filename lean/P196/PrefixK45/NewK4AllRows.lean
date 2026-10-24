import P196.PrefixK45.NewK4Rows000
import P196.PrefixK45.NewK4Rows001
import P196.PrefixK45.NewK4Rows002
import P196.PrefixK45.NewK4Rows003
import P196.PrefixK45.NewK4Rows004
import P196.PrefixK45.NewK4Rows005
import P196.PrefixK45.NewK4Rows006
import P196.PrefixK45.NewK4Rows007
import P196.PrefixK45.NewK4Branch

/-! Generated certificate data (untrusted; kernel-checked use). -/
namespace PrefixK45.NewK4
open Agent124.CodeCert
set_option maxRecDepth 100000

open Agent124.PrefixR

set_option maxHeartbeats 100000000
theorem allRowsAll : ranks.All (fun c r => rowOK ranks 4 c r = true) :=
  ⟨⟨⟨⟨⟨rows_leaf0000, row_branch0000, rows_leaf0001⟩, row_branch0002, ⟨rows_leaf0002, row_branch0001, rows_leaf0003⟩⟩, row_branch0006, ⟨⟨rows_leaf0004, row_branch0003, rows_leaf0005⟩, row_branch0005, ⟨rows_leaf0006, row_branch0004, rows_leaf0007⟩⟩⟩, row_branch0014, ⟨⟨⟨rows_leaf0008, row_branch0007, rows_leaf0009⟩, row_branch0009, ⟨rows_leaf0010, row_branch0008, rows_leaf0011⟩⟩, row_branch0013, ⟨⟨rows_leaf0012, row_branch0010, rows_leaf0013⟩, row_branch0012, ⟨rows_leaf0014, row_branch0011, rows_leaf0015⟩⟩⟩⟩, row_branch0030, ⟨⟨⟨⟨rows_leaf0016, row_branch0015, rows_leaf0017⟩, row_branch0017, ⟨rows_leaf0018, row_branch0016, rows_leaf0019⟩⟩, row_branch0021, ⟨⟨rows_leaf0020, row_branch0018, rows_leaf0021⟩, row_branch0020, ⟨rows_leaf0022, row_branch0019, rows_leaf0023⟩⟩⟩, row_branch0029, ⟨⟨⟨rows_leaf0024, row_branch0022, rows_leaf0025⟩, row_branch0024, ⟨rows_leaf0026, row_branch0023, rows_leaf0027⟩⟩, row_branch0028, ⟨⟨rows_leaf0028, row_branch0025, rows_leaf0029⟩, row_branch0027, ⟨rows_leaf0030, row_branch0026, rows_leaf0031⟩⟩⟩⟩⟩

theorem allRows : RowsClosed 4 (R ranks) := rowsClosed_of_all (by decide) allRowsAll

#print axioms allRows

end PrefixK45.NewK4
