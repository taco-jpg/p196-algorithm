from lib import *
import itertools
def phiB(b,B):
    """autonomous B-system: assume e2 = 1-e1. returns (B2 trimmed, u, e1, gam) ; B2 trimmed of trailing n's"""
    n=b-1
    E1=e1(b,B)
    C=[0] if E1==1 else [2*n]       # dummy centre forcing e2=1-e1
    assert e2(b,B,C)==1-E1
    nb=nextB(b,B,C); g=gam(b,B,C)
    u=0
    while nb and nb[-1]==n: nb=nb[:-1]; u+=1
    return nb,u,E1,g
def decoupling_test():
    # 1) decoupling test: on real runs the B part of canonical run equals the autonomous B orbit
    rng=random.Random(3); ok=0; tot=0
    for b in (10,11,17,26,8):
        for _ in range(4000):
            B,C=rand_state(b,rng,(1,7),(0,7))
            if not hyp(b,B,C): continue
            cur=(B,C); Bs=B
            for t in range(30):
                E=step(b,cur[0],cur[1])
                if E is None: break
                Bn,u,E1,g=phiB(b,Bs)
                assert Bn==E[2] and u==E[4] and g==gam(b,cur[0],cur[1]),(b,cur,E,Bn)
                cur=(E[2],E[3]); Bs=Bn; tot+=1
    print("B autonomous (depends on C only through e2=1-e1): verified on",tot,"transitions")

# 2) B-cycles of the autonomous system in base 10 (m<=4), orbit following until repeat
def bcycles(b,maxm,maxlen=14,maxsteps=400):
    n=b-1; found={}
    for m in range(0,maxm+1):
        for B in itertools.product(range(2*n+1),repeat=m):
            B=list(B)
            if B and B[0]==0: continue
            seen={}; cur=tuple(B); t=0; gs=[]
            while cur not in seen and t<maxsteps and len(cur)<=maxlen:
                seen[cur]=t
                nb,u,E1,g=phiB(b,list(cur)); gs.append((E1,g,u)); cur=tuple(nb); t+=1
                if nb and nb[0]==0: break
            if cur in seen:
                s=seen[cur]; cyc=tuple(gs[s:])
                key=min(tuple(cyc[i:]+cyc[:i]) for i in range(len(cyc)))
                if sum(x[1] for x in cyc)>0 and key not in found: found[key]=(cur,len(cyc))
    return found
if __name__=="__main__":
  decoupling_test()
  for b,mm in ((10,3),(11,3),(16,2)):
      f=bcycles(b,mm)
      print("base",b,"B-system cycles with sum(gam)>0 for |B|<=",mm,":",len(f))
      for k,v in list(f.items())[:12]: print("   period",len(k),"(e1,gam,u) per step:",k,"rep B=",v[0])
