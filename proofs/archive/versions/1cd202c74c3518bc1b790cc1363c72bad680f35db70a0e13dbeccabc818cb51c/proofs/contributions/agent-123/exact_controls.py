#!/usr/bin/env python3
"""Same-author, independently structured finite controls; not Lean evidence."""
import hashlib,itertools,json
from pathlib import Path

def actual(q,cut):
    whole=isolated=0
    mask=[]
    for x,b in zip(q,cut):
        whole=(x+whole)//10
        isolated=(x+(0 if b else isolated))//10
        mask.append(whole-isolated)
    return tuple(mask)

def activity(q):
    carry=0
    result=[]
    for x in q:
        result.append(int(x==9 and carry==1))
        carry=(x+carry)//10
    return tuple(result)

def constraints(q,a,k):
    return (all(not b or x for b,x in zip(k,a)) and
            all(q[i+1]!=9 or k[i]<=k[i+1] for i in range(len(q)-1)))

def check_word(q):
    bits=list(itertools.product((0,1),repeat=len(q)))
    a=activity(q)
    observed={actual(q,c) for c in bits}
    predicted={k for k in bits if constraints(q,a,k)}
    assert observed==predicted,(q,observed,predicted)
    assert {sum(k) for k in observed}==set(range(sum(a)+1)),q
    for k in predicted:
        frontier=tuple(int(k[i]==1 and (i==0 or k[i-1]==0)) for i in range(len(k)))
        assert actual(q,frontier)==k,(q,k,frontier)
        for c in bits:
            if actual(q,c)==k:
                assert all(not f or b for f,b in zip(frontier,c)),(q,k,c)
    return len(bits),len(observed)

def main():
    digest=hashlib.sha256()
    words=partitions=0
    # Every coefficient 0..18 through width three, then threshold representatives.
    domains=[(range(19),n) for n in range(4)]+[((0,8,9,10,18),n) for n in range(4,7)]
    for alphabet,n in domains:
        for q in itertools.product(alphabet,repeat=n):
            p,m=check_word(q)
            words+=1;partitions+=p
            digest.update(repr((q,p,m)).encode())
    result={'status':'EXACT-CONTROLS-PASS','evidence_level':'same-author computational diagnostic, not a formal theorem or independent reviewer',
            'word_count':words,'partition_count':partitions,'transcript_sha256':digest.hexdigest(),
            'domains':'all 0..18 words of widths 0..3; all {0,8,9,10,18} words of widths 4..6',
            'checks':['exact mask-set equality','complete mass interval','frontier realizes each mask','every realization includes frontier']}
    dest=Path(__file__).parent/'evidence'/'exact-controls.json'
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True),flush=True)
if __name__=='__main__':main()
