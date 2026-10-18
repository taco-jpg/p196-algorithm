import P196.Drafts.D20261015ScalarFiniteCertificateFormalPilotArray.JobCatalog
namespace ScalarJobData
open ScalarFinite
def meta0 (i : Nat) : Nat := if i < 7 then (if i < 3 then (if i < 1 then 28 else (if i < 2 then 57 else 247)) else (if i < 5 then (if i < 4 then 52 else 242) else (if i < 6 then 47 else 230))) else 0
def components0 (i : Nat) : Nat := if i < 7 then 0 else 0
def nextCodes0 (i : Nat) : Nat := if i < 14 then (if i < 7 then (if i < 3 then (if i < 1 then 2 else (if i < 2 then 0 else 3)) else (if i < 5 then (if i < 4 then 0 else 4) else (if i < 6 then 4 else 0))) else (if i < 10 then (if i < 8 then 5 else 6) else (if i < 12 then (if i < 11 then 0 else 7) else 1))) else 0
def ranks0 (i : Nat) : Nat := if i < 1 then 659 else 0
def component0 (v : Nat) : Nat := components0 v
def childCode0 (c : Nat) : Nat := if c=0 then 2 else 0
def data0 : Data where
  size := 7
  phase v := (meta0 v)%7
  last v := (meta0 v)/7%19
  low v := (meta0 v)/133
  next u bit := nextCodes0 (2*u+bit)

def ranking0 : Ranking where
  component := component0
  cyclic c := decide (childCode0 c ≠ 0)
  weight c := if childCode0 c=0 then 1 else jobBound (childCode0 c-1)
  rank c := ranks0 c
  bound := jobBound 0
end ScalarJobData
