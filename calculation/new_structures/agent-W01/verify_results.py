#!/usr/bin/env python3
"""Independent log/control checker for the two arithmetic implementations."""
import csv
import pathlib
import re
import sys
p=pathlib.Path(sys.argv[1])
digits=(p/'digits.log').read_text()
events=re.search(r'W01_EVENTS (.*)',digits)
assert events, 'missing decimal digit-vector summary'
actual=dict(re.findall(r'(\w+)=(-?\d+)',events.group(1)))
expected={'overlap':2154,'nonlinear':2161,'unexpected':2161,
          'odd_failure':-1,'front_88_failure':-1,'digit_window_88_failure':-1,
          'digit_equalities':9234486,'window_times':19001,
          'checksum':3579271548077735118,'shape_fail':-1,
          'shape_checks':298285792,'minimum_intact':1456}
for k,v in expected.items(): assert actual.get(k)==str(v),(k,actual.get(k),v)
rows=list(csv.DictReader((p/'keyframes.csv').open()))
assert rows[0]['t']=='0' and rows[-1]['t']=='20000'
assert len(rows)==259, len(rows)
assert rows[-1]['front_B']==rows[-1]['front_D']=='1456'
assert rows[-1]['overlap']=='12086' and rows[-1]['nonlinear']=='1326'
assert rows[-1]['unexpected']=='56' and rows[-1]['decimal_length']=='34000'
final={0:1250752879650488018,1:5226968435340452601,
       2:16313672923089106462,3:15507195321027655971}
for k,h in final.items():
    s=(p/f'gmp{k}.log').read_text()
    assert f'W01_GMP_PASS flags={k} steps=20000 prefix_checks=29121456' in s
    assert f'W01_GMP_CHECKPOINT t=20000 len=34000 fnv64={h}' in s
# The GMP engine and the decimal digit-vector engine compute identical D hashes at six milestones.
for line in re.findall(r'W01_D_CHECKPOINT .*',digits):
    assert line.replace('W01_D_CHECKPOINT','W01_GMP_CHECKPOINT') in (p/'gmp3.log').read_text(),line
assert 'GMP_SHAPE_FAIL t=8 j=0' in (p/'wrong.log').read_text()
print('VERIFY_RESULTS_PASS four GMP 20k orbits, 20k four-orbit interactions, and negative phase control')
