"""Exact growing multi-periodic-word family certificates for reverse-add.

Each segment is a periodic word truncated to a*k+b positions.  Unlike the
older affine-run checker, its number of constant runs can grow without bound.
All symbolic branches hold for every integer k>=0; finite tests only discover
candidate families.  Several spatial periods and independent growth rates
are allowed, with parameter residues resolving changing phase alignment.
"""
from dataclasses import dataclass
from math import gcd,lcm
import argparse,json,random,time

class Unresolved(Exception):pass

@dataclass(frozen=True)
class A:
    a:int
    b:int
    def __add__(self,o):
        if isinstance(o,int):o=A(0,o)
        return A(self.a+o.a,self.b+o.b)
    def __sub__(self,o):
        if isinstance(o,int):o=A(0,o)
        return A(self.a-o.a,self.b-o.b)
    def at(self,k):return self.a*k+self.b
    def zero(self):return self.a==self.b==0
    def positive(self):return self.a>=0 and self.b>=1

@dataclass(frozen=True)
class S:
    w:tuple
    n:A

def primitive(w):
    w=tuple(w)
    for p in range(1,len(w)+1):
        if len(w)%p==0 and all(w[i]==w[i%p] for i in range(len(w))):return w[:p]

def rotate(w,j):
    j%=len(w);return w[j:]+w[:j]

def letters(s,n=None):
    n=s.n.b if n is None else n
    return tuple(s.w[i%len(s.w)] for i in range(n))

def norm(ss):
    out=[]
    for s in ss:
        if s.n.zero():continue
        if not s.n.positive():raise Unresolved(('nonpositive',s))
        w=primitive(s.w);s=S(w,s.n)
        if s.n.a%len(w):raise Unresolved(('variable-phase',s))
        if out and out[-1].n.a==0 and s.n.a==0:
            t=out.pop();v=letters(t)+letters(s);s=S(primitive(v),A(0,len(v)))
        if out:
            t=out[-1]
            if len(t.w)==len(s.w) and rotate(t.w,t.n.b)==s.w:
                out[-1]=S(t.w,t.n+s.n);continue
            if t.n.a==0 and s.n.a:
                v=letters(t);p=len(s.w)
                if all(v[-1-j]==s.w[(-1-j)%p] for j in range(len(v))):
                    out.pop();s=S(rotate(s.w,-len(v)),s.n+len(v))
            elif t.n.a and s.n.a==0:
                v=letters(s);p=len(t.w)
                if all(v[j]==t.w[(t.n.b+j)%p] for j in range(len(v))):
                    out[-1]=S(t.w,t.n+len(v));continue
        out.append(s)
    return tuple(out)

def minimum(x,y):
    d=x-y
    if d.a>=0 and d.b>=0:return y
    if d.a<=0 and d.b<=0:return x
    raise Unresolved(('crossing',x,y))

def reverse(ss):
    return tuple(S(tuple(s.w[(s.n.b-1-i)%len(s.w)] for i in range(len(s.w))),s.n) for s in ss[::-1])

def advance(s,n):
    if n.a%len(s.w):raise Unresolved(('advance-phase',s,n))
    return S(rotate(s.w,n.b),s.n-n)

def zipped(a,b,combine):
    a=list(a);b=list(b);i=j=0;out=[]
    while i<len(a) and j<len(b):
        x,y=a[i],b[j];n=minimum(x.n,y.n)
        p=lcm(len(x.w),len(y.w)) if n.a else n.b
        w=tuple(combine(x.w[k%len(x.w)],y.w[k%len(y.w)]) for k in range(p))
        out.append(S(w,n))
        xx=advance(x,n);yy=advance(y,n)
        if xx.n.zero():i+=1
        elif xx.n.positive():a[i]=xx
        else:raise Unresolved(('left-residual',xx))
        if yy.n.zero():j+=1
        elif yy.n.positive():b[j]=yy
        else:raise Unresolved(('right-residual',yy))
    if i!=len(a) or j!=len(b):raise Unresolved('unequal-lengths')
    return norm(out)

def digit_family(q,base=10):
    out=[];c=0
    for s in q:
        if s.n.a==0:
            ds=[]
            for v in letters(s):ds.append((v+c)%base);c=(v+c)//base
            out.append(S(tuple(ds),s.n));continue
        p=len(s.w)
        if s.n.b<p:raise Unresolved(('short-variable-segment',s))
        first=[]
        for v in s.w:first.append((v+c)%base);c=(v+c)//base
        stable=c;ds=[]
        for v in s.w:ds.append((v+c)%base);c=(v+c)//base
        if c!=stable:raise AssertionError('carry did not stabilize in one word')
        if first==ds:out.append(S(tuple(ds),s.n))
        else:
            out.append(S(tuple(first),A(0,p)))
            out.append(S(tuple(ds),s.n-p))
        c=stable
        for v in s.w[:s.n.b%p]:c=(v+c)//base
    if c:out.append(S((c,),A(0,1)))
    return norm(out)

def step(q,base=10):
    d=digit_family(q,base)
    return zipped(d,reverse(d),lambda a,b:a+b)

