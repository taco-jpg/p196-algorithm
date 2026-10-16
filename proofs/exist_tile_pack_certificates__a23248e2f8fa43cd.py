from exist_tile_timevarying import *
from exist_tile_independent_check import arithmetic,verify as independent_verify

def signature(k):
    if k<len(FE):
        u,q,o,v=FE[k];return ('edge',FS[u],q,o,FS[v])
    x,c,extra,oc=TS[k-len(FE)];return ('end',FS[x],c,extra,oc)

for name in ('196','18887'):
    cc=json.load(open(f'exist_tile_timevarying_{name}.json'));needed=set(history_path((tuple(cc['unsafe'][0]),cc['unsafe'][1])));trimmed=[]
    for rows in cc['levels'][::-1]:
        keep=[dict(row,signature=signature(row['tile'])) for row in rows if row['tile'] in needed]
        assert {row['tile'] for row in keep}==needed
        needed=set()
        for row in keep:needed.update(history_path((tuple(row['input'][0]),row['input'][1])))
        trimmed.append(keep)
    assert needed<=set(history_path((tuple(cc['seed'][0]),cc['seed'][1])))
    cc['levels']=trimmed[::-1];cc['certificate_scope']='No arbitrary time-dependent safe closed language defined only by allowed full carry tiles can contain this seed.'
    assert independent_verify(cc)['checked'];json.dump(cc,open(f'exist_tile_timevarying_{name}_certificate.json','w'),indent=2);print(name,[len(r) for r in cc['levels']],sum(map(len,cc['levels'])),flush=True)
