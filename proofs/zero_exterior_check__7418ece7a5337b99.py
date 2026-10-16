"""Independent ordinary-integer controls for the triple-zero exterior theorem.

All 18*19^3 four-column prefixes, with both realized incoming carries, are
tested. The accompanying written column proof establishes arbitrary width.
"""
from itertools import product
from pathlib import Path
from collections import Counter
import gzip
import hashlib
import json

HERE=Path(__file__).resolve().parent


def realize(q):
    assert q==q[::-1] and q[0]>0
    digits=[0]*len(q)
    for i in range(len(q)//2):
        digits[i]=max(q[i]-9,0)
        digits[-i-1]=min(q[i],9)
    if len(q)%2:
        assert q[len(q)//2]%2==0
        digits[len(q)//2]=q[len(q)//2]//2
    return int(''.join(map(str,digits[::-1])))


def paired(n):
    s=str(n)
    return tuple(int(a)+int(b) for a,b in zip(s,s[::-1]))


def advance(n):
    return n+int(str(n)[::-1])


def main():
    counts=Counter()
    source_hash=hashlib.sha256()
    output_hash=hashlib.sha256()
    path=HERE/'zero_exterior_column_outcomes.bin.gz'
    with path.open('wb') as f:
        with gzip.GzipFile(fileobj=f,mode='wb',mtime=0) as g:
            for p in range(1,19):
                for rest in product(range(19),repeat=3):
                    prefix=(p,)+rest
                    for incoming in (0,1):
                        q=prefix+(18*incoming,)+prefix[::-1]
                        n=realize(q)
                        assert paired(n)==q
                        out=advance(n)
                        h=len(str(out))-len(str(n))
                        qnext=paired(out)
                        # Record 4 input coefficients, incoming, overflow,
                        # and 4 output coefficients, each as one byte.
                        record=bytes(prefix+(incoming,h)+qnext[:4])
                        assert len(record)==10
                        g.write(record)
                        output_hash.update(record)
                        source_hash.update(f'{n},{out}\n'.encode())
                        counts['controls']+=1
                        if qnext[1:4]==(0,0,0):
                            counts[f'triple_zero_overflow_{h}']+=1
                            assert h==0
                            assert prefix[1:]==(0,0,0)
                            assert qnext[0]==2*p
                        if h==0 and qnext[1:3]==(0,0):
                            counts['nonoverflow_double_zero']+=1
                            assert prefix[1:3]==(0,0)
                            assert qnext[0]==2*p
    assert counts['controls']==18*19**3*2
    assert counts['triple_zero_overflow_1']==0
    # Sharpness of the temporal bound; palindromes are intentionally
    # continued, since the theorem concerns all positive ordinary orbits.
    n=10**4
    sharp=[]
    for t in range(6):
        sharp.append({'time':t,'integer':str(n),'q':paired(n)})
        if t<=4:
            assert paired(n)[:4]==(2**t,0,0,0)
        n=advance(n)
    q=(9,10,9,0,9,10,9)
    n=realize(q)
    out=advance(n)
    assert len(str(out))==len(q)+1
    assert paired(out)[:3]==(10,0,0)
    assert paired(out)[3]!=0
    boundary_path=HERE/'zero_exterior_small_width_outcomes.bin.gz'
    boundary_hash=hashlib.sha256()
    boundary_counts=Counter()
    with boundary_path.open('wb') as f:
        with gzip.GzipFile(fileobj=f,mode='wb',mtime=0) as g:
            for width in range(1,9):
                half_width=width//2
                if not half_width:
                    words=((2*i,) for i in range(1,10))
                else:
                    halves=((p,)+rest for p in range(1,19)
                            for rest in product(range(19),repeat=half_width-1))
                    words=(half+center+half[::-1] for half in halves
                           for center in (tuple((2*j,)) for j in range(10))) if width%2 else (half+half[::-1] for half in halves)
                for qq in words:
                    nn=realize(qq)
                    actual=advance(nn)
                    qout=paired(actual)
                    h=len(qout)-width
                    record=bytes((width,)+qq+(len(qout),)+qout)
                    g.write(record)
                    boundary_hash.update(record)
                    boundary_counts[str(width)]+=1
                    if len(qout)>=4 and qout[1:4]==(0,0,0):
                        assert h==0 and len(qq)>=4
                        assert qq[1:4]==(0,0,0) and qout[0]==2*qq[0]
                    if h==0 and len(qout)>=3 and qout[1:3]==(0,0):
                        assert qq[1:3]==(0,0) and qout[0]==2*qq[0]
    result={
        'status':'all-length written carry theorem, with independent finite integer controls',
        'counts':dict(counts),
        'control_domain':'every positive four-column prefix; both interior carries realized by a center 0 or 18',
        'archive':path.name,
        'record_layout':'10 uint8 fields: input q0,q1,q2,q3; incoming; overflow; output q0,q1,q2,q3',
        'record_order':'q0=1..18, lexicographic q1,q2,q3=0..18, incoming=0,1',
        'uncompressed_sha256':output_hash.hexdigest(),
        'integer_transition_sha256':source_hash.hexdigest(),
        'compressed_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'small_width_counts':dict(boundary_counts),
        'small_width_archive':boundary_path.name,
        'small_width_record_layout':'uint8 input width, input coefficients, uint8 output width, output coefficients',
        'small_width_uncompressed_sha256':boundary_hash.hexdigest(),
        'small_width_compressed_sha256':hashlib.sha256(boundary_path.read_bytes()).hexdigest(),
        'sharp_time_four_example':sharp,
        'two_zeros_do_not_exclude_overflow':{'q':q,'seed':str(n),'output':str(out),'output_q':paired(out)},
        'decimal_lychrel_existence_proved':False}
    (HERE/'zero_exterior_check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('sharp_time_four_example',)},indent=2))


if __name__=='__main__':
    main()
