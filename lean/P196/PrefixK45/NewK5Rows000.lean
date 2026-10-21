import P196.PrefixK45.NewK5Tree

/-! Generated certificate data (untrusted; kernel-checked use). -/
namespace PrefixK45.NewK5
open Agent124.CodeCert
set_option maxRecDepth 100000

theorem rows_leaf0000 : leaf0000.All (fun c r => rowOK ranks 5 c r = true) :=
  allRowsC_sound (by decide +kernel)

theorem rows_leaf0001 : leaf0001.All (fun c r => rowOK ranks 5 c r = true) :=
  allRowsC_sound (by decide +kernel)

theorem rows_leaf0002 : leaf0002.All (fun c r => rowOK ranks 5 c r = true) :=
  allRowsC_sound (by decide +kernel)

theorem rows_leaf0003 : leaf0003.All (fun c r => rowOK ranks 5 c r = true) :=
  allRowsC_sound (by decide +kernel)

end PrefixK45.NewK5
