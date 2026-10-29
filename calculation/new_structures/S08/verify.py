from dataclasses import dataclass
from math import lcm
from typing import Tuple

@dataclass(frozen=True)
class E:
    q:int=0; k:int=0; c:int=0
    def __add__(self,o):
        if isinstance(o,int): o=E(c=o)
        return E(self.q+o.q,self.k+o.k,self.c+o.c)
    __radd__=__add__
    def __neg__(self): return E(-self.q,-self.k,-self.c)
    def __sub__(self,o): return self+(-o if isinstance(o,E) else -o)
    def __mul__(self,n): return E(self.q*n,self.k*n,self.c*n)
    __rmul__=__mul__
    def val(self,q,k): return self.q*q+self.k*k+self.c
    def __str__(self): return f'{self.q}q+{self.k}k+{self.c}'
Q=E(q=1); K=E(k=1)
@dataclass(frozen=True)
class R:
    word:Tuple[int,...]; n:E
    def length(self): return self.n*len(self.word)
class CannotProve(Exception): pass

def nonnegative(e,qmin,kmin):
    if e.q<0 or e.k<0 or e.val(qmin,kmin)<0:
        raise CannotProve('count not uniformly >=0: '+str(e))
def run(w,n=1): return R(tuple(w),E(c=n) if isinstance(n,int) else n)
def clean(seq):
    out=[]
    for r in seq:
        if not r.word or r.n==E(): continue
        if out and out[-1].word==r.word:
            out[-1]=R(r.word,out[-1].n+r.n)
        elif out and out[-1].n.q==out[-1].n.k==r.n.q==r.n.k==0 and len(out[-1].word)*out[-1].n.c+len(r.word)*r.n.c<=8192:
            old=out.pop();out.append(run(old.word*old.n.c+r.word*r.n.c))
        else: out.append(r)
    return out
def choose(a,b,qmin,kmin):
    d=a-b
    if d.q>=0 and d.k>=0 and d.val(qmin,kmin)>=0: return b
    if d.q<=0 and d.k<=0 and d.val(qmin,kmin)<=0: return a
    raise CannotProve('ambiguous symbolic boundary comparison '+str(a)+' vs '+str(b))
