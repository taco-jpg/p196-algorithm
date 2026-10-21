import P196.PrefixK45.NewK4Tree

/-! Generated certificate data (untrusted; kernel-checked use). -/
namespace PrefixK45.NewK4
open Agent124.CodeCert
set_option maxRecDepth 100000

theorem rows_leaf0028 : leaf0028.All (fun c r => rowOK ranks 4 c r = true) :=
  allRowsC_sound (by decide +kernel)

theorem rows_leaf0029 : leaf0029.All (fun c r => rowOK ranks 4 c r = true) :=
  allRowsC_sound (by decide +kernel)

theorem rows_leaf0030 : leaf0030.All (fun c r => rowOK ranks 4 c r = true) :=
  allRowsC_sound (by decide +kernel)

theorem rows_leaf0031 : leaf0031.All (fun c r => rowOK ranks 4 c r = true) :=
  allRowsC_sound (by decide +kernel)

end PrefixK45.NewK4
