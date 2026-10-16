"""Keep all temporal repetitions in an exact cyclic boundary language.

The seed is the new spatial-period-five / temporal-period-forty bulk,
not the previously excluded period-three bulk. Complete root reconstruction
would still need an independent full family audit. Caps remain UNKNOWN.
"""
from pathlib import Path
import json
import sys
import time
import argparse
from cyclic_bisimulation import quotient,quotient_both

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'main_existence_attempt/boundary_resume/reverse'))
sys.path.insert(0,str(ROOT/'main_existence_attempt/boundary_resume/new_clock'))
from columns import bulk_state
from check_reverse_certificate import build_tables,encode_letter
from sofic_reverse import preimage,contains_uniform

HERE=Path(__file__).resolve().parent


def run(layers=24,cap=300000,bisim=False,both=False):
    c=json.loads((HERE/'cycles_p5_k4.json').read_text())['candidates'][0]
    assert c['clock']==[0,1]*20
    a,b,z=bulk_state(c['bulk'][0],c['clock'])
    word=[encode_letter(a[2*j],a[2*j+1],b[j],z[j]) for j in range(20)]
    n=len(word)
    edges=[(j,(j+1)%n,w) for j,w in enumerate(word)]
    fibers,output,_,_=build_tables()
    root=encode_letter(0,1,1,7)
    graphs=[];records=[];status='UNKNOWN_LAYER_CAP';recurrence=None
    stem='bidirectional' if both else ('bisim' if bisim else 'alternating')
    start=time.monotonic()
    for depth in range(layers+1):
        raw_n,raw_edges=n,len(edges)
        if both:
            n,edges,blocks,rounds=quotient_both(n,edges)
        elif bisim:
            n,edges,blocks,rounds=quotient(n,edges)
        else:
            blocks,rounds=list(range(n)),0
        found=contains_uniform(n,edges,root)
        row=dict(depth=depth,vertices=n,edges=len(edges),root_cycle=found,
                 before_quotient_vertices=raw_n,before_quotient_edges=raw_edges,
                 quotient_rounds=rounds,seconds=time.monotonic()-start)
        records.append(row)
        print(json.dumps(row),flush=True)
        (HERE/f'{stem}_depth{depth}.json').write_text(json.dumps(dict(vertices=n,edges=edges),separators=(',',':'))+'\n')
        if found:
            status='ROOT_CYCLE_RECONSTRUCTION_REQUIRED';break
        old=next((i for i,g in enumerate(graphs) if g==(n,edges)),None)
        if old is not None:
            status='RECURRENCE_REQUIRES_INDEPENDENT_AUDIT'
            recurrence=dict(first=old,repeat=depth);break
        graphs.append((n,edges))
        if depth==layers:break
        result=preimage(n,edges,fibers,output,cap)
        if result is None:
            status='UNKNOWN_GRAPH_CAP';break
        n,edges,_=result
    result=dict(status=status,recurrence=recurrence,records=records,cap=cap,
                layers=layers,seed_word=word,root_label=root,
                strong_forward_bisimulation=bisim,
                alternating_forward_reverse_quotients=both,
                source='cycles_p5_k4.json candidate 0',
                all_temporal_repetitions_included=True,
                decimal_lychrel_existence_proved=False)
    (HERE/f'{stem}_language.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('records','seed_word')}))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--bisim',action='store_true')
    parser.add_argument('--both',action='store_true')
    parser.add_argument('--layers',type=int,default=24)
    parser.add_argument('--cap',type=int,default=300000)
    args=parser.parse_args()
    run(args.layers,args.cap,args.bisim,args.both)
