#!/usr/bin/env python3
import os
"""r13a: generate L/R job lines from census files.
usage: mkjobs.py MODE CLOCK Tmin Tmax [--epochs M] [--R 12] [--solver kissat404] [--s S] [--maxs S] [--out jobs.txt]
Output: job lines (full paths)."""
import sys, argparse, glob, re
PY=os.path.expanduser('~/p196_run/venv/bin/python'); RUN=os.path.expanduser('~/p196_run/r13a/bandrun.py')
def parse(clock, smax=8):
    bands=[]
    for s in range(1,smax+1):
        fn=os.path.expanduser(f'~/p196_run/r13a/census/b{clock}_s{s}.txt')
        try: f=open(fn)
        except: continue
        for line in f:
            if not line.startswith('BAND'): continue
            m=re.match(r'BAND s=(\d+) T=(\d+) Trot=(\d+) twist=(\d+) cyclelen=(\d+) V=([\d,]+)',line)
            s_,T,Trot,tw,cl,V=m.groups()
            bands.append(dict(s=int(s_),T=int(T),Trot=int(Trot),twist=int(tw),V=V))
    return bands
if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('mode'); ap.add_argument('clock'); ap.add_argument('tmin',type=int); ap.add_argument('tmax',type=int)
    ap.add_argument('--R',type=int,default=12); ap.add_argument('--epochs',type=int,default=1)
    ap.add_argument('--solver',default='kissat404'); ap.add_argument('--maxs',type=int,default=8)
    ap.add_argument('--tau',type=int,default=0)
    a=ap.parse_args()
    for B in parse(a.clock,a.maxs):
        if not (a.tmin<=B['T']<=a.tmax): continue
        for r in range(B['s']):
            print(f"{PY} {RUN} {a.mode} --b 10 --clock {a.clock} --V {B['V']} --T {B['T']} --tau {a.tau} --rot {r} --R {a.R} --epochs {a.epochs} --solver {a.solver}")
