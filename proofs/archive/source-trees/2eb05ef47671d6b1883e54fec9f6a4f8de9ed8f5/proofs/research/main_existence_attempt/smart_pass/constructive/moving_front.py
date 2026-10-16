"""Exact half-infinite exterior evolution against a nonneutral periodic tail.

The half-infinite state is an auxiliary model, never a finite Lychrel witness.
Every transition uses actual exterior carries and derives its overflow flag.
"""
from dataclasses import dataclass
from pathlib import Path
import argparse, json, random

HERE = Path(__file__).resolve().parent


def periodic_carries(bulk):
    p=len(bulk)
    assert p and any(x != 9 for x in bulk)
    low=[0]*p; high=[0]*p; c=0
    for _ in range(2):
        for i,x in enumerate(bulk):
            low[i]=c; c=(x+c)//10
    c=0
    for _ in range(2):
        for i in range(p-1,-1,-1):
            c=(bulk[i]+c)//10; high[i]=c
    assert all((bulk[i]+low[i])//10 == low[(i+1)%p] for i in range(p))
    assert all((bulk[i]+high[(i+1)%p])//10 == high[i] for i in range(p))
    return low,high


def bulk_step(bulk,h):
    a,b=periodic_carries(bulk); p=len(bulk)
    return tuple((bulk[i]+a[i])%10+(bulk[(i-h)%p]+b[(i-h+1)%p])%10 for i in range(p))


@dataclass(frozen=True)
class Exterior:
    prefix: tuple
    bulk: tuple

    def at(self,i):
        assert i>=0
        return self.prefix[i] if i<len(self.prefix) else self.bulk[i%len(self.bulk)]

    def trim(self):
        n=len(self.prefix)
        while n>0 and self.prefix[n-1]==self.bulk[(n-1)%len(self.bulk)]:n-=1
        return Exterior(self.prefix[:n],self.bulk)

    def step(self):
        p=len(self.bulk); end=len(self.prefix)+p+2
        a,b=periodic_carries(self.bulk)
        low=[]; c=0
        for i in range(end):
            v=self.at(i)+c;low.append(v%10);c=v//10
        assert c==a[end%p]
        high=[0]*end;c=b[end%p]
        for i in range(end-1,-1,-1):
            v=self.at(i)+c;high[i]=v%10;c=v//10
        h=c
        nxt=bulk_step(self.bulk,h)
        word=tuple(low[i]+(1 if h and i==0 else high[i-h]) for i in range(end))
        assert all(word[i]==nxt[i%p] for i in range(end-2,end))
        return Exterior(word,nxt).trim(),h


def finite_step(q):
    ds=[];c=0
    for x in q:
        z=x+c; ds.append(z%10); c=z//10
    if c:ds.append(c)
    return tuple(a+b for a,b in zip(ds,ds[::-1])),c


def realization(q):
    assert q==q[::-1] and q[0]>0 and all(0<=x<=18 for x in q)
    L=len(q);d=[0]*L
    for i in range(L//2):
        high=min(9,q[i]); d[L-1-i]=high; d[i]=q[i]-high
    if L%2:assert q[L//2]%2==0;d[L//2]=q[L//2]//2
    return sum(x*10**i for i,x in enumerate(d))


def controls():
    rng=random.Random(20261014);comparisons=0
    for _ in range(600):
        p=rng.randrange(1,9)
        bulk=tuple(rng.randrange(19) for _ in range(p))
        if all(x==9 for x in bulk):continue
        prefix=(rng.randrange(1,19),)+tuple(rng.randrange(19) for _ in range(rng.randrange(12)))
        e=Exterior(prefix,bulk).trim()
        for t in range(6):
            # A full periodic block both before and after the probe cuts
            # isolates carries; the distant arbitrary symmetric cap is real.
            cut=len(e.prefix)+2*p+3
            half=tuple(e.at(i) for i in range(cut+2*p))
            q=half+(2*rng.randrange(10),)+half[::-1]
            out,h=finite_step(q);ne,hh=e.step()
            assert hh==h and out[:cut]==tuple(ne.at(i) for i in range(cut))
            n=realization(q);s=n+int(str(n)[::-1]);sd=tuple(map(int,str(s)[::-1]))
            actual=tuple(a+b for a,b in zip(sd,sd[::-1]))
            assert actual==out
            comparisons+=1;e=ne
            if all(x==9 for x in e.bulk):break
    return dict(exact_finite_integer_comparisons=comparisons)


def probe(prefix,bulk,steps=360):
    e=Exterior(tuple(prefix),tuple(bulk)).trim();rows=[];hs=[]
    growth=0;min_gap=0
    for t in range(steps):
        if all(x==9 for x in e.bulk):break
        ne,h=e.step();hs.append(h);growth+=h
        # Twice this quantity is the disturbance position relative to center.
        offset=2*len(ne.prefix)-growth
        min_gap=max(min_gap,offset)
        rows.append((t+1,len(ne.prefix),growth,offset))
        e=ne
    return dict(prefix=prefix,bulk=bulk,steps=len(hs),neutral_tail=all(x==9 for x in e.bulk),clock=''.join(map(str,hs)),
                alternating=all(h==t%2 for t,h in enumerate(hs)),
                final_prefix=len(e.prefix),overflows=growth,
                maximum_twice_center_penetration=min_gap,
                checkpoints=[r for r in rows if r[0]%12==0],
                final_suffix=e.prefix[-30:])


def run():
    records=[]
    for b in [(9,3,6),(5,2,5),(3,10,15,8),(6,), (9,12,15)]:
        for prefix in [(8,), (8,9,8), (8,10,8), (8,9,9), (8,10,9), (8,9,7), (8,10,7)]:
            records.append(probe(prefix,b))
    out=dict(status='finite_discovery_only',controls=controls(),records=records,
             finite_witness=False,decimal_lychrel_existence_proved=False)
    (HERE/'moving_front_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out['controls']))
    for r in records:
        print(json.dumps({k:v for k,v in r.items() if k not in ('clock','checkpoints','final_suffix')}))

if __name__=='__main__':run()
