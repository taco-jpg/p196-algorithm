"""Replay all saved bidirectional quotient certificates and exercise lifting.

This is an audit of the representation and reconstruction machinery, not
a finite exterior witness. Every real lifted strip is checked against the
decimal column equations at every temporal position.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from collections import defaultdict
import json,time
from compressed_search import lift_cycle
from bisimulation import quotient
from search525 import HERE,decode_letter

def cycle(g):
    outgoing=[[]for _ in range(g['vertices'])]
    for i,(u,v,l)in enumerate(g['edges']):outgoing[u].append(i)
    u=next(i for i,es in enumerate(outgoing)if es);seen={};path=[]
    while u not in seen:
        seen[u]=len(path);e=outgoing[u][0];path.append(e);u=g['edges'][e][1]
    return path[seen[u]:]

def lift_operation(current,walk,op):
    before=op['graph'];original_labels=[current['edges'][e][2]for e in walk]
    if op['reverse']:
        qr=dict(vertices=current['vertices'],edges=[(v,u,l)for u,v,l in current['edges']])
        rr=dict(vertices=before['vertices'],edges=[(v,u,l)for u,v,l in before['edges']])
        result,power=lift_cycle(qr,list(reversed(walk)),rr,op['blocks'])
        result=list(reversed(result))
    else:result,power=lift_cycle(current,walk,before,op['blocks'])
    assert [before['edges'][e][2]for e in result]==original_labels*power
    assert all(before['edges'][result[j]][1]==before['edges'][result[(j+1)%len(result)]][0]for j in range(len(result)))
    return result,power

def audit_operation(before,after,blocks,reverse):
    assert len(blocks)==before['vertices']
    assert set(blocks)==set(range(after['vertices']))
    expected={(blocks[u],blocks[v],l)for u,v,l in before['edges']}
    assert expected==set(map(tuple,after['edges']))
    got=[set()for _ in range(before['vertices'])]
    wanted=[set()for _ in range(after['vertices'])]
    for u,v,l in before['edges']:
        if reverse:got[v].add((l,blocks[u]))
        else:got[u].add((l,blocks[v]))
    for u,v,l in after['edges']:
        if reverse:wanted[v].add((l,u))
        else:wanted[u].add((l,v))
    assert all(got[u]==wanted[blocks[u]]for u in range(before['vertices']))

def artificial():
    records=[]
    examples=[dict(vertices=6,edges=[(i,(i+1)%6,i%3)for i in range(6)]),
              dict(vertices=4,edges=[(0,1,0),(1,2,1),(2,3,2),(3,1,0)])]
    for case,g0 in enumerate(examples):
        for reverse in (False,True):
            # Mirror the input when testing the backward quotient, so the
            # same forced-power/transient phenomenon occurs in its direction.
            g=dict(vertices=g0['vertices'],edges=[(v,u,l)for u,v,l in g0['edges']]if reverse else g0['edges'])
            oriented=[(v,u,l)for u,v,l in g['edges']]if reverse else g['edges']
            q=quotient(g['vertices'],oriented)
            after=dict(vertices=q['vertices'],edges=[(v,u,l)for u,v,l in q['edges']]if reverse else q['edges'])
            op=dict(graph=g,blocks=q['blocks'],reverse=reverse)
            w=cycle(after);lifted,power=lift_operation(after,w,op)
            if case==0:assert power==2
            records.append(dict(case=case,reverse=reverse,power=power,quotient_length=len(w),lifted_length=len(lifted)))
    return records

def check_column(old,new,column):
    n=len(old)
    assert len(new)==n and len(column)==2*n
    for j in range(n):
        a,b,c,z=decode_letter(old[j]);alpha,beta,delta,zeta=decode_letter(new[j]);Q,R=column[2*j:2*j+2]
        e=(R-zeta)//10
        assert e in(0,1)and R-10*e==zeta
        assert 0<=Q<=18 and 0<=R<=18
        assert (Q+delta)//10==c
        assert R==(Q+a)%10+(Q+delta)%10
        assert (Q+a)//10==alpha and (R+b)//10==beta
        assert column[(2*j+2)%(2*n)]==(R+b)%10+z+e
        assert 0<=z+e<=9
        assert not(R<9 and e or R>9 and not e)

def real_strip(directory,depth,options):
    history=[json.loads((directory/f'graph_{k}.json').read_text())for k in range(depth+1)]
    current=history[-1]['graph'];walk=cycle(current);initial_length=len(walk);checks=0;powers=[]
    for k in range(depth,-1,-1):
        data=history[k];current=data['graph'];stage=data['stage']
        for op in reversed(stage['operations']):
            walk,power=lift_operation(current,walk,op);powers.append(power);current=op['graph']
        raw=stage['graph'];assert current==raw
        if k==0:break
        newwalk=[];col=[];old=[raw['edges'][e][2]for e in walk]
        for e in walk:
            u,v,l=raw['edges'][e];next_e,option=raw['origin'][u]
            newwalk.append(next_e);Q,a,b,c,oc,R=options[option];col.extend((Q,R))
        nextgraph=history[k-1]['graph']
        new=[nextgraph['edges'][e][2]for e in newwalk]
        check_column(old,new,col);checks+=len(old);walk=newwalk
    return dict(directory=directory.name,depth=depth,initial_pair_period=initial_length,
                final_pair_period=len(walk),power_factors=powers,checked_temporal_column_positions=checks,
                root_exterior_witness=False)

def run():
    start=time.monotonic();files=0;operations=0;vertices=0;edges=0
    for directory in [HERE/'bidirectional525',HERE/'all_bulk_bidir']:
        paths=sorted(directory.glob('graph_*.json'),key=lambda p:int(p.stem.split('_')[-1]))
        for path in paths:
            data=json.loads(path.read_text());ops=data['stage']['operations']
            for i,op in enumerate(ops):
                after=ops[i+1]['graph']if i+1<len(ops)else data['graph']
                audit_operation(op['graph'],after,op['blocks'],op['reverse'])
                operations+=1;vertices+=op['graph']['vertices'];edges+=len(op['graph']['edges'])
            files+=1
    options=json.loads((HERE.parent/'reverse/local_inverse_tables.json').read_text())['options']
    result=dict(status='saved_quotients_and_lift_checks_verified',
        graph_checkpoints=files,quotient_operations=operations,
        summed_input_vertices=vertices,summed_input_edges=edges,
        artificial_power_and_transient_checks=artificial(),
        real_inverse_strip_checks=[real_strip(HERE/'bidirectional525',6,options),
                                  real_strip(HERE/'all_bulk_bidir',5,options)],
        seconds=time.monotonic()-start,finite_exterior_found=False,
        arbitrary_width_status='UNKNOWN',decimal_lychrel_existence_proved=False)
    (HERE/'lift_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':run()
