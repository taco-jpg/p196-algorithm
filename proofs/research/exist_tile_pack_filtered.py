from exist_tile_timevarying import *
from exist_tile_filtered_check import verify

def signature(k):
    if k<len(FE):u,q,o,v=FE[k];return ('edge',FS[u],q,o,FS[v])
    x,c,extra,oc=TS[k-len(FE)];return ('end',FS[x],c,extra,oc)

def pack(path,out):
    cc=json.load(open(path));m=cc.get('length_modulus',2);cc['length_modulus']=m;needed=[set() for _ in range(m)];needed[cc['unsafe_parity']]=set(history_path((tuple(cc['unsafe'][0]),cc['unsafe'][1])));trimmed=[]
    for level in cc['levels'][::-1]:
        rows=level['rows'];keep=[[dict(row,signature=signature(row['tile'])) for row in rows[k] if row['tile'] in needed[k]] for k in range(m)]
        for k in range(m):assert {r['tile'] for r in keep[k]}==needed[k]
        needed=[set() for _ in range(m)]
        for rr in keep:
            for row in rr:needed[row['input_parity']].update(history_path((tuple(row['input'][0]),row['input'][1])))
        trimmed.append(dict(residue=level['residue'],rows=keep))
    seed=(tuple(cc['seed'][0]),cc['seed'][1]);cl=(2*len(seed[0])+int(seed[1] is not None))%m
    for k in range(m):assert needed[k]<=(set(history_path(seed)) if k==cl else set())
    cc['levels']=trimmed[::-1];cc['scope']='Excludes time-dependent full-carry-tile languages with the stated residue and length filters; does not establish or disprove decimal Lychrel existence.'
    result=verify(cc);json.dump(cc,open(out,'w'),indent=2);return result

results=[]
for name in ('196','18887'):
    for suffix in ('residue','residue11'):
        src=f'exist_tile_{suffix}_{name}.json';out=f'exist_tile_filtered_{suffix}_{name}_certificate.json';results.append(dict(file=out,**pack(src,out)))
for m in (4,8,16,32):
    src=f'exist_tile_length_residue11_196_{m}.json';out=f'exist_tile_filtered_residue11_196_mod{m}_certificate.json';results.append(dict(file=out,**pack(src,out)))
json.dump(results,open('exist_tile_filtered_check_results.json','w'),indent=2)
for r in results:print(json.dumps(r))
