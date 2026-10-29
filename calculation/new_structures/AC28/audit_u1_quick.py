"""AC28 U=(0,18,9): independent BigInt checks at five widths."""
from bigint_verify import check
from prefix_check import check as prefix_check
U=[0,18,9]
for code in [0,12345,2476098]:
 x=code;J=[]
 for _ in range(5):J.append(x%19);x//=19
 for C in ([4,4],[4,14,4]):
  ref=check(J,U,C,14,100);p=prefix_check(J,U,C,100)
  assert ref["first"]==p[1] and ref["gamma"]==p[2]==30
  for q,k in [(20,80),(40,160),(80,320),(160,640)]:
   r=check(J,U,C,q,k)
   assert r["first"]==ref["first"]+9*(q-14) and r["gamma"]==30
print("PASS: 30 independent BigInt trajectories, including 6 step-by-step prefix cross-checks")
