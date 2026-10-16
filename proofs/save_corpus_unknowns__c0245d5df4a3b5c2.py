"""Preserve and replay every UNKNOWN in the redundant short-word corpus.

This is archival bookkeeping, not an additional search or a safety claim.
These words are intentionally not used as negative SAT labels.
"""
from pathlib import Path
import gzip, hashlib, itertools, json


def main():
    root=Path(__file__).parent
    with gzip.open(root/'dfa4_neg2.terminating.json.gz','rt') as f:
        labelled={(tuple(x['pairs']),x['center']) for x in json.load(f)}
    records=[]
    for k in range(3):
        prefixes=[()] if not k else ((q,)+rest for q in range(1,19) for rest in itertools.product(range(19),repeat=k-1))
        for p in prefixes:
            for c in [None]+list(range(0,19,2)):
                if not p and c in (None,0):continue
                if (p,c) in labelled:continue
                s=''.join(str(min(q,9)) for q in p)
                if c is not None:s+=str(c//2)
                s+=''.join(str(max(q-9,0)) for q in p[::-1])
                n=int(s);orbit=[n]
                for t in range(60):
                    n+=int(str(n)[::-1]);orbit.append(n)
                    assert str(n)!=str(n)[::-1]
                records.append(dict(pairs=p,center=c,orbit=orbit,status='UNKNOWN',positive_addition_cap=60))
    assert len(records)==263
    target=root/'short_corpus_unknowns.json.gz'
    with target.open('wb') as f:
        with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:
            z.write(json.dumps(records,separators=(',',':')).encode())
    with gzip.open(target,'rt') as f:restored=json.load(f)
    assert len(restored)==263
    for record in restored:
        chain=record['orbit'];assert len(chain)==61
        for a,b in zip(chain,chain[1:]):
            assert b==a+int(str(a)[::-1])
            assert str(b)!=str(b)[::-1]
    out=dict(verified=True,unknown_words=263,additions_per_word=60,checked_additions=263*60,
             horizon_status='UNKNOWN only; no infinite safety inference',
             artifact=target.name,sha256=hashlib.sha256(target.read_bytes()).hexdigest())
    (root/'short_corpus_unknowns_check.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
