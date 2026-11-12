import subprocess, os, tempfile, numpy as np
from tools import *
HERE=os.path.dirname(os.path.abspath(__file__))
def run_closure(F, starts, pars=(), maxnodes=2000000, dump=False, workdir=None, timeout=None):
    """pars: list of (case_int, parity list). Returns dict summary (+ nodes/edges if dump)."""
    P=F.P
    lines=["%d %d %d %d"%(F.B,P,maxnodes,1 if dump else 0)]
    lines.append(' '.join(map(str,F.alpha)))
    lines.append(' '.join(map(str,F.gamma)))
    lines.append(str(len(pars)))
    for cas,par in pars:
        lines.append(str(cas)+' '+' '.join(map(str,par)))
    lines.append(str(len(starts)))
    for H in starts:
        lines.append(' '.join(' '.join(map(str,x)) for x in H))
    wd=workdir or tempfile.mkdtemp(prefix='cx_',dir='/tmp')
    try:
        r=subprocess.run([os.path.join(HERE,'closure')],input='\n'.join(lines)+'\n',capture_output=True,text=True,cwd=wd,timeout=timeout)
    except subprocess.TimeoutExpired:
        return {'timeout':True}
    out={'cyc':[],'cands':[],'wd':wd,'timeout':False}
    for ln in r.stdout.splitlines():
        w=ln.split()
        if w[0]=='NODES':
            out['nodes']=int(w[1]); out['expanded']=int(w[3]); out['complete']=bool(int(w[5])); out['live']=int(w[7]); out['dfs']=int(w[9])
        elif w[0]=='CYC':
            out['cyc'].append({'size':int(w[2]),'hasstart':int(w[4]),'rep':int(w[6])})
        elif w[0]=='CAND':
            out['cands'].append({'case':int(w[2]),'i':int(w[4]),'w':int(w[5]),'path':list(map(int,w[7:]))})
    if dump:
        raw=np.fromfile(os.path.join(wd,'nodes.bin'),dtype=np.uint8).reshape(-1,2*P)
        out['raw']=raw
        e=np.fromfile(os.path.join(wd,'edges.bin'),dtype=np.int32).reshape(-1,2)
        out['edges']=e
        out['comp']=np.fromfile(os.path.join(wd,'comp.bin'),dtype=np.int32)
    return out
def node_from_raw(raw,i):
    row=raw[i]; x=row[0::2]; y=row[1::2]
    return (tuple(int(v) for v in x>>4),tuple(int(v) for v in x&15),tuple(int(v) for v in y>>2),tuple(int(v) for v in y&3))
def edge_lists(n,e):
    L=[[] for _ in range(n)]
    for v,w in e: L[int(v)].append(int(w))
    return L
