import P196.PrefixK45.NewK4Tree

/-! Generated certificate data (untrusted; kernel-checked use). -/
namespace PrefixK45.NewK4
open Agent124.CodeCert
set_option maxRecDepth 100000

theorem rows_leaf0008 : leaf0008.All (fun c r => rowOK ranks 4 c r = true) :=
  allRowsC_sound (by decide +kernel)

theorem rows_leaf0009 : leaf0009.All (fun c r => rowOK ranks 4 c r = true) :=
  allRowsC_sound (by decide +kernel)

theorem rows_leaf0010 : leaf0010.All (fun c r => rowOK ranks 4 c r = true) :=
  allRowsC_sound (by decide +kernel)

theorem rows_leaf0011 : leaf0011.All (fun c r => rowOK ranks 4 c r = true) :=
  allRowsC_sound (by decide +kernel)

end PrefixK45.NewK4
