"""Full slice extremal-J BigInt controls at five widths."""
from bigint_verify import check
from prefix_check import check as prefix_check
codes=[0,1,18,19,360,361,6858,12345,543210,1234567,1999999,2476098]
for code in codes:
 x=code;J=[]
 for _ in range(5):J.append(x%19);x//=19
 U=[9,0,18]
 for C in ([4,4],[4,14,4],[6,2,8,2,6]):
  ref=check(J,U,C,14,100);p=prefix_check(J,U,C,100)
  assert ref["first"]==p[1] and ref["gamma"]==p[2]==30
  for q,k in ((20,80),(40,160),(80,320),(160,640)):
   z=check(J,U,C,q,k)
   assert z["first"]==ref["first"]+9*(q-14) and z["gamma"]==30
print("PASS 180 independent Python BigInt width controls and 36 prefix-by-step controls")
