import P196.PrefixK45.NewK5Tree

/-! Generated certificate data (untrusted; kernel-checked use). -/
namespace PrefixK45.NewK5
open Agent124.CodeCert
set_option maxRecDepth 100000

open Agent124.PrefixK Agent124.PrefixR

theorem short_w0 : (symWords 0).all (shortOKC ranks) = true := by
  decide +kernel

theorem short_w1 : (symWords 1).all (shortOKC ranks) = true := by
  decide +kernel

theorem short_w2 : (symWords 2).all (shortOKC ranks) = true := by
  decide +kernel

theorem short_w3 : (symWords 3).all (shortOKC ranks) = true := by
  decide +kernel

theorem short_w4 : (symWords 4).all (shortOKC ranks) = true := by
  decide +kernel

theorem short : ShortClosed 5 (R ranks) := shortClosed_of_widths fun n hn => by
  have : n = 0 ∨ n = 1 ∨ n = 2 ∨ n = 3 ∨ n = 4 := by omega
  rcases this with rfl | rfl | rfl | rfl | rfl
  · exact short_w0
  · exact short_w1
  · exact short_w2
  · exact short_w3
  · exact short_w4

#print axioms short

end PrefixK45.NewK5
