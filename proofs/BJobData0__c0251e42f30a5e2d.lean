import BJobCatalog
namespace BroaderJobData
open ScalarFinite
def meta0 (i : Nat) : Nat := if i < 15 then (if i < 7 then (if i < 3 then (if i < 1 then 28 else (if i < 2 then 57 else 64)) else (if i < 5 then (if i < 4 then 247 else 261) else (if i < 6 then 234 else 248))) else (if i < 11 then (if i < 9 then (if i < 8 then 60 else 221) else (if i < 10 then 228 else 68)) else (if i < 13 then (if i < 12 then 208 else 236) else (if i < 14 then 6 else 202)))) else 0
def components0 (i : Nat) : Nat := if i < 15 then 0 else 0
def nextCodes0 (i : Nat) : Nat := if i < 30 then (if i < 15 then (if i < 7 then (if i < 3 then (if i < 1 then 2 else (if i < 2 then 3 else 4)) else (if i < 5 then (if i < 4 then 0 else 5) else (if i < 6 then 0 else 6))) else (if i < 11 then (if i < 9 then (if i < 8 then 6 else 7) else (if i < 10 then 7 else 8)) else (if i < 13 then (if i < 12 then 0 else 9) else (if i < 14 then 10 else 13)))) else (if i < 22 then (if i < 18 then (if i < 16 then 13 else 11) else (if i < 20 then 12 else (if i < 21 then 0 else 15))) else (if i < 26 then (if i < 24 then (if i < 23 then 14 else 0) else (if i < 25 then 0 else 15)) else (if i < 28 then 1 else (if i < 29 then 0 else 1))))) else 0
def ranks0 (i : Nat) : Nat := if i < 1 then 636 else 0
def component0 (v : Nat) : Nat := components0 v
def childCode0 (c : Nat) : Nat := if c=0 then 2 else 0
def data0 : Data where
  size := 15
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
end BroaderJobData
