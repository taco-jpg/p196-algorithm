#!/usr/bin/env python3
"""Exact 2-sheet carry-fibre polarization using the actual W30 decimal overflow word."""
from collections import deque
from pathlib import Path
import json, hashlib, sys
from fibre_graph import f,reflect

def graph():
    start=((17,3,14,3,17),4)
    queue=deque([start]);seen={start};G={}
    while queue:
        u=queue.popleft();r,delta=u
        G[u]=((f(r,0),delta),(f(r,1),(delta+1)%5))
        for x in G[u]:
            if x not in seen:seen.add(x);queue.append(x)
    assert len(seen)==1800
    return G

def complement(x):
    return tuple(18-v for v in x[0]),x[1]

def test(bits):
    G=graph()
    for u,nxt in G.items():
        assert complement(u) in G
        for k in (0,1):
            assert G[complement(u)][k]==complement(nxt[k])
    states=set(x for x in G if x[1]==4)
    assert len(states)==360 and all(complement(x) in states for x in states)
    cur=states
    checkpoint={};first2=None;prebreak=None;lasso20=None;lasso30=None
    fixed_start=26710
    for t in range(len(bits)+1):
        if t==26710:prebreak=sorted(cur)
        if t==20:lasso20=cur.copy()
        if t==30:lasso30=cur.copy()
        if t in [0,8,40,200,20000,26710,26711,26720,26800,27000,27100,27200,27300,27350,27380,27390,27400,30000,50000]:
            checkpoint[t]={'rank':len(cur),'states':[{'row':list(z[0]),'axis':z[1]} for z in sorted(cur)[:2]]}
        assert len(cur)%2==0 and all(complement(x) in cur for x in cur)
        if len(cur)==2 and first2 is None:first2=t
        if t==len(bits):break
        g=int(bits[t]);cur={G[x][g] for x in cur}
    assert first2 is not None
    assert lasso20==lasso30 and lasso20==set(prebreak) and len(lasso20)==32
    assert all(cp['rank']>=2 for cp in checkpoint.values())
    print('FIRST_RANK_TWO',first2,'postbreak length',first2-fixed_start,'ranks',[(k,v['rank']) for k,v in checkpoint.items()]);print('TWO_SHEET',checkpoint[first2]);
    a,b=sorted(cur);assert complement(a)==b
    postbits=bits[fixed_start:first2]
    reset_first=[]
    # Find the rank-drop moments near the switch, independently recompute at each whole stream step.
    now=states;last=len(now)
    for t,bit in enumerate(bits):
        new={G[x][int(bit)] for x in now}
        if len(new)<last and t>=fixed_start-4:reset_first.append([t+1,last,len(new)])
        now=new;last=len(now)
        if t+1==first2:break
    result={
      'label':'COMPUTED','base':10,'carrier_spatial_period':5,'whole_reachable_states':1800,
      'compatible_start_axis':4,'all_compatible_start_rows':360,
      'complete_binary_graph_edges_checked_for_18_complement':3600,
      'rank_before_global_clock_break_t26710':checkpoint[26710]['rank'],
      'alternating_overflow_lasso_start':20,
      'alternating_overflow_lasso_word':'1010101010',
      'lasso_repeats_to_t26710':2669,
      'lasso_set_size':32,
      'first_rank2_state_time':first2,'postbreak_length':len(postbits),
      'postbreak_gamma_bits':postbits,
      'prebreak_rank32_rows':[{'row':list(u[0]),'axis':u[1]} for u in prebreak],
      'postbreak_gamma_sha256':hashlib.sha256(postbits.encode()).hexdigest(),
      'rank2_complement_pair':checkpoint[first2]['states'],
      'rank_decreases_after_break':reset_first,
      'rank2_at_steps_30000_and_50000':[checkpoint[30000],checkpoint[50000]],
      'scope':'actual W30 seed overflow through this finite prefix; conditional reset of an unrooted 360-row periodic centre language, not an all-time Lychrel proof'
    }
    p=Path(__file__).with_name('sync_physical.json');p.write_text(json.dumps(result,indent=2)+'\n');return result

if __name__=='__main__':
    p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('gamma60000.txt')
    if not p.is_file():raise SystemExit('generate gamma file using extract_gamma.cpp 60000 and pass its path')
    b=p.read_text().strip();assert len(b)>=50000
    test(b)
