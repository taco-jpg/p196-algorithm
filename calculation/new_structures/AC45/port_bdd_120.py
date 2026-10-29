#!/usr/bin/env python3
"""AC45: exact local 120-layer two-ended carry ROBDD, NOT global T* emptiness.
Run: python3 calculation/new_structures/AC45/port_bdd_120.py --self-test
No external packages. Coefficients and digit arrays are LSD first.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

@dataclass(frozen=True)
class Port:
    lo: int
    hi: int
    lag: int = -1

def edge(x,port,gamma,first=False):
    """One spatial column, all permitted inner high carries; yield (h,port',q)."""
    assert 0 <= x <= 18 and gamma in (0,1)
    a=(x+port.lo)%10; lo=(x+port.lo)//10
    for h in (0,1):
        if (x+h)//10 != port.hi: continue
        b=(x+h)%10
        y=(a+1 if first and gamma else a+b if not gamma else a+port.lag)
        assert 0 <= y <= 18
        yield h,Port(lo,h,b),y

def from_int(n): return tuple(map(int,str(n)[::-1]))
def to_int(ds): return int(''.join(map(str,reversed(ds))))
def pair(ds): return tuple(a+b for a,b in zip(ds,reversed(ds)))

def realize(p):
    assert p and tuple(p)==tuple(reversed(p)) and all(0<=x<=18 for x in p)
    n=len(p);d=[0]*n
    for i in range(n//2):
        hi=min(9,p[i]);d[i]=p[i]-hi;d[n-1-i]=hi
    if n%2:
        assert p[n//2]%2==0
        d[n//2]=p[n//2]//2
    assert d[-1]>0
    return tuple(d)

def folded_one(p,gamma):
    """Full centre-joined NFA; result is a dict of outputs and path counts."""
    n=len(p);h=n//2
    states={(Port(0,gamma),()):1}
    for i in range(h):
        nxt={}
        for (port,seen),count in states.items():
            for _,nextport,y in edge(p[i],port,gamma,first=(i==0)):
                key=(nextport,seen+(y,));nxt[key]=nxt.get(key,0)+count
        states=nxt
    accepted={}
    for (s,seen),count in states.items():
        if n%2==0:
            if s.lo != s.hi:continue
            if gamma:
                half=seen+(2*s.lag,);out=half+half[:-1][::-1]
            else:out=seen+seen[::-1]
        else:
            middle=p[h]
            if middle%2 or (middle+s.lo)//10!=s.hi:continue
            dig=(middle+s.lo)%10
            if gamma:
                half=seen+(dig+s.lag,);out=half+half[::-1]
            else:
                half=seen+(2*dig,);out=half+half[:-1][::-1]
        accepted[out]=accepted.get(out,0)+count
    return accepted

class ROBDD:
    def __init__(self):self.nodes={};self.unique={};self.counter=2
    def node(self,bit,lo,hi):
        if lo==hi:return lo
        key=(bit,lo,hi)
        if key not in self.unique:
            self.unique[key]=self.counter;self.nodes[self.counter]=key;self.counter+=1
        return self.unique[key]
    def satcount(self,root,nvars):
        @lru_cache(None)
        def rec(u,start):
            if u==0:return 0
            if u==1:return 1<<(nvars-start)
            v,a,b=self.nodes[u]
            return (rec(a,v+1)+rec(b,v+1))<<(v-start)
        return rec(root,0)
    def live(self,root):
        seen=set()
        def rec(u):
            if u<2 or u in seen:return
            seen.add(u);_,a,b=self.nodes[u];rec(a);rec(b)
        rec(root);return len(seen)

def column_bdd(ports,clock,index,allowed=range(19),target=None):
    """Complete local 120-track product from ONE fixed incoming port vector.

    Five top bits encode x_0; subsequent bits encode all high-in carry
    choices. target=None demands x_120=x_0. No centre joining or spatial
    reachability from earlier columns is inferred from this local relation.
    """
    D=len(clock);assert len(ports)==D
    b=ROBDD();seen=set()
    @lru_cache(None)
    def visit(t,initial,x):
        seen.add((t,initial,x))
        if t==D:return int(x==(initial if target is None else target))
        arcs={h:visit(t+1,initial,y) for h,_,y in edge(x,ports[t],clock[t],first=index==0)}
        return b.node(5+t,arcs.get(0,0),arcs.get(1,0))
    roots={x:visit(0,x,x) for x in allowed}
    @lru_cache(None)
    def encode(bit,values):
        if not values:return 0
        if bit==5:
            assert len(values)==1
            return roots[values[0]]
        lo=tuple(x for x in values if not (x>>(4-bit))&1)
        hi=tuple(x for x in values if (x>>(4-bit))&1)
        return b.node(bit,encode(bit+1,lo),encode(bit+1,hi))
    root=encode(0,tuple(sorted(roots)))
    return {'paths':b.satcount(root,5+D),'bdd_nodes':b.live(root),'dp_states':len(seen)}

def tpl(B,W,J,U,C,q,k):
    h=tuple(B)+tuple(W)*q+tuple(J)+tuple(U)*k
    return h+tuple(C)+h[::-1]

def load_lattice(filename):
    rows=[list(map(int,line.split())) for line in Path(filename).read_text().splitlines()]
    assert rows[0]==[12,34,9,10] and rows[1]==[1,0,0,0]*3
    return rows[26],rows[2]

def trajectory(p,steps=120):
    d=realize(p);n=to_int(d);rows=[tuple(p)];clock=[]
    for _ in range(steps):
        v=n+int(str(n)[::-1]);dd=from_int(v)
        clock.append(len(dd)-len(d));rows.append(pair(dd));n=v;d=dd
    return rows,clock

def ports_at(rows,clock,i):
    result=[]
    for t,g in enumerate(clock):
        p=rows[t];L=len(p);c=[0];d=[]
        for x in p:
            z=x+c[-1];c.append(z//10);d.append(z%10)
        assert c[-1]==g
        result.append(Port(c[i],c[L-i],d[L-i] if i else -1))
    return result

def verify():
    from itertools import product
    checks=0
    for length in (2,3,4,5):
        h=length//2
        for side in product(range(19),repeat=h):
            for middle in (range(0,19,2) if length%2 else (None,)):
                p=side+((middle,) if middle is not None else ())+side[::-1]
                try:d=realize(p)
                except AssertionError:continue
                z=to_int(d);v=z+int(str(z)[::-1]);actual=pair(from_int(v))
                gamma=len(str(v))-len(d)
                assert folded_one(p,gamma)=={actual:1}
                assert folded_one(p,1-gamma)=={}
                checks+=1
    # Artificial planted genuine decimal clock returns, gamma 0 and gamma 1.
    assert folded_one((3,3),0)=={(6,6):1}
    assert folded_one((10,10),1)=={(1,2,1):1}
    # ROBDD vs separate brute force of high-carry assignments, short clocks.
    from random import Random
    r=Random(45);bdtests=0
    for D in (1,2,3,4,6,8):
        for _ in range(25):
            gam=[r.randrange(2) for t in range(D)]
            s=[Port(r.randrange(2),r.randrange(2),r.randrange(10)) for t in range(D)]
            idx=r.randrange(3);x0=r.randrange(19);target=r.randrange(19)
            frontier=[x0]
            for t in range(D):
                nxt=[]
                for x in frontier:
                    a=(x+s[t].lo)%10
                    for h in (0,1):
                        if (x+h)//10!=s[t].hi:continue
                        y=a+(1 if idx==0 and gam[t] else (x+h)%10 if not gam[t] else s[t].lag)
                        if 0<=y<=18:nxt.append(y)
                frontier=nxt
            expected=sum(x==target for x in frontier)
            assert column_bdd(s,gam,idx,[x0],target)['paths']==expected
            bdtests+=1
    B,W=load_lattice(Path(__file__).resolve().parents[2]/'decimal_frontier/lattice_kinks/data/lat_p12m9.txt')
    root=tpl(B,W,[5],[9,0,18],[4,4],14,100)
    rows,g=trajectory(root)
    assert g==[1,0,0,0]*30
    for t in range(120):assert folded_one(rows[t],g[t])=={rows[t+1]:1}
    ports=ports_at(rows,g,0)
    bdd=column_bdd(ports,g,0,[root[0]],target=rows[-1][0])
    assert bdd['paths']==1<<30 and bdd['bdd_nodes']==95
    print('PASS',{'small_full_centre_inputs':checks,'short_clock_bdd_controls':bdtests,
                  'physical_macro_edges':120,'column0_successors':bdd['paths'],
                  'column0_robdd_nodes':bdd['bdd_nodes'],'global_Tstar':'UNDECIDED'})

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--self-test',action='store_true');z=a.parse_args()
    if z.self_test:verify()
    else:a.print_help()
