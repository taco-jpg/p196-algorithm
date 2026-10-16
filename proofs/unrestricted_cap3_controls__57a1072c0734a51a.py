#!/usr/bin/env python3
"""Complete finite cap-three experiment using independent whole-word arithmetic."""
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib
import json
from independent_controls import exterior

HERE = Path(__file__).resolve().parent
hist = Counter()
byphase = {}
cycles = []
longest = []
maximum = 0
for c in range(2,17,2):
    counts = Counter()
    for width in range(4):
        for B in product(range(19),repeat=width):
            cc, word = c, list(B)
            path, seen = [], set()
            while len(word) <= 3:
                key = (cc,tuple(word))
                if key in seen:
                    cycles.append({'initial':[c,list(B)],'path':path,'repeated':[cc,word]})
                    break
                assert len(path) < 100, (c,B,path)
                seen.add(key)
                path.append([cc,word])
                cc,word = exterior(cc,word)
            else:
                t = len(path)
                hist[t] += 1
                counts[t] += 1
                if t > maximum:
                    maximum = t
                    longest = []
                if t == maximum:
                    longest.append({'initial':[c,list(B)],'path':path+[[cc,word]]})
    byphase[c] = dict(sorted(counts.items()))
result = {
    'status':'PASS' if not cycles else 'CYCLES_FOUND',
    'evidence_kind':'complete finite computation, not Lean',
    'domain':'all 8 even phases 2..16 and all words over 0..18 of length <=3, no validity/trim/positive-head filter',
    'state_count':sum(hist.values())+len(cycles),
    'exit_histogram':dict(sorted(hist.items())), 'byphase':byphase,
    'maximum_first_exit_time':maximum, 'maximizers':longest,
    'cycles':cycles,
    'method':'Independent full symmetric column-word normalization; no author outer-map implementation imported',
    'input_sources_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),HERE/'independent_controls.py']},
    'infinite_safe_orbit_or_p196':False,
}
(HERE/'unrestricted_cap3_controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['byphase','maximizers','cycles']},sort_keys=True))
print('maximizers',len(longest),'cycles',len(cycles))