def eat(r:R,amt:E,qmin,kmin):
    m=len(r.word)
    if amt.q%m or amt.k%m:
        raise CannotProve('parameter-dependent cut phase '+str(amt)+' mod '+str(m))
    t=E(amt.q//m,amt.k//m,amt.c//m); rem=amt.c%m
    if rem:
        n=r.n-t-E(c=1);nonnegative(n,qmin,kmin)
        return clean([R(r.word[rem:]+r.word[:rem],n),run(r.word[rem:])])
    n=r.n-t;nonnegative(n,qmin,kmin)
    return clean([R(r.word,n)])
def add_runs(a:R,b:R,amt:E,qmin,kmin):
    if amt.q==0 and amt.k==0:
        return [run([a.word[i%len(a.word)]+b.word[i%len(b.word)] for i in range(amt.c)])]
    m=lcm(len(a.word),len(b.word))
    if amt.q%m or amt.k%m:
        raise CannotProve('parameter-dependent paired phase '+str(amt)+' mod '+str(m))
    w=tuple(a.word[i%len(a.word)]+b.word[i%len(b.word)] for i in range(m))
    copies=E(amt.q//m,amt.k//m,amt.c//m);nonnegative(copies,qmin,kmin);rem=amt.c%m
    return clean([R(w,copies),run(w[:rem])])
def zip_pair(left,right,qmin,kmin,compare=False,limit=25000):
    aa=clean(left);bb=clean(right);out=[];pos=E();iterations=0
    while aa and bb:
        iterations+=1
        if iterations>limit: raise CannotProve('symbolic fragment limit')
        a,b=aa[0],bb[0];amt=choose(a.length(),b.length(),qmin,kmin)
        if amt.val(qmin,kmin)<=0: raise CannotProve('zero-width interval at bound')
        if compare:
            period=lcm(len(a.word),len(b.word)) if amt.q or amt.k else amt.c
            cap=min(amt.val(qmin,kmin),period)
            for h in range(cap):
                if a.word[h%len(a.word)]!=b.word[h%len(b.word)]:
                    return {'return':False,'first_mismatch':str(pos+E(c=h)),
                            'observed':a.word[h%len(a.word)],'expected':b.word[h%len(b.word)]}
            if cap<period and (amt.q!=0 or amt.k!=0):
                raise CannotProve('too short for universal period equality')
        else: out+=add_runs(a,b,amt,qmin,kmin)
        pos+=amt;aa=eat(a,amt,qmin,kmin)+aa[1:];bb=eat(b,amt,qmin,kmin)+bb[1:]
    if aa or bb: raise CannotProve('symbolic unequal total lengths')
    return {'return':True,'length':str(pos)} if compare else clean(out)
def reverse(s): return [R(r.word[::-1],r.n) for r in reversed(s)]
def normalized(s,qmin,kmin):
    carry=0;out=[]
    for r in s:
        if r.n==E(): continue
        nonnegative(r.n-E(c=1),qmin,kmin)
        d=[];c=carry
        for a in r.word: z=a+c;d.append(z%10);c=z//10
        out.append(run(d));stable=[];cc=c
        for a in r.word: z=a+cc;stable.append(z%10);cc=z//10
        if cc!=c: raise CannotProve('block carry transducer not idempotent')
        out.append(R(tuple(stable),r.n-E(c=1)));carry=c
    if carry: out.append(run([carry]))
    return clean(out),carry
def step(s,qmin,kmin):
    d,g=normalized(s,qmin,kmin)
    return zip_pair(d,reverse(d),qmin,kmin),g
def tpl(B,W,J,U,C):
    H=[run(B),R(tuple(W),Q),run(J),R(tuple(U),K)]
    return clean(H+[run(C)]+reverse(H))
def replay(B,W,J,U,C,qmin=20,kmin=20,nsteps=120):
    current=tpl(B,W,J,U,C);gam=[];odd=[]
    for t in range(nsteps):
        offset=E();witness=None
        for r in current:
            for h,x in enumerate(r.word):
                if x&1 and r.n.val(qmin,kmin)>=1:
                    witness=str(offset+E(c=h));break
            if witness is not None: break
            offset+=r.length()
        odd.append(witness)
        current,g=step(current,qmin,kmin);gam.append(g)
        if len(current)>10000: raise CannotProve('atom explosion')
    expected=tpl(B,W,J,U,C);delta=5*(nsteps//120)
    expected=[R(a.word,a.n+E(c=delta)) if a.n.k else a for a in expected]
    ans=zip_pair(current,expected,qmin,kmin,compare=True)
    ans.update({'gamma':''.join(map(str,gam)),'sum_gamma':sum(gam),
                'fragment_count':len(current),'q_min':qmin,'k_min':kmin,
                'clock_exact':gam==[1,0,0,0]*(nsteps//4),
                'odd_witnesses_complete':all(x is not None for x in odd),
                'first_missing_odd_witness':next((i for i,x in enumerate(odd) if x is None),None)})
    return ans

B4=[10,4,7,5,13,6,11,1,9,16,16,18,10,9,4,8,1,7,0,2,15,15,9,7,7,10,17,14,18,8,6,6,18,4]
W4=[8,1,15,4,0,5,5,18,4]
J=[17,5,5,9,6,6,6,14,5,11,7,10,14,7,8,15,9,6,4,18,9,10,17,2]
U=[18,0,9]

centers=[[a,b,a] for a in range(19) for b in range(0,19,2) if (2*a-b)%11==5]
assert len(centers)==17
for steps,pos,obs,exp in ((120,"9q+0k+35",9,5),(240,"9q+0k+12",6,5)):
    for center in centers:
        ans=replay(B4,W4,J,U,center,512,512,steps)
        assert ans['return'] is False
        assert ans['first_mismatch']==pos,(center,steps,ans)
        assert ans['observed']==obs and ans['expected']==exp,(center,steps,ans)
        assert ans['sum_gamma']==30*(steps//120)
        assert ans['clock_exact'] and ans['odd_witnesses_complete']
    print('SYMBOLIC_CLASS',steps,'centres=',len(centers),'q_min=512','k_min=512',
          'first_mismatch=',pos,'observed=',obs,'expected=',exp)

B8=[10,4,15,4,1,7,9,11,11,18,0,18,6,9,17,4,0,12,0,2,10,1,12,4,2,15,0,13,4,8,4,8,10,15]
W8=[4,0,5,5,18,4,8,1,15]
GAMMA=[1,0,0,0,1,0,0,0,1,0,0,0]
C0=[4,14,4]
def int_tpl(q,k,center=C0):
    h=B4+W4*q+J+U*k
    return h+center+h[::-1]
def int_digits(n): return [int(ch) for ch in str(n)[::-1]]
def int_pair(d): return [d[i]+d[-1-i] for i in range(len(d))]
def normalize_pair(p):
    out=[];carry=0
    for x in p:
        z=x+carry;out.append(z%10);carry=z//10
    while carry:
        out.append(carry%10);carry//=10
    return out
def realize(p):
    d=[0]*len(p)
    for i in range(len(p)//2):
        d[i]=min(p[i],9);d[-1-i]=p[i]-d[i]
        assert 0<=d[i]<=9 and 0<=d[-1-i]<=9
    if len(p)%2:
        assert p[len(p)//2]%2==0
        d[len(p)//2]=p[len(p)//2]//2
    assert d[-1]!=0 and int_pair(d)==p
    return int(''.join(str(x) for x in d[::-1]))
def first_diff(a,b):
    for i,(x,y) in enumerate(zip(a,b)):
        if x!=y:return i
    return min(len(a),len(b)) if len(a)!=len(b) else -1

for q in (20,40,80,160):
    for k in (20,40,80,160):
        p=int_tpl(q,k);n=realize(p);gamma_sum=0;checks={}
        assert int_pair(int_digits(n))==p
        for t in range(240):
            d=int_digits(n);assert int_pair(d)==p
            vdigits=normalize_pair(p)
            n2=n+int(str(n)[::-1]);d2=int_digits(n2)
            assert d2==vdigits,(q,k,t,'integer/vector normalization mismatch')
            p2=int_pair(d2)
            assert p2==int_pair(vdigits),(q,k,t,'pairword mismatch')
            gamma=len(d2)-len(d)
            assert gamma==GAMMA[(4+t)%12],(q,k,t,'overflow clock mismatch')
            gamma_sum+=gamma;n=n2;p=p2
            if t+1==120:
                target=int_tpl(q,k+5)
                assert len(p)==len(target) and first_diff(p,target)==34+9*q+1
                assert p[:34+9*q]==B4+W4*q
                checks[120]=(first_diff(p,target),gamma_sum)
            if t+1==136:
                prefix8=B8+W8*q
                assert first_diff(p[:len(prefix8)],prefix8)==34+9*q-1
                assert p[34+9*q-1]==14 and prefix8[34+9*q-1]==15
                checks[136]=(34+9*q-1,p[34+9*q-1],prefix8[34+9*q-1])
        target=int_tpl(q,k+10);x=34+9*q
        assert gamma_sum==60
        assert first_diff(p,target)==x-22 and p[x-22]==6 and target[x-22]==5
        assert p[:x]!=B4+W4*q
        checks[240]=(first_diff(p,target),p[x-22],target[x-22],gamma_sum)
        print('BIGINT_CONTROL',f'q={q}',f'k={k}',f't120={checks[120]}',
              f't136={checks[136]}',f't240={checks[240]}')
print('S08_ALL_CHECKS_PASSED')
