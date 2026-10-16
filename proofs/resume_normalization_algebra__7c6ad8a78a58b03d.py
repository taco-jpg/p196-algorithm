"""Validate the direct protected-run identities independently of the DFA."""
from itertools import product
import random,json


def pair_map(word,h):
    q=(0,0)+tuple(word)+(0,0)
    c=0;right=[]
    for x in q:
        s=x+c;right.append(s%10);c=s//10
    c=0;left=[]
    for x in reversed(q):
        s=x+c;left.append(s%10);c=s//10
    left.reverse()
    out=tuple(right[i]+left[i-h] for i in range(1,len(q)-1))
    while out and out[0]==0:out=out[1:]
    while out and out[-1]==0:out=out[:-1]
    return out


def protected(word,d):
    if any(x not in tuple(range(d+1))+(9,10) for x in word):return False
    q=(0,)+tuple(word)+(0,);i=1
    while i<len(q)-1:
        if q[i]!=9:i+=1;continue
        j=i
        while q[j]==9:j+=1
        if {q[i-1],q[j]}!={0,10}:return False
        i=j
    return True


def check(word,d):
    assert protected(word,d)
    image=pair_map(word,1)
    bound=2 if d==0 else 4
    assert protected(image,bound),(word,image)
    if d==2:
        p=(0,)+image+(0,)
        assert all(p[i-1]<9 and p[i+1]<9 for i,x in enumerate(p[1:-1],1) if x==4)
        assert all(x<=9 for x in pair_map(word,0))
        assert all(x<=9 for x in pair_map(image,0))


def validate():
    counts={0:0,2:0}
    for d in (0,2):
        alphabet=tuple(range(d+1))+(9,10)
        for n in range(7):
            for q in product(alphabet,repeat=n):
                if protected(q,d):check(q,d);counts[d]+=1
    rng=random.Random(940)
    for _ in range(10000):
        d=rng.choice((0,2))
        plain=(0,)+tuple(rng.choice(tuple(range(d+1))+(10,)) for _ in range(rng.randrange(1,80)))+(0,)
        word=[]
        for a,b in zip(plain,plain[1:]):
            word.append(a)
            if {a,b}=={0,10}:word.extend([9]*rng.randrange(15))
        word.append(plain[-1])
        check(word,d);counts[d]+=1
    return dict(protected_word_checks=counts,finite_state_certificate_used=False)


if __name__=='__main__':print(json.dumps(validate(),indent=2))
