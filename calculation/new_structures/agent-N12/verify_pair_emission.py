#!/usr/bin/env python3
"""Independent complete-table aggregation and master-collision consistency check."""
import csv
import hashlib
import sys
from collections import Counter
from pathlib import Path
p=Path(sys.argv[1]);m=Path(sys.argv[2])
assert hashlib.sha256(p.read_bytes()).hexdigest()=='8e9e43633153ca7993bcd486e258acbcc8b4fee2e0a7109706f5fdceee28004a'
a=list(csv.DictReader(p.open()));b=list(csv.DictReader(m.open()))
assert len(a)==256 and len(b)==257
assert [int(r['k']) for r in a]==list(range(256))
for k,r in enumerate(a):
 assert int(r['short_gap'])==31000+k and int(r['long_gap'])==31001+k
 assert int(r['collision_short'])==int(b[k]['first_zero'])
 assert int(r['collision_long'])==int(b[k+1]['first_zero'])
 assert int(r['first_divergence'])>=min(int(r['collision_short']),int(r['collision_long']))+1
 assert int(r['lag_from_earlier_collision'])==int(r['first_divergence'])-min(int(r['collision_short']),int(r['collision_long']))
 assert r['first16_pair_equal']=='1'
 assert int(r['hamming_at_birth']) in (2,3)
 assert int(r['radius_at_birth']) in (1,2)
assert Counter(int(r['hamming_at_birth']) for r in a)=={2:242,3:14}
assert Counter(int(r['lag_from_earlier_collision']) for r in a)=={1:110,2:97,3:33,4:12,5:4}
assert Counter(int(r['radius_at_birth']) for r in a)=={1:243,2:13}
assert a[3]['first_divergence']=='51469' and a[3]['collision_long']=='51468' and a[3]['collision_short']=='51470'
assert a[12]['first_divergence']=='51483' and a[12]['hamming_at_birth']=='3'
print('PAIR_EMISSION_ALL_256_PASS birth2=242 birth3=14 lag1to5')
