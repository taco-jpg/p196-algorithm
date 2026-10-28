import P196.AbsorbingBand.Base13

/-!
# Negative controls for the base-13 absorbing-band cycle

The same checker `lcycleOK` rejects corrupted versions of the certificate.
-/

namespace AbsorbingBand.Base13

open AbsorbingBand Agent120.Neutral

-- One edge gets a wrong trimming number.
set_option maxRecDepth 100000 in
example : lcycleOK 13 (cert.map (fun e => if e.B = B3 then { e with u := 2 } else e)) B0 16 = false := by
  decide

-- One edge gets a wrong next block (reversed).
set_option maxRecDepth 100000 in
example : lcycleOK 13 (cert.map (fun e => if e.B = B3 then { e with B2 := e.B2.reverse } else e)) B0 16 = false := by
  decide

-- Dropping the last edge: the chain does not close.
set_option maxRecDepth 100000 in
example : lcycleOK 13 cert.dropLast B0 16 = false := by decide

-- Wrong band value at the start.
set_option maxRecDepth 100000 in
example : lcycleOK 13 cert B0 8 = false := by decide

-- The data are for base 13 only.
set_option maxRecDepth 100000 in
example : lcycleOK 12 cert B0 16 = false := by decide

-- Wrong next band value in one edge.
set_option maxRecDepth 100000 in
example : lcycleOK 13 (cert.map (fun e => if e.B = B3 then { e with c2 := e.c2 + 1 } else e)) B0 16 = false := by
  decide

-- The empty cycle is rejected.
example : lcycleOK 13 [] B0 16 = false := by decide

end AbsorbingBand.Base13
