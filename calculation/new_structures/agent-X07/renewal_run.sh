#!/bin/sh
set -eu
cd "$(dirname "$0")"
c++ -std=c++17 -O3 renewal_census.cpp -o /tmp/x07_renewal_$$
trap 'rm -f /tmp/x07_renewal_$$' EXIT
/tmp/x07_renewal_$$ 4 200 > /tmp/x07_m4_$$
/tmp/x07_renewal_$$ 6 200 > /tmp/x07_m6_$$
python3 independent_renewal.py renewal_events.json
python3 - /tmp/x07_m4_$$ /tmp/x07_m6_$$ <<'PY'
import json,re,sys
want=json.load(open('renewal_events.json'))['events']
got=[]
for file in sys.argv[1:]:
 for row in open(file):
  d=dict(A=int(re.search(r'A=(\d+)',row).group(1)),m=int(re.search(r'm=(\d+)',row).group(1)),first_lost=int(re.search(r'firstbad=(\d+)',row).group(1)))
  d['entries']=[dict(t=int(t),L=int(L)) for t,L in re.findall(r'(\d+):(\d+)',row)]
  got.append(d)
assert got == want,(len(got),len(want))
print('Independent fixture versus full C++ exhaustive census: 136/136 exact matches')
PY
rm -f /tmp/x07_m4_$$ /tmp/x07_m6_$$
