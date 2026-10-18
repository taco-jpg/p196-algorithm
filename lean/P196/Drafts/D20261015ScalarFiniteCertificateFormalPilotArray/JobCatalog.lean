import P196.Drafts.D20261015ScalarFiniteCertificateFormalPilotArray.RankRows
namespace ScalarJobData
open ScalarFinite
def bounds (i : Nat) : Nat := if i < 16 then (if i < 8 then (if i < 4 then (if i < 2 then 659 else (if i < 3 then 649 else 14)) else (if i < 6 then (if i < 5 then 606 else 588) else (if i < 7 then 561 else 513))) else (if i < 12 then (if i < 10 then (if i < 9 then 474 else 378) else (if i < 11 then 305 else 277)) else (if i < 14 then (if i < 13 then 208 else 157) else 19))) else 0
def widths (i : Nat) : Nat := if i < 16 then (if i < 8 then (if i < 4 then (if i < 2 then (if i < 1 then 1 else 2) else (if i < 3 then 3 else 4)) else (if i < 6 then (if i < 5 then 4 else 5) else (if i < 7 then 6 else 7))) else (if i < 12 then (if i < 10 then (if i < 9 then 8 else 9) else (if i < 11 then 10 else 11)) else (if i < 14 then (if i < 13 then 12 else 13) else (if i < 15 then 14 else 12)))) else 0
def jobBound (j : Nat) : Nat := bounds j
def jobWidth (j : Nat) : Nat := widths j
end ScalarJobData
