"""Exact eventual periodic-word arithmetic, with integer affine run lengths.

This extends the archived constant-digit affine-run arithmetic to periodic
blocks. Each returned family is exact for all integer m >= its returned
threshold, not just for a sampled m. No decimal existence claim is made.
"""
from dataclasses import dataclass
from math import gcd
import argparse
import json
import random
import time


@dataclass(frozen=True)
class Seg:
    p: tuple
    a: int
    b: int

    def size(self, m):
        return self.a*m+self.b


def primitive(p):
    for d in range(1, len(p)+1):
        if len(p)%d == 0 and all(p[i] == p[i%d] for i in range(len(p))):
            return p[:d]
    raise AssertionError


def append(out, p, a, b):
    if a == 0 and b == 0:
        return
    p = primitive(tuple(p))
    assert a >= 0 and a % len(p) == 0
    if out and len(out[-1].p) == len(p):
        old = out[-1]
        shift = old.b % len(p)
        rotated = old.p[shift:]+old.p[:shift]
        if rotated == p:
            out[-1] = Seg(old.p, old.a+a, old.b+b)
            return
    out.append(Seg(p, a, b))


def positive_threshold(a, b):
    assert a > 0
    return (-b)//a+1


def minimum(x, y, threshold):
    """Select the eventual smaller affine length, raising the threshold."""
    da, db = x.a-y.a, x.b-y.b
    if da:
        if da > 0:
            threshold = max(threshold, positive_threshold(da, db))
            return y.a, y.b, threshold
        threshold = max(threshold, positive_threshold(-da, -db))
        return x.a, x.b, threshold
    if db <= 0:
        return x.a, x.b, threshold
    return y.a, y.b, threshold


def drop(seg, a, b):
    if seg.a == a and seg.b == b:
        return None
    assert a % len(seg.p) == 0
    offset = b % len(seg.p)
    return Seg(seg.p[offset:]+seg.p[:offset], seg.a-a, seg.b-b)


def reverse_word(word):
    return [Seg(tuple(s.p[(s.b-1-i)%len(s.p)] for i in range(len(s.p))),
                s.a,s.b) for s in word[::-1]]


def add_word(word, threshold, base=10):
    """Ordinary reverse-add, exact for every m >= threshold."""
    right = reverse_word(word)
    i = j = 0
    x, y = word[0], right[0]
    carry = 0
    out = []
    while True:
        a,b,threshold = minimum(x,y,threshold)
        if a == 0:
            assert b > 0
            digits = []
            for r in range(b):
                total = x.p[r%len(x.p)]+y.p[r%len(y.p)]+carry
                digits.append(total%base)
                carry = total//base
            # A fixed literal word has no repeated-variable length constraint.
            append(out,digits,0,b)
        else:
            period = len(x.p)*len(y.p)//gcd(len(x.p),len(y.p))
            assert a % period == 0
            # Keep the tail strictly positive throughout the claimed domain.
            threshold = max(threshold,positive_threshold(a,b-period))
            first = []
            for r in range(period):
                total=x.p[r%len(x.p)]+y.p[r%len(y.p)]+carry
                first.append(total%base)
                carry=total//base
            stable_carry=carry
            stable=[]
            for r in range(period):
                total=x.p[r%len(x.p)]+y.p[r%len(y.p)]+carry
                stable.append(total%base)
                carry=total//base
            # Each column carry map is 0, identity, or 1; so is their
            # composition. Applying it twice reaches its fixed point.
            assert carry == stable_carry
            append(out,first,0,period)
            append(out,stable,a,b-period)
            # The actual tail may contain a final partial period.
            for r in range(b%period):
                total=x.p[r%len(x.p)]+y.p[r%len(y.p)]+carry
                carry=total//base
        x=drop(x,a,b)
        y=drop(y,a,b)
        if x is None:
            i+=1
            if i<len(word): x=word[i]
        if y is None:
            j+=1
            if j<len(right): y=right[j]
        if i==len(word) or j==len(right):
            assert i==len(word) and j==len(right)
            break
    if carry:
        append(out,(carry,),0,1)
    return out,threshold


def eventually_equal(left,right,threshold):
    """Return a Boolean valid for all m at or above the returned threshold."""
    i=j=0
    x,y=left[0],right[0]
    while True:
        a,b,threshold=minimum(x,y,threshold)
        period=len(x.p)*len(y.p)//gcd(len(x.p),len(y.p))
        if a:
            threshold=max(threshold,positive_threshold(a,b-period+1))
            count=period
        else:
            assert b>0
            count=min(period,b)
        if any(x.p[r%len(x.p)]!=y.p[r%len(y.p)] for r in range(count)):
            return False,threshold
        x=drop(x,a,b)
        y=drop(y,a,b)
        if x is None:
            i+=1
            if i<len(left): x=left[i]
        if y is None:
            j+=1
            if j<len(right): y=right[j]
        if i==len(left) or j==len(right):
            return i==len(left) and j==len(right),threshold


