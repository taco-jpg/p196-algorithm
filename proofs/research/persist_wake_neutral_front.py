"""Universal finite prefixes at the neutral interface (no finite witness claimed)."""
from persist_wake_neutral_cut22 import CLOCK,INCOMING

def prefix_step(q,u,t):
 r=INCOMING[t%11];h=CLOCK[t%11]
 c=r;lo=[]
 for x in q:
  z=x+c;lo.append(z%10);c=z//10
 c=u;hi=[]
 for x in q[::-1]:
  z=x+c;hi.append(z%10);c=z//10
 if c!=1-r:return None
 hi.reverse()
 return tuple(a+b for a,b in zip(lo,hi))if not h else (lo[0]+9*r,)+tuple(lo[i]+hi[i-1]for i in range(1,len(q)))

def universal(q,steps=11):
 states={q};sizes=[]
 for t in range(steps):
  nxt=set()
  for st in states:
   for u in (0,1):
    out=prefix_step(st,u,t)
    if out is None:return False,t,sizes,states
    nxt.add(out)
  states=nxt;sizes.append(len(states))
 return True,steps,sizes,states

if __name__=='__main__':
 p=(15,17,18,13,17,18)
 for k in range(1,7):
  good,t,sizes,states=universal(p[:k]);print(k,good,t,sizes,'outputs',sorted(states)[:8])
