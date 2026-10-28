"""Own utilities on top of the repo mirror (mirror.py = copy of calculation/neutral_band_search.py)."""
import re, sys
import mirror as m

def parse_lean_certs(path):
    src=open(path).read()
    defs={mm[1]:[int(x) for x in mm[2].split(',')] for mm in re.finditer(r"def (\w+) : List Nat := \[([^\]]*)\]",src)}
    mm=re.search(r"def cert20 : List Edge :=\s*(\[.*?\])\n\n",src,re.S) or re.search(r"def cert\w* : List Edge :=\s*(\[.*?\])\n\n",src,re.S)
    es=[]
    for e in re.finditer(r"⟨(\w+), (\w+), (\w+), (\w+), (\d+), (\d+)⟩",mm[1]):
        es.append((defs[e[1]],defs[e[2]],defs[e[3]],defs[e[4]],int(e[5]),int(e[6])))
    return es

def Bstep(b,B):
    """autonomous B step (untrimmed next, then maximal trim): returns (Bnext_trimmed, e1, gam, u)."""
    e1=m.e1(b,B); e2=1-e1
    # emulate nextB with C such that e2=1-e1 : nextB depends only on B when e2=1-e1
    DB=m.DB(b,B); R,gm=m.norm(b,B[::-1],e2)
    xd=(b-1)*(1-e1)
    if gm==0: nb=m._zw(DB,R[::-1])
    else: nb=m._zw(DB+[xd],[1]+R[::-1])
    u=0
    while nb and nb[-1]==b-1: nb=nb[:-1]; u+=1
    return nb,e1,gm,u

def Bcycle_streams(b,es):
    out=[]
    for E in es:
        B=E[0]; out.append((len(B),m.e1(b,B),m.gam(b,B,E[1])))
    return out
