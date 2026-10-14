"""Exact correlated-language identities; no Lychrel existence claim.

The main checker uses literal positive decimal integers.  The independent
small-column implementation is used only for a cross-check and proof traces.
All-length conclusions in the accompanying notes are algebraic lemmas, not
extrapolations from these finite tests.
"""
from itertools import product
import json
from pathlib import Path


def complement_reverse(xs):
    return tuple(18 - x for x in reversed(xs))


def family_a(u):
    return (tuple(u) + complement_reverse(u), None)


def family_b(x, v):
    return ((x,) + tuple(v) + (9,) + complement_reverse(v), 18 - 2 * x)


def unfold(w):
    p, c = w
    return p + (() if c is None else (c,)) + p[::-1]


def fold(q):
    return (tuple(q[:len(q)//2]), q[len(q)//2] if len(q) % 2 else None)


def representative(w):
    q = unfold(w)
    d = []
    for i, x in enumerate(q):
        j = len(q) - 1 - i
        d.append(max(x-9, 0) if i < j else min(x, 9) if i > j else x//2)
    assert 1 <= d[-1] <= 9
    assert all(0 <= x <= 9 for x in d)
    assert tuple(a+b for a, b in zip(d, d[::-1])) == q
    return sum(x*10**i for i, x in enumerate(d))


def numeric_step(w):
    n = representative(w)
    out = n + int(str(n)[::-1])
    ds = tuple(map(int, str(out)[::-1]))
    q = tuple(a+b for a, b in zip(ds, ds[::-1]))
    return fold(q), len(ds) - len(str(n))


def column_step(w):
    carry = 0
    d = []
    for q in unfold(w):
        d.append((q+carry) % 10)
        carry = (q+carry)//10
    if carry:
        d.append(carry)
    return fold(tuple(a+b for a, b in zip(d, d[::-1])))


def bad(w):
    q = unfold(w)
    return all(x <= 9 for x in q) or q[0] == 11 and all(x in (0,11) for x in q)


def is_a(w):
    p, c = w
    return c is None and len(p) % 2 == 0 and p == family_a(p[:len(p)//2])[0]


def r(q):
    return q - 9 * (q >= 10)


def trace(w, limit=20):
    rows=[]
    actual=representative(w)
    for t in range(limit):
        n=representative(w)
        ds=tuple(map(int,str(actual)[::-1]))
        assert fold(tuple(a+b for a,b in zip(ds,ds[::-1])))==w
        rows.append(dict(t=t, folded=w, representative=n,
                         actual_numeric_iterate=actual,bad=bad(w)))
        if bad(w):
            out=actual+int(str(actual)[::-1])
            assert out==n+int(str(n)[::-1])
            assert str(out)==str(out)[::-1]
            rows[-1]['next_palindrome']=out
            return rows
        w=column_step(w)
        actual+=int(str(actual)[::-1])
    return rows


def check():
    counts={'a_words':0,'a_no_overflow':0,'a_overflow_non_neutral_outer':0,
            'a_overflow_neutral_outer':0,'a_reduced_adjacency':0,'b_small_outer':0}
    for m in range(1,4):
        for u in product(range(19),repeat=m):
            if u[0]==0:
                continue
            w=family_a(u)
            y,h=numeric_step(w)
            assert y==column_step(w)
            assert bad(w)==all(x==9 for x in u)
            counts['a_words']+=1
            nonneutral=[i for i,x in enumerate(u) if x!=9]
            if not nonneutral:
                continue
            k=nonneutral[0]
            assert h==(u[k]>9)
            if not h:
                assert is_a(y)
                counts['a_no_overflow']+=1
            elif k==0:
                x=u[0]-9
                v=y[0][1:m]
                assert y==family_b(x,v)
                assert bad(y)==(x>=5 and all(z==9 for z in v))
                counts['a_overflow_non_neutral_outer']+=1
                if 9 not in u:
                    expected=tuple(r(u[i])+r(u[i-1]) for i in range(1,m))
                    assert v==expected
                    counts['a_reduced_adjacency']+=1
            else:
                # All-length mismatch strip: epsilon is indexed on the
                # first half of the unfolded input, of length s=2*m.
                s=2*m
                eps=lambda i: 9 if i<k else -1 if i==k else 0
                assert y[0][0]==10 and y[1]==18
                for i in range(1,s):
                    assert y[0][i]+y[0][s-i]==18+eps(i)+eps(s-i)
                assert not bad(y)
                counts['a_overflow_neutral_outer']+=1
    for m in range(1,5):
        for v in product(range(19),repeat=m-1):
            for x in range(1,5):
                w=family_b(x,v)
                y,h=numeric_step(w)
                assert y==column_step(w)
                assert not h
                xp=y[0][0]
                assert 2*x<=xp<=2*x+1
                assert y==family_b(xp,y[0][1:m])
                counts['b_small_outer']+=1
    counterexamples={
        'marked_a_defect':trace(family_a((2,3))),
        'marked_b_defect':trace(family_b(3,(4,))),
    }
    # Check every member through k=12 of an explicitly arbitrary-length
    # family whose first update is bad. The proof is the adjacency formula.
    annihilating=[]
    for m in range(1,13):
        u=tuple(17 if i%2==0 else 10 for i in range(m))
        w=family_a(u)
        y,h=numeric_step(w)
        assert h==1 and y==family_b(8,(9,)*(m-1)) and bad(y)
        annihilating.append(dict(m=m, input_folded=w, output_folded=y))
    return {'status':'NO_SAFE_CLOSED_LANGUAGE_OR_LYCHREL_WITNESS',
            'counts':counts,'counterexamples':counterexamples,
            'arbitrary_length_annihilation_controls':annihilating,
            'next_obligation':'Find a correlated language with a seed and a defect condition closed under all exact updates, including neutral-prefix mismatch repair and odd-width high-root branches.'}


if __name__=='__main__':
    out=check()
    target=Path(__file__).with_name('astra_languages_complement_results.json')
    target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'counts':out['counts'],
                      'counterexample_first_bad_times':{k:v[-1]['t'] for k,v in out['counterexamples'].items()}},indent=2))
