#!/usr/bin/env python3
"""Symbolic backwards safety-language construction for folded pairwords.
Bad_0 = PrePal. Bad_{h+1} = Bad_h union R^-1(Bad_h).
Each finite-stage language is regular, and complement of a fixed point is
an inductively closed candidate certificate format. This is constructive
positive synthesis, not an exclusion census.
"""
from collections import deque
from transducer import fold,pairs,step_digits
from dfa_checker import DFA,check_dfa

ALPH=list(range(19))+['E']+[f'O{i}' for i in range(0,19,2)]
AIDX={x:i for i,x in enumerate(ALPH)}

class TableDFA(DFA):
    def __init__(self,trans,accept):
        self.trans=trans;self.accept=accept
        super().__init__(0,lambda q,x:self.trans[q][AIDX[x]],lambda q: self.accept[q])


def nfa_pal_init():
    return frozenset(('P',g,0,g,-1,0) for g in [0,1])

def nfa_pre_init(prior):
    return frozenset([('U',prior.initial,0)]+[('T',g,0,g,-1,0,prior.initial) for g in [0,1]])


def update_outer(st,x,prior=None):
    typ=st[0];new=[]
    if typ=='ACCEPT':return []
    if typ=='U':
        _,q,started=st
        if not started and x==0:return []
        return [('U',prior.delta(q,x),1)]
    if typ=='P':
        _,g,c,t,prev,started=st
    else:
        _,g,c,t,prev,started,q=st
    if not started and x==0:return []
    lo=(x+c)%10; nc=(x+c)//10
    for nt in [0,1]:
        if (x+nt)//10 != t:continue
        hi=(x+nt)%10
        if typ=='P':
            if g==0 and lo!=hi: continue
            if g==1 and lo!=(1 if not started else prev):continue
            new.append(('P',g,nc,nt,hi,1))
        else:
            emitted=(lo+hi if g==0 else lo+(1 if not started else prev))
            new.append(('T',g,nc,nt,hi,1,prior.delta(q,emitted)))
    return new


def terminal_accept(st,term,prior=None):
    typ=st[0]
    if typ=='ACCEPT':return False
    if typ=='U':
        _,q,started=st
        if term=='E':return started and prior.final(prior.delta(q,'E'))
        z=int(term[1:]);return (started or z>=2) and prior.final(prior.delta(q,term))
    if typ=='P':_,g,c,t,prev,started=st
    else:_,g,c,t,prev,started,q=st
    if term=='E':
        if not started or c!=t:return False
        if typ=='P':return True
        return prior.final(prior.delta(q,'E' if g==0 else f'O{2*prev}'))
    z=int(term[1:]);
    if not started and z<2:return False
    a=(z+c)%10
    if (z+c)//10!=t:return False
    if typ=='P':return g==0 or a==(prev if started else 1)
    if g==0:return prior.final(prior.delta(q,f'O{2*a}'))
    q=prior.delta(q,a+(prev if started else 1))
    return prior.final(prior.delta(q,'E'))


def build_dfa(prior=None,limit=100000):
    """Subset construction with terminal accepted/rejected sinks.
    Only accepts complete physically-realizable folded words.
    """
    start=nfa_pal_init() if prior is None else nfa_pre_init(prior)
    sets=[start]; ids={start:0}; queue=deque([start]); trans=[]; final=[]
    while queue:
        ss=queue.popleft()
        row=[]
        for symbol in ALPH:
            if isinstance(symbol,int):
                nxt=frozenset(y for st in ss for y in update_outer(st,symbol,prior))
            else:
                accept_any=any(terminal_accept(st,symbol,prior) for st in ss)
                nxt=frozenset({('ACCEPT',)}) if accept_any else frozenset()
            if nxt not in ids:
                if len(sets)>=limit: return {'status':'CAPPED','states':len(sets)}
                ids[nxt]=len(sets);sets.append(nxt);queue.append(nxt)
            row.append(ids[nxt])
        trans.append(row)
        final.append(ss==frozenset({('ACCEPT',)}))
    assert len(trans)==len(sets)
    return TableDFA(trans,final)


def seed_folds(seed,steps):
    digits=list(map(int,str(seed)[::-1]))
    words=[]
    for t in range(steps+1):
        words.append(fold(pairs(digits)))
        digits=step_digits(digits)
    return words


def minimize_moore(dfa,verbose=False):
    """Exact DFA right-language partition refinement, no heuristics."""
    n=len(dfa.trans)
    cls=[int(x) for x in dfa.accept]
    it=0; oldcount=len(set(cls))
    while True:
        lookup={};cnew=[0]*n
        for i,row in enumerate(dfa.trans):
            sig=(cls[i],tuple(cls[t] for t in row))
            k=lookup.get(sig)
            if k is None:
                k=len(lookup);lookup[sig]=k
            cnew[i]=k
        if verbose: print('MOORE_ITER',it,'classes',len(lookup))
        if len(lookup)==oldcount:
            cls=cnew;break
        cls=cnew;oldcount=len(lookup);it+=1
    reps={}
    for i,k in enumerate(cls):reps.setdefault(k,i)
    trans=[[cls[v] for v in dfa.trans[reps[i]]] for i in range(len(reps))]
    final=[dfa.accept[reps[i]] for i in range(len(reps))]
    # normalize start index to 0, because TableDFA expects 0 initial
    initial=cls[0]
    if initial !=0:
        order=[initial]+[i for i in range(len(reps)) if i!=initial]
        perm={v:i for i,v in enumerate(order)}
        trans=[[perm[v] for v in trans[q]] for q in order]
        final=[final[q] for q in order]
    return TableDFA(trans,final)


def test():
    bad=None
    words=seed_folds(196,100)
    for h in range(5):
        candidate=build_dfa(bad,limit=350000)
        assert not isinstance(candidate,dict), ('STATE_CAP',h,candidate)
        raw=len(candidate.trans)
        bad=minimize_moore(candidate)
        print('STAGE',h,'raw',raw,'minimal',len(bad.trans),'seed196_in_bad',bad.run(*words[0]))
        assert not any(bad.run(*w) for w in words)
        for n in range(1,1000):
            d=list(map(int,str(n)[::-1])); is_bad=False
            for _ in range(h+1):
                d=step_digits(d)
                is_bad |= (d == d[::-1])
            src=fold(pairs(list(map(int,str(n)[::-1]))))
            assert bad.run(*src)==is_bad,(h,n)
        print('INDEPENDENT_999_SEEDS_PASS',h)
        if h==0:
            good=DFA(bad.initial,bad.delta,lambda q:not bad.final(q))
            r=check_dfa(good,safety=False)
            assert r['status']=='COUNTEREXAMPLE'
            print('INITIAL_SAFE_NOT_CLOSED',r['source'])
    print('SYNTHESIS_HIERARCHY_CHECKS_PASSED')

if __name__=='__main__':test()
