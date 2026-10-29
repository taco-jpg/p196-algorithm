#!/usr/bin/env python3
"""All 12800**Q distinct decimal SFT mosaics have one common second iterate."""
import sys,json,math,random
from collections import defaultdict
from sft import B0,W,cycles,edges
from validate import numeral_from_folded,integer_pairs
if hasattr(sys,"set_int_max_str_digits"):sys.set_int_max_str_digits(0)
S=(1,1,4);START=(0,1,1)
def prefix_paths():
    paths={START:[()]}
    for p in B0:
        nxt=defaultdict(list)
        for (a,rprev,uprev),words in paths.items():
            for r in range(2):
                if (p+r)//10!=rprev:continue
                lo=(p+a)%10
                to=((p+a)//10,r,(p+r)%10)
                for word in words:nxt[to].append(word+(lo+uprev,))
        paths=nxt
    return paths
def iterate(n):
    return n+int(str(n)[::-1])
def n0(tiles):
    return numeral_from_folded(B0+[x for tile in tiles for x in tile])
def run():
    pp=prefix_paths()
    assert len(pp[S])==1
    prefix=pp[S][0]
    assert len(prefix)==39 and prefix[0]==8 and sum(x%2 for x in prefix)==19
    opts=[ps for ps,path in cycles(W[1],1) if path[0]==S]
    assert len(opts)==12800==len(set(opts))
    assert all(any(x%2 for x in ps) for ps in opts)
    assert tuple(W[0]) in opts
    assert S[0]==S[1] and S[2]*2==8
    for ps in opts:
        states={(S,())}
        for i,p in enumerate(ps):
            nxt=set()
            for state,output in states:
                for to,_ in edges(W[1][i],1,p).get(state,[]):
                    nxt.add((to,output+(W[1][i],)))
            states=nxt
        assert (S,tuple(W[1])) in states
    rng=random.Random(20261029)
    tested=0
    for Q,sample in [(1,opts),(2,[rng.choice(opts) for _ in range(100)]),
                     (3,[rng.choice(opts) for _ in range(100)]),
                     (10,[None]*40),(50,[None]*20),(600,[None]*6)]:
        baseline=n0([tuple(W[0])]*Q)
        target=iterate(iterate(baseline))
        half=list(prefix)+W[1]*Q
        expected=half+[8]+half[::-1]
        for selected in sample:
            tiles=[selected] if Q==1 else (
                [selected]*Q if selected else [rng.choice(opts) for _ in range(Q)])
            N=n0(tiles);N1=iterate(N)
            assert integer_pairs(N1)==expected,(Q,"P1")
            assert iterate(N1)==target,(Q,"N2")
            assert str(N)!=str(N)[::-1]
            assert str(N1)!=str(N1)[::-1]
            tested+=1
    print(json.dumps({
      "label":"PAPER PROOF (finite carry-port induction; finite premises exhaustively checked)",
      "port":S,"root_prefix_output":list(prefix),"root_paths_to_port":len(pp[S]),
      "admissible_distinct_tiles":len(opts),"common_second_iterate_for_all_Q":True,
      "formula":"12800**Q seeds of length 78+40*Q, for every Q>=1",
      "Q600_initial_digits":24078,"Q600_log10_number_of_seeds":600*math.log10(12800),
      "exhaustive_Q1_bigint_trials":12800,"additional_bigint_trials":tested-12800},indent=2))
if __name__=="__main__":run()
