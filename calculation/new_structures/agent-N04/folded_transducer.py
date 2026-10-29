#!/usr/bin/env python3
"""Finite-state folded reverse-add relation (exact, in any base 2..36).
NFA on low-to-centre pair-sum coefficients, with guessed reverse-side carry.
No integer arithmetic is used in transduce(); bigint is ONLY in controls.
"""
import argparse, itertools, json, random

def transduce(half, odd, base=10):
    """Return all (overflow, folded_target_coefficients, new_odd) via local 2-carry NFA.
    The final half entry is the central coefficient iff odd (necessarily even).
    Values have digits 0..2b-2; the first entry must be >0.
    """
    assert base >= 2 and len(half) >= (2 if odd else 1)
    assert 1 <= half[0] <= 2*base-2
    assert all(0 <= x <= 2*base-2 for x in half)
    if odd: assert half[-1] % 2 == 0
    row=half[:-1] if odd else half
    states=[] # (g, lower_carry_next, last_upper_carry, last_upper_digit, output_tuple)
    p=row[0]
    for r0 in (0,1):
        g=(p+r0)//base
        if g>1:continue
        upper=(p+r0)%base
        lower=p%base
        out0=lower+upper if g==0 else lower+1
        states.append((g,p//base,r0,upper,(out0,)))
    for p in row[1:]:
        updated=[]
        for g,l,rprev,upperprev,out in states:
            for r in (0,1):
                if (p+r)//base != rprev:continue
                lower=(p+l)%base
                upper=(p+r)%base
                nxt=lower+(upper if g==0 else upperprev)
                updated.append((g,(p+l)//base,r,upper,out+(nxt,)))
        states=updated
    answers=set()
    for g,l,r,upper,out in states:
        if odd:
            centre=half[-1]
            if (centre+l)//base != r:continue
            digit=(centre+l)%base
            if g==0:
                ans=out+(2*digit,)
            else:
                ans=out+(digit+upper,)
        else:
            if l!=r:continue
            ans=out if g==0 else out+(2*upper,)
        answers.add((g,ans,bool((odd and g==0) or (not odd and g==1))))
    return answers

def digits(n,b):
    ans=[]
    while n:
        n,d=divmod(n,b);ans.append(d)
    return ans or [0]

def int_of_digits(ds,b):
    return sum(d*b**i for i,d in enumerate(ds))

def target_independent(half,odd,base):
    full=half + (half[:-1][::-1] if odd else half[::-1])
    n=len(full)
    assert n>=2
    ds=[0]*n
    for i,p in enumerate(half[:n//2]):
        top=min(p,base-1);ds[n-1-i]=top;ds[i]=p-top
    if odd:ds[n//2]=half[-1]//2
    assert ds[-1]!=0
    n0=int_of_digits(ds,base)
    # independent ordinary big-integer reverse and add, *not* coefficient normalization
    v=n0+int_of_digits(ds[::-1],base)
    dst=digits(v,base)
    pair=[dst[i]+dst[-1-i] for i in range((len(dst)+1)//2)]
    return (len(dst)-n,tuple(pair),bool(len(dst)%2))

def controls():
    counts={}; witnesses={}
    for base in (9,10):
        c=0;bad=0
        for odd in (False,True):
            for h in (1,2):
                for row in itertools.product(range(2*base-1),repeat=h):
                    if row[0]==0:continue
                    for centre in (range(0,2*base-1,2) if odd else (None,)):
                        half=tuple(row)+((centre,) if odd else ())
                        actual=target_independent(half,odd,base)
                        got=transduce(half,odd,base)
                        c+=1
                        if got!={actual}:
                            bad+=1
                            if bad<=2:print('FAILED',base,half,odd,actual,got)
        counts[str(base)]={'exhaustive_small':c,'mismatches':bad}
    rng=random.Random(4074)
    for base in (9,10):
        c=0;bad=0
        for _ in range(3000):
            h=rng.randint(3,100);odd=bool(rng.randrange(2))
            row=[rng.randrange(2*base-1) for _ in range(h)]
            row[0]=rng.randrange(1,2*base-1)
            if odd:row.append(2*rng.randrange(base))
            actual=target_independent(row,odd,base)
            got=transduce(row,odd,base)
            c+=1
            if got!={actual}:
                bad+=1
                if bad<=2:print('FAILED LONG',base,row,odd,actual,got)
        counts[str(base)]['random_long']=c
        counts[str(base)]['random_mismatches']=bad
    print(json.dumps(counts,sort_keys=True,indent=2))
    assert all(d['mismatches']==0 and d['random_mismatches']==0 for d in counts.values())
    return counts
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='');a=ap.parse_args()
    data=controls()
    if a.output:json.dump(data,open(a.output,'w'),indent=2)
