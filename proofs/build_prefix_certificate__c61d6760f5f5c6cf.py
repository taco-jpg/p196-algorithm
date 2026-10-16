#!/usr/bin/env python3
"""Complete necessary three-column relation for high-region two-step returns."""
import gzip
import hashlib
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent


def node_id(word):
    a,b,c = word
    return 100*(a-10)+10*(b-9)+(c-9)


def transition(word, incoming):
    A,B,C = word
    a,x,y = A-9,A+B-18,B+C-18
    low = x//10
    high2 = (y+incoming)//10
    high1 = (x+high2)//10
    overflow = (a+high1)//10
    # These are no-overflow reflection formulas. Overflow controls are retained
    # but their would-be result is not asserted to be the actual next prefix.
    candidate = [2*a+high1,
                 x%10+(x+high2)%10,
                 (y+low)%10+(y+incoming)%10]
    reasons = []
    if overflow:
        reasons.append('second_overflow_excluded_by_neutral_exterior_theorem')
    if not 10 <= candidate[0] <= 18:
        reasons.append('exterior_outside_high_region')
    if not all(9 <= c <= 18 for c in candidate[1:]):
        reasons.append('next_two_coefficients_outside_high_region')
    accepted = not reasons
    return {'incoming':incoming,'p_prefix':[a,x,y],
            'low_carry_into_p2':low,'high_carry_into_p1':high2,
            'high_carry_into_p0':high1,'second_overflow':overflow,
            'no_overflow_candidate':candidate,
            'accepted':accepted,'rejection_reasons':reasons,
            'target':node_id(candidate) if accepted else None}


def main():
    words = [[a,b,c] for a in range(10,19) for b in range(9,19) for c in range(9,19)]
    rows = [{'id':i,'word':word,'controls':[transition(word,w) for w in (0,1)]}
            for i,word in enumerate(words)]
    assert all(node_id(r['word'])==r['id'] for r in rows)
    visiting = set()

    @lru_cache(None)
    def rank(i):
        assert i not in visiting, ('cycle',i)
        visiting.add(i)
        value = max((1+rank(c['target']) for c in rows[i]['controls'] if c['accepted']), default=0)
        visiting.remove(i)
        return value

    for r in rows:
        r['rank'] = rank(r['id'])
    accepted = 0
    for r in rows:
        for c in r['controls']:
            if c['accepted']:
                accepted += 1
                assert rows[c['target']]['rank'] < r['rank']
    counts = dict(sorted(Counter(r['rank'] for r in rows).items()))
    assert accepted == 258 and counts == {0:760,1:123,2:14,3:3}
    certificate = {'schema':1,
        'index':'100*(A-10)+10*(B-9)+(C-9)',
        'domain':{'A':[10,18],'B':[9,18],'C':[9,18]},
        'incoming_domain':[0,1],
        'scope':'Necessary no-overflow boundary relation only. Actual interior carry supplies incoming; arbitrary accepted edges need not be realizable.',
        'vertices':rows}
    raw = (json.dumps(certificate,indent=2,sort_keys=True)+'\n').encode()
    compressed = gzip.compress(raw,mtime=0)
    (HERE/'prefix_certificate.json.gz').write_bytes(compressed)
    report = {'result':'PASS','vertices':len(rows),'control_cases':2*len(rows),
              'accepted_edges':accepted,'rejected_controls':2*len(rows)-accepted,
              'rank_counts':counts,'max_rank':max(counts),
              'rank_three_words':[r['word'] for r in rows if r['rank']==3],
              'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'certificate':{'path':'prefix_certificate.json.gz',
                  'compressed_bytes':len(compressed),'compressed_sha256':hashlib.sha256(compressed).hexdigest(),
                  'recovered_bytes':len(raw),'recovered_sha256':hashlib.sha256(raw).hexdigest()},
              'scope':'Finite rank certificate. The actual-orbit bridge and width-one/two cases are written proofs; see FULL_HIGH_RETURN.md.'}
    (HERE/'prefix_verification.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
