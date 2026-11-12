# Exact any-depth closure in a wall frame: 9-wire (rooted, p11 / p12) -> wall moving inward by Q columns per P steps -> anything.
from pipeline import *
import sys, time
B=10
def wires(g):
    r=rooted(B,g)
    out=[]
    for c,walk in cycles_of(r):
        H=r['order'][walk[0]]
        if all(s==B-1 for s in psums(H)): out.append((r,walk))
    return out
def wall_scan(name,g,kmax,Qmax,maxnodes=1500000):
    d=len(g); S=sum(g)
    for (r,walk) in wires(g):
        Hw=r['order'][walk[0]]
        for k in range(1,kmax+1):
            G=tuple(g)*k; P=d*k; SP=S*k
            ov=[t for t in range(P) if G[t]==1]
            for Q in range(1,Qmax+1):
                if 2*Q>=SP: break          # wall must be slower than the fold (Q < S/2)
                # spread the Q advances evenly over the overflow steps
                adv={ov[(i*len(ov))//Q] for i in range(Q)}
                F,phi=make_frame(B,G,adv)
                cells=lattice_cells(B,[Hw])
                sn=sheared_node(B,F,phi,cells,0)
                t0=time.time()
                rr=run_closure(F,[sn],maxnodes=maxnodes,dump=True,timeout=240)
                if rr.get('timeout'):
                    print('%s stream c=%s P=%d Q=%d: timeout'%(name,''.join(map(str,Hw[2])),P,Q)); sys.stdout.flush(); continue
                other=[c for c in rr['cyc'] if not c['hasstart']]
                desc=[]
                for c in other:
                    H=node_from_raw(rr['raw'],c['rep'])
                    desc.append('size %d psums %s'%(c['size'],psums(H)[:12]))
                print('%s stream c=%s P=%d Q=%d: closure %d nodes, complete=%s, live=%d, other cycles: %s (%.1fs)'%(
                    name,''.join(map(str,Hw[2])),P,Q,rr['nodes'],rr['complete'],rr['live'],desc if desc else 'none',time.time()-t0)); sys.stdout.flush()
if __name__=='__main__':
    wall_scan('p11',(0,0,0,0,1,1,1,0,0,0,1),3,3)
    wall_scan('p12',(0,0,0,1,0,0,0,1,0,0,0,1),3,3)