def expand(q,k=0):return tuple(v for s in q for v in letters(s,s.n.at(k)))
def same(a,b):
    z=zipped(a,b,lambda x,y:int(x!=y))
    return all(all(v==0 for v in (s.w if s.n.a else s.w[:min(len(s.w),s.n.b)])) for s in z)

def safe(q,base=10):
    if base!=10:
        # The special decimal bad-word criterion must not be generalized to
        # base two. Instead find an actual digit mismatch persisting for all k.
        d=digit_family(q,base)
        diffs=zipped(d,reverse(d),lambda a,b:int(a!=b))
        return any(any(v for v in s.w[:min(len(s.w),s.n.b)]) for s in diffs)
    # Every segment present at k=0 remains a prefix of that segment for k>=0.
    # Thus each positive safety witness persists for the entire family.
    present=[v for s in q for v in s.w[:min(len(s.w),s.n.b)]]
    return max(present)>=base and (q[0].w[0]!=base+1 or any(v not in (0,base+1) for v in present))

def numeric_step(q,base=10):
    d=[];c=0
    for v in q:d.append((v+c)%base);c=(v+c)//base
    if c:d.append(c)
    return tuple(x+y for x,y in zip(d,d[::-1]))

def compress(q,maxperiod=6,minlength=8):
    """Discovery only: greedily split literal/long periodic blocks."""
    out=[];literal=[];i=0;n=len(q)
    def flush():
        if literal:out.append((tuple(literal),len(literal),False));literal.clear()
    while i<n:
        best=(0,0)
        for p in range(1,maxperiod+1):
            if i+max(minlength,3*p)>n:continue
            j=i+p
            while j<n and q[j]==q[i+(j-i)%p]:j+=1
            length=j-i
            if length>=max(minlength,3*p) and length-p>best[0]-best[1]:best=(length,p)
        length,p=best
        if p:
            flush();out.append((tuple(q[i:i+p]),length,True));i+=length
        else:literal.append(q[i]);i+=1
    flush();return out

