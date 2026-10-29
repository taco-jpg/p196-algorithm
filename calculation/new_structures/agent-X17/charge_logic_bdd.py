#!/usr/bin/env python3
"""An exact reduced 12-node binary decision diagram for a FINITE t=107 charge gate."""
import csv
import json
import sys
from pathlib import Path

ORDER=(5,3,4,0,1,2,6,7)  # 0-indexed perturbation bits: offsets 6,4,5,1,2,3,7,8.
NS=(2001,6001,10001,20001)

def read(src):
    with open(src,newline='') as f: rows=list(csv.DictReader(f))
    assert len(rows)==256
    assert [int(r['mask']) for r in rows]==list(range(256))
    return rows

def get_bdd(truth):
    uniq={}
    nodes={}
    def make(idx,ids):
        v=[truth[i] for i in ids]
        if all(x==v[0] for x in v):return v[0]
        bit=ORDER[idx]
        low=make(idx+1,[m for m in ids if not(m>>bit&1)])
        high=make(idx+1,[m for m in ids if m>>bit&1])
        if low==high:return low
        key=(bit,low,high)
        if key not in uniq:
            nid=len(uniq)+2
            uniq[key]=nid
            nodes[nid]={'bit':bit,'low':low,'high':high}
        return uniq[key]
    root=make(0,list(range(256)))
    assert len(nodes)==12
    for m in range(256):
        v=root
        while v>1:
            node=nodes[v]
            v=node['high' if m>>node['bit']&1 else 'low']
        assert v==truth[m]
    return root,nodes

def main(folder,dst):
    rs={n:read(folder/f'charge_logic_{n}.csv') for n in NS}
    truth=[int(r['differential_carry']) for r in rs[2001]]
    assert sum(truth)==170
    for n in NS[1:]:
        assert [int(r['differential_carry']) for r in rs[n]]==truth
        for a,b in zip(rs[2001],rs[n]):
            mask=int(a['mask']);original=int(a['matched_high_t108']);actual=int(b['matched_high_t108']);delta=n-2001
            expectation = original + (delta if mask==0 else delta//2 if int(a['differential_carry'])==0 else 0)
            assert actual==expectation, (n,mask,actual,expectation)
    anf=truth[:]
    for k in range(8):
        for mask in range(256):
            if mask>>k&1: anf[mask]^=anf[mask^(1<<k)]
    monomials=[mask for mask,val in enumerate(anf) if val]
    assert len(monomials)==135 and max(m.bit_count() for m in monomials)==7
    root,nodes=get_bdd(truth)
    assert len(nodes)==12
    data={'status':'COMPUTED, finite lengths n=2001,6001,10001,20001 at exact t=107 only',
          'motif':'88283583','time':107,'bits':'k=1..8 single +1 off-centre digits',
          'lengths':list(NS),'neutral_gate_column':'n-14 at time 107 (after 47 length overflows)',
          'safe_masks':86,'charged_masks':170,'anf_nonzero_monomials':135,'anf_degree':7,
          'variable_order_0_based':list(ORDER),'root':root,
          'nodes':{str(k):nodes[k] for k in sorted(nodes)}}
    Path(dst).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print('PASS: 1024 rows, four exact lengths, identical 8-input gate; affine high-width scaling')
    print('PASS: reduced 12-node BDD reproduces all 256 outcomes; 135-term degree-7 ANF')

if __name__=='__main__': main(Path(sys.argv[1] if len(sys.argv)>1 else '.'),sys.argv[2] if len(sys.argv)>2 else 'charge_logic_bdd.json')
