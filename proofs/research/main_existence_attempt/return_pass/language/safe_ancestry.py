r"""One bounded safe-ancestry refinement, preserving all older certificates.

S_1=G(Canonical\B), S_2=G(S_1\B). Thus every r-step generating history
avoids palindromes at all r positive-time integer outputs. The test takes
the exact image language and intersects its state partition with D0, then
synthesizes every possible terminal acceptance set by the universal kernel.
"""
from collections import deque
import json
import time
from residual_kernel import HERE,base_machine,minimize,kernel
from compact_kernel import carry_graph
from image_ancestry import product_observer,predecessors


def safe_source(image=None):
    bd,bf=base_machine()
    if image is None:
        return bd,[[v==0 for v in row] for row in bf]
    d,f=image
    keys=[(0,0)]
    ids={keys[0]:0}
    nd,nf=[],[]
    for a,b in keys:
        row=[]
        for q in range(19):
            key=d[a][q],bd[b][q]
            if key not in ids:
                ids[key]=len(keys)
                keys.append(key)
            row.append(ids[key])
        nd.append(row)
        nf.append([bool(f[a][j]) and bf[b][j]==0 for j in range(11)])
    return minimize((nd,nf))


def image_of(source,deadline,cap=100000,nfa_save=None):
    d,f=source
    fedges,fterms=carry_graph()
    keys=[(0,0),(1,0)]
    ids={key:i for i,key in enumerate(keys)}
    transitions=[]
    flags=[]
    terminal_extra=[]
    for index,(x,a) in enumerate(keys):
        if index%1000==0 and time.monotonic()>deadline:
            return None,dict(status='UNKNOWN_time_cap',phase='nfa',states=len(keys))
        row={}
        for q,out,y in fedges[x]:
            key=y,d[a][q]
            if key not in ids:
                ids[key]=len(keys)
                keys.append(key)
            row.setdefault(out,set()).add(ids[key])
        mask=0
        extra_symbols=set()
        for cidx,extra,ocidx in fterms[x]:
            if not f[a][cidx]:
                continue
            if extra is None:
                mask|=1<<ocidx
            else:
                assert ocidx==0
                extra_symbols.add(extra)
        transitions.append(row)
        flags.append(mask)
        terminal_extra.append(extra_symbols)
    last=len(keys)
    for row,extras in zip(transitions,terminal_extra):
        for q in extras:
            row.setdefault(q,set()).add(last)
    transitions.append({})
    flags.append(1)
    # Trim nonaccepting dead paths before the output subset construction.
    rev=[[] for _ in transitions]
    for a,row in enumerate(transitions):
        for targets in row.values():
            for b in targets:
                rev[b].append(a)
    useful={a for a,flag in enumerate(flags) if flag}
    todo=list(useful)
    for b in todo:
        for a in rev[b]:
            if a not in useful:
                useful.add(a)
                todo.append(a)
    order=sorted(useful)
    ren={old:new for new,old in enumerate(order)}
    es=[]
    fs=[]
    for old in order:
        row=[0]*19
        for q,targets in transitions[old].items():
            for b in targets:
                if b in ren:
                    row[q]|=1<<ren[b]
        es.append(row)
        fs.append(flags[old])
    initial=sum(1<<ren[a] for a in (0,1) if a in ren)
    raw_nfa=len(transitions)
    if nfa_save is not None:
        sparse=[]
        for row in es:
            entries=[]
            for q,bits in enumerate(row):
                if not bits:
                    continue
                targets=[]
                while bits:
                    bit=bits&-bits
                    targets.append(bit.bit_length()-1)
                    bits-=bit
                entries.append([q,targets])
            sparse.append(entries)
        nfa_save.write_text(json.dumps(dict(initial=[ren[a] for a in (0,1) if a in ren],
                            terminal_masks=fs,transitions=sparse),separators=(',',':'))+'\n')
    del transitions,rev,keys,ids
    subsets=[initial]
    ids={initial:0}
    nd,nf=[],[]
    largest=0
    for index,bits in enumerate(subsets):
        if index%100==0 and time.monotonic()>deadline:
            return None,dict(status='UNKNOWN_time_cap',phase='subsets',states=len(subsets),nfa_states=raw_nfa,trimmed_nfa_states=len(es))
        largest=max(largest,bits.bit_count())
        out=[0]*19
        mask=0
        b=bits
        while b:
            bit=b&-b
            a=bit.bit_length()-1
            mask|=fs[a]
            for q in range(19):
                out[q]|=es[a][q]
            b-=bit
        row=[]
        for target in out:
            if target not in ids:
                if len(subsets)>=cap:
                    return None,dict(status='UNKNOWN_state_cap',phase='subsets',states=len(subsets),processed_subsets=index,nfa_states=raw_nfa,trimmed_nfa_states=len(es),largest_subset=largest)
                ids[target]=len(subsets)
                subsets.append(target)
            row.append(ids[target])
        nd.append(row)
        nf.append([int(bool(mask&(1<<j))) for j in range(11)])
    machine=minimize((nd,nf))
    return machine,dict(status='COMPLETE',source_states=len(d),nfa_states=raw_nfa,
                        trimmed_nfa_states=len(es),subset_states=len(subsets),
                        states=len(machine[0]),largest_subset=largest)


