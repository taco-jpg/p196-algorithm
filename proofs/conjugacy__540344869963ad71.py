"""Explore globally conjugated group scores; exact elimination only."""
import presentation as p
import json,time,sys
from collections import Counter
from pathlib import Path

def build():
    rels,nv,meta=p.build();h=nv+1
    offset=2+meta['safety'][1]+meta['safety'][2]+4
    end=offset+meta['closure'][1]+meta['closure'][2]
    for i in range(offset,end):
        r=rels[i];assert -p.w.NW<=r[0]<=-1
        rels[i]=(-h,r[0],h)+r[1:]
    meta=dict(meta,variables=h,inner_update_generator=h)
    return rels,h,meta

if __name__=='__main__':
    rels,nv,meta=build();pr=p.Presentation(rels,nv)
    elapsed=pr.eliminate(45,12)
    tiles=[pr.expand((i+1,)) for i in range(p.w.NW)]
    remaining=sorted(set(abs(x) for r in pr.rels.values() for x in r))
    remaining_tiles=sorted(set(abs(x) for r in tiles for x in r))
    out=dict(meta=meta,elapsed=elapsed,remaining_relation_generators=remaining,remaining_tile_generators=remaining_tiles,remaining_relations=len(pr.rels),lengths=dict(Counter(map(len,pr.rels.values()))),eliminations=len(pr.steps),nonidentity_tile_words=sum(bool(a) for a in tiles),relations=list(pr.rels.values()),tile_words=tiles,substitutions=pr.subs,steps=pr.steps,infinite_existence_proved=False)
    out['seed18887']=pr.expand(tuple(k+1 for k in p.w.history_path(((8,16),16))))
    out['seed196']=pr.expand(tuple(k+1 for k in p.w.history_path(((7,),18))))
    (Path(__file__).parent/'conjugacy.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({k:v for k,v in out.items() if k not in ('relations','tile_words','substitutions','steps')}),flush=True)
