import P196.Drafts.D20261015ScalarFiniteCertificateFormalPilotArray.RankRows
namespace BroaderJobData
open ScalarFinite
def bounds (i : Nat) : Nat := if i < 15 then (if i < 7 then (if i < 3 then (if i < 1 then 636 else (if i < 2 then 636 else 14)) else (if i < 5 then (if i < 4 then 600 else 588) else (if i < 6 then 561 else 513))) else (if i < 11 then (if i < 9 then (if i < 8 then 474 else 378) else (if i < 10 then 305 else 277)) else (if i < 13 then (if i < 12 then 208 else 157) else 19))) else 0
def widths (i : Nat) : Nat := if i < 15 then (if i < 7 then (if i < 3 then (if i < 1 then 2 else (if i < 2 then 3 else 4)) else (if i < 5 then (if i < 4 then 4 else 5) else (if i < 6 then 6 else 7))) else (if i < 11 then (if i < 9 then (if i < 8 then 8 else 9) else (if i < 10 then 10 else 11)) else (if i < 13 then (if i < 12 then 12 else 13) else (if i < 14 then 14 else 12)))) else 0
def jobBound (j : Nat) : Nat := bounds j
def jobWidth (j : Nat) : Nat := widths j
end BroaderJobData
