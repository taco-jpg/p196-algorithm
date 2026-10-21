import P196.PrefixK45.NewK4Tree

/-! Generated certificate data (untrusted; kernel-checked use). -/
namespace PrefixK45.NewK4
open Agent124.CodeCert
set_option maxRecDepth 100000

theorem rows_leaf0012 : leaf0012.All (fun c r => rowOK ranks 4 c r = true) :=
  allRowsC_sound (by decide +kernel)

theorem rows_leaf0013 : leaf0013.All (fun c r => rowOK ranks 4 c r = true) :=
  allRowsC_sound (by decide +kernel)

theorem rows_leaf0014 : leaf0014.All (fun c r => rowOK ranks 4 c r = true) :=
  allRowsC_sound (by decide +kernel)

theorem rows_leaf0015 : leaf0015.All (fun c r => rowOK ranks 4 c r = true) :=
  allRowsC_sound (by decide +kernel)

end PrefixK45.NewK4
