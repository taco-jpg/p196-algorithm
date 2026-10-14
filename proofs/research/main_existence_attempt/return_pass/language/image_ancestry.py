"""Focused exact image-ancestry refinement; fixed five-minute experiment.

Membership concerns a folded pair-sum word, not one chosen digit splitting.
An inverse path supplies a canonical predecessor whose numerical image has
the requested pair-sum word. Exhausting the finite path graph proves absence.
"""
from collections import deque
import json
import time
from residual_kernel import (HERE,CENTERS,START_FST,fst_edge,fst_term,ci,
                             canonical,realize,numeric_word,minimize,kernel)


def predecessors(word, all_paths=False):
    pairs,center=word
    layers=[{st:[()] for st in START_FST}]
    answers=set()
    examined=0
    for k in range(len(pairs)+1):
        layer=layers[-1]
        for st,paths in layer.items():
            for c in CENTERS:
                term=fst_term(st,c)
                if term is None:
                    continue
                extra,oc=term
                if oc!=center:
                    continue
                if ((extra is None and k==len(pairs)) or
                    (extra is not None and k+1==len(pairs) and extra==pairs[k])):
                    for p in paths:
                        assert canonical(p,c)
                        n=realize(p,c)
                        assert numeric_word(n+int(str(n)[::-1]))==(tuple(pairs),center)
                        answers.add((p,c))
        if k==len(pairs):
            break
        nxt={}
        for st,paths in layer.items():
            for q in range(19):
                for target,out in fst_edge(st,q):
                    examined+=1
                    if out!=pairs[k]:
                        continue
                    ps=nxt.setdefault(target,[])
                    if all_paths:
                        ps.extend(p+(q,) for p in paths)
                    elif not ps:
                        ps.append(paths[0]+(q,))
        layers.append(nxt)
    return sorted(answers,key=lambda w:(len(w[0]),w[0],ci(w[1]))),examined


def image_machine(cap=100000):
    keys=list(START_FST)
    ids={s:i for i,s in enumerate(keys)}
    edges=[]
    terms=[]
    for st in keys:
        row=[0]*19
        for q in range(19):
            for target,out in fst_edge(st,q):
                if target not in ids:
                    ids[target]=len(keys)
                    keys.append(target)
                row[out]|=1<<ids[target]
        edges.append(row)
        terms.append([fst_term(st,c) for c in CENTERS])
    assert len(keys)==46
    final=46
    finish=[0]*47
    for i,ts in enumerate(terms):
        for term in ts:
            if term is None:
                continue
            extra,oc=term
            if extra is None:
                finish[i]|=1<<ci(oc)
            else:
                assert oc is None
                edges[i][extra]|=1<<final
    edges.append([0]*19)
    finish[final]=1
    subsets=[3]
    sid={3:0}
    d,f=[],[]
    for bits in subsets:
        row=[0]*19
        mask=0
        b=bits
        while b:
            bit=b&-b
            i=bit.bit_length()-1
            mask|=finish[i]
            for q in range(19):
                row[q]|=edges[i][q]
            b-=bit
        out=[]
        for target in row:
            if target not in sid:
                if len(subsets)>=cap:
                    return None,dict(status='UNKNOWN_state_cap',states=len(subsets))
                sid[target]=len(subsets)
                subsets.append(target)
            out.append(sid[target])
        d.append(out)
        f.append([int(bool(mask&(1<<j))) for j in range(11)])
    machine=minimize((d,f))
    return machine,dict(status='COMPLETE',nfa_states=47,subset_states=len(subsets),states=len(machine[0]))


def product_observer(machine,image,cap=300000):
    d,f=machine
    e,g=image
    states=[(0,0)]
    ids={states[0]:0}
    nd,nf=[],[]
    for a,b in states:
        row=[]
        for q in range(19):
            st=d[a][q],e[b][q]
            if st not in ids:
                if len(states)>=cap:
                    return None
                ids[st]=len(states)
                states.append(st)
            row.append(ids[st])
        nd.append(row)
        nf.append(f[a])
    # Deliberately retain image context; minimizing only the bad-bit outputs
    # would erase the refinement. Terminal acceptance remains unrestricted.
    return nd,nf


def main():
    started=time.monotonic()
    deadline=started+300
    replay=json.loads((HERE/'independent_replay_extended.json').read_text())[-1]
    chain=replay['seed196_language_obstruction']
    rows=[]
    for item in chain:
        word=item['pair_word']
        preds,visited=predecessors(word,all_paths=True)
        depth2=[]
        for first in preds:
            second,_=predecessors(first)
            if second:
                depth2=[second[0],first]
                break
        row=dict(word=word,representative=item['witness_number'],image1=bool(preds),
                 exact_predecessor_count=len(preds),inverse_edges_examined=visited,
                 image2=bool(depth2))
        if preds:
            first=preds[0]
            n=realize(*first)
            row.update(predecessor_word=first,predecessor_integer=str(n),
                       actual_image_integer=str(n+int(str(n)[::-1])))
        if depth2:
            n=realize(*depth2[0])
            z=n+int(str(n)[::-1])
            zz=z+int(str(z)[::-1])
            assert numeric_word(zz)==(tuple(word[0]),word[1])
            row.update(two_step_predecessor=str(n),two_step_middle=str(z),two_step_image=str(zz))
        rows.append(row)
    image,build=image_machine()
    result=dict(status='FOCUSED_EXPERIMENT_COMPLETE',chain_membership=rows,image_build=build,kernel_runs=[])
    if image:
        (HERE/'image1_machine.json').write_text(json.dumps(dict(delta=image[0],finish=image[1]),separators=(',',':'))+'\n')
        for depth in range(4):
            obs=json.loads((HERE/('observation_depth%d.json'%depth)).read_text())
            prod=product_observer((obs['delta'],obs['finish']),image)
            if prod is None:
                result['kernel_runs'].append(dict(depth=depth,status='UNKNOWN_observer_cap'))
                break
            (HERE/('observation_image1_depth%d.json'%depth)).write_text(json.dumps(dict(depth=depth,delta=prod[0],finish=prod[1]),separators=(',',':'))+'\n')
            answer=kernel(prod,cap=1000000,deadline=deadline)
            (HERE/('kernel_image1_depth%d.json'%depth)).write_text(json.dumps(answer,separators=(',',':'))+'\n')
            summary=dict(depth=depth,image_refined_states=len(prod[0]),**{k:v for k,v in answer.items() if k not in ('eliminated','live_classes')})
            summary['live_class_count']=len(answer['live_classes']) if 'live_classes' in answer else None
            result['kernel_runs'].append(summary)
            print(json.dumps(summary),flush=True)
            if answer['status']!='EMPTY_KERNEL':
                break
    result['seconds']=time.monotonic()-started
    (HERE/'image_ancestry_report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(seconds=result['seconds'],image_build=build,chain_memberships=[(r['image1'],r['image2']) for r in rows])),flush=True)


if __name__=='__main__':
    main()
