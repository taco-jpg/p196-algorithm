"""Reverse transfer for the exact finite exterior problem.

Every returned edge is replayed by the independently derived forward equations.
Truncated enumeration is a search limit, never an impossibility certificate.
"""
from pathlib import Path
import sys, json, time
sys.path.insert(0,str(Path(__file__).parent))
from exterior_columns import bulk_state, initial, successors

def predecessors(new, limit=100000):
    na,nb,nc,nz=new
    choices=[]
    for j in range(12):
        opts=[]
        for co in (0,1):
            R=nz[j]+10*co
            if not 0<=R<=18: continue
            if R<9 and co!=0 or R>9 and co!=1: continue
            for Q in range(19):
                for a in (0,1):
                    if (Q+a)//10!=na[j]: continue
                    c=(Q+nc[j])//10
                    if (Q+a)%10+(Q+nc[j])%10!=R: continue
                    for b in (0,1):
                        if (R+b)//10==nb[j]:
                            opts.append((Q,a,b,c,co,R))
        choices.append(opts)
    out={};cut=False
    def compatible(x,y):
        z=y[0]-(x[5]+x[2])%10-x[4]
        if not -1<=z<=9:return None
        if z==-1 and x[4]!=1 or z==9 and x[4]!=0:return None
        return z
    def visit(path,zs):
        nonlocal cut
        if cut:return
        j=len(path)
        if j==12:
            z=compatible(path[-1],path[0])
            if z is None:return
            old=(tuple(x[1] for x in path),tuple(x[2] for x in path),
                 tuple(x[3] for x in path),tuple(zs+[z]))
            row=tuple(v for x in path for v in (x[0],x[5]))
            out.setdefault(old,row)
            if len(out)>=limit:cut=True
            return
        for opt in choices[j]:
            if not path:visit([opt],[])
            else:
                z=compatible(path[-1],opt)
                if z is not None:visit(path+[opt],zs+[z])
            if cut:break
    visit([],[])
    return out,cut,[len(x) for x in choices]

def verify_edge(old,new,row):
    for j in range(12):
        a,b,c,z=(x[j] for x in old)
        na,nb,nc,nz=(x[j] for x in new)
        Q,R=row[2*j:2*j+2];Qn=row[(2*j+2)%24]
        co=(R-nz)//10
        assert co in (0,1) and R-10*co==nz
        assert (Q+nc)//10==c
        assert R==(Q+a)%10+(Q+nc)%10
        assert Qn==(R+b)%10+z+co
        assert na==(Q+a)//10 and nb==(R+b)//10
        assert not (R<9 and co!=0 or R>9 and co!=1)
        assert not (z==-1 and co!=1 or z==9 and co!=0)

def probe():
    start=time.monotonic();records=[]
    for B in [(5,2,5),(2,5,5),(5,5,2)]:
        state=bulk_state(B);out,cut,counts=predecessors(state)
        for old,row in out.items():verify_edge(old,state,row)
        record=dict(bulk=B,predecessors=len(out),truncated=cut,
                    temporal_choices=counts,contains_initial=initial() in out)
        records.append(record);print(json.dumps(record),flush=True)
    result=dict(records=records,seconds=time.monotonic()-start,finite_seed_proved=False)
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':probe()
