#!/usr/bin/env python3
"""r13a: independent replay of a centre witness (V, C, N, j, clock) by direct digit arithmetic on the palindromic window
V^m C rev(V)^m (absolute left frame), with forced clock; boundary: left low carry = periodic background alpha of the band at column 0 of the window;
right boundary digit at overflow steps = next background band digit (left mirror) -- as in satc.py.  Target after N steps: V_N^(m+j) C rev(V_N)^(m+j) (V_N = V).
Also checks that the band rows are correct on the protected zone at all times.
usage: centre_replay.py --V 5,11,8 --C 13,2,13 --N 24 --j 1 [--clock 1000] [--b 10]"""
import sys, argparse
def rowstep(x, g, b):
    n=len(x); st=next(i for i in range(n) if x[i]!=b-1)
    al=[0]*n; a=1 if x[st]>=b else 0
    for k in range(1,n):
        i=(st+k)%n; al[i]=a; a=1 if x[i]+a>=b else 0
    al[st]=a
    be=[0]*n; h=1 if x[st]>=b else 0; be[st]=h
    for k in range(1,n):
        i=(st-k)%n; h=1 if x[i]+h>=b else 0; be[i]=h
    lo=[(x[c]+al[c])%b for c in range(n)]; hi=[(x[c]+be[(c+1)%n])%b for c in range(n)]
    y=[lo[c]+(hi[(c-1)%n] if g else hi[c]) for c in range(n)]
    return y,al,be
ap=argparse.ArgumentParser(); ap.add_argument('--V',required=True); ap.add_argument('--C',default=''); ap.add_argument('--N',type=int,required=True); ap.add_argument('--j',type=int,required=True); ap.add_argument('--clock',default='1000'); ap.add_argument('--b',type=int,default=10); ap.add_argument('--m',type=int,default=0)
a=ap.parse_args()
V=[int(x) for x in a.V.split(',')]; C=[int(x) for x in a.C.split(',')] if a.C else []
s=len(V); b=a.b; p=len(a.clock); cl=[int(ch) for ch in a.clock]
clock=[cl[t%p] for t in range(a.N)]
rows=[list(V)]; als=[]
for g in clock:
    y,al,be=rowstep(rows[-1],g,b); rows.append(y); als.append(al)
assert rows[a.N]==list(V), ('band not N-periodic',rows[a.N])
m=a.m if a.m else (2*a.N+20)//s+3
w=list(V)*m+list(C)+list(V[::-1])*m
assert w==w[::-1], 'window not palindromic'
for t,g in enumerate(clock):
    N=len(w); c=als[t][0]; e=[]
    for x in w:
        z=x+c; e.append(z%b); c=1 if z>=b else 0
    if g==0:
        w=[e[j]+e[N-1-j] for j in range(N)]
    else:
        e.append((rows[t][-1]+c)%b)
        w=[e[j]+e[N-j] for j in range(N+1)]
    assert w==w[::-1], ('lost palindromy',t)
tgt=list(rows[a.N])*(m+a.j)+list(C)+list(rows[a.N][::-1])*(m+a.j)
print('final length',len(w),'target length',len(tgt),'EQUAL' if w==tgt else 'DIFFERENT')
if w!=tgt:
    d=[i for i in range(min(len(w),len(tgt))) if w[i]!=tgt[i]]
    print('first differences at',d[:10],'of',len(d))
sys.exit(0 if w==tgt else 1)
