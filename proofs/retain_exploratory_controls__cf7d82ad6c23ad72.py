#!/usr/bin/env python3
"""Retain the small hand-constructed examples considered during derivation."""
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def pairs(n):
    d=list(map(int,str(n)))[::-1]
    return [a+b for a,b in zip(d,d[::-1])]


def realize(q):
    d=[0]*len(q)
    for i in range(len(q)//2):
        d[i]=min(q[i],9)
        d[-1-i]=q[i]-d[i]
    if len(q)%2:
        assert q[len(q)//2]%2==0
        d[len(q)//2]=q[len(q)//2]//2
    n=sum(x*10**i for i,x in enumerate(d))
    assert pairs(n)==q
    return n


def high(q):
    return q[0]>=10 and all(9<=x<=18 for x in q)


def main():
    examples=[
      ([14,9,18,18,9,14], 'A return with low intermediate coefficients, outside the restricted all-high-interior condition.'),
      ([17,9,18,18,9,17], 'Another low-interior return construction; no infinite closure claim.'),
      ([18,9,17,17,9,18], 'Exterior eighteen can return without second overflow; the next return is blocked.'),
      ([17,9,18,9,17,17,9,18,9,17], 'Attempt to realize three safe returns by inserting a low boundary block and high center; the proposed continuation fails.'),
      ([17,9,18,9,17,18,18,17,9,18,9,17], 'Longer hand-constructed high-center attempt; it also fails to realize three safe returns.'),
      ([17,9,18,9,17], 'Independent-review stream sharp witness for three unrestricted returns; time two is a palindrome.')]
    records=[]
    for q,note in examples:
        n=realize(q); values=[n]
        for _ in range(8):
            values.append(values[-1]+int(str(values[-1])[::-1]))
        words=[pairs(x) for x in values]
        records.append({'initial_word':q,'purpose':note,'seed':n,'integers':values,
            'pair_words':words,'high_at_even_times':[high(words[t]) for t in range(0,9,2)],
            'palindromic_at_times':[str(x)==str(x)[::-1] for x in values]})
    assert records[-1]['high_at_even_times']==[True,True,True,True,False]
    assert records[-1]['palindromic_at_times'][2]
    for r in records[3:5]:
        assert not all(r['high_at_even_times'][:4])
    (HERE/'exploratory_controls.json').write_text(json.dumps({
        'scope':'Six bounded hand-constructed controls retained from the derivation. This is not an exhaustive seed search or a proof of any unbounded quantifier.',
        'records':records},indent=2)+'\n')
    print('PASS: six exact hand-constructed controls retained')


if __name__=='__main__':
    main()
