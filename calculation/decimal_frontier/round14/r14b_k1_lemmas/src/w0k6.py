import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r14
HOME=os.path.expanduser("~/p196_run/")
name=sys.argv[1]; K0=int(sys.argv[2]); dirn=sys.argv[3]
L = r14.Lat(HOME+"mchk13b/lat/%s.txt"%name)
T,K,lay = r14.load_layers(HOME+"r14b/data/%s/K%d.bin"%(dirn,K0))
S=[set(c) for ph,c in lay]; ph=[p for p,c in lay]
K2=K+1
cand=[{w+(v,) for w in S[l] for v in range(19)} for l in range(T)]
succ=[dict() for _ in range(T)]
for l in range(T):
    l2=(l+1)%T
    for w in cand[l]:
        succ[l][w]=[nw for d,v,nw in L.succ(ph[l],w) if nw in cand[l2]]
pred=[collections.defaultdict(list) for _ in range(T)]
for l in range(T):
    l2=(l+1)%T
    for w,o in succ[l].items():
        for nw in o: pred[l2][nw].append(w)
def isacc(l,w): return w[0]!=L.W[ph[l][0]][ph[l][1]]
# forward-infinite set (greatest fixed point: has infinite forward path): iterative removal
def inf_set(nbr, l_delta):
    alive=[set(cand[l]) for l in range(T)]
    outd=[{w:len(nbr[l][w]) if isinstance(nbr[l],dict) else 0 for w in alive[l]} for l in range(T)]
    return alive
# compute F (states with infinite forward path) by removing states with no successor iteratively
Fset=[set(cand[l]) for l in range(T)]
changed=True
outd=[{w:len(succ[l][w]) for w in cand[l]} for l in range(T)]
from collections import deque
q=deque((l,w) for l in range(T) for w in cand[l] if outd[l][w]==0)
while q:
    l,w=q.popleft()
    if w not in Fset[l]: continue
    Fset[l].discard(w)
    l0=(l-1)%T
    for pw in pred[l].get(w,[]):
        if pw in Fset[l0]:
            outd[l0][pw]-=1
            if outd[l0][pw]==0: q.append((l0,pw))
# B set: infinite backward path
Bset=[set(cand[l]) for l in range(T)]
ind=[{w:len(pred[l].get(w,[])) for w in cand[l]} for l in range(T)]
q=deque((l,w) for l in range(T) for w in cand[l] if ind[l][w]==0)
while q:
    l,w=q.popleft()
    if w not in Bset[l]: continue
    Bset[l].discard(w)
    l2=(l+1)%T
    for nw in succ[l][w]:
        if nw in Bset[l2]:
            ind[l2][nw]-=1
            if ind[l2][nw]==0: q.append((l2,nw))
acc=sum(1 for l in range(T) for w in cand[l] if isacc(l,w))
accF=sum(1 for l in range(T) for w in Fset[l] if isacc(l,w))
accB=sum(1 for l in range(T) for w in Bset[l] if isacc(l,w))
accFB=sum(1 for l in range(T) for w in Fset[l]&Bset[l] if isacc(l,w))
print(name,"K",K2,"candidates",sum(len(c) for c in cand),"accepted cand",acc,"accepted with inf forward",accF,"with inf backward",accB,"both",accFB)
acF=collections.Counter(); acB=collections.Counter()
for l in range(T):
    for w in Fset[l]:
        if isacc(l,w): acF[ph[l]]+=1
    for w in Bset[l]:
        if isacc(l,w): acB[ph[l]]+=1
print(" phases with accepted & inf forward:",sorted(acF.items(),key=lambda kv:(kv[0][0],kv[0][1]))[:20])
print(" phases with accepted & inf backward:",sorted(acB.items(),key=lambda kv:(kv[0][0],kv[0][1]))[:20])
# lifetimes: forward depth of accepted states not in Fset (how many steps until dead)
memo={}
import sys as _s
_s.setrecursionlimit(100000)
def fdepth(l,w):
    k=(l,w)
    if k in memo: return memo[k]
    if w in Fset[l]: 
        memo[k]=10**6; return 10**6
    best=0
    for nw in succ[l][w]:
        d=fdepth((l+1)%T,nw)
        if d+1>best: best=d+1
    memo[k]=best
    return best
hist=collections.Counter()
for l in range(T):
    for w in cand[l]:
        if isacc(l,w) and w not in Fset[l]:
            hist[fdepth(l,w)]+=1
print(" forward lifetime histogram of accepted states without infinite future:",sorted(hist.items())[:30])
