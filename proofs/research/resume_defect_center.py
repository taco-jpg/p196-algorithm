"""Exact local center dynamics in supplied periodic decimal q bulks.

The supplied overflow schedule is conditional on a finite exterior still
being constructed. No fixed center found here alone proves a Lychrel number.
"""
from itertools import product
import json, time
from family_search_bulk_periods import bulk_step


BASE=(3,10,15,8)


def advance(q, bulk, origin, h):
    # Carries arriving from the omitted periodic bulk. All tested bulk phases
    # are nonneutral, so the preceding symbol itself fixes this bit.
    prev=bulk[(origin-1)%len(bulk)]
    assert prev != 9
    carry=int(prev>=10)
    digits=[]
    for x in q:
        z=x+carry
        digits.append(z%10)
        carry=z//10
    if h:
        out=tuple(digits[i]+digits[len(q)-i] for i in range(1,len(q)))
    else:
        out=tuple(a+b for a,b in zip(digits,reversed(digits)))
    nb=next(iter(bulk_step(bulk,h)))
    return out,nb,origin+h


def return_center(core,bulk=BASE,steps=16,reps=6,trace=False):
    q=bulk*reps+core+tuple(reversed(bulk))*reps
    start=q
    origin=0
    history=[]
    for t in range(steps):
        q,bulk,origin=advance(q,bulk,origin,t%2)
        if trace:history.append(q)
    # Eight artificial pair croppings counter the eight physical growth
    # digits, leaving four fewer symbols per side after16 steps.
    trim=steps//4
    expected=start[trim:len(start)-trim]
    return q==expected,q,expected,history


def center_words(pairs):
    for side in product(range(19),repeat=pairs):
        rev=tuple(reversed(side))
        yield side+rev
        for mid in range(0,19,2):
            yield side+(mid,)+rev


def search(maxpairs=2):
    result=[]
    for rot in range(4):
        bulk=BASE[rot:]+BASE[:rot]
        for k in range(maxpairs+1):
            now=time.monotonic();hits=[];total=0
            for core in center_words(k):
                if not core:continue
                total+=1
                ok,*_=return_center(core,bulk)
                if ok:hits.append(core)
            r=dict(rotation=rot,pairs=k,tested=total,hits=hits,
                   seconds=round(time.monotonic()-now,3))
            result.append(r);print(json.dumps(r),flush=True)
    return result


def normalized_return(core,bulk=BASE):
    _,q,_,_=return_center(core,bulk)
    j=0
    while 2*(j+4)<=len(q) and q[j:j+4]==bulk and q[len(q)-j-4:len(q)-j]==bulk[::-1]:
        j+=4
    return q[j:len(q)-j]


def renewals(maxpairs=2,limit=32):
    # Rotations2 and3 are the complements of0 and1; retain all four
    # explicitly in this finite experiment.
    results=[]
    for rot in range(4):
        bulk=BASE[rot:]+BASE[:rot]
        cases=[(c,c) for k in range(maxpairs+1) for c in center_words(k)]
        counts=[]
        for t in range(1,limit+1):
            nxt=[]
            for seed,core in cases:
                out=normalized_return(core,bulk)
                if len(out)-len(core)<=8:nxt.append((seed,out))
            cases=nxt;counts.append(len(cases))
            if not cases:break
        results.append(dict(rotation=rot,survivor_counts=counts,
                            remaining_seeds=[a for a,b in cases]))
    return results


def validate_local(samples=1000):
    import random
    rng=random.Random(816)
    for _ in range(samples):
        rot=rng.randrange(4);bulk=BASE[rot:]+BASE[:rot]
        side=tuple(rng.randrange(19) for _ in range(rng.randrange(6)))
        middle=() if rng.randrange(2) else (2*rng.randrange(10),)
        core=side+middle+side[::-1]
        prefix=(rng.randrange(1,19),)+tuple(rng.randrange(19) for _ in range(5))
        halfprefix=prefix+bulk
        domain=bulk*3+core+bulk[::-1]*3
        full=halfprefix+domain+halfprefix[::-1]
        # Construct canonical decimal digits with exactly these pair sums.
        ds=[0]*len(full)
        for i in range(len(full)//2):
            lead=max(1 if i==0 else 0,full[i]-9)
            ds[-1-i]=lead;ds[i]=full[i]-lead
        if len(full)%2:ds[len(full)//2]=full[len(full)//2]//2
        n=sum(d*10**i for i,d in enumerate(ds))
        s=str(n);m=n+int(s[::-1]);outdigits=tuple(map(int,str(m)[::-1]))
        actual=tuple(a+b for a,b in zip(outdigits,outdigits[::-1]))
        h=len(str(m))-len(s)
        local,_,_=advance(domain,bulk,0,h)
        crop=len(halfprefix)+h
        assert local==actual[crop:len(actual)-crop]
    return samples


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--pairs',type=int,default=2)
    ap.add_argument('--renewals',action='store_true')
    ap.add_argument('--validate',action='store_true')
    args=ap.parse_args()
    if args.validate:
        print(json.dumps(dict(local_integer_checks=validate_local())))
        raise SystemExit
    if args.renewals:
        data=renewals(args.pairs)
        print(json.dumps(data,indent=2))
        open('resume_defect_center_renewals.json','w').write(json.dumps(data,indent=2))
        raise SystemExit
    data=search(args.pairs)
    open('resume_defect_center_results.json','w').write(json.dumps(data,indent=2))
