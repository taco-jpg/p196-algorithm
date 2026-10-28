import sys, random
sys.path.insert(0,'/home/claude/research/w3_formats/code')
sys.path.insert(0,'/home/claude/taco-jpg/p196-algorithm/calculation'); import neutral_band_search as M
from gt import *
import io, contextlib

# 1. random regression: single neutral band, gt.step == mirror.step
rng = random.Random(5)
n_ok = 0; n_break = 0
for trial in range(20000):
    b = rng.choice([2,3,4,5,8,10,11,16,26])
    lb = rng.randint(1,6); lc = rng.randint(0,6)
    B = [rng.randint(0,2*b-2) for _ in range(lb)]
    if B[0]==0: continue
    half = [rng.randint(0,2*b-2) for _ in range((lc+1)//2)]
    C = half + half[:lc//2][::-1]
    E = M.step(b,B,C)
    T = mk_one_band(b,B,C)
    T2,gm,info = step(T)
    if E is None:
        # mirror says Hyp fails (break) -> gt continues with absorbing band; check that flip fails
        assert M.e1(b,B)==M.e2(b,B,C) or any(v>2*(b-1) for v in B)
        n_break += 1
        continue
    _,_,B2,C2,u,v = E
    exp = mk_one_band(b,B2,C2)
    assert T2 == exp, (b,B,C,fmt(T2),fmt(exp))
    old,mult,off = gm[0]
    assert (old,mult)==(0,1) and off == -M.gam(b,B,C)+u+v, (b,B,C,gm,u,v)
    n_ok += 1
print("single-band regression OK:", n_ok, "agree; flip-failures:", n_break)

# 2. known certificates
for b,es in M._lean_certs():
    B,C = es[0][0],es[0][1]
    B,C,_,_ = M.trim(b,B,C)
    T = mk_one_band(b,B,C)
    off_total = 0
    cur = T
    for k,E in enumerate(es):
        T2,gm,info = step(cur)
        B2,C2,uu,vv = M.trim(b,list(E[2])+[b-1]*E[4], [b-1]*E[5]+list(E[3])+[b-1]*E[5])
        assert T2 == mk_one_band(b,B2,C2), (b,k,fmt(T2),B2,C2)
        off_total += gm[0][2]
        cur = T2
    # compare with canonical start
    print(f"base {b}: {len(es)} edges re-derived by gt.step (canonical trim), returns={cur==T}, net gap change per cycle {off_total}")
