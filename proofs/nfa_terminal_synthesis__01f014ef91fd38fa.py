"""Direct NFA terminal-acceptance synthesis without determinization.

Each terminal flag denotes the language of all complete NFA paths ending
there. An arbitrary flag subset accepts their union. A concrete terminating
word in a component forbids its flag in EVERY safe forward-closed union.
This searches the positive family by eliminating only proved-impossible
flags. An uneliminated flag is not a positive invariant certificate.
"""
from collections import deque,Counter
from pathlib import Path
import hashlib,heapq,json,random,time,argparse

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCE=ROOT/'main_existence_attempt/return_pass/language/safe_image2_nfa.json'


def number(p,c):
    return int(''.join(str(min(9,q)) for q in p)+('' if c is None else str(c//2))+
               ''.join(str(max(0,q-9)) for q in reversed(p)))


def palindrome_hit(p,c,limit):
    n=number(p,c)
    for t in range(1,limit+1):
        n+=int(str(n)[::-1])
        if str(n)==str(n)[::-1]:
            return t
    return None


def parent_word(parent,key):
    pairs=[]
    nodes=[key[0] if isinstance(key,tuple) else key]
    while parent[key] is not None:
        key,q=parent[key]
        pairs.append(q)
        nodes.append(key[0] if isinstance(key,tuple) else key)
    return tuple(reversed(pairs)),list(reversed(nodes))


def direct_safety(a,proofs):
    initial=[(s,True,True,False) for s in a['initial']]
    parent={s:None for s in initial}
    queue=list(initial)
    for key in queue:
        u,low,exc,started=key
        for j in range(11):
            if not(a['terminal_masks'][u]>>j&1) or (u,j) in proofs:
                continue
            c=None if j==0 else 2*(j-1)
            if not started and c in (None,0):
                continue
            isbad=(low and (c is None or c<=9)) or (exc and started and c in (None,0))
            if isbad:
                pairs,path=parent_word(parent,key)
                assert palindrome_hit(pairs,c,1)==1
                proofs[u,j]=dict(flag=[u,j],pairs=pairs,center=c,path=path,hit_steps=1,
                                 discovery='exact_current_safety_product')
        for q,targets in a['transitions'][u]:
            if q==0 and not started:
                continue
            for v in targets:
                nxt=(v,low and q<=9,exc and (q in (0,11) if started else q==11),True)
                if nxt not in parent:
                    parent[nxt]=key,q
                    queue.append(nxt)
    return len(queue)


def representative_tree(a,rng,trial):
    initial=list(a['initial'])
    rng.shuffle(initial)
    parent={s:None for s in initial}
    if trial<10:
        queue=list(initial)
        for u in queue:
            edges=[(q,v) for q,vs in a['transitions'][u] for v in vs]
            rng.shuffle(edges)
            for q,v in edges:
                if v not in parent:
                    parent[v]=u,q
                    queue.append(v)
    else:
        # Random positive edge costs give finite alternate prefixes, including
        # longer representatives that the shortest-prefix tree cannot expose.
        distance={s:0 for s in initial}
        heap=[(0,s) for s in initial]
        heapq.heapify(heap)
        while heap:
            cost,u=heapq.heappop(heap)
            if distance[u]!=cost:
                continue
            for q,vs in a['transitions'][u]:
                for v in vs:
                    nc=cost+rng.randrange(1,10)
                    if nc<distance.get(v,10**12):
                        distance[v]=nc
                        parent[v]=u,q
                        heapq.heappush(heap,(nc,v))
    return parent


def main(seconds=300,trials=150,orbit_limit=200):
    start=time.monotonic()
    a=json.loads(SOURCE.read_text())
    flags={(u,j) for u,m in enumerate(a['terminal_masks']) for j in range(11) if m>>j&1}
    proofs={}
    safety_states=direct_safety(a,proofs)
    safety_excluded=len(proofs)
    rng=random.Random(1400926)
    seen_words={}
    progress=[]
    for trial in range(trials):
        if len(proofs)==len(flags) or time.monotonic()-start>=seconds:
            break
        parent=representative_tree(a,rng,trial)
        for u,j in sorted(flags-proofs.keys()):
            if time.monotonic()-start>=seconds:
                break
            p,path=parent_word(parent,u)
            c=None if j==0 else 2*(j-1)
            w=p,c
            if w not in seen_words:
                seen_words[w]=palindrome_hit(p,c,orbit_limit)
            hit=seen_words[w]
            if hit is not None:
                proofs[u,j]=dict(flag=[u,j],pairs=p,center=c,path=path,hit_steps=hit,
                                 discovery='finite_arithmetic_component_witness',trial=trial)
        row=dict(trial=trial,excluded=len(proofs),remaining=len(flags)-len(proofs),
                 different_words_tested=len(seen_words),seconds=time.monotonic()-start)
        progress.append(row)
        print(json.dumps(row),flush=True)
    remaining=sorted(flags-proofs.keys())
    data=dict(status='EMPTY_ACCEPTANCE_FAMILY' if not remaining else 'UNRESOLVED_ACCEPTANCE_FAMILY',
              nfa_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),nfa_states=len(a['transitions']),
              flags=len(flags),safety_product_states=safety_states,direct_safety_exclusions=safety_excluded,
              eliminated=len(proofs),remaining_flags=remaining,orbit_limit=orbit_limit,
              trial_cap=trials,seconds_cap=seconds,seconds=time.monotonic()-start,
              progress=progress,proofs=[proofs[k] for k in sorted(proofs)])
    (HERE/'terminal_acceptance_result.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in data.items() if k not in ('proofs','progress','remaining_flags')}),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--seconds',type=float,default=300)
    p.add_argument('--trials',type=int,default=150)
    p.add_argument('--orbit-limit',type=int,default=200)
    args=p.parse_args()
    main(args.seconds,args.trials,args.orbit_limit)
