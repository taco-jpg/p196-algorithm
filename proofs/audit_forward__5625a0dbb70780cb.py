"""Independent arithmetic/provenance audit of saved forward histories.

Checks complete SCC-trimmed images, every saved bisimulation quotient,
and explicitly lifted cycles using ordinary two-direction decimal carries.
It does not upgrade a capped join to a completed one.
"""
from pathlib import Path
from collections import defaultdict,deque,Counter
from itertools import product
import sys,json,time
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE),str(HERE.parent/'structure')]
from forward_join import forward_tables,decode_forward,any_cycle
from pair_language import scc

def decode(v):
    bits,z=divmod(v,11)
    return bits//4,(bits//2)%2,bits%2,z-1

def encode(a,b,c,z):return ((a*2+b)*2+c)*11+z+1

def independent_options():
    result=[set()for _ in range(88)]
    for letter in range(88):
        a,b,c,z=decode(letter)
        for Q in range(19):
            for innerN in range(2):
                high_value=Q+innerN
                if high_value//10!=c:continue
                low_value=Q+a
                R=high_value%10+low_value%10
                for outerO in range(2):
                    if not any((R+innerO)//10==outerO for innerO in range(2)):continue
                    previous_high_digit=z+outerO
                    if not 0<=previous_high_digit<=9:continue
                    odd_value=R+b
                    nextQ=odd_value%10+previous_high_digit
                    if not 0<=nextQ<=18:continue
                    new=encode(low_value//10,odd_value//10,innerN,R-10*outerO)
                    result[letter].add((Q,innerN,outerO,R,nextQ,new))
    return result

def check_image(old,raw,options,fibers):
    es=old['edges'];vertices=[(e,o)for e,(_,_,l)in enumerate(es)for o in fibers[l]]
    index={x:i for i,x in enumerate(vertices)}
    starts=defaultdict(list)
    for v,(e,o)in enumerate(vertices):starts[es[e][0],options[o][0]].append(v)
    generated=[]
    for u,(e,o)in enumerate(vertices):
        for v in starts[es[e][1],options[o][4]]:
            generated.append((u,v,options[o][5]))
    component=scc(len(vertices),[(u,v)for u,v,l in generated])
    retained=[e for e in generated if component[e[0]]==component[e[1]]]
    # A singleton component retains only its actual self-loops.
    wanted_origins=sorted({vertices[u]for u,v,l in retained}|{vertices[v]for u,v,l in retained})
    assert len(set(map(tuple,raw['origin'])))==raw['vertices']
    assert set(map(tuple,raw['origin']))==set(wanted_origins)
    expected={(vertices[u],vertices[v],l)for u,v,l in retained}
    actual={(tuple(raw['origin'][u]),tuple(raw['origin'][v]),l)for u,v,l in raw['edges']}
    assert expected==actual and len(raw['edges'])==len(actual)
    return dict(raw_vertices=len(vertices),raw_edges=len(generated),
                trimmed_vertices=raw['vertices'],trimmed_edges=len(raw['edges']))

def check_quotients(record):
    operations=record['stage']['operations'];counts=[]
    for i,op in enumerate(operations):
        raw=op['graph'];blocks=op['blocks'];reverse=op['reverse']
        expected=operations[i+1]['graph']if i+1<len(operations)else record['graph']
        assert len(blocks)==raw['vertices']
        n=max(blocks,default=-1)+1
        projected={(blocks[u],blocks[v],l)for u,v,l in raw['edges']}
        assert n==expected['vertices'] and projected==set(map(tuple,expected['edges']))
        actual=[set()for _ in blocks];wanted=[set()for _ in range(n)]
        for u,v,l in raw['edges']:
            if reverse:u,v=v,u
            actual[u].add((l,blocks[v]))
        for u,v,l in projected:
            if reverse:u,v=v,u
            wanted[u].add((l,v))
        assert all(actual[u]==wanted[blocks[u]]for u in range(len(blocks)))
        counts.append(dict(reverse=reverse,old_vertices=len(blocks),new_vertices=n))
    return counts

def replay_strip(columns,cut_word):
    """Ordinary carries, without the forward transfer generator."""
    width=len(columns);n=len(cut_word);assert all(len(c)==2*n for c in columns)
    for j,letter in enumerate(cut_word):
        end_a,end_b,end_c,end_z=decode(letter)
        Q=[col[2*j]for col in columns];R=[col[2*j+1]for col in columns]
        assert Q[0]==8 and R[0]==17
        assert all(0<=x<=18 for x in Q+R)
        # Normalize N from the known inner carry outwards.
        highN=[0]*width;carry=end_c
        for i in range(width-1,-1,-1):
            carry,highN[i]=divmod(Q[i]+carry,10)
        assert carry==0
        lowN=[];carry=0
        for x in Q:carry,digit=divmod(x+carry,10);lowN.append(digit)
        assert carry==end_a
        assert R==[x+y for x,y in zip(lowN,highN)]
        # Last outward O carry is fixed by the pending-digit component z.
        assert (R[-1]-end_z)%10==0
        outward=(R[-1]-end_z)//10;assert outward in (0,1)
        assert any((R[-1]+inner)//10==outward for inner in (0,1))
        highO=[None]*width;carry=outward
        for i in range(width-2,-1,-1):
            carry,highO[i]=divmod(R[i]+carry,10)
        assert carry==1
        lowO=[];carry=0
        for x in R:carry,digit=divmod(x+carry,10);lowO.append(digit)
        assert carry==end_b
        expected=[lowO[0]+1]+[lowO[i]+highO[i-1]for i in range(1,width)]
        actual=[col[(2*j+2)%(2*n)]for col in columns]
        assert expected==actual
    return dict(width=width,pair_period=n,ordinary_column_phase_checks=2*n*width)

def independent_empty_product(left,right):
    """Rebuild every matching-label product edge, then delete sinks."""
    by_label=defaultdict(list)
    for x,y,label in right['edges']:by_label[label].append((x,y))
    ids={};incoming=[];outdegree=[];height=[];nedges=0
    def node(u,x):
        key=u*right['vertices']+x
        old=ids.get(key)
        if old is not None:return old
        i=len(ids);ids[key]=i;incoming.append([]);outdegree.append(0);height.append(0)
        return i
    for u,v,label in left['edges']:
        for x,y in by_label[label]:
            a=node(u,x);b=node(v,y)
            incoming[b].append(a);outdegree[a]+=1;nedges+=1
    queue=deque(i for i,d in enumerate(outdegree)if not d);removed=0
    while queue:
        v=queue.popleft();removed+=1
        for u in incoming[v]:
            height[u]=max(height[u],height[v]+1);outdegree[u]-=1
            if not outdegree[u]:queue.append(u)
    assert removed==len(ids)
    return dict(product_vertices=len(ids),product_edges=nedges,
                sink_deletion_count=removed,maximum_product_path=max(height,default=0),
                height_histogram=dict(sorted(Counter(height).items())),empty_cyclic_intersection=True)

def main():
    start=time.monotonic();options,fibers=forward_tables();independent=independent_options()
    assert sum(map(len,fibers))==1640
    assert all({options[i]for i in fibers[l]}==independent[l]for l in range(88))
    paths=sorted(HERE.glob('graph_*.json'),key=lambda p:int(p.stem.split('_')[-1]))
    history=[json.loads(p.read_text())for p in paths]
    images=[];quotients=[];lifts=[]
    for k in range(1,len(history)):
        rec=history[k]
        image=check_image(history[k-1]['graph'],rec['stage']['graph'],options,fibers)
        images.append(dict(depth=k,**image))
        ops=check_quotients(rec);quotients.extend(dict(depth=k,**x)for x in ops)
        cycle=any_cycle(rec['graph']['vertices'],rec['graph']['edges'])
        assert cycle is not None
        cols,power,logs=decode_forward(history[:k+1],cycle,options)
        word=[rec['graph']['edges'][e][2]for e in cycle]*power
        lifts.append(dict(depth=k,lift_power=power,**replay_strip(cols,word)))
        print(json.dumps(dict(depth=k,image=image,quotient_operations=len(ops),lift=lifts[-1])),flush=True)
    # Positive control for graph intersection: each cycle intersects itself.
    from forward_join import intersection
    controls=[]
    for k in (0,1,2,3):
        hit,stats=intersection(history[k]['graph'],history[k]['graph'],2000000)
        assert hit is not None and stats['cycle_length']>0
        controls.append(dict(depth=k,cycle_length=stats['cycle_length']))
    checked_joins=[]
    for mode,folder,depth in [('525','bidirectional525',12),('all334','all_bulk_bidir',9)]:
        path=HERE.parent/'reverse525'/folder/f'graph_{depth}.json'
        right=json.loads(path.read_text())['graph']
        checked_joins.append(dict(mode=mode,forward_depth=4,reverse_depth=depth,
                                 width=5+depth,**independent_empty_product(history[4]['graph'],right)))
        print(json.dumps(dict(kind='independent_join',**checked_joins[-1])),flush=True)
    result=dict(status='PASS',local_forward_options=1640,local_letters=88,
                complete_images=images,quotient_operations=len(quotients),quotient_details=quotients,
                lifted_forward_strips=lifts,positive_intersection_controls=controls,
                independent_empty_joins=checked_joins,
                seconds=time.monotonic()-start,
                finite_exterior_found=False,finite_lychrel_witness=False)
    (HERE/'audit_forward_result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k not in ('complete_images','quotient_details','lifted_forward_strips')}),flush=True)

if __name__=='__main__':main()
