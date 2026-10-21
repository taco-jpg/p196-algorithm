import P196.PrefixK45.NewK4Tree

/-! Generated certificate data (untrusted; kernel-checked use). -/
namespace PrefixK45.NewK4
open Agent124.CodeCert
set_option maxRecDepth 100000

theorem rows_leaf0016 : leaf0016.All (fun c r => rowOK ranks 4 c r = true) :=
  allRowsC_sound (by decide +kernel)

theorem rows_leaf0017 : leaf0017.All (fun c r => rowOK ranks 4 c r = true) :=
  allRowsC_sound (by decide +kernel)

theorem rows_leaf0018 : leaf0018.All (fun c r => rowOK ranks 4 c r = true) :=
  allRowsC_sound (by decide +kernel)

theorem rows_leaf0019 : leaf0019.All (fun c r => rowOK ranks 4 c r = true) :=
  allRowsC_sound (by decide +kernel)

end PrefixK45.NewK4
