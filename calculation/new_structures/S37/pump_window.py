#!/usr/bin/env python3
"""S37: exact physical two-cut pumping sufficient-condition checker.

A PASS is a conditional *all-q,k* certificate for a fixed d-periodic seam family,
provided the finite local insertion lemma in reports/AgentS37CyclicSeamPumping.md is accepted.  No ordinary
finite-horizon sampling is promoted.  Ordinary decimal integer arithmetic is
independently cross-checked at the d reference widths.

Supply a JSON file with Q,K,B,W,U,J,C where J,C are arrays of d finite words.
All words are LSD-first coefficient words (entries 0..18).  The family is
P(q,k) = H(q,k) + C[k%d] + reverse(H(q,k)),
H(q,k)=B + W*q + J[k%d] + U*k, q>=Q,k>=K.
Target is P(q,k+gain) after `steps` ordinary reverse-add steps.
"""
import json, argparse, sys

def norm(p):
    d=[]; carry=0; carries=[0]
    for x in p:
        z=x+carry; d.append(z%10); carry=z//10; carries.append(carry)
    if carry:d.append(carry)
    return d,carry,carries

def normfrom(w,carry):
    d=[]
    for x in w:
        z=x+carry;d.append(z%10);carry=z//10
    return d,carry

def folded(p):
    d,g,c=norm(p)
    return [x+y for x,y in zip(d,reversed(d))],d,g,c

def tmpl(B,W,U,J,C,q,k):
    h=B+W*q+J[k%len(J)]+U*k
    return h+C[k%len(C)]+h[::-1]

def realize(p):
    if p!=p[::-1]:raise ValueError('input coefficient word is asymmetric')
    n=len(p); d=[0]*n
    for i in range(n//2):
        a=p[i]; hi=min(a,9);lo=a-hi
        if not 0<=lo<=9:raise ValueError('unrealizable coefficient')
        d[i]=lo;d[n-i-1]=hi
    if n&1:
        if p[n//2]&1:raise ValueError('odd central coefficient')
        d[n//2]=p[n//2]//2
    if d[-1]==0:raise ValueError('leading zero')
    x=0
    for z in reversed(d):x=10*x+z
    return x

def actualpairs(n):
    d=[]
    while n:
        n,x=divmod(n,10);d.append(x)
    return [x+y for x,y in zip(d,reversed(d))]

def reverse_num(n):
    r=0
    while n:
        n,x=divmod(n,10);r=10*r+x
    return r

def trace_and_oracle(p,steps):
    n=realize(p); out=[]
    for t in range(steps+1):
        if actualpairs(n)!=p:raise ValueError(f'independent integer mismatch at step {t}')
        if t==steps:return out,p
        nxt,d,g,c=folded(p)
        out.append((p,d,g,c))
        n=n+reverse_num(n)
        p=nxt

def one_cut(trace,cut,word):
    """Check *per phase* exact carry loops, overflow-one seam alignment."""
    V=word[:]; transcript=[]
    for t,(p,d,g,c) in enumerate(trace):
        n=len(p);b=n-cut
        if not 0<cut<b<n: return {'ok':False,'step':t,'reason':'non-interior cut'}
        lo,cl=normfrom(V,c[cut]); hi,ch=normfrom(V[::-1],c[b])
        if cl!=c[cut]:return {'ok':False,'step':t,'reason':'low carry did not reset'}
        if ch!=c[b]:return {'ok':False,'step':t,'reason':'upper carry did not reset'}
        if g and d[b]!=hi[0]:return {'ok':False,'step':t,'reason':'upper lag seam mismatch'}
        m=len(V)
        successor=[lo[i]+hi[(m-1-i if not g else -i)%m] for i in range(m)]
        transcript.append((V,g,successor))
        V=successor
    return {'ok':True,'return':V==word,'terminal_word':V,'transcript':transcript}

def check(cfg):
    B,W,U=map(lambda n:list(cfg[n]),('B','W','U'))
    J=[list(x) for x in cfg['J']]; C=[list(x) for x in cfg['C']]
    Q=int(cfg['Q']); K=int(cfg['K']);d=len(J)
    steps=int(cfg.get('steps',120));gain=int(cfg.get('gain',5))
    if steps != 120 or gain != 5:
        raise ValueError('this checker certifies only the 120-step k -> k+5 return')
    iw=int(cfg['W_cut_copies']); iu=int(cfg['U_cut_copies'])
    assert d>0 and len(C)==d
    assert Q>=2 and K>=2*d and 0<iw<Q and 0<iu<K
    assert all(len(j)==len(J[0]) for j in J),'seam lengths must agree'
    assert all(len(c)==len(C[0]) for c in C),'centre lengths must agree'
    assert all(c==c[::-1] for c in C),'C must be palindromic'
    assert all(0<=x<=18 for word in [B,W,U]+J+C for x in word)
    assert all(len(c)%2==0 or c[len(c)//2]%2==0 for c in C)
    assert B[0]>0 and len(W)==9 and len(U)==3
    assert gain>0 and steps>0
    outputs=[]
    for j in range(d):
        q=Q;k=K+j
        p=tmpl(B,W,U,J,C,q,k)
        tr,terminal=trace_and_oracle(p,steps)
        target=tmpl(B,W,U,J,C,q,k+gain)
        clock=''.join(str(x[2]) for x in tr)
        gamma_target='1000'*30
        odd_good=all(any(x&1 for x in x0[0]) for x0 in tr)
        cw=len(B)+iw*9
        cu=len(B)+q*9+len(J[k%d])+iu*3
        # The U cut inserts d *full* U copies, so it preserves k mod d.
        pW=one_cut(tr,cw,W)
        pU=one_cut(tr,cu,U*d)
        flags={'actual_return':terminal==target,'correct_clock':clock==gamma_target,
               'odd_guards':odd_good,'W_port':pW['ok'] and pW['return'],
               'U_port':pU['ok'] and pU['return']}
        outputs.append({'residue':j,'q':q,'k':k,'pass':all(flags.values()),
                        'flags':flags,'W_detail':{x:v for x,v in pW.items() if x!='transcript'},
                        'U_detail':{x:v for x,v in pU.items() if x!='transcript'},
                        'first_mismatch':next((i for i in range(min(len(terminal),len(target)))
                                  if terminal[i]!=target[i]),None)})
    return {'all_q_k_pumping':all(x['pass'] for x in outputs),
            'scope':f'q>={Q}, k>={K}, all residues modulo {d}',
            'finite_window':f'q={Q}; k={K}..{K+d-1}', 'outputs':outputs}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('candidate')
    args=ap.parse_args()
    with open(args.candidate) as f:cfg=json.load(f)
    ans=check(cfg)
    print(json.dumps(ans,indent=2))
    sys.exit(0 if ans['all_q_k_pumping'] else 1)
