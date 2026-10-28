import sys
sys.path.insert(0,'/home/claude/research/w5_exterior/py')
from fc_graph import edges
b=10
E=edges(b); n=2*b-2
succ={0:{},1:{}}
for q,q2,g,h in E: succ[g].setdefault(q,set()).add(q2)
def words(m):
    # all binary words of length m readable from some state
    cur={'':set(range(1,n+1))}
    for _ in range(m):
        nxt={}
        for w,S in cur.items():
            for a in (0,1):
                T=set()
                for q in S: T|=succ[a].get(q,set())
                if T: nxt[w+str(a)]=T
        cur=nxt
    return sorted(cur)
if __name__=='__main__':
    m=int(sys.argv[1]); ws=words(m)
    print(len(ws),file=sys.stderr)
    print('\n'.join(ws))
