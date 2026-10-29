#!/usr/bin/env python3
"""Standalone independent checker for decimal aperiodic eight-step centre bridges.
Usage: python3 bridge_certificate.py [bridge_witness.txt]
"""
from pathlib import Path
from functools import lru_cache
from itertools import product
from random import Random
import sys
D='0123456789ABCDEFGHI'
G=(1,0,1,0,1,0,1,0)

def parse(path):
    groups=[]; cur=None
    for line in Path(path).read_text().splitlines():
        t=line.split()
        if not t:continue
        if t[0]=='BRIDGE-SEED':
            if cur:groups.append(cur)
            info=dict(v.split('=',1) for v in t[1:])
            cur={'seed':int(info['q']),'cut':int(info['h']),
                 'state':(int(info['L']),int(info['H']),int(info['Y']))}
        elif t[0] in ('BRIDGEPREFIX','BRIDGEA','BRIDGEB','BRIDGEEXT'):
            assert cur is not None
            cols=tuple(tuple(D.index(z) for z in w) for w in t[2:])
            assert len(cols)==int(t[1][2:])
            assert all(len(c)==8 and all(0<=x<=18 for x in c) for c in cols)
            cur[t[0]]=cols
    if cur:groups.append(cur)
    assert sorted(x['seed'] for x in groups)==[98791,199884]
    return groups

@lru_cache(None)
def transitions(state,column):
    l,h,y=state
    choices=[]; LL=0
    for t,x in enumerate(column):
        low=(l>>t)&1
        LL |= ((x+low)//10)<<t
        candidates=[]
        for carry_hi in (0,1):
            high=(x+carry_hi)//10
            if high != (h>>t)&1: continue
            upper=(x+carry_hi)%10
            lower=(x+low)%10
            yy=(y>>(4*(t//2)))&15 if G[t] else upper
            if lower+yy != column[(t+1)%8]:continue
            candidates.append((carry_hi,upper))
        if not candidates:return ()
        choices.append(candidates)
    result=set()
    for choice in product(*choices):
        H=0;Y=0
        for t,(carry_hi,upper) in enumerate(choice):
            H |= carry_hi<<t
            if G[t]:Y |= upper << (4*(t//2))
        result.add((LL,H,Y))
    return tuple(sorted(result))

def follows(start, columns):
    qs={start}
    for col in columns:
        nexts=set()
        for q in qs:nexts.update(transitions(q,col))
        qs=nexts
        if not qs:break
    return qs

def words_fib(n):
    w='A'
    while len(w)<n:w=''.join('AB' if x=='A' else 'A' for x in w)
    return w[:n]

def words_thue(n):return ''.join('AB'[i.bit_count()%2] for i in range(n))

def revadd(d):
    out=[];carry=0
    for a,b in zip(d,reversed(d)):
        s=a+b+carry;out.append(s%10);carry=s//10
    if carry:out.append(carry)
    return out

def pairs(d):return [d[i]+d[-i-1] for i in range((len(d)+1)//2)]

def check_integer(group,word):
    path=list(group['BRIDGEPREFIX'])
    for c in word:path.extend(group['BRIDGE'+c])
    half=len(path); allcols=path+list(group['BRIDGEEXT'])
    x0=[a[0] for a in path]
    seed=[a//2 for a in x0]+[a-a//2 for a in reversed(x0)]
    assert seed[-1]>0 and seed!=seed[::-1]
    d=seed
    for t in range(9):
        assert d!=d[::-1]
        actual=pairs(d)
        assert actual==[a[t%8] for a in allcols[:len(actual)]],(group['seed'],len(word),t,'pair mismatch')
        if t<8:
            nxt=revadd(d)
            assert len(nxt)==len(d)+G[t]
            d=nxt
    # The first failure of attempted second-period centre renewal is local.
    for t in range(9,17):d=revadd(d)
    actual=pairs(d);target=[a[0] for a in allcols]
    mismatch=next((i for i,(x,y) in enumerate(zip(actual,target)) if x!=y),min(len(actual),len(target)))
    assert mismatch==half+1,(group['seed'],len(word),mismatch,half)
    return half, len(seed), len(d), mismatch

def main():
    path=sys.argv[1] if len(sys.argv)>1 else Path(__file__).with_name('bridge_witness.txt')
    groups=parse(path)
    root=(0,0b01010101,0x1111)
    for group in groups:
        q=group['state'];prefix=group['BRIDGEPREFIX']
        assert len(prefix)==group['cut']
        assert q in follows(root,prefix),(group['seed'],'prefix does not reach q')
        for name in ('BRIDGEA','BRIDGEB'):
            assert q in follows(q,group[name]),(group['seed'],name,'loop not closed')
        assert group['BRIDGEA'] != group['BRIDGEB']
        # Finite suffix plus identical carry state supplies the same centre interface.
        assert group['BRIDGEA'][-6:]==group['BRIDGEB'][-6:]==prefix[-6:]
        assert group['BRIDGEEXT']==group['BRIDGEA'][:2]==group['BRIDGEB'][:2]
        print('FINITE-STATE-PASS seed',group['seed'],'cut',group['cut'],
              'loopA',len(group['BRIDGEA']),'loopB',len(group['BRIDGEB']),
              'q',q,'closed automaton edges')
        # Negative controls: a corrupted coefficient or wrong carry state must fail.
        bad=list(group['BRIDGEB']); changed=list(bad[0])
        changed[0]=(changed[0]+1)%19;bad[0]=tuple(changed)
        assert q not in follows(q,bad), 'mutated loop incorrectly accepted'
        wrong=(q[0]^1,q[1],q[2])
        assert wrong not in follows(wrong,group['BRIDGEA']), 'wrong cut state accepted'
        rng=Random(group['seed'])
        controls=['','A','B','ABA','ABBA','BAAB',words_fib(16),words_thue(16),
                  words_fib(64),words_thue(64),
                  ''.join(rng.choice('AB') for _ in range(120))]
        controls += [''.join('AB' if c=='A' else 'BA' for c in w)
                     for w in (words_fib(60),words_thue(60))]
        for word in controls:
            h,n0,n16,mismatch=check_integer(group,word)
            print('INTEGER-PASS seed',group['seed'],'letters',len(word),
                  'seed_digits',n0,'step16_digits',n16,'first_second-cycle-defect',mismatch)
    print('ALL CHECKS PASSED: 2 rooted states, 4 return loops, 26 independent decimal whole-word tests')
if __name__=='__main__':main()
