"""Bounded exact search for a two-step delayed repair through an overflow.

Exhausts every admissible even symmetric core of length 2,4,6,8, with a
nonzero endpoint, in the p=5 (NO) and p=10 (ON) padded families at r=8.
The complete finite outcome stream is saved in compressed form; no long
orbit or all-time claim is made.
"""
from __future__ import annotations

import base64
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import sys
import zlib

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "main_existence_attempt/correlation_pass/constructive"))
from seam_overlap import canonical, literal_step, realize
from variable_overlap import shifted_double

HERE = Path(__file__).resolve().parent


def cores(half_width):
    for half in itertools.product(range(19), repeat=half_width):
        if not half[0] or half[-1] > 9:
            continue
        if any(x+y > 18 for x,y in zip(half,half[1:])):
            continue
        yield half + half[::-1]


def main():
    counts = Counter()
    outcomes = bytearray()
    delayed = []
    for p in (5,10):
        for half_width in (1,2,3,4):
            for core in cores(half_width):
                a = (p,)+(0,)*8+core+(0,)*8+(p,)
                q = shifted_double(a,1)
                assert canonical(a) and canonical(q)
                a1,q1=literal_step(a),literal_step(q)
                a2,q2=literal_step(a1),literal_step(q1)
                s1,s2=len(q1)-len(a1),len(q2)-len(a2)
                c1=s1>=0 and q1==shifted_double(a1,s1)
                c2=s2>=0 and q2==shifted_double(a2,s2)
                clock=(len(q1)-len(q),len(q2)-len(q1))
                assert clock == ((0,1) if p==5 else (1,0))
                counts[(p,len(core),int(c1),int(c2))]+=1
                outcomes.append(int(c1)+2*int(c2))
                if c2 and not c1:
                    n=realize(q)
                    safe=True
                    for _ in range(2):
                        n += int(str(n)[::-1])
                        safe &= str(n)!=str(n)[::-1]
                    delayed.append({"p":p,"core":core,"r":8,"shift":s2,
                                    "safe_through_return":safe,
                                    "component_after_two":a2,"whole_after_two":q2})
    compressed=zlib.compress(bytes(outcomes),9)
    result={
        "status":"complete bounded two-step overflow-core probe",
        "configuration":{"outer_p":[5,10],"r":8,"initial_shift":1,
                         "core_lengths":[2,4,6,8],"alphabet":"0..18",
                         "constraints":"symmetric; positive endpoint; all adjacent sums <=18"},
        "ordering":"p, half_width, lexicographic half over range(19), filtered by cores()",
        "outcome_encoding":"one byte per accepted input: closed_1 + 2*closed_2",
        "outcome_count":len(outcomes),
        "outcome_sha256":hashlib.sha256(outcomes).hexdigest(),
        "outcome_zlib_base64":base64.b64encode(compressed).decode(),
        "compressed_bytes":len(compressed),
        "counts":[{"p":p,"core_length":l,"closed_1":c1,"closed_2":c2,"count":n}
                  for (p,l,c1,c2),n in sorted(counts.items())],
        "genuine_delayed_returns":delayed,
        "unsearched":"longer cores, other initial shifts, and returns after more than two updates",
        "finite_Lychrel_witness":False,
    }
    (HERE/'overflow_core_probe.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in
                     ('outcome_zlib_base64','genuine_delayed_returns','counts')},indent=2))
    print("genuine_delayed_return_count",len(delayed))


if __name__=='__main__':
    main()
