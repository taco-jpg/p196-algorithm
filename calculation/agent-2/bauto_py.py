#!/usr/bin/env python3
# Complete independent Python enumeration for fixed overflow word.
import sys
G = sys.argv[1] if len(sys.argv)>1 else '1000100010001000'
p = len(G)
g = tuple(map(int,G))
tg = tuple(i for i,z in enumerate(g) if z)
gi = {t:j for j,t in enumerate(tg)}
def accept(S):
    L,H,Y=S
    return (all(((L>>t)&1)+((H>>t)&1)==1 for t in range(p)) and
            all(Y[j]==9*((L>>t)&1) for j,t in enumerate(tg)))
def succ(S, first):
    L,H,Y=S
    for x0 in range(1 if first else 0,19):
        stack=[(0,x0,0,0,())]
        while stack:
            t,x,nl,nh,ny=stack.pop()
            for h in (0,1):
                if (x+h)//10 != ((H>>t)&1): continue
                low=(x+((L>>t)&1))%10
                nx=low+(Y[gi[t]] if g[t] else (x+h)%10)
                NL=nl|(((x+((L>>t)&1))//10)<<t)
                NH=nh|(h<<t)
                NY=ny+((x+h)%10,) if g[t] else ny
                if t==p-1:
                    if nx==x0:yield (NL,NH,NY)
                else:stack.append((t+1,nx,NL,NH,NY))
start=(0,sum(bit<<t for t,bit in enumerate(g)),(1,)*len(tg))
seen={start};front={start};depth=0;found=0
while front and depth<100:
    nxt=set()
    for S in front:
        if accept(S): found+=1
        for T in succ(S,first=(depth==0)):
            if T not in seen:seen.add(T);nxt.add(T)
    front=nxt;depth+=1
print("RESULT", "EXHAUSTED" if not front else "UNDECIDED",
      "depth",depth,"states",len(seen),"accepted",found)