def encoded_family(a,b,k,shift=0):
    A=tuple(map(int,str(a).zfill(k)[::-1]))
    B=tuple(map(int,str(b).zfill(k)[::-1]))
    out=[]
    for p,slope,const in ((A,k,k*shift),(B,0,k),(A,0,k),
                          (B,k,k*shift),(A,0,k),(B,0,k)):
        append(out,p,slope,const)
    return out


def expand(word,m):
    out=[]
    for s in word:
        n=s.size(m)
        assert n>0
        out.extend(s.p[i%len(s.p)] for i in range(n))
    return ''.join(map(str,out[::-1]))


def decimal_step(s):
    return str(int(s)+int(s[::-1]))


def width(word):
    return sum(s.a for s in word),sum(s.b for s in word)


def check_code(a,b,k,validate=False):
    word=encoded_family(a,b,k)
    target=encoded_family(a,b,k,1)
    threshold=3
    hits=[]
    maximum_segments=len(word)
    for t in range(1,10*k+5):
        before=word
        word,threshold=add_word(word,threshold)
        if validate:
            for m in (threshold,threshold+1,threshold+7):
                assert decimal_step(expand(before,m))==expand(word,m),(a,b,k,t,m)
        equal,threshold=eventually_equal(word,target,threshold)
        if equal:
            hits.append(t)
        maximum_segments=max(maximum_segments,len(word))
        current_width=width(word)
        assert current_width[0]==2*k
        if current_width[1]>6*k:
            return {'threshold':threshold,'steps':t,'hits':hits,
                    'maximum_segments':maximum_segments}
    return {'threshold':threshold,'steps':10*k+4,'hits':hits,
            'maximum_segments':maximum_segments}


def positive_controls():
    controls=[]
    families=[]
    families.append((2,4,encoded_family(0,1,1),encoded_family(0,1,1,1)))
    four=[]
    four_target=[]
    for out,shift in ((four,0),(four_target,1)):
        append(out,(0,),1,2+shift)
        append(out,(3,2,3),0,3)
        append(out,(3,),1,shift)
        append(out,(0,1),0,2)
    families.append((4,6,four,four_target))
    for base,period,word,target in families:
        threshold=3
        for t in range(period):
            pal,threshold=eventually_equal(word,reverse_word(word),threshold)
            assert not pal
            word,threshold=add_word(word,threshold,base)
        equal,threshold=eventually_equal(word,target,threshold)
        assert equal
        controls.append({'base':base,'period':period,
                         'all_parameter_threshold':threshold,
                         'return_identity':True,'all_phases_nonpalindromic':True})
    return controls


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--max-k',type=int,default=3)
    parser.add_argument('--validate',action='store_true')
    parser.add_argument('--all-pairs',action='store_true')
    parser.add_argument('--controls-only',action='store_true')
    parser.add_argument('--random-count',type=int,default=0)
    parser.add_argument('--random-seed',type=int,default=19610413)
    args=parser.parse_args()
    controls=positive_controls()
    if args.controls_only:
        print(json.dumps({'positive_controls':controls},indent=2))
        return
    if args.random_count:
        rng=random.Random(args.random_seed)
        started=time.monotonic()
        threshold=3
        for _ in range(args.random_count):
            k=rng.choice((3,4,5,6))
            Q=10**k
            a=rng.randrange(Q)
            b=rng.randrange(Q//10,Q)
            r=check_code(a,b,k,True)
            threshold=max(threshold,r['threshold'])
            assert not r['hits']
        print(json.dumps({'status':'passed','count':args.random_count,
                          'widths':[3,4,5,6],'seed':args.random_seed,
                          'ordinary_integer_validation_parameters':'M, M+1, M+7 at each symbolic step',
                          'largest_threshold':threshold,'positive_controls':controls,
                          'seconds':time.monotonic()-started},indent=2))
        return
    result={'claim':'exact eventual periodic-block arithmetic; not a decimal existence proof',
            'validated_numerically':args.validate,'positive_controls':controls,'widths':[]}
    for k in range(1,args.max_k+1):
        started=time.monotonic()
        Q=10**k
        tested=0
        threshold=3
        max_steps=0
        max_segments=0
        hits=[]
        for b in range(Q//10,Q):
            choices=range(Q) if args.all_pairs else range((-Q*b)%99,Q,99)
            for a in choices:
                r=check_code(a,b,k,args.validate)
                tested+=1
                threshold=max(threshold,r['threshold'])
                max_steps=max(max_steps,r['steps'])
                max_segments=max(max_segments,r['maximum_segments'])
                if r['hits']: hits.append({'a':a,'b':b,**r})
        row={'k':k,'tested':tested,'uniform_threshold':threshold,
             'maximum_steps':max_steps,'maximum_segments':max_segments,
             'eventual_returns':hits,'seconds':time.monotonic()-started}
        result['widths'].append(row)
        print(json.dumps(row),flush=True)
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
