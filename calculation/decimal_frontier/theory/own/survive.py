# for each initial palindromic centre (phase 0, trimmed) of width L, how many phases (steps) does it survive? exact mirror semantics.
import sys, itertools, collections
sys.path.insert(0,'/home/claude/research/w2_theory'); sys.path.insert(0,'/home/claude/research/w2_theory/scripts')
import lib, mirror as m
from parse_bw import parse_bw
line=[l for l in open('/home/claude/research/w2_theory/out2/bauto_p11_w.txt') if 'ACCEPT' in l][0]
b,p,g,e,Bs=parse_bw(line)
W=int(sys.argv[1]); start=int(sys.argv[2]) if len(sys.argv)>2 else 0
def survive(C,start):
    cur=list(C); t=start; n=0
    while True:
        r=m.step(b,Bs[t%p],cur)
        if r is None or len(r[3])==0: return n,cur
        cur=r[3]; t+=1; n+=1
        if n>=400: return n,cur
best={}
hist=collections.defaultdict(collections.Counter)
for L in range(1,W+1):
    h=(L+1)//2
    for half in itertools.product(range(2*b-1),repeat=h):
        if L%2==1 and half[-1]%2: continue
        if L>=2 and half[0]==b-1: continue
        C=list(half)+list(half[:L//2][::-1])
        n,last=survive(C,start)
        hist[L][n]+=1
        if L not in best or n>best[L][0]: best[L]=(n,C)
for L in range(1,W+1):
    print("width",L,"max phases survived",best[L][0],"example",best[L][1],"hist(top)",sorted(hist[L].items())[-4:])
