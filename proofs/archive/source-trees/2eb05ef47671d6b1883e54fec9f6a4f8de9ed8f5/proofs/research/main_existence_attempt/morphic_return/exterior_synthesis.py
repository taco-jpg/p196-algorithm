"""Exact finite exterior obligations for the positive 525/936 front.

This targets one specific locally proved front. SAT supplies a local
exterior only; an assembled finite family still needs exact whole-word
verification and a compatible finite center. UNKNOWN excludes nothing.
"""
from pathlib import Path
import sys,json,time,argparse
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'research'))
from astra_substitution_gluing import trace,fold,bv
from astra_substitution_enumerate import transition,outer_three_filter
import z3 as z
HERE=Path(__file__).resolve().parent


def outer_cycle():
    data=outer_three_filter();live={tuple(q)for q in data['return_states']}
    edges={tuple(r['q']):[tuple(v)for v in r['targets']if tuple(v)in live]for r in data['graph']if tuple(r['q'])in live}
    q=(8,12,9);out=[]
    for _ in range(8):out.append(q);assert len(edges[q])==1;q=edges[q][0]
    assert q==out[0] and set(out)==live
    return out


def solve(B,width,phase,seconds):
    start=time.monotonic();bt=trace(tuple(B));prefix=outer_cycle()
    s=z.Then('simplify','propagate-values','solve-eqs','simplify','bit-blast','sat').solver()
    s.set(timeout=int(seconds*1000));rows=[]
    for t in range(24):
        row=[bv(v)for v in prefix[(t+2*phase)%8]]+[z.BitVec(f'q{t}_{i}',5)for i in range(3,width)]
        for x in row[3:]:s.add(z.ULE(x,bv(18)))
        rows.append(row)
    for t,row in enumerate(rows):
        h=t%2;nrow=rows[(t+1)%24];b=bt[t];bn=bt[(t+1)%24]
        lo,hi,lc,rc=fold(s,row,0,b['R'][0],f't{t}')
        s.add(lc==bv(b['A'][0]),rc==bv(h))
        for i in range(width):s.add(nrow[i]==lo[i]+(bv(1)if h and i==0 else hi[i-h]))
        if h:s.add(bv(bn['q'][0])==bv(b['lo'][0])+hi[-1])
    built=time.monotonic();status=s.check()
    result=dict(bulk=B,width=width,outer_phase=phase,period=24,clock=[t%2 for t in range(24)],status=str(status),build_seconds=built-start,solve_seconds=time.monotonic()-built)
    if status==z.sat:
        model=s.model();words=[tuple(model.eval(x,model_completion=True).as_long()for x in row)for row in rows]
        for t in range(24):assert transition('exterior',words[t],bt,t)==words[(t+1)%24]
        result.update(rows=words,integer_column_replay=True)
    elif status==z.unknown:result['reason']=s.reason_unknown()
    result['finite_seed_proved']=False
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=24);p.add_argument('--seconds',type=float,default=5);p.add_argument('--prefix',default='exterior24');a=p.parse_args()
    records=[];base=(5,2,5)
    for r in range(3):
        B=base[r:]+base[:r]
        for phase in range(4):
            row=solve(B,a.width,phase,a.seconds);records.append(row)
            print(json.dumps(row),flush=True)
            (HERE/f'{a.prefix}.json').write_text(json.dumps(records,indent=2)+'\n')
            if row['status']=='sat':raise SystemExit