def accepted(machine,w):
    d,f=machine
    s=0
    for q in w[0]:
        s=d[s][q]
    return bool(f[s][0 if w[1] is None else w[1]//2+1])


def main():
    start=time.monotonic()
    deadline=start+300
    image=None
    report=dict(status='FOCUSED_SAFE_ANCESTRY',seconds_cap=300,runs=[])
    splice=((5,0,5,13,17),None)
    first,_=predecessors(splice,True)
    second=[]
    for middle in first:
        ps,_=predecessors(middle,True)
        second.extend(ps)
    report['splice_exact_predecessors']=[list(w) for w in first]
    report['splice_exact_two_step_predecessors']=[list(w) for w in second]
    for r in (1,2):
        image,build=image_of(safe_source(image),deadline)
        if image is None:
            report['runs'].append(dict(ancestry_depth=r,build=build,status='UNKNOWN',live_class_count=None))
            break
        tag='safe%d_'%r
        (HERE/('safe_image%d_machine.json'%r)).write_text(json.dumps(dict(delta=image[0],finish=image[1]),separators=(',',':'))+'\n')
        product=product_observer(base_machine(),image,cap=300000)
        row=dict(ancestry_depth=r,build=build,splice_in_safe_image=accepted(image,splice))
        if product is None:
            row.update(status='UNKNOWN_observer_cap',live_class_count=None)
            report['runs'].append(row)
            break
        (HERE/('observation_%sdepth0.json'%tag)).write_text(json.dumps(dict(depth=0,delta=product[0],finish=product[1]),separators=(',',':'))+'\n')
        result=kernel(product,cap=1000000,deadline=deadline)
        (HERE/('kernel_%sdepth0.json'%tag)).write_text(json.dumps(result,separators=(',',':'))+'\n')
        row.update({k:v for k,v in result.items() if k not in ('eliminated','live_classes')})
        row['live_class_count']=len(result['live_classes']) if 'live_classes' in result else None
        report['runs'].append(row)
        print(json.dumps(row),flush=True)
        # Even if the S1 kernel hits its product cap, building S2 is a different
        # exact refinement and may remove the known splice. No depth beyond 2.
        if result['status']=='POSITIVE_CANDIDATE' or time.monotonic()>deadline:
            break
    report['seconds']=time.monotonic()-start
    (HERE/'safe_ancestry_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(seconds=report['seconds'],statuses=[r['status'] for r in report['runs']])),flush=True)


if __name__=='__main__':
    main()
