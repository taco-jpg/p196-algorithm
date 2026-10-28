import re, sys
sys.path.insert(0,'/home/claude/research/w3_formats/code')
from gt import *
def parse(fn):
    out=[]
    for line in open(fn):
        if not line.startswith('SCC'): continue
        m = re.match(r'SCC p=(\d+) g=(\w+) size=(\d+) cyclen=(\d+) depth=(\d+) path=(.*) cyc=(.*)', line.strip())
        p,g,size,cl,depth,path,cyc = m.groups()
        cols = lambda s: [list(map(int,c.split(','))) for c in re.findall(r'\[([^\]]*)\]', s)]
        out.append(dict(p=int(p),g=g,size=int(size),cyclen=int(cl),depth=int(depth),path=cols(path),cyc=cols(cyc)))
    return out
def templates(rec, b=10, core=()):
    p=rec['p']; P=rec['path']; C=rec['cyc']; n=len(P); m=len(C)
    Ts=[]
    for t in range(p):
        B=tuple(P[k][t] for k in range(n))
        W=tuple(C[j][t] for j in range(m))
        Ts.append(Template(b,[('L',B),('B',W,0)],core))
    return Ts
if __name__=='__main__':
    recs=parse(sys.argv[1])
    for ri,rec in enumerate(recs):
        Ts=templates(rec)
        ok=0
        for t in range(rec['p']):
            T=Ts[t]; T2,gm,info=step(T)
            exp=Ts[(t+1)%rec['p']]
            # compare B' lowest n positions (engine canonical form may trim/rotate)
            P1=instantiate(T2,{0:12}); P2=instantiate(exp,{0:12})
            n=len(rec['path'])
            match = P1[:n]==P2[:n]
            print(f"rec{ri} t={t} gam_engine={info['gam']} gam_pred={rec['g'][t]} first{n}-match={match} engine T2 band len {[len(it[1]) for it in T2.Hs if it[0]=='B']}")
            ok+=match
        print('rec',ri,'matches',ok,'/',rec['p'])
