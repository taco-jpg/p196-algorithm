#!/usr/bin/env python3
"""N20 affine-strip digit/carry certificate; mathematical proof in report.
Reproduce from repository root:
 python3 calculation/new_structures/agent-N20/affine_sheet.py --self-test --control-b9 --replay 20000
"""
import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Aff:
    a: int
    b: int
    def at(self, q):
        return self.a*q+self.b

@dataclass(frozen=True)
class Strip:
    lo: Aff
    hi: Aff
    pattern: tuple
    def at(self, q, i):
        assert self.lo.at(q)<=i<self.hi.at(q)
        return self.pattern[(i-self.lo.at(q))%len(self.pattern)]

@dataclass
class Phase:
    digits: list
    carries: list
    n0: int
    gain: int
    witness: int
    def length(self, q):
        return self.n0+self.gain*q

def evaluate(strips,q,i):
    for s in strips:
        if s.lo.at(q)<=i<s.hi.at(q):
            return s.at(q,i)
    raise AssertionError(('missing-cell',q,i))

def boundaries(phase,nxt,wrap):
    """Breakpoints of every local recurrence term in source coordinate i."""
    n=Aff(phase.gain,phase.n0)
    bd=[Aff(0,0),n,Aff(0,phase.witness),
        Aff(n.a,n.b-1-phase.witness)]
    for strips in (phase.digits,phase.carries):
        for s in strips:
            bd.extend((s.lo,s.hi))
    for s in phase.digits:
        for b in (s.lo,s.hi):
            bd.append(Aff(n.a-b.a,n.b-b.b))
    for s in phase.carries:
        for b in (s.lo,s.hi):
            bd.append(Aff(b.a,b.b-1))
    for s in nxt.digits:
        for b in (s.lo,s.hi):
            bd.append(Aff(b.a,b.b+b.a*wrap))
    return list(set(bd))

