"""Heuristic ICE state merging; every candidate must pass exact global checks.

This is a search procedure, not a proof of a decimal Lychrel number.
The 19 folded symbols and 11 center terminators form a 30-letter alphabet.
"""
from collections import deque
import json, time
import creative_regular_invariant as r

def word(w): return w[0]+(19+r.terminal_index(w[1]),)

def safe_product(dfa):
    """Intersect a learned language with the exact safe-word language."""
    delta,finish=dfa;start=(0,True,True,False);states=[start];ids={start:0};d=[];f=[]
    for s,low,exc,started in states:
        row=[]
        for q in range(19):
            nxt=(delta[s][q],low and q<=9,exc and (q in (0,11) if started else q==11),True)
            if nxt not in ids:ids[nxt]=len(states);states.append(nxt)
            row.append(ids[nxt])
        d.append(row);flags=[]
        for j,c in enumerate([None]+list(range(0,19,2))):
            bad=(low and (c is None or c<=9)) or (exc and started and (c is None or c==0))
            flags.append(finish[s][j] and not bad)
        f.append(flags)
    return d,f

def learn(positive, negative, implications):
    trans=[{}]
    def insert(w):
        s=0
        for a in word(w):
            if a not in trans[s]:
                trans[s][a]=len(trans);trans.append({})
            s=trans[s][a]
        return s
    ps={insert(w) for w in sorted(positive,key=lambda w:(len(w[0]),word(w)))}
    ns={insert(w) for w in sorted(negative,key=lambda w:(len(w[0]),word(w)))}
    impl=[(insert(a),insert(b)) for a,b in sorted(implications,key=lambda ab:(len(ab[0][0]),word(ab[0]),word(ab[1])))]
    parent=list(range(len(trans)))
    def root(par,a):
        while par[a]!=a:a=par[a]
        return a
    def accepting(par):
        pos={root(par,a) for a in ps};neg={root(par,a) for a in ns}
        edges={}
        for a,b in impl:edges.setdefault(root(par,a),set()).add(root(par,b))
        queue=list(pos)
        while queue:
            a=queue.pop()
            if a in neg:return None
            for b in edges.get(a,()):
                if b not in pos:pos.add(b);queue.append(b)
        return pos
    def merge(a,b):
        par=parent[:];tr=[dict(t) for t in trans];queue=[(a,b)]
        while queue:
            a,b=(root(par,x) for x in queue.pop())
            if a==b:continue
            if a>b:a,b=b,a
            par[b]=a
            for symbol,c in tr[b].items():
                if symbol in tr[a]:queue.append((tr[a][symbol],c))
                else:tr[a][symbol]=c
        if accepting(par) is None:return None
        return par,tr
    assert accepting(parent) is not None
    red={0}
    while True:
        red={root(parent,a) for a in red}
        blue={root(parent,b) for a in red for b in trans[a].values()}-red
        if not blue:break
        b=min(blue);merged=False
        for a in sorted(red):
            out=merge(a,b)
            if out is not None:
                parent,trans=out;merged=True;break
        if not merged:red.add(b)
    yes=accepting(parent);roots=sorted({root(parent,a) for a in range(len(parent))})
    # Only states reachable through raw pair symbols need appear in the output DFA.
    relevant={root(parent,0)};todo=list(relevant)
    while todo:
        a=todo.pop()
        for q,b in trans[a].items():
            b=root(parent,b)
            if q<19 and b not in relevant:relevant.add(b);todo.append(b)
    relevant=sorted(relevant);ren={a:i for i,a in enumerate(relevant)};dead=len(relevant)
    d=[];f=[]
    for a in relevant:
        d.append([ren[root(parent,trans[a][q])] if q in trans[a] else dead for q in range(19)])
        f.append([19+j in trans[a] and root(parent,trans[a][19+j]) in yes for j in range(11)])
    d.append([dead]*19);f.append([False]*11)
    dfa=(d,f)
    assert all(r.accepted(dfa,w) for w in positive)
    assert all(not r.accepted(dfa,w) for w in negative)
    assert all(not r.accepted(dfa,a) or r.accepted(dfa,b) for a,b in implications)
    return dfa,len(trans)

def main(seconds=240):
    positive=set();negative=set();implications=set();w=((7,),18)
    for _ in range(50):positive.add(w);w=r.qstep(w)
    for n in range(1,1001):
        ds=tuple(map(int,str(n)));w=r.fold(tuple(a+b for a,b in zip(ds,ds[::-1])));chain=[]
        for _ in range(15):
            if r.bad(w):negative.update(chain+[w]);break
            chain.append(w);w=r.qstep(w)
    start=time.time();log=[]
    for i in range(1000):
        learned,nodes=learn(positive,negative,implications)
        dfa=safe_product(learned)
        ce=r.safety_counterexample(dfa)
        if ce is not None:negative.add(ce);kind='safety'
        else:
            ce=r.closure_counterexample(dfa)
            if ce is None:
                result={'status':'CERTIFICATE','dfa':dfa,'iteration':i}
                with open('creative_regular_merge_certificate.json','w') as fp:json.dump(result,fp)
                print(json.dumps(result),flush=True);return
            source,target=ce;w=target;chain=[source,target]
            for _ in range(20):
                if r.bad(w):negative.update(chain);kind='terminating';break
                w=r.qstep(w);chain.append(w)
            else:implications.add(ce);kind='closure'
        row={'iteration':i,'states':len(dfa[0]),'trie_nodes':nodes,'counterexample':kind,'seconds':round(time.time()-start,2)}
        log.append(row);print(json.dumps(row),flush=True)
        with open('creative_regular_merge_results.json','w') as fp:json.dump(log,fp,indent=2)
        if time.time()-start>seconds:break

if __name__=='__main__':main()
