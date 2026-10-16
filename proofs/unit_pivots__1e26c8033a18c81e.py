"""Try exact unit-pivot elimination over Z[t,t^-1].

A completed1079-pivot certificate rules out nonzero history scores over
every field at every invertible scalar t, without relying on prime sampling.
"""
from pathlib import Path
import sys,json,time
sys.path.insert(0,str(Path(__file__).resolve().parent))
from search import make_rows,m

HERE=Path(__file__).resolve().parent

def padd(a,b,scale=1):
    out=dict(a)
    for e,v in b.items():
        z=out.get(e,0)+scale*v
        if z:out[e]=z
        elif e in out:del out[e]
    return out

def pmul(a,b):
    out={}
    for e,v in a.items():
        for f,w in b.items():
            k=e+f;z=out.get(k,0)+v*w
            if z:out[k]=z
            elif k in out:del out[k]
    return out

def subtract_row(row,pivot,factor):
    for k,poly in pivot.items():
        new=padd(row.get(k,{}),pmul(factor,poly),-1)
        if new:row[k]=new
        elif k in row:del row[k]

def initial_rows():
    zero,_,_=make_rows(0)
    one,_,_=make_rows(1)
    assert len(zero)==len(one)
    rows=[]
    for a,b in zip(zero,one):
        row={}
        for j in a.keys()|b.keys():
            p={}
            if a.get(j,0):p[0]=a[j]
            if b.get(j,0)-a.get(j,0):p[1]=b.get(j,0)-a.get(j,0)
            if p:row[j]=p
        rows.append(row)
    return rows

def main():
    start=time.monotonic();rows=initial_rows()
    order=sorted(range(len(rows)),key=lambda i:len(rows[i]))
    pending=[(i,rows[i],[]) for i in order if rows[i]]
    pivots=[];pivcols={};records=[]
    for sweep in range(10):
        waiting=[];added=0
        for original,row,operations in pending:
            while True:
                present=[pivcols[k] for k in row if k in pivcols]
                if not present:break
                ix=min(present);col,pro=pivots[ix];factor=row[col]
                operations.append((ix,sorted(factor.items())))
                subtract_row(row,pro,factor)
            units=[(k,next(iter(p.items()))) for k,p in row.items()
                   if len(p)==1 and abs(next(iter(p.values())))==1]
            if not units:
                if row:waiting.append((original,row,operations))
                continue
            col,(degree,sign)=min(units)
            pro={k:{e-degree:v*sign for e,v in poly.items()}
                 for k,poly in row.items()}
            assert pro[col]=={0:1}
            pivcols[col]=len(pivots);pivots.append((col,pro));added+=1
            records.append(dict(original_row=original,operations=operations,
                                pivot_column=col,normalization=[-degree,sign]))
            if len(pivots)==m.NW-44:break
            if time.monotonic()-start>100:break
        print(json.dumps(dict(sweep=sweep,rank=len(pivots),new=added,
                              pending=len(waiting),seconds=time.monotonic()-start)),flush=True)
        if len(pivots)==m.NW-44 or not added or time.monotonic()-start>100:break
        pending=waiting
    result=dict(ring='Z[t,t^-1]',unit_pivots=len(pivots),target=m.NW-44,
                complete=len(pivots)==m.NW-44,records=records,
                seconds=time.monotonic()-start)
    (HERE/'unit_pivot_certificate.json').write_text(json.dumps(result,separators=(',',':')))
    print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)

if __name__=='__main__':main()
