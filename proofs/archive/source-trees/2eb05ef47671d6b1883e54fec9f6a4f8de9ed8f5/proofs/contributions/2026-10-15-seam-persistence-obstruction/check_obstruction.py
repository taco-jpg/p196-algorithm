#!/usr/bin/env python3
"""Small exact controls for an all-parameter two-step obstruction."""

from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def digits(n, b):
    out = []
    while n:
        n, a = divmod(n, b)
        out.append(a)
    return out


def value(word, b):
    return sum(a*b**i for i,a in enumerate(word))


def ordinary_step(n, b):
    return n + value(digits(n,b)[::-1], b)


def normalize(word, b, incoming=0):
    carry, out, carries = incoming, [], []
    for a in word:
        carry, digit = divmod(a+carry,b)
        out.append(digit)
        carries.append(carry)
    return out, carry, carries


def realize(q, b):
    assert q == q[::-1] and q[0] > 0
    d = [0]*len(q)
    for i in range(len(q)//2):
        d[-1-i] = min(b-1,q[i])
        d[i] = q[i]-d[-1-i]
    if len(q)%2:
        assert q[len(q)//2]%2 == 0
        d[len(q)//2] = q[len(q)//2]//2
    n = value(d,b)
    assert [x+y for x,y in zip(d,d[::-1])] == q
    assert digits(n,b) == d
    return n


def seam(q, lengths, b):
    actual, e, carries = normalize(q,b)
    if e:
        actual.append(e)
    assert actual == digits(value(q,b),b)
    isolated = [0]*(len(q)+1)
    k = [0]*len(q)
    offset = 0
    for length in lengths:
        block = q[offset:offset+length]
        out, final, _ = normalize(block,b)
        for i,d in enumerate(out):
            isolated[offset+i] += d
        isolated[offset+length] += final
        incoming = carries[offset-1] if offset else 0
        for i,a in enumerate(block):
            if a != b-1:
                break
            k[offset+i] += incoming
        offset += length
    assert offset == len(q)
    pad = actual + [0]*(len(isolated)-len(actual))
    correction = [-b*x for x in k]+[0]
    for i,x in enumerate(k):
        correction[i+1] += x
    assert pad == [a+c for a,c in zip(isolated,correction)]
    assert sum(actual) == sum(isolated)-(b-1)*sum(k)
    return dict(isolated_raw=isolated, normalized=actual, active_polynomial=k,
                digit_mass_deficit=(b-1)*sum(k), pair_mass_deficit=2*(b-1)*sum(k))


def control(q,b,n=None):
    h=(b-1)//2
    assert q==q[::-1] and q[0]>=b and all(b-1<=a<=b+h-1 for a in q)
    if n is None:
        n=realize(q,b)
    d=digits(n,b)
    assert [a+c for a,c in zip(d,d[::-1])] == q
    n1=ordinary_step(n,b)
    n2=ordinary_step(n1,b)
    d1,d2=digits(n1,b),digits(n2,b)
    predicted=[q[0]-b]+[a+1-b for a in q[1:]]+[1]
    assert d1==predicted and max(d1)<=h
    assert d2==d2[::-1]
    first=1 if d1==d1[::-1] else 2
    assert first==(1 if all(a==b+1 for a in q) else 2)
    return dict(base=b,pair_word=q,seed=n,first_output=n1,second_output=n2,
                first_output_digits=d1,second_output_digits=d2,first_palindrome_time=first)


def adjacent_control(q,b):
    assert q==q[::-1] and q[0]>=b and all(b-1<=a<=2*b-2 for a in q)
    n=realize(q,b)
    n1=ordinary_step(n,b)
    n2=ordinary_step(n1,b)
    d1,d2=digits(n1,b),digits(n2,b)
    r=[a-b+1 for a in q]
    predicted=[r[0]]+[a+c for a,c in zip(r,r[1:])]+[r[0]]
    actual=[a+c for a,c in zip(d1,d1[::-1])]
    assert actual==predicted
    small=all(a+c<=3*b-3 for a,c in zip(q,q[1:]))
    pal=d2==d2[::-1]
    assert pal==small
    assert (d1==d1[::-1])==all(a==b+1 for a in q)
    if not small:
        assert 0<actual[0]<=b-1 and any(a>=b for a in actual)
    return dict(kind='exact_adjacent_criterion',base=b,pair_word=q,seed=n,
                first_output=n1,second_output=n2,next_pair_word=actual,
                all_adjacent_sums_bounded=small,second_output_palindromic=pal)


def main():
    rows=[]
    for b in range(3,13):
        h=(b-1)//2
        # Every allowed length-two symmetric word, including constant b+1
        # when that exception lies in the interval.
        for outside in range(b,b+h):
            rows.append(dict(kind='two_column_interval',**control([outside]*2,b)))
        # Nonconstant longer interval words; parity is automatic at even width.
        for interior in range(b-1,b+h):
            rows.append(dict(kind='four_column_interval',**control([b,interior,interior,b],b)))
        for m in (1,2,4):
            q=[b,b]+[b-1]*(2*m)+[b,b]
            n=b**(2*m+4)-b**(m+2)+b+1
            row=dict(kind='canonical_collision',m=m,**control(q,b,n))
            assert row['first_output']==b**(2*m+2)*(b*b+b+1)+b
            assert normalize([b,b],b)[1]==1
            assert normalize([b-1]*(2*m),b)[1]==0
            three=seam(q,[2,2*m,2],b)
            singleton=seam(q,[1]*len(q),b)
            expected=[0,0]+[1]*(2*m)+[0,0]
            assert three['active_polynomial']==singleton['active_polynomial']==expected
            assert three['digit_mass_deficit']==singleton['digit_mass_deficit']==2*m*(b-1)
            row.update(isolated_overflow_bits=[1,0],three_block=three,singleton=singleton)
            rows.append(row)
            short=[b]+[b-1]*(2*m)+[b]
            n_short=b**(2*m+2)-b**(m+1)+1
            shortrow=dict(kind='shorter_whole_word',m=m,**control(short,b,n_short))
            assert shortrow['first_output']==(b+1)*b**(2*m+1)
            assert shortrow['second_output']==(b+1)*(b**(2*m+1)+1)
            shortrow['singleton_exterior_canonical']=(b%2==0)
            rows.append(shortrow)
        for q in ([b,b], [b+1,b+1], [2*b-2]*4,
                  [2*b-2,b-1,b-1,2*b-2], [b,2*b-2,2*b-2,b]):
            rows.append(adjacent_control(q,b))
        # Width one is admissible only with an even coefficient.
        if b%2==0:
            rows.append(adjacent_control([b],b))
    controls=HERE/'controls.json'
    controls.write_text(json.dumps(rows,indent=2)+'\n')
    report=dict(status='PASS_EXACT_TWO_STEP_CONTROLS',cases=len(rows),
        controls_sha256=sha256(controls.read_bytes()).hexdigest(),
        source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        kinds={kind:sum(row['kind']==kind for row in rows) for kind in sorted({row['kind'] for row in rows})},
        scope='Small deterministic controls. All-base/all-width proof is in SEAM_PERSISTENCE_OBSTRUCTION.md; no claim of a general orbit invariant.')
    (HERE/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':
    main()