def candidate(start,end,period,base=10,max_residues=24):
    if len(start)!=len(end):return None,'shape'
    ds=[];L=1
    for (u,m,r),(v,n,s) in zip(start,end):
        if u!=v or r!=s or (not r and m!=n):return None,'shape'
        d=n-m
        if d<0:return None,'shrinking'
        ds.append(d)
        if d:L=lcm(L,len(u))
    if not any(ds):return None,'no-growth'
    # All variable coefficients must be multiples of every spatial period.
    for u,m,r in start:L=lcm(L,len(u)) if r else L
    residue=L
    if residue>max_residues:return None,'residue-cap'
    for shift in (0,2,8,32):
        proof=[];ok=True
        for r in range(residue):
            try:
                q=norm([S(u,A(residue*d,m+(shift+r)*d)) for (u,m,_),d in zip(start,ds)])
                goal=norm([S(u,A(residue*d,m+(shift+r+1)*d)) for (u,m,_),d in zip(start,ds)])
                if not same(q,reverse(q)):return None,'not-symmetric'
                q0=expand(q)
                if not q0 or q0[0]<=0:return None,'not-valid'
                if any(v<0 or v>2*base-2 for s in q for v in s.w):return None,'not-valid'
                if len(q0)%2 and q0[len(q0)//2]%2:return None,'odd-center'
                # Symmetry is universal, and total parity is invariant because
                # all nonzero slopes occur in reflected pairs. Odd-center
                # symbol must also be stable for every k; inspect k=1 and prove
                # below using a center split after the final successful check.
                q1=expand(q,1)
                if len(q1)%2 and q1[len(q1)//2]%2:return None,'odd-center'
                w=q
                for t in range(period):
                    if not safe(w,base):return None,'unsafe'
                    w=step(w,base)
                if not same(w,goal):ok=False;break
                proof.append({'residue':r,'initial':serialize(q),'target':serialize(goal)})
            except Unresolved:ok=False;break
        if ok:
            # Enforce validity independently for all k using the middle segment.
            for data in proof:
                q=deserialize(data['initial'])
                if not all_center_even(q):return None,'center-unresolved'
            raw=expand(deserialize(proof[0]['initial']))
            d=expand(digit_family(deserialize(proof[0]['initial']),base))
            return {'status':'EXACT_PERIODIC_BLOCK_IDENTITY','base':base,'period':period,'residues':residue,'shift':shift,'growth':ds,'family':proof,'seed_digits_lsf':list(d),'seed_q':list(raw)},'certificate'
    return None,'unresolved-or-not-identity'

def all_center_even(q):
    # Exact check of every possible center location, including locations that
    # cross segment boundaries as k grows. Residues freeze both width parity
    # and the central position modulo every motif period.
    total=A(sum(s.n.a for s in q),sum(s.n.b for s in q))
    prefix=A(0,0)
    for s in q:
        R=2*len(s.w)
        for r in range(R):
            if total.at(r)%2==0:continue
            off=A(total.a*R//2-prefix.a*R,(total.at(r)-1)//2-prefix.at(r))
            rem=A(s.n.a*R-off.a,s.n.at(r)-off.b-1)
            lo=0;hi=None;possible=True
            for e in (off,rem):
                if e.a>0:lo=max(lo,-(e.b//e.a))
                elif e.a<0:
                    upper=e.b//(-e.a);hi=upper if hi is None else min(hi,upper)
                elif e.b<0:possible=False
            if possible and (hi is None or lo<=hi):
                assert off.a%len(s.w)==0
                if s.w[off.b%len(s.w)]%2:return False
        prefix=prefix+s.n
    return True

def serialize(q):return [[list(s.w),s.n.a,s.n.b] for s in q]
def deserialize(q):return tuple(S(tuple(w),A(a,b)) for w,a,b in q)

def controls():
    rng=random.Random(196)
    checks=0
    for base in (2,3,10):
        for test in range(100):
            patterns=[tuple(rng.randrange(2*base-1) for _ in range(rng.randint(1,4))) for j in range(3)]
            L=lcm(*(len(w) for w in patterns));half=[]
            for w in patterns:half.append(S(w,A(L*rng.randrange(3),rng.randrange(8,20)*len(w))))
            q=norm(half+[S((2*rng.randrange(base),),A(0,1))]+list(reverse(half)))
            for t in range(8):
                try:nxt=step(q,base)
                except Unresolved:break
                for k in (0,1,2,7):
                    assert expand(nxt,k)==numeric_step(expand(q,k),base);checks+=1
                q=nxt
    # An intentional variable-phase ambiguity must be refused.
    try:norm([S((1,2),A(1,9))]);raise AssertionError('accepted variable phase')
    except Unresolved:pass
    # Known binary growing run certificate also validates this richer engine.
    # Imported only as a positive test fixture, never as search/discovery code.
    import importlib.util
    spec=importlib.util.spec_from_file_location('old','exist_affine_runs.py');old=importlib.util.module_from_spec(spec)
    import sys;sys.modules['old']=old;spec.loader.exec_module(old)
    binary=old.controls();fam=binary['family'];period=binary['period']
    fam=[(v,a,b+2*a) for v,a,b in fam]
    q=norm([S((v,),A(a,b)) for v,a,b in fam]);w=q
    for t in range(period):assert safe(w,2);w=step(w,2)
    assert same(w,norm([S((v,),A(a,b+a)) for v,a,b in fam]))
    return {'exact_numeric_comparisons':checks,'binary_positive_control_period':period}

def search(count,steps,maxperiod,stride,seed,seconds):
    rng=random.Random(seed);starttime=time.monotonic();stats={};attempted=set();best=[]
    for it in range(count):
        half=[]
        for j in range(rng.randint(2,4)):
            p=rng.randint(2,maxperiod)
            motif=tuple(rng.randrange(19) for _ in range(p))
            if not half and motif[0]==0:motif=(rng.randrange(1,19),)+motif[1:]
            half.extend(motif*rng.randint(4,15))
            half.extend(rng.randrange(19) for _ in range(rng.randrange(4)))
        middle=[] if rng.randrange(2) else [2*rng.randrange(10)]
        q=tuple(half+middle+half[::-1]);seen={};why='step-cap'
        for t in range(steps):
            if not (max(q)>=10 and (q[0]!=11 or any(x not in (0,11) for x in q))):why='palindrome';break
            if t%stride==0:
                compressed=compress(q,maxperiod)
                key=tuple((w,r) for w,n,r in compressed)
                if any(r for w,n,r in compressed):
                    for u,old in seen.get(key,[])[-3:]:
                        signature=(key,tuple(n-m for (_,m,_),(_,n,_) in zip(old,compressed)),t-u)
                        if signature in attempted:continue
                        attempted.add(signature)
                        cert,result=candidate(old,compressed,t-u)
                        stats['candidate:'+result]=stats.get('candidate:'+result,0)+1
                        if cert:return {'attempts':it+1,'certificate':cert,'stats':stats,'seconds':time.monotonic()-starttime}
                    seen.setdefault(key,[]).append((t,compressed))
            q=numeric_step(q)
        stats[why]=stats.get(why,0)+1
        best.append((t,len(q)));best=sorted(best,reverse=True)[:10]
        if (it+1)%25==0:print(json.dumps({'attempts':it+1,'seconds':time.monotonic()-starttime,'stats':stats}),flush=True)
        if time.monotonic()-starttime>=seconds:break
    return {'attempts':it+1,'stats':stats,'seconds':time.monotonic()-starttime,'best':best,'decimal_existence_proved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--count',type=int,default=200);p.add_argument('--steps',type=int,default=360);p.add_argument('--maxperiod',type=int,default=4);p.add_argument('--stride',type=int,default=6);p.add_argument('--seed',type=int,default=20261013);p.add_argument('--seconds',type=float,default=180);p.add_argument('--out',default='astra_substitution_periodic_results.json');args=p.parse_args()
    control=controls();print(json.dumps({'controls':control}),flush=True)
    out=search(args.count,args.steps,args.maxperiod,args.stride,args.seed,args.seconds);out['controls']=control
    with open(args.out,'w') as f:json.dump(out,f,indent=2)
    print(json.dumps(out),flush=True)