def tail_cutoff(phases):
    """After Q, different-slope boundaries are separated by >=M;
    all growing intervals see every residue, fixed-width intervals translate
    by multiples of M under q->q+M. Hence finite universal checking.
    """
    M=math.lcm(*(len(s.pattern) for p in phases for s in p.digits+p.carries))
    Q=0
    for p,phase in enumerate(phases):
        nxt=phases[(p+1)%len(phases)]
        bd=boundaries(phase,nxt,p==len(phases)-1)
        for f in bd:
            for g in bd:
                if f.a<g.a:
                    Q=max(Q,(M+f.b-g.b+g.a-f.a-1)//(g.a-f.a))
    return max(0,Q),M

def validate(phases,base):
    assert base>=2 and phases
    gain=phases[0].gain
    assert gain>=0
    for p,phase in enumerate(phases):
        assert phase.gain==gain
        for strips,offset,maxval in ((phase.digits,0,base-1),
                                     (phase.carries,1,1)):
            assert strips and strips[0].lo==Aff(0,0)
            assert strips[-1].hi==Aff(gain,phase.n0+offset)
            for j,s in enumerate(strips):
                assert s.pattern and all(isinstance(v,int) and
                                0<=v<=maxval for v in s.pattern)
                assert s.lo.a<=s.hi.a
                assert s.lo.b<=s.hi.b
                if j: assert strips[j-1].hi==s.lo
        assert phase.n0>=2 and 0<=phase.witness<phase.n0//2
        assert evaluate(phase.carries,0,0)==0
        nxt=phases[(p+1)%len(phases)]
        gamma=nxt.n0-phase.n0+(gain if p==len(phases)-1 else 0)
        assert gamma in (0,1),(p,gamma)

def verify(phases,base,verbose=False):
    """PAPER-PROVED finite all-q criterion, not a heuristic finite replay."""
    validate(phases,base)
    Q,M=tail_cutoff(phases)
    checks=0
    for q in range(Q+M):
        for p,phase in enumerate(phases):
            n=phase.length(q)
            nq=q+(p==len(phases)-1)
            nxt=phases[(p+1)%len(phases)]
            gamma=nxt.length(nq)-n
            assert 0<=gamma<=1
            source=[evaluate(phase.digits,q,i) for i in range(n)]
            carries=[evaluate(phase.carries,q,i) for i in range(n+1)]
            dest=[evaluate(nxt.digits,nq,i) for i in range(n+gamma)]
            if carries[0]!=0 or source[-1]==0:
                raise ValueError(('boundary/leading',p,q))
            k=phase.witness
            if source[k]==source[n-1-k]:
                raise ValueError(('palindrome-witness',p,q,k))
            for i in range(n):
                v=source[i]+source[n-1-i]+carries[i]
                if v%base!=dest[i] or v//base!=carries[i+1]:
                    raise ValueError(('recurrence',p,q,i,v))
                checks+=1
            if carries[n]!=gamma:
                raise ValueError(('overflow',p,q,carries[n],gamma))
            if gamma and dest[n]!=1:
                raise ValueError(('new-leading',p,q,dest[n]))
    if verbose:
        print('AFFINE SHEET: PAPER PROOF criterion passed; base',base,
              'phases',len(phases),'Q',Q,'M',M,'q tests',Q+M,
              'digit recurrences',checks)
    return {'base':base,'phases':len(phases),'Q':Q,'M':M,
            'q_tests':Q+M,'cells':checks}

def norm_pair(B,W,l,base):
    pair=B+[W[i%len(W)] for i in range(l)]+B[::-1]
    out=[];c=0
    for x in pair:
        t=x+c
        out.append(t%base);c=t//base
    if c:out.append(c)
    assert out[-1]
    return out

def add_reverse(digits,base):
    carries=[0];out=[]
    for i,x in enumerate(digits):
        t=x+digits[-1-i]+carries[-1]
        out.append(t%base)
        carries.append(t//base)
    if carries[-1]:out.append(carries[-1])
    return out,carries

def extract_insert(a,b,c,width,cut):
    """Check one fixed insertion cut against q=0,1,2, not just one gap."""
    assert len(b)==len(a)+width and len(c)==len(a)+2*width
    w=tuple(b[cut:cut+width])
    assert b==a[:cut]+list(w)+a[cut:]
    assert c==a[:cut]+list(w)*2+a[cut:]
    return w

def piecewise(a,band,cut,gain):
    left=[Strip(Aff(0,i),Aff(0,i+1),(v,)) for i,v in enumerate(a[:cut])]
    center=[Strip(Aff(0,cut),Aff(gain,cut),tuple(band))]
    right=[Strip(Aff(gain,cut+i),Aff(gain,cut+i+1),(v,))
           for i,v in enumerate(a[cut:])]
    return left+center+right

def build_b9_control(cert):
    """Reconstruct digit formula AND ordinary-add carries from repository
    base-9 pairword control; no new base-9 certificate is claimed."""
    base=cert['base'];T=cert['p'];gain=cert['S_p']
    assert base==9 and T==10 and gain==4
    cut=62;phases=[];prefix=[0]
    for g in cert['gam']:prefix.append(prefix[-1]+g)
    assert prefix[-1]==gain
    for p in range(T):
        B=cert['B_t'][p];W=cert['w_t'][p]
        d=[];c=[]
        for q in range(3):
            ds=norm_pair(B,W,cert['l0']+prefix[p]+gain*q,base)
            _,carry=add_reverse(ds,base)
            d.append(ds);c.append(carry)
        wd=extract_insert(*d,gain,cut)
        wc=extract_insert(*c,gain,cut)
        witness=next(k for k in range(cut) if d[0][k]!=d[0][-1-k])
        phases.append(Phase(piecewise(d[0],wd,cut,gain),
                     piecewise(c[0],wc,cut,gain),len(d[0]),gain,witness))
    return phases

def expand(strips,q):
    return [x for s in strips for x in
            (s.pattern[k%len(s.pattern)] for k in
             range(s.hi.at(q)-s.lo.at(q)))]

def independent_replay(phases,base,steps):
    """Evolve actual digit arrays, never the finite-checker transition."""
    ds=expand(phases[0].digits,0)
    for t in range(steps):
        p=t%len(phases);q=t//len(phases)
        predicted=phases[p]
        if len(ds)!=predicted.length(q):
            raise AssertionError(('length',t))
        if ds!=expand(predicted.digits,q):
            raise AssertionError(('digit',t))
        if ds==ds[::-1]:
            raise AssertionError(('palindrome',t))
        ds,_=add_reverse(ds,base)
    return len(ds)

def self_test():
    # False base-ten fixed point 21 -> 33 must fail.
    p=Phase(piecewise([1,2],(0,),1,0),
            piecewise([0,0,0],(0,),1,0),2,0,0)
    try:verify([p],10)
    except (AssertionError,ValueError):pass
    else:raise AssertionError('negative control was accepted')
    print('SELF TEST: rejects false decimal fixed point')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--control-b9',action='store_true')
    ap.add_argument('--self-test',action='store_true')
    ap.add_argument('--replay',type=int,default=2000)
    args=ap.parse_args()
    if args.self_test:self_test()
    if args.control_b9:
        for rec in (0,1):
            path=Path(f'calculation/decimal_frontier/lattice_formats/cert_b9_rec{rec}.json')
            cert=json.loads(path.read_text())
            phases=build_b9_control(cert)
            print('CONTROL b9 rec',rec,json.dumps(verify(phases,9,True),sort_keys=True))
            print('Independent digit-list replay:',args.replay,
                  'steps; final digits:',independent_replay(phases,9,args.replay))
            old=phases[0].digits[62]
            phases[0].digits[62]=Strip(old.lo,old.hi,
                                       tuple((v+1)%9 for v in old.pattern))
            try:verify(phases,9)
            except ValueError:print('Corruption control: rejected changed band')
            else:raise AssertionError('Corruption accepted')

if __name__=='__main__':main()
