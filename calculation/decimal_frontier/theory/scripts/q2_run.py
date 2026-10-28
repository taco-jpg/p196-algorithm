#!/usr/bin/env python3
"""Q2 driver: for every exterior (g,e) stream in out2/extG_b*_G*.txt with even G (and p<=PMAX) run cauto_fast (all widths, all trim patterns).
Sequential; run inside ONE heavy call.  usage: q2_run.py outfile PMAX per_call_timeout bases..."""
import sys, re, subprocess, glob, os, time
out=sys.argv[1]; PMAX=int(sys.argv[2]); TMO=int(sys.argv[3]); bases=[int(x) for x in sys.argv[4:]]
D="/home/claude/research/w2_theory"
fo=open(out,"a")
def log(s):
    fo.write(s+"\n"); fo.flush()
done=set()
if os.path.exists(out):
    for l in open(out):
        if l.startswith("RES "): done.add(tuple(l.split()[1:5]))
for b in bases:
    streams=[]
    for f in sorted(glob.glob(f"{D}/out2/extG_b{b}_G*.txt")):
        for l in open(f):
            m=re.search(r"ACCEPT b=(\d+) p=(\d+) g=(\d+) e=(\d+)",l)
            if m: streams.append((int(m[2]),m[3],m[4]))
    streams=sorted(set(streams))
    for p,g,e in streams:
        G=g.count('1')
        if G%2 or p>PMAX: continue
        key=(str(b),str(p),g,e)
        if key in done: continue
        t0=time.time()
        try:
            r=subprocess.run([f"{D}/bin/cauto_fast",str(b),e,g,"1","1","-vall","-allm","-sym","-cap","20000000"],capture_output=True,text=True,timeout=TMO)
            outp=r.stdout
            st={}
            for l in outp.splitlines():
                mm=re.search(r"status=(\w+)",l)
                if l.startswith("DONE") and mm: st[mm[1]]=st.get(mm[1],0)+1
            res=" ".join(f"{k}={v}" for k,v in sorted(st.items()))
            hits=[l for l in outp.splitlines() if l.startswith("FEASIBLE_CLASS") or l.startswith("FEASIBLE ")][:2]
        except subprocess.TimeoutExpired:
            res="TIMEOUT"; hits=[]
        log(f"RES {b} {p} {g} {e} G={G} {res} t={time.time()-t0:.1f}s {hits[0][:90] if hits else ''}")
fo.close()
