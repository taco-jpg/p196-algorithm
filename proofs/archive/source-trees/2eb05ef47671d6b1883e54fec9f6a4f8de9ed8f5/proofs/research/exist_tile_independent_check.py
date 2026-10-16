"""Stdlib-only checker for time-dependent carry-tile exclusion certificates.

The tile labels are recomputed from ordinary decimal carries; no SAT solver,
transducer enumeration, discovery code, or previous output is imported.
"""
import json,sys

def freeze(x):return tuple(freeze(y) for y in x) if isinstance(x,list) else x

def canonical(w):
    p,c=w;p=tuple(p)
    assert all(isinstance(x,int) and 0<=x<=18 for x in p)
    assert (p and p[0]>0) or (not p and c is not None and c>0)
    assert c is None or isinstance(c,int) and 0<=c<=18 and c%2==0
    return p,c

def arithmetic(w):
    p,c=canonical(w);q=p+(() if c is None else (c,))+p[::-1];carry=[0];digits=[]
    for x in q:digits.append((x+carry[-1])%10);carry.append((x+carry[-1])//10)
    full=digits+([1] if carry[-1] else [])
    sums=tuple(x+y for x,y in zip(full,full[::-1]));out=(sums[:len(sums)//2],sums[len(sums)//2] if len(sums)%2 else None)
    h=carry[-1];state=(h,0,h,1 if h else -1,False);tiles=[];L=len(q)
    for i,x in enumerate(p):
        # State contains low incoming carry, high outgoing carry, and the
        # previous outer high output digit when length increases.
        assert state[1]==carry[i] and state[2]==carry[L-i]
        hi=digits[L-i-1];o=digits[i]+(state[3] if h else hi)
        nxt=(h,carry[i+1],carry[L-i-1],hi if h else -1,True)
        tiles.append(('edge',state,x,o,nxt));state=nxt
    if c is None:extra=None;oc=2*state[3] if h else None
    else:extra=digits[len(p)]+state[3] if h else None;oc=None if h else 2*digits[len(p)]
    tiles.append(('end',state,c,extra,oc))
    return out,tiles

def palindrome_predecessor(w):
    # Compute the next number directly from the redundant symmetric word.
    p,c=canonical(w);q=p+(() if c is None else (c,))+p[::-1]
    n=sum(v*10**i for i,v in enumerate(q));return str(n)==str(n)[::-1]

def verify(c):
    _,seedtiles=arithmetic(c['seed']);allowed=set(seedtiles)
    for stage,rows in enumerate(c['levels']):
        forced=set()
        for row in rows:
            image,inputtiles=arithmetic(row['input']);assert set(inputtiles)<=allowed,(stage,'input tiles')
            assert image==canonical(row['image']),(stage,'arithmetic')
            _,outputtiles=arithmetic(image);sig=freeze(row['signature']);assert sig in outputtiles,(stage,'output tile');forced.add(sig)
        allowed=forced
    img,lasttiles=arithmetic(c['unsafe']);assert set(lasttiles)<=allowed
    assert img==canonical(c['unsafe_image']);assert palindrome_predecessor(img)
    assert len(c['levels'])==c['unsafe_time'];return dict(seed=c['seed'],stages=len(c['levels']),word_rows=sum(map(len,c['levels'])),last_word=c['unsafe'],checked=True,decimal_existence_proved=False)

if __name__=='__main__':
    files=sys.argv[1:] or ['exist_tile_timevarying_196_certificate.json','exist_tile_timevarying_18887_certificate.json']
    for path in files:print(json.dumps(dict(file=path,**verify(json.load(open(path))))))
