#!/usr/bin/env python3
"""Y37 p8/rec0 rotation-shard checker. Run at repository root via this path.
Uses ordinary unbounded integers and n + reverse(n), not a pairword-only stepper.
This certifies a scoped 160-step endpoint map, not an all-time Lychrel orbit.
"""
import hashlib, json, re, sys
from pathlib import Path
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parents[3]
ROWS = ROOT / "calculation/new_structures/agent-N26/p8_rec0_rows.txt"
REC1 = ROOT / "calculation/decimal_frontier/lattice_formats/agent14_p8_rows.json"
OUT = Path(__file__).resolve().parent / "daughters.json"

def tables():
    lines = ROWS.read_text().splitlines()
    parse = lambda line: [tuple(map(int, x.split(","))) for x in re.findall(r"\[([^\]]+)\]", line)]
    br, wr = parse(lines[0]), parse(lines[1])
    assert len(br) == 39 and len(wr) == 20
    B, W = [x[0] for x in br], [x[0] for x in wr]
    R = json.loads(REC1.read_text())["rec1"]
    assert len(R) == 8 and all(len(x) == 20 for x in R)
    assert W == [17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13]
    return B, W, R

def rot(a, s):
    s %= len(a); return list(a[s:]) + list(a[:s])

def pairword(n):
    d = [ord(c)-48 for c in str(n)[::-1]]
    return [d[i]+d[-1-i] for i in range(len(d))]

