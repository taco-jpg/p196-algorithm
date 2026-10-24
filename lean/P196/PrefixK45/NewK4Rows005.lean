import P196.PrefixK45.NewK4Tree

/-! Generated certificate data (untrusted; kernel-checked use). -/
namespace PrefixK45.NewK4
open Agent124.CodeCert
set_option maxRecDepth 100000

theorem rows_leaf0020 : leaf0020.All (fun c r => rowOK ranks 4 c r = true) :=
  allRowsC_sound (by decide +kernel)

theorem rows_leaf0021 : leaf0021.All (fun c r => rowOK ranks 4 c r = true) :=
  allRowsC_sound (by decide +kernel)

theorem rows_leaf0022 : leaf0022.All (fun c r => rowOK ranks 4 c r = true) :=
  allRowsC_sound (by decide +kernel)

theorem rows_leaf0023 : leaf0023.All (fun c r => rowOK ranks 4 c r = true) :=
  allRowsC_sound (by decide +kernel)

end PrefixK45.NewK4
