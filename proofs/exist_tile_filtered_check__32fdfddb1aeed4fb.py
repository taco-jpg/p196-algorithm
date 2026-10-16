"""Stdlib-only arithmetic verifier for filtered carry-tile obstructions."""
from exist_tile_independent_check import arithmetic,canonical,freeze,palindrome_predecessor
import json,sys

def width(w):p,c=canonical(w);return 2*len(p)+int(c is not None)
def halfsum(w):p,c=canonical(w);return sum(p)+(0 if c is None else c//2)
def qvalue(w):
    p,c=canonical(w);q=p+(() if c is None else (c,))+p[::-1];return sum(v*10**i for i,v in enumerate(q))

def verify(c):
    modulus=c['length_modulus'];start11=c.get('mod11_start');seed=canonical(c['seed']);r0=halfsum(seed)%9
    allowed=[set() for _ in range(modulus)];_,tt=arithmetic(seed);allowed[width(seed)%modulus]=set(tt)
    def filters(w,t,cl):
        assert width(w)%modulus==cl
        assert halfsum(w)%9==r0*pow(2,t,9)%9
        if start11 is not None and t>=start11:assert qvalue(w)%11==0
    for t,level in enumerate(c['levels']):
        assert level['residue']==r0*pow(2,t,9)%9
        forced=[set() for _ in range(modulus)]
        for outputclass,rows in enumerate(level['rows']):
            for row in rows:
                inp,img=canonical(row['input']),canonical(row['image']);ic=row['input_parity'];oc=row['output_parity'];assert oc==outputclass
                filters(inp,t,ic);filters(img,t+1,oc)
                actual,inputtiles=arithmetic(inp);assert set(inputtiles)<=allowed[ic];assert actual==img
                _,outputtiles=arithmetic(img);sig=freeze(row['signature']);assert sig in outputtiles;forced[oc].add(sig)
        allowed=forced
    t=len(c['levels']);last=canonical(c['unsafe']);cl=c['unsafe_parity'];filters(last,t,cl)
    img,lasttiles=arithmetic(last);assert set(lasttiles)<=allowed[cl];assert img==canonical(c['unsafe_image']);assert palindrome_predecessor(img)
    assert c['unsafe_time']==t
    return dict(checked=True,seed=seed,length_modulus=modulus,mod11_start=start11,stages=t,word_rows=sum(len(rows) for level in c['levels'] for rows in level['rows']),last_word=last,decimal_existence_proved=False)

if __name__=='__main__':
    paths=sys.argv[1:]
    if not paths:
        from pathlib import Path
        paths=sorted(map(str,Path('.').glob('exist_tile_filtered_*_certificate.json')))
    for path in paths:print(json.dumps(dict(file=path,**verify(json.load(open(path))))))