def seed(B,W,V,q,k):
    E = list(W); E[9] = 10; J = [18,0,1,1]
    H = list(B)+list(W)*q+E+J+list(V)*k
    P = H+[5,5]+H[::-1]
    half = P[:len(P)//2]
    lo = [min(9,x) for x in half]; hi = [x-y for x,y in zip(half,lo)]
    digits = lo+hi[::-1]
    n = int("".join(str(d) for d in digits[::-1]))
    assert pairword(n) == P and str(n)[0] != "0"
    return n

def evolve(B,W,V,q,k,steps=160):
    n=seed(B,W,V,q,k); states=[pairword(n)]; over=[]; pals=[]
    for t in range(steps):
        s=str(n)
        if s == s[::-1]: pals.append(t)
        n2=n+int(s[::-1]); over.append(len(str(n2))>len(s)); n=n2
        states.append(pairword(n))
    if str(n)==str(n)[::-1]: pals.append(steps)
    return states,over,pals

def ins(P,A,c):
    n=len(P); Q=P[:c]+A+P[c:n-c]+A[::-1]+P[n-c:]
    assert Q==Q[::-1]
    return Q

def run_of(H,V,start):
    m=len(V); best=0; pos=None
    for p in range(start,len(H)-m+1):
        if H[p:p+m]!=V: continue
        r=0
        while p+(r+1)*m<=len(H) and H[p+r*m:p+(r+1)*m]==V: r+=1
        if r>best: best,pos=r,p
    return best,pos

def endpoint(P,B,W,V):
    H=P[:len(P)//2]; p=len(B); qout=0
    while H[p:p+20]==W: p+=20; qout+=1
    kout,vp=run_of(H,V,p); assert vp is not None
    prefix=H[p:vp]; tail=H[vp+20*kout:-1]
    centre=P[len(P)//2-1:len(P)//2+1]
    return {"q_out":qout,"k_out":kout,"collar_total":len(H)-1-len(B)-20*qout-20*kout,
            "prefix_collar_len":len(prefix),"tail_collar_len":len(tail),"centre":centre,
            "half_len":len(H),"prefix_collar":prefix,"tail_collar":tail}

def check_insertions(B,W,R,s):
    V=rot(R[0],s)
    base,gb,pb=evolve(B,W,V,20,20); wp,gw,pw=evolve(B,W,V,21,20)
    vp,gv,pv=evolve(B,W,V,20,21); both,g2,p2=evolve(B,W,V,21,21)
    clock=[i%2==0 for i in range(160)]
    assert gb==gw==gv==g2==clock and not (pb or pw or pv or p2)
    awseq=[]; avseq=[]
    for t in range(161):
        P,Qw,Qv,Q2=base[t],wp[t],vp[t],both[t]
        aw=Qw[239:259]; av=Qv[663:683]; av2=Q2[683:703]
        assert ins(P,aw,239)==Qw, (s,"W",t)
        assert ins(P,av,663)==Qv, (s,"V",t)
        assert av2==av and ins(ins(P,aw,239),av,683)==Q2, (s,"double",t)
        awseq.append(aw); avseq.append(av)
    assert awseq[0]==W==awseq[160] and avseq[0]==V==avseq[160]
    out=endpoint(base[160],B,W,V)
    assert (out["q_out"],out["k_out"],out["collar_total"],out["prefix_collar_len"],out["tail_collar_len"])==(19,12,244,164,80)
    return V,out

def check_width(B,W,R,s,q,k):
    V=rot(R[0],s); states,over,pals=evolve(B,W,V,q,k)
    assert over==[i%2==0 for i in range(160)] and not pals
    out=endpoint(states[160],B,W,V)
    assert (out["q_out"],out["k_out"],out["collar_total"])==(q-1,k-8,244), (s,q,k,out)
    return out

def baseline_ledger(B,W,R,q):
    V=rot(R[0],7); n=seed(B,W,V,q,q); rows=[]; over=[]
    for t in range(320):
        s=str(n); assert s!=s[::-1], (q,t)
        n2=n+int(s[::-1]); over.append(len(str(n2))>len(s)); n=n2
        if t+1 in (80,160,240,320):
            o=endpoint(pairword(n),B,W,V)
            rows.append({"t":t+1,**{k:o[k] for k in ("q_out","k_out","collar_total","prefix_collar_len","tail_collar_len","centre","half_len")},"overflow_count":sum(over)})
    assert over==[i%2==0 for i in range(320)]
    expect=[(q+1,q-4,104,64,40,[2,2]),(q+1,q-8,204,124,80,[10,10]),
            (q,q-12,324,204,120,[6,6]),(q-1,q-15,424,264,160,[16,16])]
    for r,e in zip(rows,expect):
        assert (r["q_out"],r["k_out"],r["collar_total"],r["prefix_collar_len"],r["tail_collar_len"],r["centre"])==e
    return rows

def main():
    B,W,R=tables(); assigned=[2,6,10,14,18]
    daughters=[]; controls=[]
    for s in assigned:
        V,o=check_insertions(B,W,R,s)
        pre=o.pop("prefix_collar"); tail=o.pop("tail_collar")
        daughters.append({"ledger_index":s+1,"spatial_shift":s,**o,"prefix_collar":pre,"tail_collar":tail,
          "prefix_sha256":hashlib.sha256(bytes(pre)).hexdigest(),"tail_sha256":hashlib.sha256(bytes(tail)).hexdigest()})
        for q,k in [(20,20),(40,40),(80,80),(160,160),(20,40),(40,20),(23,26),(80,160),(160,80)]:
            x=check_width(B,W,R,s,q,k)
            controls.append({"shift":s,"q_in":q,"k_in":k,"q_out":x["q_out"],"k_out":x["k_out"],"collar_total":x["collar_total"],"centre":x["centre"]})
    baselines=[{"q_in":q,"rows":baseline_ledger(B,W,R,q)} for q in (20,40,80,160)]
    OUT.write_text(json.dumps({"label":"scoped all-width 160-step endpoint; not a Lychrel certificate",
      "assigned_shifts":assigned,"daughters":daughters,"width_controls":controls,
      "baseline_t14_80_step_ledger_by_width":baselines},indent=2)+"\n")
    print("PASS: five 161-state insertion certificates; W, V and double-insertion identities exact.")
    print("PASS: 45 diagonal/off-diagonal big-integer controls; all five give q_out=q-1, k_out=k-8, collar=244.")
    print("PASS: T14 shift-7 t=80/160/240/320 ledger at q=k=20,40,80,160.")
    print("Generated",OUT)
if __name__=="__main__": main()
